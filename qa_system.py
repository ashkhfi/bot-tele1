import torch
from transformers import BertForQuestionAnswering, BertTokenizer
from utils import is_coordinate
model = BertForQuestionAnswering.from_pretrained('Ashkh0099/my-bert-QA')
tokenizer = BertTokenizer.from_pretrained('Ashkh0099/my-bert-QA')

def answer_question(question, context):
    """Answer the question based on the site context."""
    if context == "Site name not found.":
        return context

    inputs = tokenizer(question, context, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    start_position = torch.argmax(start_logits)
    end_position = torch.argmax(end_logits)

    input_ids = inputs['input_ids'].tolist()[0]
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[start_position:end_position+1]))

    answer = answer.upper()

    if answer in ["[SEP]", ""]:
        return "DATA NOT FOUND."

    if is_coordinate(answer):
        answer = ''.join(answer.split())
        answer = f"https://www.google.com/maps?q={answer}"
        return answer

    return answer.replace("temp _ ", "").strip()
