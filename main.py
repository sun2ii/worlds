import os
import re
import subprocess
from datetime import datetime

# Terminal color codes
RESET = "\033[0m"  # Reset all attributes
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright colors
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"


def main():
    main_menu_text = (
        f"{BRIGHT_MAGENTA}1. View Worlds{RESET}\n"
        f"{BRIGHT_CYAN}2. Create World{RESET}\n"
        f"{YELLOW}x. Exit{RESET}"
    )
    while True:
        print(main_menu_text)
        choice = input("")

        if choice == "1":
            os.system("clear")
            data_folder = os.path.join(os.getcwd(), "data")

            if not os.path.exists(data_folder):
                print("No worlds found. The 'data' folder does not exist.")
            else:
                worlds = [
                    filename
                    for filename in os.listdir(data_folder)
                    if filename.endswith(".yaml")
                ]
                if worlds:
                    max_name_length = max(
                        len(filename.replace(".yaml", "")) for filename in worlds
                    )

                    for filename in worlds:
                        world_name = filename.replace(".yaml", "")
                        file_path = os.path.join(data_folder, filename)
                        with open(file_path, "r") as file:
                            content = file.read()
                            # Count occurrences of T* lines (e.g., T1., T2., ...)
                            t_entries = re.findall(r"^T\d+\.", content, re.MULTILINE)
                            # Generate display string for task blocks
                            task_blocks = " - ".join(["[ ]" for _ in t_entries])

                            # Print world name, aligned to max_name_length, and task blocks on the next line
                            print(f"{world_name.ljust(max_name_length)}")
                            print(f"{task_blocks}\n")
                else:
                    print("No worlds found.")

            # Wait for the user to press Enter before returning to the main menu
            input("\nPress Enter to return to the main menu...")

        elif choice == "2":
            world_name = input("What would you like to name your world? ")
            file_name = f"{world_name}.yaml"
            file_path = os.path.join(os.getcwd(), "data", file_name)
            os.makedirs("data", exist_ok=True)
            world_data = f"""---
world: {world_name}
date_created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

T1. 
T2. 
T3. 
T4. 
T5. 
"""
            with open(file_path, "w") as file:
                file.write(world_data)
            print(f"'./data/{world_name}.yaml' created.")

            try:
                subprocess.run(["vim", file_path])
            except Exception as e:
                print(f"Could not open the file automatically: {e}")

        elif choice == "x":
            break
        else:
            print("select 1, 2, or x")


if __name__ == "__main__":
    main()
