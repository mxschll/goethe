from LanguageTools import LanguageTools
from Token import Token


class Tokenizer:
    """Creates a list of tokens based on the syllables and stylistic elements of a text.
    """

    def __init__(self, language_tools: LanguageTools):
        """
        Args:
            language_tools (LanguageTools): A LanguageTools instance.
        """

        self.__program = []
        self.__lt = language_tools

        self.syllables = self.__lt.count_syllables_in_lines()
        alliterations = self.__lt.find_alliteration()
        epistrophe = self.__lt.find_epistrophe()
        assonance = self.__lt.find_assonance()
        anaphora = self.__lt.find_anaphora()

        # Removes epistrophe that overlap with anaphora.
        epistrophe = [e for e in epistrophe if e not in
                      list(set(anaphora).intersection(epistrophe))]

        for verse in alliterations:
            self.syllables[verse] = 7

        for verse in assonance:
            self.syllables[verse] = 9

        # Adds the syllable numbers of consecutive verses with anaphors.
        for verse in anaphora[::-1]:
            self.syllables[verse[0]] += self.syllables[verse[1]]
            del self.syllables[verse[1]]

        # Subtracts the syllable numbers of consecutive verses with anaphors.
        for verse in epistrophe[::-1]:
            self.syllables[verse[0]] -= self.syllables[verse[1]]
            del self.syllables[verse[1]]

        self.syllables = map(abs, self.syllables)

    def __append_token(self, token: Token) -> None:
        """Appends the given token to the program.

        Args:
            token (Token): Token to be appended.
        """

        self.__program.append(token)

    def tokenize(self) -> list:
        """Converts syllables into a list of program tokens.

        Returns:
            list: List of tokens.
        """

        if not self.__program:
            for i, element in enumerate(self.syllables):
                self.__append_token(Token(element % 10))

        return self.__program
