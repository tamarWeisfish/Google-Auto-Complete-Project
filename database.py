from pathlib import Path
from node import Node


class DataBase:
    """manages the database of the program: dictionary and trie"""

    def __init__(self):
        self.trie_root = Node(None)
        self.dict_of_sentences = {}
        self.num_words = 0

    def get_sentence_by_id(self, id):
        """return sentence from dictionary by id"""
        return self.dict_of_sentences.get(id)

    def add_word_to_database(self, word):
        """add one word to trie"""
        next_node = self.trie_root
        for char in word:
            if char not in next_node.get_next_chars():
                current_char = Node(char)
                next_node.add_char_to_node(current_char)
            next_node = next_node.get_node(char)
        if "$" not in next_node.get_next_chars():
            end_of_word = Node("$")
            next_node.add_char_to_node(end_of_word)
        else:
            end_of_word = next_node.get_node("$")
        end_of_word.add_sentence_to_node(self.num_words)

    def add_sentence_to_database(self, sentence):
        """add sentence to database by adding every word in sentence to trie, and every sentence to dictionary"""
        self.dict_of_sentences.update({self.num_words: sentence})
        parsed_sentence = sentence.lower().split()
        for word in parsed_sentence:
            self.add_word_to_database(word)
        self.num_words += 1

    def insert_data_to_db(self):
        """insert all the given data to the database"""
        files = list(Path("./data").rglob("*.[tT][xX][tT]"))
        for file in files:
            with open(file, encoding="utf8") as my_file:
                lines = my_file.readlines()
            for sentence in lines:
                if sentence[:-1]:
                    self.add_sentence_to_database(sentence[:-1])

    def get_sentences_of_word(self, word):
        """passing the trie and finding the sentences of word"""
        word = word.replace(" ", "$")
        word_counter = 0
        node = self.trie_root
        while word_counter < len(word):
            if word[word_counter] in node.get_next_chars():
                node = node.get_node(word[word_counter])
                word_counter += 1
            else:
                return []
        node = node.get_node("$")
        if node:
            res = node.get_sentences()
            if res:
                return res
        return []
