# Goethe Language

## Requirements
- Python  3.8+
## Language Specification



### Syllables per verse

| Syllables | Command | Description                                                  |      |
| --------- | ------- | ------------------------------------------------------------ | ---- |
| 0         | PASS    | Do nothing.                                                  |      |
| 1         | LOOP    | Jump to the appropriate FI if the current memory value is 0. |      |
| 2         | POOL    | Jump to the appropriate IF if the current memory value is != 0. |      |
| 3         | INCVAL  | Increment the current memory value.                          |      |
| 4         | DECVAL  | Decrement the current memory value.                          |      |
| 5         | INCPTR  | Increment the program pointer.                               |      |
| 6         | DECPTR  | Decrement the program pointer.                               |      |
| 7         | OUT     | Output the current memory value as ASCII.                    |      |
| 8         | IN      | Read the user input character by character and write it into the memory. |      |
| 9         | RND     | Write random number between 0 and 255 into memory.           |      |



### Stylistic devices

TODO
