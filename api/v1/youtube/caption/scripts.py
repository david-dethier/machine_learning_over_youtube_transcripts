import requests
from transformers import pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import BartTokenizer, BartForConditionalGeneration
import timeit


def get_the_dialog():
    dialog_text = ""
    starting = timeit.default_timer()
    
    response = requests.get("http://127.0.0.1:8000/caption/", params={"videoId": "ObyO8dX647M"})
    # ObyO8dX647M
    # M7FIvfx5J10
    if response.status_code == 200:
        dialog_text = " ".join([key["text"] for key in response.json()])
        print(dialog_text)
    ending = timeit.default_timer() - starting
    print(ending)
    return dialog_text





def summarize_through_bart_pipeline(dialog_text):
    starting = timeit.default_timer()
    summarization = pipeline(task="summarization", model="facebook/bart-large-cnn", truncation=True)
    summary = summarization(dialog_text)[0]['summary_text']
    ending = timeit.default_timer() - starting
    return {"timing": ending, "summary": summary}


def summarize_through_t5(dialog_text):
    starting = timeit.default_timer()
    
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")
    inputs_ids = tokenizer.encode("summarize: " + dialog_text, return_tensors="pt", truncation=True)
    outputs = model.generate(inputs_ids, max_length=512, min_length=40, length_penalty=2.0, num_beams=4,
                             early_stopping=True)
    summary = tokenizer.decode(outputs[0])
    ending = timeit.default_timer() - starting
    return {"timing": ending, "summary": summary}


def summarize_through_bart(dialog_text):
    starting = timeit.default_timer()
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    inputs = tokenizer(dialog_text, return_tensors="pt", truncation=True)
    inputs_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=512)
    summary = tokenizer.batch_decode(inputs_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    ending = timeit.default_timer() - starting
    return {"timing": ending, "summary": summary}


if __name__ == "__main__":
    dialog = get_the_dialog()
    # print(summarize_through_bart_pipeline(dialog))
    # print(summarize_through_t5(dialog))
    print(summarize_through_bart(dialog))
    # print(summarize_through_distillbart(dialog))
