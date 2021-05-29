class Memory:
    """Represents a register–memory of a given length and allows operations on it.

    Attributes:
        _memory (list): The list that represents the memory.
        _size (int): Size of the memory.
        _pointer (int): Points at the current memory position.
    """

    def __init__(self, size=1024):
        """Memory class constructor.

        Args:
            size (int, optional): Size of the memory. Defaults to 1024.
        """

        self._memory = [0]*size
        self._size = size
        self._pointer = 0

    def reset(self) -> None:
        """Sets pointer to 0 and sets all memory cells to 0.
        """

        self._memory = [0]*self._size
        self.set_pointer_value(0)

    def increment_pointer(self, steps=1) -> None:
        """Increments the pointer position by a given number of steps.

        Args:
            steps (int, optional): Number of steps the pointer should be increased. Defaults to 1.
        """

        self._pointer = (self._pointer + steps) % self._size

    def decrement_pointer(self, steps=1) -> None:
        """Decrements the pointer position by a given number of steps.

        Args:
            steps (int, optional): Number of steps the pointer should be decreased. Defaults to 1.
        """

        self._pointer = (self._pointer - steps) % self._size

    def set_pointer_value(self, value: int) -> None:
        """Sets the memory pointer to the given value.

        Args:
            value (int): Value to which the memory piointer should be set.
        """

        self._pointer = value % self._size

    def get_pointer_value(self) -> int:
        """Returns the current memory pointer value.

        Returns:
            int: Current pointer value.
        """

        return self._pointer

    def increment_value(self, number=1) -> None:
        """Increments the byte value by a given number.

        Args:
            number (int, optional): The number by which the byte value should be increased. Defaults to 1.
        """

        self._memory[self._pointer] += number

    def decrement_value(self, number=1) -> None:
        """Decrements the byte value by a given number.

        Args:
            number (int, optional): The number by which the byte value should be decreased. Defaults to 1.
        """

        self._memory[self._pointer] -= number

    def set_value(self, value: int) -> None:
        """Sets memory byte to a given value.

        Args:
            value (int): Value to be saved.
        """
        self._memory[self._pointer] = value

    def get_value(self) -> None:
        """Returns memory value at current pointer position.

        Returns:
            int: Memory value at current pointer position.
        """
        return int(self._memory[self._pointer])

    def __sizeof__(self) -> int:
        """Returns the size of the byte array.

        Returns:
            int: Size of byte array.
        """

        return self._size

    def __repr__(self) -> str:
        """Returns the byte array as ascii decoded string.

        Returns:
            string: Ascii decoded byte array.
        """

        return ''.join(chr(c) for c in self._memory)

    def to_list(self) -> list:
        """Returns memory contents as integer list.

        Returns:
            list: The memory list.
        """

        return self._memory
