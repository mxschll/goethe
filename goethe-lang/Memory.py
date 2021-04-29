class Memory:
    """Represents a register–memory of a given length and allows operations on it.

    Attributes:
        _memory (bytearray): The byte array that represents the memory.
        _size (int): Size of the byte array.
        _pointer (int): Points at the current memory position.
    """

        """Memory class constructor.

        Args:
            size (int, optional): Size of the memory. Defaults to 512.
        """

        self._memory = bytearray(size)

    def increment_pointer(self, steps=1):
        """Increments the pointer position by a given number of steps.

        Args:
            steps (int, optional): Number of steps the pointer should be increased. Defaults to 1.
        """


    def decrement_pointer(self, steps=1):
        """Decrements the pointer position by a given number of steps.

        Args:
            steps (int, optional): Number of steps the pointer should be decreased. Defaults to 1.
        """


        """Increments the byte value by a given number.

        Args:
            number (int, optional): The number by which the byte value should be increased. Defaults to 1.
        """

        """Decrements the byte value by a given number.

        Args:
            number (int, optional): The number by which the byte value should be decreased. Defaults to 1.
        """
    def __sizeof__(self):
        """Returns the size of the byte array.

        Returns:
            int: Size of byte array.
        """

    def __repr__(self):
        """Returns the byte array as ascii decoded string.

        Returns:
            string: Ascii decoded byte array.
        """
