from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

# 1. 加载本地 AI 模型 (第一次运行会自动下载，约 80MB)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. 连接数据库
engine = create_engine("postgresql://admin:mysecretpassword@localhost:5432/personal_vault")

# 3. 准备一条有深度的内容
title = "CS 2114 学习心得"
content = "数据结构是算法的基础，理解内存分配对性能优化至关重要。"

# 4. 生成向量
vector = model.encode(content).tolist()

# 5. 存入数据库
with engine.connect() as conn:
    query = text("INSERT INTO my_notes (title, content, embedding) VALUES (:t, :c, :v)")
    conn.execute(query, {"t": title, "c": content, "v": str(vector)})
    conn.commit()
    print("🚀 AI 笔记已存入，包含 384 维向量特征！")