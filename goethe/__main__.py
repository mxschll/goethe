import sys
import getopt
from Editor import Editor
from Interpreter import Interpreter

HELP_MESSAGE = """options:
    -h, --help      Show this message.
    -e, --editor    Open Goethe editor.
    -i, --input     Run file in console mode."""


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:e",
                                   ["help", "input=", 'editor'])
    except getopt.GetoptError as err:
        # Print help information and exit.
        print(err)
        print(HELP_MESSAGE)
        sys.exit(2)

    for option, arg in opts:
        if option in ("-h", "--help"):
            # Show help message.
            print(HELP_MESSAGE)
            sys.exit()
        elif option in ("-e", "--editor"):
            # Open Goethe editor.
            editor = Editor()
            editor.main()
        elif option in ("-i", "--input"):
            # Run program in command line.
            with open(arg) as file:
                interpreter = Interpreter(file.read())
                interpreter.run()
        else:
            assert False, "Unhandled option."


if __name__ == "__main__":
    main()
