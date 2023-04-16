import os
from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast

model_dir = "bart_base_transformers"
tok = PreTrainedTokenizerFast(tokenizer_file=os.path.join(model_dir, "tokenizer.json"))
model = BartForConditionalGeneration.from_pretrained(model_dir)
sent = "Druga<mask>światowa zakończyła się w<mask>roku kapitulacją hitlerowskich<mask>"
batch = tok(sent, return_tensors='pt')
generated_ids = model.generate(batch['input_ids'])
print(tok.batch_decode(generated_ids, skip_special_tokens=True))
# ['Druga wojna światowa zakończyła się w 1945 roku kapitulacją hitlerowskich Niemiec.']