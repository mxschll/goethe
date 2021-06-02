import sys
import time
import random
from Token import Token
from Memory import Memory
from Tokenizer import Tokenizer
from LanguageTools import LanguageTools


class Interpreter:
    def __init__(self, text='', lang='de_DE', console_mode=False):
        self.console_mode = console_mode
        self.user_input = ''

        self.event_listeners = dict()

        self.tokenizer = Tokenizer(LanguageTools(text, lang))

        self.program = self.tokenizer.tokenize()
        self.pointer = 0
        self.memory = Memory(256)

    def set_text(self, text='', lang='de_DE'):
        self.tokenizer = Tokenizer(LanguageTools(text, lang))
        self.program = self.tokenizer.tokenize()
        self.pointer = 0
        self.memory.reset()

    def _get_next_instruction(self):
        if self.pointer >= len(self.program):
            return None

        self.pointer += 1
        return self.program[self.pointer]

    def _get_previous_instruction(self):
        if self.pointer < 0:
            return None

        self.pointer -= 1
        return self.program[self.pointer]

    def _get_current_instruction(self):
        if self.pointer < len(self.program):
            return self.program[self.pointer]

        return None

    def CP(self):
        current_pointer = self.memory._pointer

        pointer_one = self._get_next_instruction()

        self.memory.set_pointer_value(int(self._get_next_instruction()))
        value = self.memory.get_value()
        self.memory.set_pointer_value(pointer_one)
        self.memory.set_value(int(value))

        self.memory.set_pointer_value(current_pointer)

    def IF(self):
        if self.memory.get_value() != 0:
            return

        nesting = 1
        while nesting:
            instruction = self._get_next_instruction()
            if instruction == Token.IF:
                nesting += 1
            elif instruction == Token.FI:
                nesting -= 1

    def FI(self):
        if self.memory.get_value() == 0:
            return

        nesting = -1
        while nesting:
            instruction = self._get_previous_instruction()
            if instruction == Token.IF:
                nesting += 1
            elif instruction == Token.FI:
                nesting -= 1

    def IN(self):
        if self.console_mode:
            char = ord(sys.stdin.read(1))
            if char == 10:  # Ascii enter code
                return

        else:
            if len(self.user_input):
                char = ord(self.user_input[0])
                self.user_input = self.user_input[1:]
            else:
                return

        self.memory.set_value(char)
        self.__dispatch_event('<in>', chr(self.memory.get_value()))

    def OUT(self):
        if self.console_mode:
            print(chr(self.memory.get_value()), end="", flush=True)

        self.__dispatch_event('<out>', chr(self.memory.get_value()))

    def INCPTR(self):
        self.memory.increment_pointer()

    def DECPTR(self):
        self.memory.decrement_pointer()

    def INCVAL(self):
        self.memory.increment_value()

    def DECVAL(self):
        self.memory.decrement_value()

    def RND(self):
        value = random.randint(0, 255)
        self.memory.set_value(value)

    def run(self):
        self.pointer = 0
        self.memory.reset()

        while self._get_current_instruction():
            self.step()

        self.step()  # Last step, program has reached the end

    def step(self):
        instruction = self._get_current_instruction()

        if instruction == None:
            self.pointer = 0
            self.memory.reset()
            self.__dispatch_event('<end>')
            return

        if hasattr(self, instruction.name):
            getattr(self, instruction.name)()
        self.pointer += 1
        self.__dispatch_event('<step>')

    def add_event_listener(self, type, listener):
        if type not in self.event_listeners:
            self.event_listeners[type] = []

        self.event_listeners[type].append(listener)

    def __dispatch_event(self, type, value=False):
        if type in self.event_listeners:
            for event in self.event_listeners[type]:
                event(value)

    def set_user_input(self, input):
        self.user_input = input


if __name__ == "__main__":
    argv = sys.argv[1:]

    i = Interpreter()
    i.run()
