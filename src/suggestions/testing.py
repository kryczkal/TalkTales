from suggestionsLibrary import upgradeSentence
from sys import argv

if __name__ == "__main__":
    while True:
        zdanie = input("Enter sentence: ") if len(argv) == 1 else argv[1]
        # use quotes to make a sentence a single argument:
        # python3 getWordProbability.py "To jest zdanie przykładowe"
        # print("Prompt: ",zdanie)
        upgradeSentence(zdanie)
        # print("Upgrade: ",upgradeSentence(zdanie))
