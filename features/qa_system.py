import torch
from transformers import BertForQuestionAnswering, BertTokenizer
from utils import is_coordinate, is_billing
model = BertForQuestionAnswering.from_pretrained('Ashkh0099/my-bert-new-version-6.0')
tokenizer = BertTokenizer.from_pretrained('Ashkh0099/my-bert-new-version-6.0')

def answer_question(question, context):
    """Answer the question based on the site context."""
    threshold = 0.5
    question = question.lower() + "?"
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

    # Ambil jawaban berdasarkan start dan end indeks
    answer_ids = inputs['input_ids'][0][start_idx:end_idx+1]
    answer = tokenizer.decode(answer_ids, skip_special_tokens=True)

    # Menampilkan pertanyaan dan jawaban
    print(f"Question: {question}")
    print(f"Answer: {answer}")

    if len(answer) > 200:
        answer = "I don't know"

    # Format jawaban ke dalam bentuk "cur _ <angka>"
    if "cur" in answer:
        print("cur terdeteksi")
        # Menghapus "cur _ " dari teks dan mengonversi sisa teks ke format rupiah
        answer = answer.replace("cur _ ", "").strip()
        try:
            number = int(answer)  # Mengonversi teks ke angka
            answer = f"Rp {number:,.0f}".replace(",", ".")  # Format ke rupiah
        except ValueError:
            print("Error: Teks setelah 'cur _' bukan angka valid.")
            answer = "Invalid format"

    if answer == "tlp":
        answer = "please look into sitename!!!"

    # Menampilkan hasil akhir
    answer = answer.upper()
    return answer.replace("temp _ ", "").strip()

