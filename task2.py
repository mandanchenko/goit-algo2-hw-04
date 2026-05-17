from trie import Trie

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        pass


    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError(f"Illegal argument: prefix = {prefix} must be a string")

        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        
        return True

if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
   # assert trie.count_words_with_suffix("e") == 1  # apple
    #assert trie.count_words_with_suffix("ion") == 1  # application
    #assert trie.count_words_with_suffix("a") == 1  # banana
    #assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
