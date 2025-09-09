import mysql.connector
import json
import ollama
import regex as re
import os
# from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables
# load_dotenv()

# Konfigurasi Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")

llm_agent = ollama.Client(host=OLLAMA_HOST)
embedder = SentenceTransformer('BAAI/bge-m3')

# Konfigurasi Database
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 4000)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    ssl_ca=os.getenv("DB_SSL_CA"),
    ssl_verify_cert=True,
    ssl_verify_identity=True
)


def search_document(database, query, k_top=1):
    database.ping(reconnect=True)
    results = []

    query_embedding_list = embedder.encode(query).tolist()
    query_embedding_str = json.dumps(query_embedding_list)

    curr = database.cursor()

    sql_query = f"""
        SELECT question, answer, vec_cosine_distance(embedding, %s) AS distance
        FROM documents
        ORDER BY distance ASC
        LIMIT {k_top}
    """
    curr.execute(sql_query, (query_embedding_str,))
    search_results = curr.fetchall()
    database.commit()
    curr.close()

    for result in search_results:
        question, answer, distance = result
        results.append({
            "question": question,
            "answer": answer,
            "distance": distance
        })

    return results


def response_query(database, query):
    retrieved_doc = search_document(database, query, k_top=1)

    if not retrieved_doc:
        return "Maaf, saya tidak tahu."

    answer = retrieved_doc[0]['answer']

    # Prompt ketat
    prompt = f"""
    Kamu adalah asisten QA berbahasa Indonesia.
    Aturan sangat ketat:
    1. Jawablah HANYA berdasarkan "Context Answer" di bawah ini.
    2. Jangan menambahkan informasi lain di luar context.
    3. Jangan berimprovisasi, jangan berasumsi.
    4. Jawab singkat (maksimal 1–2 kalimat).
    5. Jika pertanyaan tidak sesuai atau context tidak ada jawabannya, balas persis:
       "Maaf, saya tidak tahu."
    6. Selalu gunakan bahasa Indonesia.

    Pertanyaan: {query}
    Context Answer: {answer}

    Jawaban:
    """

    response = llm_agent.chat(
        model=OLLAMA_MODEL,
        messages=[{'role': 'user', 'content': prompt}]
    )

    raw_response = response['message']['content']
    final_response = clean_response(raw_response)
    return final_response


def clean_response(text):
    # hapus blok <think>...</think>
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # hapus awalan "Jawaban:" kalau masih muncul
    cleaned = re.sub(r"^Jawaban:\s*", "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip()


if __name__ == "__main__":
    print("Chat Bot is running...")
    while True:
        query_text = input("Prompt: ")

        if query_text.lower() in ['exit', 'quit', 'q']:
            print("Exiting Chat Bot...")
            break

        response = response_query(database=db, query=query_text)
        print("Chatbot: ", response)

    print("Chat Bot is closing...")