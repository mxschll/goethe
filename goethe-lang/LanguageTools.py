import re
import pyphen


class LanguageTools:
    def __init__(self, text, lang='de_DE'):
        self.hyphen = pyphen.Pyphen(lang=lang)

        self.text = text.casefold()
        self.lines = []
        self.words_in_lines = []
        self.syllables_in_lines = []

        self.__alliteration = []
        self.__assonance = []
        self.__anaphora = []
        self.__epistrophe = []

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

    def count_syllables(self, word: str):
        """Counts syllables in words.

        Args:
            word (str): Word of which the syllables are to be counted.

        Returns:
            int: Number of syllables. Zero, if input is not a word.
        """

        return len(self.hyphen.positions(word.strip())) + 1 if word.strip().isalnum() else 0

    def count_syllables_in_lines(self):
        if not self.syllables_in_lines:
            for line in self.words_in_lines:
                counter = 0
                for word in line:
                    counter += self.count_syllables(word)

                self.syllables_in_lines.append(counter)

        return self.syllables_in_lines

    def find_alliteration(self):
        """Returns a list of positions of alliterations in the text.

        Returns:
            list: List of positions of alliterations in the text.
        """

        if not self.__alliteration:
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
                    self.__alliteration.append(i)

        return self.__alliteration

    def find_assonance(self):
        """This is probably the worst assonance finding algorithm.

        Returns:
            list: List of positions of assonances in the text.
        """
        if not self.__assonance:
            for i in range(len(self.lines)):
                word_list = self.words_in_lines[i]

                if len(word_list) <= 3:
                    # Skip sentences with 3 words or less.
                    continue

                letters_pairs = {}

                for word in word_list:
                    if(len(word) <= 3):
                        # Skip words with 3 characters or less.
                        continue

                    found_pairs = set()

                    for j in range(len(word)):

                        if j < len(word) - 1 and word[j + 1] in 'aeiouäöü':
                            pair = word[j] + word[j + 1]
                            if pair in found_pairs:
                                continue

                            found_pairs.add(pair)
                            letters_pairs[pair] = letters_pairs.get(
                                pair, 0) + 1

                        elif j < len(word) - 1 and word[j] in 'aeiouäöü':
                            pair = word[j] + word[j + 1]
                            if pair in found_pairs:
                                continue

                            found_pairs.add(pair)
                            letters_pairs[pair] = letters_pairs.get(
                                pair, 0) + 1

                if letters_pairs[max(letters_pairs, key=letters_pairs.get)] / len(word_list) > 0.6:
                    self.__assonance.append(i)

        return self.__assonance

    def find_anaphora(self):
        """Recognizes anaphora in successive stanzas.

        Example:
            In every cry of every Man,
            In every infant's cry of fear,
            In every voice, in every ban,
            The mind-forg'd manacles I hear

        Results in:
             [(0, 1), (1, 2)]

        Returns:
            list: List of positions of anaphora in successive stanzas.
        """

        if not self.__anaphora:
            last_starting_word = None
            for i in range(len(self.lines)):
                word_list = self.words_in_lines[i]

                if last_starting_word == word_list[0]:
                    self.__anaphora.append((i - 1, i))

                last_starting_word = word_list[0]

        return self.__anaphora

    def find_epistrophe(self):
        """Recognizes epistrophe in successive stanzas.

        Example:
            Most strange, but yet most truly, will I speak:
            That Angelo's forsworn; is it not strange?
            That Angelo's a murderer; is't not strange?
            That Angelo is an adulterous thief,
            An hypocrite, a virgin-violator;
            Is it not strange and strange? <-- Is not recognized!

        Results in:
            [(1, 2)]

        Returns:
            list: List of positions of epistrophe in successive stanzas.
        """

        if not self.__epistrophe:
            last_ending_word = None
            for i in range(len(self.lines)):
                word_list = self.words_in_lines[i]

                if last_ending_word == word_list[-1]:
                    self.__epistrophe.append((i - 1, i))

                last_ending_word = word_list[-1]

        return self.__epistrophe

