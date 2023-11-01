import torch
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

# Settings
DYNAMIC_THRESHOLD = True
PERCENTILE_VALUE = 25
PROBABILITY_THRESHOLD = 0.1
MODEL_NAME = "allegro/herbert-large-cased"
TOKENIZER_NAME = "allegro/herbert-large-cased"
DEBUG = 0
HARD_DEBUG: int = 0

if DEBUG != 1:
    HARD_DEBUG = 0
# Checking for GPU and assigning device accordingly
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name()}")
else:
    device = torch.device("cpu")
    print("Using CPU")

# Loading pretrained model and tokenizer
MODEL = AutoModelForMaskedLM.from_pretrained(MODEL_NAME).to(device)
TOKENIZER = AutoTokenizer.from_pretrained(TOKENIZER_NAME)
# Initialize fill-mask pipeline
fill_mask = pipeline("fill-mask", model=MODEL_NAME, tokenizer=MODEL_NAME, device=device.index)


#

def get_word_probability(
        tokens: List[str]
) -> List[float]:
    """
        Get probabilities of each word's presence in a sentence using masked language models.

        Parameters:
        - tokens (List[str]): The input list of tokenized words that form the sentence.

        Returns:
        - List[float]: A list of probabilities corresponding to each word in the sentence.
        """

    if DEBUG:
        print("")

    # Calculate probability of each word being present in the sentence
    probabilities = {}
    for index, token in enumerate(tokens):
        # Create a version of the sentence with the current token masked out
        masked_sentence = tokens.copy()
        masked_sentence[index] = TOKENIZER.mask_token
        masked_sentence.insert(0, TOKENIZER.cls_token)
        masked_sentence.append(TOKENIZER.sep_token)

        # Convert the masked sentence into a tensor of token IDs
        output = TOKENIZER.convert_tokens_to_ids(masked_sentence)
        input_tensor = torch.tensor([output]).to(device)

        # Use the masked language model to predict the masked token
        with torch.no_grad():
            output = MODEL(input_tensor)
        predictions = output.logits[0, index + 1].softmax(dim=-1)

        # Calculate the probability of the original token being correct
        probability = predictions[TOKENIZER.convert_tokens_to_ids([token])[0]].item()
        probabilities[token] = probability

    # Initialize counters for aggregating probabilities and syllable counts
    total_probability = 0
    syllable_count = 0
    probabilities_of_words = []

    if HARD_DEBUG:
        print("Splitting sentence to tokens:", tokens)

    # Aggregate probabilities and syllable counts for each word
    for index, token in enumerate(tokens):
        syllable_count += 1
        total_probability += probabilities[token]
        if token.find("</w>") != -1:
            probabilities_of_words.append(total_probability / syllable_count)
            syllable_count = 0
            total_probability = 0
    return probabilities_of_words


#
def generate_suggestions(
        sentence: List[str],
        index: int,
        tokens_i_mod: int,
        tokens: List[str]
) -> str:
    if DEBUG:
        print("")

    mask_token = TOKENIZER.mask_token

    if HARD_DEBUG:
        print("index:", index)
        print("tokens_i_mod", tokens_i_mod)
        print("tokens_index", tokens_i_mod + index)
        print("")

    if HARD_DEBUG:
        print("Masking low probability worlds tokens")

    if HARD_DEBUG:
        print("Checking whether world is represented by multiple tokens")

    # Check whether the word at the given index is composed of multiple tokens
    if tokens[index + tokens_i_mod].find("</w>") == -1:
        if HARD_DEBUG:
            print("Tak")

        # copying starting world index
        new_index = deepcopy(index + tokens_i_mod)

        # Remove tokens until the end-of-word token "</w>" is found
        while tokens[new_index].find("</w>") == -1:
            if HARD_DEBUG:
                print(f"Word-building tokens: {tokens[new_index]}")

            tokens.pop(new_index)
            # new_index += 1

        # Replace the end-of-word token with a mask token
        if HARD_DEBUG:
            print(f"Last token: {tokens[new_index]}")

        tokens[new_index] = mask_token
    else:
        if HARD_DEBUG:
            print("Nie")
        # Directly replace the token at the calculated index with the mask token
        tokens[index + tokens_i_mod] = mask_token

    # Add a period if this is the last token in the sentence
    if index + tokens_i_mod == len(tokens) - 1:
        tokens.append(".")

    # Convert the token list back to a sentence string
    masked_sentence = TOKENIZER.convert_tokens_to_string(tokens)

    if HARD_DEBUG:
        print("Masked sentence:", masked_sentence)

    # Use a fill-mask function to predict the most probable word to replace the mask
    result = fill_mask(masked_sentence)

    # Replacing masked world with most probable ones
    tokens[index + tokens_i_mod] = result[0]["token_str"] + ' '
    new_sentence = TOKENIZER.convert_tokens_to_string(tokens)

    if HARD_DEBUG:
        print("New sentence:", new_sentence)

    new_sentence = new_sentence.split(' ')
    if HARD_DEBUG:
        print(f"Returning upgraded sentence index: {index}")

    if DEBUG:
        print(f"Not upgraded version: {sentence[index]}")
        print(f"Upgraded version: {new_sentence[index]}")

    if index + tokens_i_mod == len(tokens) - 1:
        tokens.pop()

    # Return the modified word at the index
    return new_sentence[index]


