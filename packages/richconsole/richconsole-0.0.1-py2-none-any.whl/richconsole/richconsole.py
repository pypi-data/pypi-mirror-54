# -*- coding: utf-8 -*-
from __future__ import print_function
from os import system as os_system, getpid
from sys import version_info as sys_version_info
from atexit import register as atexit_register
from ctypes.wintypes import DWORD, SHORT, SMALL_RECT, WORD
from ctypes import Structure, pointer, get_last_error, windll, sizeof, create_string_buffer, c_ulong, c_uint, c_wchar, c_long, c_int, c_void_p


if sys_version_info[0] == 2:
    from tkFont import families as tkfont_families
    from Tkinter import Tk
    FindWindow = windll.user32.FindWindowA
    SetWindowLong = windll.user32.SetWindowLongA
    GetWindowLong = windll.user32.GetWindowLongA
    GetConsoleTitle = windll.kernel32.GetConsoleTitleA
elif sys_version_info[0] == 3:
    from tkinter.font import families as tkfont_families
    from tkinter import Tk
    FindWindow = windll.user32.FindWindowW
    SetWindowLong = windll.user32.SetWindowLongW
    GetWindowLong = windll.user32.GetWindowLongW
    GetConsoleTitle = windll.kernel32.GetConsoleTitleW


# c++ data structures
class COORD(Structure):
    _fields_ = [("X", SHORT),
                ("Y", SHORT)]


class CONSOLE_FONT_INFO(Structure):
    _fields_ = [("nFont", DWORD),
                ("dwFontSize", COORD),
                ]


