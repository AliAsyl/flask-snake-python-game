import sys

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print("> This is a help command. type -h or --help to show help message.")
    else:
        print("> This command does not exist. Try typing -h or --help for help message.")
if __name__ == "__main__":
    main()
