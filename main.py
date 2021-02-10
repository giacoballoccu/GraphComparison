from Trie import *
import time

def main():
    t = Trie()
    start = time.time()
    t.populateTrieFromFile("Dataset/English-Words.txt")
    end = time.time()
    print("Time to build the trie: " + str(end - start) + "s")
    start = time.time()
    print(t.contains("maitlandite"))
    end = time.time()
    print("Time to lookup in the trie: " + str(end - start) + "s")
if __name__ == "__main__":
    main()