#
def upgrade_sentence(
        sentence: str
) -> str:

    # All transformation are done on the copy

    if DEBUG:
        print("\nLet's begin\n")

    if DEBUG:
        print("Removing dots and commas from the sentence")

    # Removing irrelevant characters from the sentence
    sentence = sentence.replace(',', '')
    sentence = sentence.replace('.', '')

    if DEBUG:
        print("Sentence after cleaning:", sentence)
    # Sentence tokenization
    tokens = TOKENIZER.tokenize(sentence)

    # Splitting sentence to world
    sentence = sentence.split(' ')

    if DEBUG:
        print("Splitting sentence to words:", sentence)
        print("Words count:", len(sentence))

    if HARD_DEBUG:
        print("Copying tokens and sentence")

    # Backup of tokens and sentence
    tokens_backup = deepcopy(tokens)
    sentence_backup = deepcopy(sentence)

    if DEBUG:
        print("Calculating probability of each world")

    probabilities = get_word_probability(tokens)

    # Calculate the probability threshold
    probability_threshold = np.percentile(probabilities, PERCENTILE_VALUE)

    if DEBUG:
        print("Results: ", probabilities)
        print("Probabilities acquired:", len(probabilities))

    # Adding suggestions to replace less probable words
    added_suggestions = 0

    suggested_words = {}

    if DEBUG:
        print("Generating suggestions for each less probable word")

    tokens_i_mod = 0
    # Loop through each word and replace if needed
    for i in range(len(probabilities)):

        if probabilities[i] < probability_threshold:

            if HARD_DEBUG:
                print("Sentence:", sentence)
                print("Tokens: ", tokens)

            if DEBUG:
                print("\bWord:", sentence[i])
                print("Less probable:", probabilities[i])

            suggestion = generate_suggestions(sentence, i, tokens_i_mod, tokens)

            if HARD_DEBUG:
                print("Changing word:", sentence[i])
                print("To:", suggestion)

            sentence[i] = suggestion

            if HARD_DEBUG:
                print("Changing sentence:", " ".join(sentence))

            added_suggestions += 1

            if HARD_DEBUG:
                print("Changed words count:", added_suggestions)

            tokens = deepcopy(tokens_backup)
            sentence = deepcopy(sentence_backup)

        # Detecting words, which are built with more than one token and updating index modifier to ensure correctness

        if i + tokens_i_mod < len(tokens):
            while tokens[i + tokens_i_mod].find("</w>") == -1 and i + tokens_i_mod < len(tokens):
                if HARD_DEBUG:
                    print("")
                    print("Detected world built with more than one token:", tokens[i + tokens_i_mod])
                    print("index:", i)
                    print("tokens_i_mod", tokens_i_mod)
                    print("tokens_index", tokens_i_mod + i)
                tokens_i_mod += 1

                if HARD_DEBUG:
                    print("Fitting in modifier:", tokens_i_mod)
                    print("")

    sorted_new_words = sorted(suggested_words.items(), key=lambda x: x[0], reverse=True)

    for index, word in sorted_new_words:
        word = "(" + word + "?)"
        sentence.insert(index + 1, word)

    print(" ".join(sentence))
    return " ".join(sentence)
