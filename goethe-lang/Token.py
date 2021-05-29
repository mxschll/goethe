from enum import Enum


class Token(Enum):
    """A token represents a command that the interpreter can execute.
    """

    PASS = 0
    IF = 1
    FI = 2
    INCVAL = 3
    DECVAL = 4
    INCPTR = 5
    DECPTR = 6
    OUT = 7
    IN = 8
    RND = 9
