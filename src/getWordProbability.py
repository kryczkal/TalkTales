# pip install torch
# pip install transformers

import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM

# Wczytaj pre-trenowany polski model BERT i tokenizer    
model = AutoModelForMaskedLM.from_pretrained("allegro/herbert-base-cased")
tokenizer = AutoTokenizer.from_pretrained("allegro/herbert-base-cased")
tokeny = ""

def prawdopodobienstwa_slow_zdaniu(tokeny):
    # Oblicz prawdopodobieństwo występowania każdego słowa w zdaniu
    prawdopodobienstwa = {}
    for index, token in enumerate(tokeny):
        # Tworzenie maskowanego zdania
        maskowane_zdanie = tokeny.copy()
        maskowane_zdanie[index] = tokenizer.mask_token
        maskowane_zdanie.insert(0, tokenizer.cls_token)
        maskowane_zdanie.append(tokenizer.sep_token)

        # Konwersja maskowanego zdania na tensor
        wejscie = tokenizer.convert_tokens_to_ids(maskowane_zdanie)
        wejscie_tensor = torch.tensor([wejscie])

        # Predykcja prawdopodobieństw dla maskowanego słowa
        with torch.no_grad():
            output = model(wejscie_tensor)
        predykcje = output.logits[0, index + 1].softmax(dim=-1)

        # Oblicz prawdopodobieństwo oryginalnego słowa
        prawdopodobienstwo = predykcje[tokenizer.convert_tokens_to_ids([token])[0]].item()
        prawdopodobienstwa[token] = prawdopodobienstwo

    return prawdopodobienstwa

def sugestie_slow(tokeny, prog_prawdopodobienstwa=0.1, top_n=3):
    prawdopodobienstwa = prawdopodobienstwa_slow_zdaniu(tokeny)
    sugestie = {}

    for index, token in enumerate(tokeny):
        if prawdopodobienstwa[token] < prog_prawdopodobienstwa:
            maskowane_zdanie = tokeny.copy()
            maskowane_zdanie[index] = tokenizer.mask_token
            maskowane_zdanie.insert(0, tokenizer.cls_token)
            maskowane_zdanie.append(tokenizer.sep_token)

            wejscie = tokenizer.convert_tokens_to_ids(maskowane_zdanie)
            wejscie_tensor = torch.tensor([wejscie])

            with torch.no_grad():
                output = model(wejscie_tensor)
            predykcje = output.logits[0, index + 1].softmax(dim=-1)

            # Wyznacz `top_n` najbardziej prawdopodobnych słów
            top_n_predykcje = torch.topk(predykcje, top_n)
            top_n_tokeny = tokenizer.convert_ids_to_tokens(top_n_predykcje.indices)
            top_n_prawdopodobienstwa = top_n_predykcje.values.tolist()

            sugestie[token] = list(zip(top_n_tokeny, top_n_prawdopodobienstwa))

    return sugestie

def zdanie_z_sugestiami(zdanie, prog_prawdopodobienstwa=0.1):
    tokeny = tokenizer.tokenize(zdanie)
    sugestie = sugestie_slow(tokeny, prog_prawdopodobienstwa=prog_prawdopodobienstwa)
    
    print(tokeny)
    nowe_zdanie = []
    for token in tokeny:
        nowe_zdanie.append(token)
        if token in sugestie:
            najlepsza_sugestia, _ = sugestie[token][0]
            nowe_zdanie.append(f"({najlepsza_sugestia})")

    # Przekształć tokeny z powrotem na tekst
    nowe_zdanie_tekst = tokenizer.convert_tokens_to_string(nowe_zdanie)
    return nowe_zdanie_tekst

# Przykładowe zdanie
zdanie = "Moja mama kocha gotować i robić pranie."

# Stwórz zdanie z sugestiami
nowe_zdanie = zdanie_z_sugestiami(zdanie)

# Wyświetl nowe zdanie
print(nowe_zdanie)