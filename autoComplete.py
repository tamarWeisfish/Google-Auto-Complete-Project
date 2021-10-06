import difflib

from database import DataBase


class AutoComplete:
    def __init__(self):
        self.db = DataBase()

    @staticmethod
    def cover_find_word(word):
        """return all the word casts"""
        words_states = {}
        all_letter = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                      "t", "u", "v", "w", "x", "y", "z", ""]
        for i in range(len(word)):
            for letter in all_letter:
                words_states.update({word[0:i] + letter + word[i + 1:len(word)]: ("change", i)})
                words_states.update({word[0:i] + letter + word[i:len(word)]: ("append/remove", i)})
                words_states.update({word[0:i] + word[i + 1:len(word)]: ("append/remove", i)})
                if i == len(word) - 1 and len(word) > 1:
                    words_states.update({word[0:i] + letter: ("append/remove", i)})
                    words_states.update({word[0:i + 1] + letter: ("append/remove", i)})

        words_states.update({word: ("no change", 0)})
        return words_states  # dict of words and status

    def sentences_for_input(self, input_of_user):
        """return all the sentences that match the input of the user"""
        if not input_of_user:
            return []
        sentences = self.get_sentences_of_sentence(input_of_user)
        reduced_sentences = {}
        for sentence, error in sentences.items():
            if sentence not in reduced_sentences:
                reduced_sentences.update({sentence: error})
        return reduced_sentences

    def get_all_sentences_of_word(self, word):
        """return all the id's of sentences that contain the given word"""
        words_states = self.cover_find_word(word)
        sentences_index = {}
        for word, error in words_states.items():
            sentences = self.db.get_sentences_of_word(word)
            for sentence in sentences:
                if sentence in sentences_index.keys():
                    if sentences_index[sentence][0] == "append/remove":
                        if sentences_index[sentence][1] > error[1]:
                            sentences_index.update({sentence: error})
                    elif sentences_index[sentence][1] > error[1]:
                        sentences_index.update({sentence: error})
                else:
                    sentences_index.update({sentence: error})
        return sentences_index  # return sentences indexes and errors

    def get_sentences_of_sentence(self, sentence):
        """return all the sentences that contain at least one word from the given sentence"""
        sentence = sentence.split()
        sentences = self.get_all_sentences_of_word(sentence[0])
        for word in sentence[1:]:
            sentence_for_word = self.get_all_sentences_of_word(word)
            for s, error in sentence_for_word.items():
                if s in sentences.keys():
                    if sentences[s][0] == "no change":
                        sentences[s] = error
                    if error[0] != "no change" and sentences[s][0] != "no change":
                        sentences.pop(s)
        return sentences

    # @staticmethod
    def score_sentence(self, sentence, input_of_user):
        """ return the score of a sentence for user's input"""
        change = {0: 5, 1: 4, 2: 3, 3: 2, 4: 1}
        append_remove = {0: 10, 1: 8, 2: 6, 3: 4, 4: 2}
        score = 2 * len(input_of_user)
        error = list(sentence.values())[0]
        current_sentence = self.db.get_sentence_by_id(list(sentence.keys())[0]).lower()
        place_of_error = error[1] + 1 if error[1] <= 3 else 4
        if error[0] == "no change" and input_of_user not in current_sentence.lower():
            score = 0
        if error[0] == "append/remove":
            score -= append_remove[place_of_error]
        if error[0] == "change":
            score -= change[place_of_error]
        return score

    def find_max_five_sentences(self, input_of_user):
        """return the five sentences whose score are the biggest"""
        sentences = self.sentences_for_input(input_of_user)
        scores = {}
        for sentence, error in sentences.items():
            score = self.score_sentence({sentence: error}, input_of_user)
            if score > 0:
                if score in scores.keys():
                    scores.update({score: scores[score] + [sentence]})
                else:
                    scores.update({score: [sentence]})
        last_scores = []
        while len(last_scores) < 5 and len(scores):
            max_score = list(scores.keys())[0] if len(scores) < 2 else max(scores)
            items = scores[max_score]
            for item in items:
                last_scores.append((max_score, item))
            scores.pop(max_score)
        if len(last_scores) > 5:
            last_scores = last_scores[:5]
        return last_scores

    def display_sentences(self, sentences):
        """print the sentences in the required display"""
        for i in range(len(sentences)):
            print(f"{i + 1}. {self.db.get_sentence_by_id(sentences[i][1])} (score: {sentences[i][0]})")

    def execute(self):
        """execute the main program"""
        self.db.insert_data_to_db()
        old_search = ''
        print('The system is ready. Enter your text: ')
        while True:
            search = input(old_search)
            old_search = '' if search == '#' else old_search + search
            if old_search:
                max_scored_sentences = self.find_max_five_sentences(old_search)
                self.display_sentences(max_scored_sentences)


if __name__ == '__main__':
    ac = AutoComplete()
    ac.execute()
