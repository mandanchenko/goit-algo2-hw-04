from trie import Trie

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        # Перевірка що передані коректні дані 
        if not isinstance(pattern, str):
            raise TypeError(f"Illegal argument: pattern = {pattern} must be a string")
        
        # Отримуєм всі можливі слова
        all_words = self.keys()
        # Задаєм лічильник для слів з підходящім закінченням
        count = 0
        # Якщо закінчення збігаються - збільшуємо лічильник
        for word in all_words:
            if word.endswith(pattern):
                count+=1

        return count


    def has_prefix(self, prefix) -> bool:
        # Перевірка що передані коректні дані 
        if not isinstance(prefix, str):
            raise TypeError(f"Illegal argument: prefix = {prefix} must be a string")

        # Заходимо в нульовий вузел
        current = self.root
        # Перевіряємо чи є кожен переданий символ в дереві 
        for char in prefix:
            # Якщо якогось символу немає - одразу повертаєм False
            if char not in current.children:
                return False
            current = current.children[char]
        
        # Якщо цикл пройшов успішно - повертаєм True
        return True

if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
