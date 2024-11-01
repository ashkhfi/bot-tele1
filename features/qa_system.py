import torch
from transformers import BertForQuestionAnswering, BertTokenizer
from utils import is_coordinate
model = BertForQuestionAnswering.from_pretrained('Ashkh0099/my-bert-new-version-5.0')
tokenizer = BertTokenizer.from_pretrained('Ashkh0099/my-bert-new-version-5.0')

def answer_question(question, context):
    """Answer the question based on the site context."""
    threshold = 0.5
    inputs = tokenizer(question, context, return_tensors="pt", truncation=True)

    # Dapatkan output logit dari model
    with torch.no_grad():
        outputs = model(**inputs)

    # Mendapatkan start_logits dan end_logits
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    # Mendapatkan probabilitas dari start dan end logits
    start_probs = torch.softmax(start_logits, dim=-1)
    end_probs = torch.softmax(end_logits, dim=-1)

    # Ambil posisi start dan end dengan probabilitas tertinggi
    start_idx = torch.argmax(start_probs, dim=-1).item()
    end_idx = torch.argmax(end_probs, dim=-1).item()

    # Ambil confidence score tertinggi
    start_confidence = start_probs[0][start_idx].item()
    end_confidence = end_probs[0][end_idx].item()
    print(f"Start confidence: {start_confidence}")
    print(f"End confidence: {end_confidence}")

    # Jika confidence score di bawah threshold, kembalikan jawaban default
    if start_confidence < threshold or end_confidence < threshold:
        return "I don't know"
    answer_ids = inputs['input_ids'][0][start_idx:end_idx+1]
    answer = tokenizer.decode(answer_ids, skip_special_tokens=True)
    answer = answer.upper()

    if is_coordinate(answer):
        answer = ''.join(answer.split())
        answer = f"https://www.google.com/maps?q={answer}"
        return answer

    return answer.replace("temp _ ", "").strip()
