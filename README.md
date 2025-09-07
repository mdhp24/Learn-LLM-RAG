# 🧠 Learn LLM + RAG

Eksperimen sederhana untuk memahami cara kerja **Large Language Model (LLM)** dengan pendekatan **Retrieval Augmented Generation (RAG)**.  
Project ini dibuat untuk belajar bagaimana menghubungkan database (dalam hal ini menggunakan **TiDB Cloud**) dengan LLM agar bisa menjawab pertanyaan berdasarkan data yang sudah ada.  

---

## ✨ Fitur
- 🔎 **Pencarian berbasis embedding**: pertanyaan user diubah menjadi vektor lalu dicocokkan dengan database.  
- 📚 **Context-aware response**: jawaban selalu berdasarkan data yang tersedia (minim halusinasi).  
- 🌐 **Integrasi dengan Ollama**: memanfaatkan model LLM lokal seperti `deepseek-r1`.  
- 🗄️ **Database RAG**: menggunakan **TiDB Cloud** untuk menyimpan knowledge base (QnA).  
- ⚡ **CLI Chatbot**: jalankan langsung via terminal.  

---
