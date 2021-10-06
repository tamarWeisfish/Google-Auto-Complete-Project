class Node:
    def __init__(self, value):
        self.value = value
        self.next_chars = []
        self.sentences = []

    def add_char_to_node(self, char):
        """add char to the list of next_chars"""
        self.next_chars.append(char)

    def add_sentence_to_node(self, sentence):
        """add sentence to the list of sentences"""
        self.sentences.append(sentence)

    def get_next_chars(self):
        """return the next_chars of node"""
        chars = []
        for char in self.next_chars:
            chars.append(char.value)
        return chars

    def get_sentences(self):
        """return the sentences of node"""
        return self.sentences

    def get_node(self, existing_char):
        """return the object Node to given char"""
        for char in self.next_chars:
            if char.value == existing_char:
                return char

    def get_node_value(self):
        """return the value=char of node"""
        return self.value
