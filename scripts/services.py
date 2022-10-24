import requests
from bs4 import BeautifulSoup
from huggingface_hub import list_models
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, MT5ForConditionalGeneration, MT5Tokenizer, T5Model, \
    T5Tokenizer, MBartForConditionalGeneration, MBart50TokenizerFast
from core.decorators import benchmark


def translateT5():
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    model = T5Model.from_pretrained("t5-base")
    
    input_ids = tokenizer(
            "Studies have been shown that owning a dog is good for you", return_tensors="pt"
    ).input_ids  # Batch size 1
    decoder_input_ids = tokenizer("Studies show that", return_tensors="pt").input_ids  # Batch size 1
    
    # forward pass
    outputs = model(input_ids=input_ids, decoder_input_ids=decoder_input_ids)
    last_hidden_states = outputs.last_hidden_state
    return last_hidden_states


def translate(to_lang, from_lang='en', **kwargs):
    tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small")
    
    model = MT5ForConditionalGeneration.from_pretrained("google/mt5-small")
    input_text = "Translate: It is time to recognize"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")  # Batch size 1
    outputs = model.generate(input_ids)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    # inputs = tokenizer.encode(
    # ,
    #          return_tensors = "pt", truncation = False)
    #
    # inputs_ids = model.generate(inputs)
    #
    # summary = tokenizer.batch_decode(inputs_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[
    #     0]
    #
    print(decoded)
    return decoded


INPUT_TEXT = "El grupo paramilitar se desplegó en Crimea y en la región ucraniana de Donbass en 2014, cuando las fuerzas respaldadas por el Kremlin expulsaron a las tropas ucranianas de las zonas que posteriormente declararon parte de Rusia. Hoy también opera en Siria, Libia, República Centroafricana y ahora en Malí."


@benchmark
def translate_mbart_large_50_many_to_many_mmt():
    model = None
    tokenizer = None
    
    if not model:
        model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    
    if not tokenizer:
        tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    
    tokenizer.src_lang = "es_XX"
    
    source = ""
    
    while source != "exit()":
        
        source = input("Texto para traducir al ingles: \n")
        
        if source == "exit()":
            break
        
        encoded_hi = tokenizer(source, return_tensors="pt")
        
        generated_tokens = model.generate(
                **encoded_hi,
                forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"]
        )
        
        traduction = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        
        print(f'TRADUCCION:')
        print("-" * 150)
        print(f'Source: \n')
        print(source)
        print("#" * 150)
        print(f'Target: \n')
        print(traduction)
        print(".." * 150)
    
    print(f'Proceso terminado con exito.')


def listar_modelos():
    model_list = list_models()
    org = "facebook"
    
    model_ids = [x.modelId for x in model_list if (x.modelId.startswith(org) and "bart" in x.modelId)]
    suffix = [x.split("/")[1] for x in model_ids]
    old_style_multi_models = [f"{org}/{s}" for s in suffix if s != s.lower()]
    
    print(f'model_ids == {model_ids}')
    print(f'suffix == {suffix}')


def get_bleu():
    req = requests.get(
            url="https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/results/tatoeba-models-all.md",
    )
    
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")
        tabla = soup.table
        rows = tabla.find_all("tr")
        lista = []
        for row in rows:
            tds = row.find_all("td")
            if tds:
                lista.append({"Model": tds[0], "chrF2": tds[1], "BLEU": tds[2]})
        
        # print(lista)
        for lst in lista:
            
            if eval(lst["BLEU"].text) > 60:
                print(lst["Model"].text, " = ", lst["BLEU"].text)


if __name__ == "__main__":
    # print(translateT5())
    # listar_modelos()
    translate_mbart_large_50_many_to_many_mmt()
    # get_bleu()
    # translatehelzinsky()


def run():
    translate_mbart_large_50_many_to_many_mmt()
