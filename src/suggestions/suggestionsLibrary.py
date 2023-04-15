import torch
from sys import argv
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
from typing import List
from copy import deepcopy
import numpy as np

# pip install numpy
# pip install torch
# pip install transformers

# suppress pool size warnings
from transformers import logging
logging.set_verbosity_error()

#Settings
DYNAMIC_TRESHOLD = True
PERCENTILE_VALUE = 25
PROBABILITY_TRESHOLD = 0.1
MODEL_NAME = "allegro/herbert-large-cased"
TOKENIZER_NAME = "allegro/herbert-large-cased"
DEBUG = 0
HARD_DEBUG = 0
#
if (DEBUG!=1):
    HARD_DEBUG = 0
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name()}")
else:
    device = torch.device("cpu")
    print("Using CPU")

MODEL = AutoModelForMaskedLM.from_pretrained(MODEL_NAME).to(device)
TOKENIZER = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
fill_mask = pipeline("fill-mask", model=MODEL_NAME, tokenizer=MODEL_NAME, device=device.index)
#

def getWordProbability(tokens: List[str]) -> List[float]:
    """Get probabilities of each word's presence in a sentence
    """

    if(DEBUG):
        print("")
    
    # Calculate probability of each word being present in the sentence
    probabilities = {}
    for index, token in enumerate(tokens):
        # Create masked sentence
        masked_sentence = tokens.copy()
        masked_sentence[index] = TOKENIZER.mask_token
        masked_sentence.insert(0, TOKENIZER.cls_token)
        masked_sentence.append(TOKENIZER.sep_token)

        # Convert masked sentence to a vector
        output = TOKENIZER.convert_tokens_to_ids(masked_sentence)
        input_tensor = torch.tensor([output]).to(device)

        # Predict probabilities for masked words
        with torch.no_grad():
            output = MODEL(input_tensor)
        predictions = output.logits[0, index + 1].softmax(dim=-1)

        # Calculate the probability of the original word
        probability = predictions[TOKENIZER.convert_tokens_to_ids([token])[0]].item()
        probabilities[token] = probability

    total_probability = 0
    syllable_count = 0
    probabilities_of_words = []
    if (HARD_DEBUG):
        print("Zamieniam zdanie na Tokeny:",tokens)
    for index, token in enumerate(tokens):
        syllable_count+=1
        total_probability += probabilities[token] 
        if token.find("</w>") != -1:
            probabilities_of_words.append(total_probability/syllable_count)
            syllable_count = 0
            total_probability = 0
    return probabilities_of_words

#
def generateSuggestions(sentence: str, index: int, tokens_i_mod: int ,tokens: List[str]) -> str:
    if(DEBUG):
        print("")
    mask_token = TOKENIZER.mask_token
    if(HARD_DEBUG):
        print("index:",index)
        print("tokens_i_mod",tokens_i_mod)
        print("tokens_index",tokens_i_mod+index)
        print("")
    if(HARD_DEBUG):
        print("Maskuje tokeny reprezentujące mało prawdopodobne słowo")
    if(HARD_DEBUG):
        print("Sprawdzam czy słowo jest reprezentowane przez kilka tokenow")
    #Jesli nie znalazlo znaku zakonczenia wyrazu
    if (tokens[index+tokens_i_mod].find("</w>") == -1):
        if(HARD_DEBUG):
            print("Tak")
        #Kopiuje index wyrazu od ktorego zaczynamy
        new_index = deepcopy(index+tokens_i_mod)
        #Dopoki nie znajduje znaku zakonczenia wyrazu dodaje usuwam tokeny
        while(tokens[new_index].find("</w>") == -1):
            if(HARD_DEBUG):
                print(f"Tokeny tworzące: {tokens[new_index]}")
            tokens.pop(new_index)
            #new_index += 1
        #Indeks ktory zakancza wyraz zamieniam na <mask>
        if(HARD_DEBUG):
            print(f"Teraz ostatni token: {tokens[new_index]}")
        tokens[new_index] = mask_token
    else:
         if(HARD_DEBUG):
            print("Nie")
         tokens[index+tokens_i_mod] = mask_token
    
    #fix z czapy
    if(index+tokens_i_mod == len(tokens)-1):
        tokens.append(".")
    masked_sentence = TOKENIZER.convert_tokens_to_string(tokens)
    if(HARD_DEBUG):
        print("Zamaskowane Zdanie:", masked_sentence)

    result = fill_mask(masked_sentence)
    # Zamień zamaskowane słowo na najbardziej prawdopodobne
    tokens[index+tokens_i_mod] = result[0]["token_str"] + ' '
    new_sentence = TOKENIZER.convert_tokens_to_string(tokens)
    if(HARD_DEBUG):
        print("Nowe Zdanie:", new_sentence)
    #print(new_sentence)
    new_sentence = new_sentence.split(' ')
    if(HARD_DEBUG):
        print(f"Zwracam Indeks poprawionego slowa: {index}")
    if(DEBUG):
        print(f"Mialem poprawic: {sentence[index]}")
        print(f"Poprawiłem na: {new_sentence[index]}")
    if(index+tokens_i_mod == len(tokens)-1):
        tokens.pop()
    return new_sentence[index]

