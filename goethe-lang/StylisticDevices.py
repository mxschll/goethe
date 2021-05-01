import re
import pyphen


class StylisticDevices:
    def __init__(self, text, lang='de_DE'):
        self.hyphen = pyphen.Pyphen(lang=lang)

        self.text = text.casefold()
        self.lines = []
        self.words_in_lines = []

        self.__alliterations = []
        self.__anaphors = []

        self.extract_lines()
        self.extract_words_in_lines()

    def extract_lines(self):
        """Splits text into lines, strips whitespace and removes empty lines.

        Returns:
            list: List of text lines.
        """

        if not self.lines:
            self.lines = [line.strip()
                          for line in self.text.splitlines() if line.strip()]

        return self.lines

    def extract_words_in_lines(self):
        """Creates multidimensional list with a list of words for every line.

        Returns:
            list: List of list with words for every text line.
        """

        if not self.words_in_lines:
            for line in self.lines:
                word_list = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß ]", '', line).split()
                self.words_in_lines.append(word_list)

        return self.words_in_lines

    def find_alliterations(self):
        """Returns a list of positions of alliterations in the text.

        Returns:
            list: List of positions of alliterations in the text.
        """

        if not self.__alliterations:
            for i in range(len(self.lines)):
                word_list = self.words_in_lines[i]

                if(len(word_list) <= 3):
                    # Skip sentences with 3 words or less.
                    continue

                initials = [word[0] for word in word_list]
                initials_count = dict((c, initials.count(c))
                                      for c in initials)

                max_occurences = initials_count[max(
                    initials_count, key=initials_count.get)]

                if max_occurences / len(initials) > 0.6:
                    self.__alliterations.append(i)

        return self.__alliterations

    def find_anaphors(self):
        """Returns a list of positions of anaphors in the text.

        Returns:
            list: List of positions of anaphors in the text.
        """

        if not self.__anaphors:
            last_starting_word = None
            for i in range(len(self.lines)):
                word_list = self.words_in_lines[i]

                if last_starting_word == word_list[0]:
                    self.__anaphors.append((i - 1, i))

                last_starting_word = word_list[0]

        return self.__anaphors
