from utils.world_creator import create_world
from utils.world_viewer import print_main_menu_text, view_worlds


def main():
    while True:
        print_main_menu_text()
        x = input("")

        if x == "1":
            view_worlds()
        elif x == "2":
            create_world()
        elif x == "x":
            break
        else:
            print("select 1, 2, or x")


if __name__ == "__main__":
    main()
