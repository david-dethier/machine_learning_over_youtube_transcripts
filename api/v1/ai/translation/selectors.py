from core.decorators import benchmark
from transformers import MBart50TokenizerFast, MBartForConditionalGeneration


@benchmark
def translate_mbart_large_50_many_to_many_mmt(input: str = "", from_lang: str = "en_XX", to_lang: str = "es_XX"):
    model = None
    tokenizer = None
    
    if not model:
        model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    
    if not tokenizer:
        tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    
    tokenizer.src_lang = from_lang
    
    source = input
    
    if not source:
        return None
    
    encoded_hi = tokenizer(source, return_tensors="pt")
    
    generated_tokens = model.generate(
            **encoded_hi,
            forced_bos_token_id=tokenizer.lang_code_to_id[to_lang]
    )
    
    traduction = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    
    return {"original": source, "translation": traduction}
