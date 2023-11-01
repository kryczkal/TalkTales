from suggestionsLibrary import upgrade_sentence
from sys import argv

if __name__ == "__main__":
    while True:
        sentence = input("Enter sentence: ") if len(argv) == 1 else argv[1]
        # use quotes to make a sentence a single argument:
        # python3 getWordProbability.py "This is example sentence"
        # print("Prompt: ",sentence)
        upgrade_sentence(sentence)
        # print("Upgrade: ",upgradeSentence(sentence))
