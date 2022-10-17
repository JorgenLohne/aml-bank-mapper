#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
import webbrowser

FILEPATH = "RequestId-aml.txt"
BASE_URL_PROD = "https://bankportal.edb.com/antihvitvask/index.jsp?req_id="
BASE_URL_TEST = "https://bankportal.preprod-restricted.evry.com/antihvitvask/index.jsp?req_id="
SKIP_LINES = 5
BANK_CODE_MAP = None
STICK_ON_TOP = False


def create_map(filepath, skip):
    """
    cleans up data and creates a mapping from bank code to url substring

    :param skip: how many lines to skip before reading input from file
    :param filepath: filepath to input file
    :return: dict with mapping from bank-code to url-substring
    """
    try:
        with open(filepath) as f:
            bank_code_to_url_map = {}
            lines = [line.rstrip() for line in f][skip:]

            for line in lines:
                url_sub_bankcode = line.strip().split("=")

                bank_code_to_url_map.update({url_sub_bankcode[-1].strip(): url_sub_bankcode[0].strip()})

            return bank_code_to_url_map

    except OSError as e:
        print(f"could not find file {FILEPATH} in current folder: {e}")


def _set_path():
    file = filedialog.askopenfilename()
    return file


def _override_bank_code_map():
    """
    recreates the bank code map when reading from file
    :return:
    """
    file = _set_path()
    global BANK_CODE_MAP
    BANK_CODE_MAP = create_map(file, SKIP_LINES)


def _toggle_sticky(gui):
    global STICK_ON_TOP
    STICK_ON_TOP = not STICK_ON_TOP
    gui.destroy()
    create_gui()


def create_gui():
    """
    Creates the GUI for the application
    :return:
    """

    root = tk.Tk()

    # Input field for bank-code
    tk.Label(root, text="Bank-code: ").grid(row=0)
    bank_code_input = tk.Entry(root)
    bank_code_input.grid(row=0, column=1)

    # Choose environment
    env = tk.StringVar()
    env.set("prod")  # default env
    tk.Label(root, text="Env:", ).grid(row=1)
    tk.Radiobutton(root, text="Test",
                   variable=env,
                   value="test",
                   indicatoron=False,
                   command=lambda: env.set("test")).grid(row=1, column=1)

    tk.Radiobutton(root, text="Prod",
                   variable=env,
                   value="prod",
                   command=lambda: env.set("prod"),
                   indicatoron=False).grid(row=1, column=2)

    # Button for opening filebrowser
    user_input_file_button = tk.Button(text="Browse", command=_override_bank_code_map)
    user_input_file_button.grid(row=2, column=0)

    global BANK_CODE_MAP
    BANK_CODE_MAP = create_map(FILEPATH, SKIP_LINES)

    # Button for opening browser
    open_web = tk.Button(text="Open web",
                         command=lambda: webbrowser.open(BASE_URL_TEST + BANK_CODE_MAP.get(bank_code_input.get()),
                                                         new=1) if env.get() == "test"
                         else webbrowser.open(BASE_URL_PROD + BANK_CODE_MAP.get(bank_code_input.get()), new=1))
    open_web.grid(row=0, column=2)

    sticky_button = tk.Button(text="Toggle stay on top", command=lambda: _toggle_sticky(root))
    sticky_button.grid(row=3)

    root.title("AML bank mapper")
    root.attributes("-topmost", STICK_ON_TOP)
    root.mainloop()


if __name__ == "__main__":
    create_gui()
