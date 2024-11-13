import curses
import os
import re
import subprocess

from .colors import BRIGHT_CYAN, BRIGHT_MAGENTA, RESET, YELLOW


def print_main_menu_text():
    print(
        f"{BRIGHT_MAGENTA}1. View Worlds{RESET}\n"
        f"{BRIGHT_CYAN}2. Create World{RESET}\n"
        f"{YELLOW}x. Exit{RESET}"
    )


def view_worlds():
    while True:  # Outer loop to stay within "Available Worlds" view
        os.system("clear")
        data_folder = os.path.join(os.getcwd(), "data")

        if not os.path.exists(data_folder):
            print("No worlds found. The 'data' folder does not exist.")
            return  # Exit to main menu if no folder is found

        worlds = [f for f in os.listdir(data_folder) if f.endswith(".yaml")]
        if not worlds:
            print("No worlds found.")
            return  # Exit to main menu if no YAML files are found

        max_name_length = max(len(f.replace(".yaml", "")) for f in worlds)
        print("Available Worlds:")

        for i, filename in enumerate(worlds, start=1):
            world_name = filename.replace(".yaml", "")
            file_path = os.path.join(data_folder, filename)

            with open(file_path, "r") as file:
                content = file.read()
                t_entries = re.findall(r"^T\d+\.", content, re.MULTILINE)
                task_blocks = " - ".join("*" for _ in t_entries)

                print(f"{i}. {world_name.ljust(max_name_length)}")
                print(f"   {task_blocks}\n")

        try:
            selection = input(
                "Select a world by number to view details or press Enter to return to the main menu: "
            ).strip()
            if selection == "":
                break  # Exit to main menu if Enter is pressed without input

            index = int(selection) - 1
            if 0 <= index < len(worlds):
                file_path = os.path.join(data_folder, worlds[index])

                # Use curses to display world details, exit curses to open Vim
                curses.wrapper(display_world_details, file_path)
                subprocess.run(["vim", file_path])  # Open the file in Vim after curses

        except ValueError:
            print("Invalid selection. Please enter a number.")


def display_world_details(stdscr, file_path):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.clear()
    curses.curs_set(0)  # Hide the cursor

    with open(file_path, "r") as file:
        content = file.read()

    world_name = re.search(r"world:\s*(.*)", content)
    date_created = re.search(r"date_created:\s*(.*)", content)
    world_name = world_name.group(1) if world_name else "Unknown"
    date_created = date_created.group(1) if date_created else "Unknown"

    tasks = re.findall(r"^T\d+\.\s*(.*)", content, re.MULTILINE)
    tasks = [task if task.strip() else "(Empty)" for task in tasks]

    display_lines = [
        ("World Details:", curses.color_pair(1)),
        (f"Name: {world_name}", curses.color_pair(2)),
        (f"Date Created: {date_created}", curses.color_pair(3)),
        ("Tasks:", curses.A_NORMAL),
    ] + [(f"  {i+1}. {task}", curses.color_pair(4)) for i, task in enumerate(tasks)]

    selected_task = 0
    max_y, max_x = stdscr.getmaxyx()

    while True:
        stdscr.clear()

        for i, (line, color) in enumerate(display_lines):
            if i == selected_task + 4:
                stdscr.addstr(i, 0, line, curses.color_pair(5))
            else:
                stdscr.addstr(i, 0, line, color)

        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_task > 0:
            selected_task -= 1
        elif key == curses.KEY_DOWN and selected_task < len(tasks) - 1:
            selected_task += 1
        elif key == ord("\n"):  # Exit display when Enter is pressed to open in Vim
            break
