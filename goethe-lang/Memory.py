class Memory:
    def __init__(self, size=128):
        self.memory = bytearray(size)
        self.size = size
        self.pointer = 0

    def increment_pointer(self, steps=1):
        self.pointer = (self.pointer + steps) % self.size

    def decrement_pointer(self, steps=1):
        self.pointer = (self.pointer - steps) % self.size

    def increment_value(self, steps=1):
        self.memory[self.pointer] += steps

    def decrement_value(self, steps=1):
        self.memory[self.pointer] -= steps

    def __sizeof__(self):
        return self.size

    def __repr__(self):
        return self.memory.decode('ascii')