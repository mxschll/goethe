class Memory:
    """Represents a register–memory of a given length and allows operations on it.

    Attributes:
        _memory (bytearray): The byte array that represents the memory.
        _size (int): Size of the byte array.
        _pointer (int): Points at the current memory position.
    """

    def __init__(self, size=1024):
        """Memory class constructor.

        Args:
            size (int, optional): Size of the memory. Defaults to 512.
        """

        self._memory = bytearray(size)
        self._size = size
        self._pointer = 0

    def increment_pointer(self, steps=1):
        """Increments the pointer position by a given number of steps.

        Args:
            steps (int, optional): Number of steps the pointer should be increased. Defaults to 1.
        """

        self._pointer = (self._pointer + steps) % self._size

    def decrement_pointer(self, steps=1):
        """Decrements the pointer position by a given number of steps.

        Args:
            steps (int, optional): Number of steps the pointer should be decreased. Defaults to 1.
        """

        self._pointer = (self._pointer - steps) % self._size

    def increment_value(self, number=1):
        """Increments the byte value by a given number.

        Args:
            number (int, optional): The number by which the byte value should be increased. Defaults to 1.
        """

        self._memory[self._pointer] += number

    def decrement_value(self, number=1):
        """Decrements the byte value by a given number.

        Args:
            number (int, optional): The number by which the byte value should be decreased. Defaults to 1.
        """

        self._memory[self._pointer] -= number

    def set_value(self, value: int):
        """Sets memory byte to a given value.

        Args:
            value (int): Value to be saved.
        """
        self._memory[self._pointer] = value

    def get_value(self):
        """Returns memory value at current pointer position.

        Returns:
            int: Memory value at current pointer position.
        """
        return self._memory[self._pointer]

    def __sizeof__(self):
        """Returns the size of the byte array.

        Returns:
            int: Size of byte array.
        """

        return self._size

    def __repr__(self):
        """Returns the byte array as ascii decoded string.

        Returns:
            string: Ascii decoded byte array.
        """

        return self._memory.decode('ascii')
