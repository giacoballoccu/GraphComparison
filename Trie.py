from string import ascii_lowercase
class Trie:

    def __init__(self):
        self.root = {}
        self.endSymbol = '*'

    def insertString(self, string):
        node = self.root
        for letter in string:
            if letter not in node:
                node[letter] = {}
            node = node[letter]
        node[self.endSymbol] = True

    def contains(self, string):
        node = self.root
        for letter in string:
            if letter not in node:
                return False
            node = node[letter]
        return self.endSymbol in node

    def populateTrieFromFile(self, path):
        f = open(path, 'r').read().split('\n')
        for x in f:
            self.insertString(x)

