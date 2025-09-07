import json
import pandas as pd
import mysql.connector

from sentence_transformers import SentenceTransformer

# Membuat instance embedder

embedder = SentenceTransformer('BAAI/bge-m3')

db = mysql.connector.connect(
  host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "2jLp6wqw9uFSTUz.root",
  password = "xJGUkaswN3PTx1tx",
  database = "RAG",
  ssl_ca = "C:\\Users\\Moch. Dicky Hanun P\\certs\\isrgrootx1.pem",
  ssl_verify_cert = True,
  ssl_verify_identity = True
)

curr = db.cursor()

#baca data csv
df = pd.read_csv("data_knowledge.csv")
print(df)

for index, row in df.iterrows():
    question = str(row['question'])
    answer = str(row['answer'])

    try:
          embedding_list = embedder.encode(question).tolist()
        # print(embedding_list)
          embedding_str = json.dumps(embedding_list)
          
          sql_query = """
          INSERT INTO documents (question,answer,embedding) VALUES (%s, %s, %s)
                      """
          
          curr.execute(sql_query, (question, answer, embedding_str))
          print(f"data index-{index}  berhasil ditambahkan")
    except Exception as e:
          print(f"Error:", {e})
          print(f"data index-{index}  gagal ditambahkan")
          
db.commit()
curr.close()
print("Semua data berhasil ditambahkan")