class CONSOLE_FONT_INFOEX(Structure):
    _fields_ = [("cbSize", c_ulong),
                ("nFont", c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", c_uint),
                ("FontWeight", c_uint),
                ("FaceName", c_wchar * 32)]


class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [("dwSize", COORD),
                ("dwCursorPosition", COORD),
                ("wAttributes", WORD),
                ("srWindow", SMALL_RECT),
                ("dwMaximumWindowSize", COORD)]


# C++ functions
SetWindowLongPtr = SetWindowLong
SetWindowLongPtr.argtypes = [c_int, c_int, c_void_p]
SetWindowLongPtr.restype = c_void_p

GetWindowLongPtr = GetWindowLong
GetWindowLongPtr.argtypes = [c_int, c_int]
GetWindowLongPtr.restype = c_void_p


def RGB(red, green, blue):
    # convert rgb values(0-255) into a c_long
    return (red << 0) + (green << 8) + (blue << 16)


# predefined text modifications
class colors:
    black = {"foreground": "30", "background": "40"}
    red = {"foreground": "31", "background": "41"}
    green = {"foreground": "32", "background": "42"}
    yellow = {"foreground": "33", "background": "43"}
    blue = {"foreground": "34", "background": "44"}
    magenta = {"foreground": "35", "background": "45"}
    cyan = {"foreground": "36", "background": "46"}
    white = {"foreground": "37", "background": "47"}
    bright_black = {"foreground": "90", "background": "100"}
    bright_red = {"foreground": "91", "background": "101"}
    bright_green = {"foreground": "92", "background": "102"}
    bright_yellow = {"foreground": "93", "background": "103"}
    bright_blue = {"foreground": "94", "background": "104"}
    bright_magenta = {"foreground": "95", "background": "105"}
    bright_cyan = {"foreground": "96", "background": "106"}
    bright_white = {"foreground": "97", "background": "107"}


class text_attributes:
    # enable
    bold = "\033[01m"
    faint = "\033[02m"
    italic = "\033[03m"
    underline = "\033[04m"
    slow_flash = "\033[05m"
    fast_flash = "\033[06m"
    swap_colors = "\033[07m"
    cross_out = "\033[09m"
    conceal = "\033[08m"
    framed = "\033[51m"
    encircled = "\033[52m"
    overlined = "\033[53m"
    # disable
    remove_bold_and_faint = "\033[22m"
    remove_italic = "\033[23m"
    remove_underline = "\033[24m"
    remove_flash = "\033[25m"
    remove_swap_colors = "\033[27m"
    remove_conceal = "\033[28m"
    remove_cross_out = "\033[29m"
    remove_framed_and_encircled = "\033[54m"
    remove_overlined = "\033[55m"
    # remove all
    remove_all = '\033[0m'


# prep script
def init(reset_at_close=True):
    # enable escape sequences
    os_system("")
    # reset Console when closed
    if reset_at_close:
        atexit_register(close)


def close():
    t = Console()
    # set text back to original font
    t.set_font_data(t.original_font)
    # set buffersize back to original
    w, h = t.original_buffer_size
    t.set_console_buffer_size(w, h)
    # set color data back to normal
    print(text_attributes.remove_all)
    # set opacity back to normal
    if t.colors_with_opacity:
        t.remove_color_transparency()
    if t.opacity != 255:
        t.set_opacity(255)


class Console:
    original_font = None
    original_buffer_size = None, None

    opacity = 255
    colors_with_opacity = list()

    def __init__(self):
        self.std_output_handle = self.get_output_handle()
        # system info
        self.pid = None
        self.hwnd = None
        self.get_hwnd()
        # Font data
        self.font = None
        self.nFont = None
        self.dwFontSize_x = None
        self.dwFontSize_y = None
        self.FontFamily = None
        self.FontWeight = None
        self.FaceName = None
        self.get_font_data()
        # console size
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_left = None
        self.viewport_top = None
        self.viewport_right = None
        self.viewport_bottom = None

        self.buffer_width = None
        self.buffer_height = None
        self.screen_width = None
        self.screen_height = None

        # cursor data
        self.cursor_x = None
        self.cursor_y = None
        self.get_console_data()

        # set global class variables
        if not Console.original_font:
            Console.original_font = self.font
        if not Console.original_buffer_size:
            Console.original_buffer_size = self.buffer_width, self.buffer_height

    def get_output_handle(self):
        return windll.kernel32.GetStdHandle(-11)

    def get_hwnd(self):
        self.pid = getpid()
        title = self.get_title()
        self.hwnd = FindWindow(0, title)

    def get_console_data(self):
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        if not windll.kernel32.GetConsoleScreenBufferInfo(self.std_output_handle, pointer(csbi)):
            error_code = get_last_error()
            if error_code == 0:
                print("your current console does not support this")
            else:
                raise Exception("windows error: %s" % error_code)

        self.buffer_width, self.buffer_height = csbi.dwSize.X, csbi.dwSize.Y
        self.viewport_left = csbi.srWindow.Left
        self.viewport_top = csbi.srWindow.Top
        self.viewport_right = csbi.srWindow.Right
        self.viewport_bottom = csbi.srWindow.Bottom
        self.screen_width, self.screen_height = csbi.dwMaximumWindowSize.X, csbi.dwMaximumWindowSize.Y
        self.cursor_x, self.cursor_y = csbi.dwCursorPosition.X, csbi.dwCursorPosition.Y

    def set_console_buffer_size(self, width=None, height=None):
        c = COORD()
        c.X = max(width if width else self.buffer_width, self.screen_width)
        c.Y = max(height if height else self.buffer_height, self.screen_height)
        if not windll.kernel32.SetConsoleScreenBufferSize(self.std_output_handle, c):
            error_code = get_last_error()
            if error_code == 0:
                print("your current console does not support this")
            else:
                raise Exception("windows error: %s" % error_code)
        self.buffer_width = c.X
        self.buffer_height = c.Y

    def set_viewport(self, x=None, y=None):
        self.get_console_data()

        self.viewport_x = x if x else self.viewport_x
        self.viewport_y = y if y else self.viewport_y

        r = SMALL_RECT()
        r.Left = self.viewport_x
        r.Top = self.viewport_y
        r.Right = r.Left + (self.screen_width - 1)
        r.Bottom = r.Top + (self.screen_height - 1)

        print("\n")

        if not windll.kernel32.SetConsoleWindowInfo(self.std_output_handle, c_long(True), pointer(r)):
            error_code = get_last_error()
            if error_code == 0:
                print("your current console does not support this")
            else:
                raise Exception("windows error: %s" % error_code)

    def set_scolling_margins(self, start="", end=""):
        print("\033[%s;%sr" % (start, end))

    # Font data
    def get_font_data(self):
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = sizeof(CONSOLE_FONT_INFOEX)
        if not windll.kernel32.GetCurrentConsoleFontEx(self.std_output_handle, c_long(False), pointer(font)):
            error_code = get_last_error()
            if error_code == 0:
                print("your current console does not support this")
            else:
                raise Exception("windows error: %s" % error_code)

        self.font = font
        self.nFont = font.nFont
        self.dwFontSize_x = font.dwFontSize.X
        self.dwFontSize_y = font.dwFontSize.Y
        self.FontFamily = font.FontFamily
        self.FontWeight = font.FontWeight
        self.FaceName = font.FaceName

    def set_font_data(self, font=None):
        if font:
            self.nFont = font.nFont
            self.dwFontSize_x = font.dwFontSize.X
            self.dwFontSize_y = font.dwFontSize.Y
            self.FontFamily = font.FontFamily
            self.FontWeight = font.FontWeight
            self.FaceName = font.FaceName

        font = CONSOLE_FONT_INFOEX()
        font.cbSize = sizeof(CONSOLE_FONT_INFOEX)
        font.nFont = self.nFont
        font.dwFontSize.X = self.dwFontSize_x
        font.dwFontSize.Y = self.dwFontSize_y
        font.FontFamily = self.FontFamily
        font.FontWeight = self.FontWeight
        font.FaceName = self.FaceName

        if not windll.kernel32.SetCurrentConsoleFontEx(self.std_output_handle, c_long(False), pointer(font)):
            error_code = get_last_error()
            if error_code == 0:
                print("your current console does not support this")
            else:
                raise Exception("windows error: %s" % error_code)

    def get_available_fonts(self):
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = sizeof(CONSOLE_FONT_INFOEX)
        font.nFont = 2
        font.dwFontSize.X = 11
        font.dwFontSize.Y = 2
        font.FontFamily = 54
        font.FontWeight = 400

        working = []
        not_working = []

        root = Tk()
        for x in tkfont_families():
            font.FaceName = x
            if not windll.kernel32.SetCurrentConsoleFontEx(self.std_output_handle, c_long(False), pointer(font)):
                error_code = get_last_error()
                if error_code == 0:
                    print("your current console does not support this")
                else:
                    raise Exception("windows error: %s" % error_code)
            self.get_font_data()
            if (x == "Courier New" and self.FaceName == "Courier New") or self.FaceName != "Courier New":
                working.append(x)
            else:
                not_working.append(x)

        root.destroy()
        self.set_font_data(Console.original_font)
        return working

    def set_font_size(self, value):
        self.dwFontSize_y = value
        self.set_font_data()

    def set_font_boldness(self, value):
        # must be a multiple of 100 within range 0-1000 default = 400
        self.FontWeight = value
        self.set_font_data()

    def set_font_type(self, name):
        self.FaceName = name
        self.set_font_data()

    # cursor
    def save_cursor_position(self):
        print("\033[s", end="")

    def restore_cursor_position(self):
        print("\033[u", end="")

    def set_cursor_position(self, x="", y=""):
        print("\033[%s;%sf" % (y, x), end="")

    def move_cursor(self, horizontal=None, vertical=None):
        if horizontal:
            if horizontal < 0:
                # left
                horizontal = abs(horizontal - 0)
                print("\033[%sD" % horizontal, end="")
            elif horizontal > 0:
                # right
                print("\033[%sC" % horizontal, end="")

        if vertical:
            if vertical < 0:
                # up
                vertical = abs(vertical)
                print("\033[%sA" % vertical, end="")
            elif vertical > 0:
                # down
                print("\033[%sB" % vertical, end="")

    def hide_cursor(self):
        print("\033[?25l", end="")

    def show_cursor(self):
        print("\033[?25h", end="")

    # etc
    def set_title(self, title):
        print("\033]2;%s\x07" % title)

    def get_title(self):
        title = create_string_buffer(250)
        if not GetConsoleTitle(title, sizeof(title)):
            error_code = get_last_error()
            if error_code == 0:
                print("your current console does not support this")
            else:
                raise Exception("windows error: %s" % error_code)
        return title.raw

    def set_foreground_color(self, color):
        if isinstance(color, dict):
            print("\033[%sm" % color["foreground"])
        elif color:
            raise TypeError("foreground has bad input")
        self.erase_display(4)

    def set_background_color(self, color):
        if isinstance(color, dict):
            print("\033[%sm" % color["background"])
        elif color:
            raise TypeError("background has bad input")
        self.erase_display(4)

    def reset_colors(self):
        print(text_attributes.remove_all)

    def set_opacity(self, value, to_color=None):
        # value - int - 0, 255
        # to_color - tuple -(red, green, blue)
        # if to_color is set the opacity will only effect this color else the whole console

        if to_color:
            red, green, blue = to_color
            flag = 0x00000001
            Console.colors_with_opacity.append(to_color)
        else:
            red, green, blue = (0, 0, 0)
            flag = 0x00000002
            Console.opacity = value

        SetWindowLongPtr(self.hwnd, -20, GetWindowLongPtr(self.hwnd, -20) | 0x00080000)
        windll.user32.SetLayeredWindowAttributes(self.hwnd, RGB(red, green, blue), value, flag)

    def set_background_transparent(self):
        self.set_background_color(colors.black)
        self.set_opacity(1, to_color=(12, 12, 12))

    def set_foreground_transparent(self):
        self.set_foreground_color(colors.bright_white)
        self.set_opacity(1, to_color=(242, 242, 242))

    def remove_color_transparency(self):
        SetWindowLongPtr(self.hwnd, -20, GetWindowLongPtr(self.hwnd, -20) & ~ 0x00080000)
        Console.colors_with_opacity = list()

    def erase_display(self, erase_type=2):
        # 0 clears from cursor position to end of screen.
        # 1 clear from cursor to beginning of screen.
        # 2 clear entire screen. Cursor moves to beginning of screen.
        # 3 clear entire screen. Deletes all saved line in scrollback buffer.
        # 4 deletes EVERYTHING! also the slowest
        if erase_type in range(4):
            print("\033[%sJ" % erase_type, end="")
        elif erase_type == 4:
            os_system("cls")

    def erase_line(self, erase_type=0):
        # 0 clear from cursor to the end of the line.
        # 1 clear from cursor to beginning of the line.
        # 2 clear entire line. Cursor position does not change.
        print("\033[%s" % erase_type, end="")

    def scroll_screen(self, value):
        if value:
            if value < 0:
                # up
                value = abs(value)
                print("\033[%sS" % value, end="")
            elif value > 0:
                # down
                print("\033[%sT" % value, end="")


class CText:
    string_functions = ['capitalize', 'center', 'count', 'decode', 'encode', 'endswith', 'expandtabs', 'find', 'format',
                        'index', 'isalnum', 'isalpha', 'isdigit', 'islower', 'isspace', 'istitle', 'isupper', 'join',
                        'ljust', 'lower', 'lstrip', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition',
                        'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title',
                        'translate', 'upper', 'zfill']

    def __init__(self, text, foreground=None, background=None, attributes=None):
        self.foreground = foreground
        self.background = background
        self.attributes = attributes
        self.color_code = ""
        self.text = text
        self.create_color_code()

    def set(self, text):
        self.text = text
        return self

    def create_color_code(self):
        # foreground
        if not self.foreground:
            foreground = ""
        elif isinstance(self.foreground, dict):
            foreground = "\033[%sm" % self.foreground["foreground"]
        elif isinstance(self.foreground, tuple):
            foreground = "\033[38;2;%s;%s;%sm" % self.foreground
        elif isinstance(self.foreground, int):
            foreground = "\033[38;5;%sm" % self.foreground
        else:
            raise TypeError("foreground has bad input")

        # background
        if not self.background:
            background = ""
        elif isinstance(self.background, dict):
            background = "\033[%sm" % self.background["background"]
        elif isinstance(self.background, tuple):
            background = "\033[48;2;%s;%s;%sm" % self.background
        elif isinstance(self.background, int):
            background = "\033[48;5;%sm" % self.background
        else:
            raise TypeError("background has bad input")

        # attributes
        if not self.attributes:
            attributes = ""
        elif isinstance(self.attributes, str):
            attributes = self.attributes
        elif isinstance(self.attributes, list):
            attributes = "".join(self.attributes)
        else:
            raise TypeError("attribute has bad input")

        # end
        end = '\033[0m'

        self.color_code = foreground + background + attributes + "%s" + end
        return self.color_code

    def flavor_text(self):
        return self.color_code % self.text

    def __str__(self):
        return self.color_code % self.text

    def __add__(self, other):
        if isinstance(other, str):
            self.text += other
        elif isinstance(other, CText):
            self.text += other.text
        return self

    def __iadd__(self, other):
        if isinstance(other, str):
            self.text += other
        elif isinstance(other, CText):
            self.text += other.text
        return self

    def __radd__(self, other):
        if isinstance(other, str):
            self.text += other
        elif isinstance(other, CText):
            self.text += other.text
        return self

    def __coerce__(self, other):
        return self, other

    def __getattr__(self, name):
        return lambda *args, **kwargs: self.extra_functions(name, *args, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, slice):
            self.text = self.text.__getitem__(item)
            return self

    def __call__(self, new_text):
        self.text = new_text
        return self

    def extra_functions(self, name, *args, **kwargs):
        # string functions
        if name in self.string_functions:
            return eval("self.text.%s" % name, {"self": self})(*args, **kwargs)

        # error
        else:
            raise NotImplementedError("%s is not a proper method" % name)

    def fg(self, fg):
        self.foreground = fg
        self.create_color_code()
        return self

    def bg(self, bg):
        self.background = bg
        self.create_color_code()
        return self

    def attr(self, attr):
        self.attributes = attr
        self.create_color_code()
        return self


if __name__ == '__main__':
    init()
    console = Console()
    console.set_background_color(colors.green)
    print("background is now green")
    print(CText("i'm my own color", foreground=(10, 20, 255), background=(150, 150, 150)))
    raw_input(CText("press enter to quit", background=(255, 0, 0)))
