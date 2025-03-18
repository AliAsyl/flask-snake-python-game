import sys

def main():
    command = sys.argv[1]

    if command in ["--help", "-h"]:
        print("> This is a help command. Type:\n\t'-h' or '--help' : shows help message.\n\t'--sum' [numbers]: sums integer numbers.")
    elif command == "--sum":
        try:
            print(f"> The sum is: { sum([int(i) for i in sys.argv[2:]]) }")        
        except ValueError:
            print("> One or more argument is not an integer.")
    else:
        print("> This command does not exist. Try typing -h or --help for help message.")


if __name__ == "__main__":
    main()
