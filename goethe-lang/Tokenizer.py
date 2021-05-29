from LanguageTools import LanguageTools
from Token import Token


class Tokenizer:
    def __init__(self, language: LanguageTools):
        self.language = language
        self.__program = []

        self.syllables = self.language.count_syllables_in_lines()
        alliterations = self.language.find_alliteration()
        epistrophe = self.language.find_epistrophe()
        assonance = self.language.find_assonance()
        anaphora = self.language.find_anaphora()

        # Removes epistrophe that overlap with anaphora
        epistrophe = [e for e in epistrophe if e not in
                      list(set(anaphora).intersection(epistrophe))]

        for verse in alliterations:
            self.syllables[verse] = 7

        for verse in anaphora[::-1]:
            self.syllables[verse[0]] += self.syllables[verse[1]]
            del self.syllables[verse[1]]

        for verse in epistrophe[::-1]:
            self.syllables[verse[0]] -= self.syllables[verse[1]]
            del self.syllables[verse[1]]

        self.syllables = ''.join(map(str, self.syllables))
        self.syllables = [int(char) for char in self.syllables]

    def tokenize(self) -> list:
        """Converts syllables into a list of program tokens.

        Returns:
            list: List of tokens.
        """

        if not self.__program:
            for i, element in enumerate(self.syllables):
                self.__append_token(Token(element % 10))

        return self.__program

    def __append_token(self, token: Token) -> None:
        """Appends the given token to the program.

        Args:
            token (Token): Token to be appended.
        """

        self.__program.append(token)
