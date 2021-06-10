import sys
import time
import random
import logging
from typing import Tuple, Callable

from Token import Token
from Memory import Memory
from Tokenizer import Tokenizer
from LanguageTools import LanguageTools


class InvalidTokenException(Exception):
    pass


class Interpreter:
    """The interpreter holds the program status and is responsible for executing the Goethe code.
    """

    def __init__(self, text='', lang='de_DE', console_mode=True):
        """
        Args:
            text (str, optional): Goethe code. Defaults to ''.
            lang (str, optional): Language code. Defaults to 'de_DE'.
            console_mode (bool, optional): Enables or disables console mode. Defaults to True.
        """
        self.user_input = ''
        self.event_listeners = dict()
        self.console_mode = console_mode

        self.tokenizer = Tokenizer(LanguageTools(text, lang))
        self.program = self.tokenizer.tokenize()
        self.memory = Memory(256)
        self.pointer = 0

    def PASS(self) -> None:
        """Does nothing.
        """

        pass

    def LOOP(self) -> None:
        """Jumps to the appropriate FI command in the program if current memory value == 0.
        """

        if self.memory.get_value() != 0:
            return

        # Finds the appropriate FI command by counting the
        # nested IF and FI commands in the program.
        nesting = 1
        while nesting:
            instruction = self._get_next_instruction()
            if instruction == Token.LOOP:
                nesting += 1
            elif instruction == Token.POOL:
                nesting -= 1

    def POOL(self) -> None:
        """Jumps to the appropriate IF command in the program if current memory value != 0.
        """

        if self.memory.get_value() == 0:
            return

        # Finds the appropriate IF command by counting the
        # nested IF and FI commands in the program.
        nesting = -1
        while nesting:
            instruction = self._get_previous_instruction()
            if instruction == Token.LOOP:
                nesting += 1
            elif instruction == Token.POOL:
                nesting -= 1

    def IN(self) -> None:
        """Reads a single char from stdin or self.user_input.
        """

        if self.console_mode:
            # Reads input from stdin if console mode is enabled.
            char = ord(sys.stdin.read(1))
            if char == 10:  # Ascii code for ENTER
                return

        else:
            # Reads input from self.user_input if console mode is disabled.
            if len(self.user_input):
                char = ord(self.user_input[0])
                self.user_input = self.user_input[1:]
            else:
                return

        self.memory.set_value(char)
        self.__dispatch_event('<in>')

    def OUT(self) -> None:
        """Writes the current memory value as ASCII to the console.
        """

        if self.console_mode:
            print(chr(self.memory.get_value()), end="", flush=True)

        self.__dispatch_event('<out>', chr(self.memory.get_value()))

    def INCPTR(self) -> None:
        """Increments memory pointer.
        """

        self.memory.increment_pointer()

    def DECPTR(self) -> None:
        """Decrements memory pointer.
        """

        self.memory.decrement_pointer()

    def INCVAL(self) -> None:
        """Increments memory value.
        """

        self.memory.increment_value()

    def DECVAL(self) -> None:
        """Decrements memory value.
        """

        self.memory.decrement_value()

    def RND(self) -> None:
        """Writes random int to memory.
        """

        value = random.randint(0, 255)
        self.memory.set_value(value)

    def set_code(self, text='', lang='de_DE') -> None:
        """Runs given text through the tokenizer and sets tokens as program.

        Args:
            text (str, optional): Goethe code. Defaults to ''.
            lang (str, optional): Language code. Defaults to 'de_DE'.
        """

        self.pointer = 0
        self.memory.reset()
        self.tokenizer = Tokenizer(LanguageTools(text, lang))
        self.program = self.tokenizer.tokenize()

    def set_user_input(self, input: str):
        """Sets the user input to the given text. Useful when console mode is disabled.

        Args:
            input (str): User input.
        """

        self.user_input = input

    def _get_next_instruction(self) -> Tuple[Token, None]:
        """Returns next program instruction and increments program pointer.

        Returns:
            Token: Next program token.
        """

        if self.pointer >= len(self.program):
            # No further instruction.
            return None

        self.pointer += 1
        return self.program[self.pointer]

    def _get_previous_instruction(self) -> Tuple[Token, None]:
        """Returns previous program instruction and decrements program pointer.

        Returns:
            Token: Previous program token.
        """

        if self.pointer < 0:
            # No previous instruction.
            return None

        self.pointer -= 1
        return self.program[self.pointer]

    def _get_current_instruction(self) -> Tuple[Token, None]:
        """Returns current program instruction.

        Returns:
            Token: Current program token.
        """

        if self.pointer < len(self.program):
            return self.program[self.pointer]

        return None

    def run(self) -> None:
        """Executes the program from the current position to the end.
        """

        while self._get_current_instruction():
            self.step()

        self.step()  # Last step, the program has reached the end.

    def step(self) -> None:
        """Executes the current command in the program.
        """

        instruction = self._get_current_instruction()

        if instruction == None:
            # The end of the program has been reached.

            if self.console_mode:
                # Print out the return character when the program finishes.
                print(chr(10), end="", flush=True)

            self.pointer = 0
            self.memory.reset()
            self.__dispatch_event('<end>')
            return

        if hasattr(self, instruction.name):
            # Calls the function matching the token.
            getattr(self, instruction.name)()
        else:
            raise InvalidTokenException

        self.pointer += 1
        self.__dispatch_event('<step>')

    def add_event_listener(self, type: str, listener: Callable[[str], None]) -> None:
        """Registers event listener that is called when the given event type occurs.

        Args:
            type (str): Event type signature.
            listener (Callable[[str], None]): Event listener to be called.
        """

        if type not in self.event_listeners:
            self.event_listeners[type] = []

        self.event_listeners[type].append(listener)

    def __dispatch_event(self, type: str, value=None) -> None:
        """Calls all event listeners for the specified event type.

        Args:
            type (str): Event type signature.
            value (str, optional): Data to be passed to the listener.. Defaults to None.
        """
        if type in self.event_listeners:
            for event in self.event_listeners[type]:
                try:
                    event(value)
                except:
                    logging.error('Event listener could not be called.')
