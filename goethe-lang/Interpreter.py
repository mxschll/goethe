import sys
from Memory import Memory
from Tokenizer import Tokenizer


class Interpreter:
    def __init__(self):
        self.program = []
        self.pointer = 0
        self.nesting = 0
        self.memory = Memory()
        self.tokenize = Tokenizer()

    def _step(self):
        self.pointer += 1

    def _get_next_instruction(self):
        if not self._has_next_instruction():
            return None

        self.pointer += 1
        return self.program[self.pointer - 1]

    def _get_previous_instruction(self):
        if self.pointer == None:
            return None

        self.pointer -= 1
        return self.program[self.pointer + 1]

    def _has_next_instruction(self):
        return self.pointer < len(self.program)

    def IF(self):
        self.nesting += 1
        if self.memory.get_value() != 0:
            return

        while self.nesting:
            instruction = self._get_next_instruction()
            if instruction == 'IF':
                self.nesting += 1
            elif instruction == 'FI':
                self.nesting -= 1

    def FI(self):
        self.nesting -= 1
        if self.memory.get_value() == 0:
            return

        while self.nesting:
            instruction = self._get_previous_instruction()
            if instruction == 'IF':
                self.nesting += 1
            elif instruction == 'FI':
                self.nesting -= 1

    def IN(self):
        char = ord(sys.stdin.read(1)) % 256
        self.memory.set_value(char)

    def OUT(self):
        print(chr(self.memory.get_value()), end="", flush=True)

    def INCPTR(self):
        self.memory.increment_pointer()

    def DECPTR(self):
        self.memory.decrement_pointer()

    def INCVAL(self):
        self.memory.increment_value()

    def DECVAL(self):
        self.memory.decrement_value()

    def SETVAL(self):
        value = int(self._get_next_instruction())
        self.memory.set_value(value)

    def _run(self):
        while self._has_next_instruction():
            instruction = self._get_next_instruction()
            getattr(self, instruction)()