#
def upgradeSentence(sentence: str) -> str:

    #Operujemy na kopi zdania.
    if(DEBUG):
        print("")
        print("Zaczynamy")
        print("")
    #Usuwamy ze zdania niepotrzebne znaki
    if(DEBUG):
        print("Usuwam z zdania przecinki i kropki")
    sentence = sentence.replace(',','')
    sentence = sentence.replace('.','')
    if(DEBUG):
        print("Zdanie po poprawkach:", sentence)
    #Tokenizujemy zdanie
    tokens = TOKENIZER.tokenize(sentence)

    #rozbijamy zdanie na wyrazy
    
    sentence = sentence.split(' ')
    
    if(DEBUG):
        print("Rozbijam zdanie na wyrazy:", sentence)
        print("Liczba slow:",len(sentence))

    if(HARD_DEBUG):
            print("Kopiuje tokeny oraz zdanie")

    tokens_backup = deepcopy(tokens)
    sentence_backup = deepcopy(sentence)

    if(DEBUG):
        print("Kalkuluje prawdopodobienstwo wystepowania kazdego slowa")
    #badamy prawdopodobienstwo wystepowania kazdego slowa
    probabilities = getWordProbability(tokens)
    PROBABILITY_TRESHOLD = np.percentile(probabilities, PERCENTILE_VALUE)
    if(DEBUG):
        print("Wyniki: ", probabilities)
        print("Liczba prawdopodobieństw:",len(probabilities))
        
    #dodajemy w petli sugestie dla malo prawdopodobnych slow
    added_suggestions = 0

    suggested_words = {}

    if(DEBUG):
        print("Generuje sugestie dla każdego mało prawdopodobnego słowa")
    
    tokens_i_mod = 0
    for i in range(len(probabilities)):
        #Jesli slowo ma niskie prawdopodobienstwo wystepowania, generujemy sugestie
        if(probabilities[i] < PROBABILITY_TRESHOLD):
            if(HARD_DEBUG):
                print("Zdanie",sentence)
                print("Tokeny",tokens)
            #Generujemy sugestie
            if(DEBUG):
                print("")
                print("Słowo:", sentence[i])
                print("Mało prawdopodobne:", probabilities[i])

            suggestion = generateSuggestions(sentence, i, tokens_i_mod, tokens)

            #suggestion = " (" + suggestion + ") "
            #sentence.insert(i + added_suggestions + 1, suggestion)
            # print("Index ",i," Slowo:",sentence[i]," Proponuje zamienic na: ", suggestion)
            #if(HARD_DEBUG):
                #print("Zamieniam slowo:", sentence[i])
                #print("Na:", suggestion)
                
            #sentence[i] = suggestion
            suggested_words[i] = suggestion

            #if(HARD_DEBUG):
            #    print("Zamienione zdanie:", " ".join(sentence))
            # print("CALKIEM PRAWDOPODOBNE", " ".join(new_sentence))
            #sentence[i] = suggestion
            added_suggestions += 1

            if(HARD_DEBUG):
                print("Liczba zmienionych slow:", added_suggestions)

            tokens = deepcopy(tokens_backup)
            sentence = deepcopy(sentence_backup)
        #Wykrywamy slowa ktore skladaja sie z paru tokenow i aktualizujemy modyfikator indeksu tak by wszystko sie zgadzalo
        if(i+tokens_i_mod < len(tokens)):
            while (tokens[i+tokens_i_mod].find("</w>") == -1 and i+tokens_i_mod < len(tokens)):
                if(HARD_DEBUG):
                    print("")
                    print("Wykryto slowo skladajace sie z wielu tokenow:",tokens[i+tokens_i_mod])
                    print("index:",i)
                    print("tokens_i_mod",tokens_i_mod)
                    print("tokens_index",tokens_i_mod+i)
                tokens_i_mod +=1
                if(HARD_DEBUG):
                    print("Dostosowuje modyfikator",tokens_i_mod)
                    print("")

    sorted_new_words = sorted(suggested_words.items(), key=lambda x: x[0], reverse=True)

    for index, word in sorted_new_words:
        word = "("+word+"?)"
        sentence.insert(index+1, word)

    print(" ".join(sentence))
    return " ".join(sentence)