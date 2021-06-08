import re
import pyphen


class LanguageTools:
    """Analyzes text for stylistic devices and syllables.
    """

    def __init__(self, text: str, lang='de_DE'):
        """
        Args:
            text (str): Text to analyze.
            lang (str, optional): Language of the text. Defaults to 'de_DE'.
        """

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

    def extract_lines(self) -> list:
        """Splits text into lines, strips whitespace and removes empty lines.

        Returns:
            list: List of text lines.
        """

        if not self.lines:
            self.lines = [line.strip() for line in self.text.splitlines()
                          if re.sub(r"[^a-zA-Z0-9äöüÄÖÜß ]", '', line)]

        return self.lines

    def extract_words_in_lines(self) -> list:
        """Creates multidimensional list with a list of words for every line.

        Returns:
            list: List of lists with words for every text line.
        """

        if not self.words_in_lines:
            for line in self.extract_lines():
                word_list = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß ]", '', line).split()
                self.words_in_lines.append(word_list)

        return self.words_in_lines

    def count_syllables(self, word: str) -> int:
        """Counts the syllables of the given word.

        Args:
            word (str): Word of which the syllables are to be counted.

        Returns:
            int: Number of syllables. Zero, if input is not a valid word.
        """

        return len(self.hyphen.positions(word.strip())) + 1 if word.strip().isalnum() else 0

    def count_syllables_in_lines(self) -> list:
        """Returns a list of syllabes for each line in the text.

        Returns:
            list: List of syllables per line.
        """

        if not self.syllables_in_lines:
            for line in self.extract_words_in_lines():
                counter = 0
                for word in line:
                    counter += self.count_syllables(word)

                self.syllables_in_lines.append(counter)

        return self.syllables_in_lines

    def find_alliteration(self) -> list:
        """Returns a list of positions of alliterations in the text.

        Returns:
            list: List of positions of alliterations in the text.
        """

        if not self.__alliteration:
            for index, word_list in enumerate(self.extract_words_in_lines()):

                if(len(word_list) <= 3):
                    # Skip sentences with 3 words or less.
                    continue

                initials = [word[0] for word in word_list]
                # Count the number of words that begin with the same letter.
                initials_count = dict((c, initials.count(c)) for c in initials)

                max_occurences = initials_count[
                    max(initials_count, key=initials_count.get)]

                if max_occurences / len(initials) > 0.6:
                    # If over 60% of the words start with the same letter, it's an aliteration.
                    self.__alliteration.append(index)

        return self.__alliteration

    def find_assonance(self) -> list:
        """Returns a list of positions of assonance in the text.

        Example:
            The light of the fire is a sight.

        Returns:
            list: List of positions of assonance in the text.
        """

        if not self.__assonance:
            for index, word_list in enumerate(self.extract_words_in_lines()):

                phonetics = []
                for word in word_list:
                    p = self.__cologne_phonetics(word)
                    if len(p) > 2:
                        phonetics.append(p)

                distances = []

                for i, one in enumerate(phonetics):
                    min_distance = None

                    for j, two in enumerate(phonetics):
                        if j == i:
                            continue

                        distance = self.__levenshtein_distance(one, two)
                        if distance != 0 and min_distance is None:
                            min_distance = distance
                        if distance != 0 and distance < min_distance:
                            min_distance = distance

                    if min_distance is not None:
                        distances.append(min_distance)

                if len(distances) > 2 and sum(distances) / len(distances) < 1.3:
                    self.__assonance.append(index)

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

    def find_anaphora(self) -> list:
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
            for index, word_list in enumerate(self.extract_words_in_lines()):
                if last_starting_word == word_list[0]:
                    self.__anaphora.append((index - 1, index))

                last_starting_word = word_list[0]

        return self.__anaphora

    def find_epistrophe(self) -> list:
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
            for index, word_list in enumerate(self.extract_words_in_lines()):
                if last_ending_word == word_list[-1]:
                    self.__epistrophe.append((index - 1, index))

                last_ending_word = word_list[-1]

        return self.__epistrophe

    def __cologne_phonetics(self, word: str) -> str:
        """Applies the cologne phonetics algorithm to the given word.
        Source: https://en.wikipedia.org/wiki/Cologne_phonetics

        Args:
            word (str): Word to which the algorithm should be applied.

        Returns:
            str: Cologne phonetics sequence for the given word.
        """

        """
            The following table lists the rules of Cologne phonetics.
            |                           Letter                            |                        Context                        | Code |
            | :---------------------------------------------------------: | :---------------------------------------------------: | :--: |
            |                     A, E, I, J, O, U, Y                     |                                                       |  0   |
            |                              H                              |                                                       |  -   |
            |                              B                              |                                                       |  1   |
            |                              P                              |                     not before H                      |      |
            |                            D, T                             |                  not before C, S, Z                   |  2   |
            |                           F, V, W                           |                                                       |  3   |
            |                              P                              |                       before H                        |      |
            |                           G, K, Q                           |                                                       |  4   |
            |                              C                              | in the initial sound before A, H, K, L, O, Q, R, U, X |      |
            |        before A, H, K, O, Q, U, X except after S, Z         |                                                       |      |
            |                              X                              |                   not after C, K, Q                   |  48  |
            |                              L                              |                                                       |  5   |
            |                            M, N                             |                                                       |  6   |
            |                              R                              |                                                       |  7   |
            |                            S, Z                             |                                                       |  8   |
            |                              C                              |                      after S, Z                       |      |
            | in initial position except before A, H, K, L, O, Q, R, U, X |                                                       |      |
            |               not before A, H, K, O, Q, U, X                |                                                       |      |
            |                            D, T                             |                    before C, S, Z                     |      |
            |                              X                              |                     after C, K, Q                     |      |
        """

        REGEX_RULES = [
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

        for sub in REGEX_RULES:
            word = re.sub(sub[0], sub[1], word, flags=re.IGNORECASE)

        return word

    def __levenshtein_distance(self, seq1: str, seq2: str) -> int:
        """Calculates the levenshtein distance of two strings.
        Source: https://en.wikipedia.org/wiki/Levenshtein_distance#Definition

        Args:
            seq1 (str): String one.
            seq2 (str): String two.

        Returns:
            int: Levenshtein distance of the given strings.
        """

        if len(seq1) > len(seq2):
            seq1, seq2 = seq2, seq1

        d = range(len(seq1) + 1)
        for i, char2 in enumerate(seq2):
            d_tmp = [i+1]
            for j, char1 in enumerate(seq1):
                if char1 == char2:
                    d_tmp.append(d[j])
                else:
                    d_tmp.append(1 + min((d[j],
                                          d[j+1],
                                          d_tmp[-1])))
            d = d_tmp

        return d[-1]
