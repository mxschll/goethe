import sys
import argparse

from goethe.Editor import Editor
from goethe.Interpreter import Interpreter


class Parser(argparse.ArgumentParser):
    def error(self, message):
        """Prints out help message when error occurs.

        Args:
            message (str): Error message.
        """
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser = Parser(description="Python interpreter for the Goethe programming language.")

output_group = parser.add_mutually_exclusive_group(required=True)
output_group.add_argument("-i", "--input", action="store", help="Input file (.goethe)")
output_group.add_argument("-e", "--editor", action="store_true", help="Open the editor")

def main():
    args = parser.parse_args()
    if args.editor:
        # Opens Goethe editor.
        editor = Editor()
        editor.main()
    elif args.input:
        # Runs Goethe interpreter in console mode.
        with open(args.input) as file:
            interpreter = Interpreter(file.read())
            interpreter.run()

if __name__ == "__main__":
    main()
