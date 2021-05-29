import re
import pyphen
import numpy as np


class LanguageTools:
    def __init__(self, text, lang='de_DE'):
        self.hyphen = pyphen.Pyphen(lang=lang)

        self.text = text.casefold()
        self.lines = []
        self.phonetics = []
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
                          for line in self.text.splitlines() if re.sub(r"[^a-zA-Z0-9äöüÄÖÜß ]", '', line)]

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
        if not self.__assonance:
            line_index = 0
            for line in self.lines:
                phonetics = [p for p in self.__cologne_phonetics(
                    line) if len(p) > 2]  # Execlude ponetics with less than 2 chars

                levenshtein_distances = []

                for i in range(len(phonetics)):
                    min_distance = None

                    for j in range(len(phonetics)):
                        if j == i:
                            continue
                        distance = self.__levenshtein_distance(
                            phonetics[i], phonetics[j])
                        if distance != 0 and min_distance is None:  # Execlude same word comparisons
                            min_distance = distance
                        if distance != 0 and distance < min_distance:
                            min_distance = distance

                    if min_distance is not None:
                        levenshtein_distances.append(min_distance)

                if len(levenshtein_distances) > 1 and sum(levenshtein_distances) / len(levenshtein_distances) < 1.4:
                    self.__assonance.append(line_index)

                line_index += 1

            return self.__assonance

    def __find_assonance_old(self):
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

    def __cologne_phonetics(self, string: str):
        # Source: https://en.wikipedia.org/wiki/Cologne_phonetics
        REGEX_RULES = [
            # Replace umlauts and non-aphanumeric chars
            (r'ä',                   'a'),
            (r'ö',                   'o'),
            (r'ü',                   'u'),
            (r'ß',                   '8'),
            (r'[^a-z]',               ''),
            (r'[dt](?![csz])',       '2'),
            (r'[dt](?=[csz])',       '8'),
            (r'[ckq]x',             '88'),
            (r'[sz]c',              '88'),
            (r'^c(?=[ahkloqrux])',   '4'),
            (r'^c',                  '8'),
            (r'(?<![sz])c',          '4'),
            (r'x',                  '48'),
            (r'p(?!h)',              '1'),
            (r'p(?=h)',              '3'),
            (r'h',                    ''),
            (r'[aeijouy]',           '0'),
            (r'b',                   '1'),
            (r'[fvw]',               '3'),
            (r'[gkq]',               '4'),
            (r'l',                   '5'),
            (r'[mn]',                '6'),
            (r'r',                   '7'),
            (r'[csz]',               '8'),
            (r'([^\w\s])|(.)(?=\2)', ''),
            (r'\B0', '')
        ]

        phonetics = []
        for word in string.split():
            for sub in REGEX_RULES:
                word = re.sub(sub[0], sub[1], word, flags=re.IGNORECASE)
            phonetics.append(word)

        return phonetics

    def __levenshtein_distance(self, seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix[x, y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1] + 1,
                        matrix[x, y-1] + 1
                    )
        return (matrix[size_x - 1, size_y - 1])
