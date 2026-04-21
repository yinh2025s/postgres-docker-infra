from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

# 1. 加载本地 AI 模型（确保你之前 pip install 了 sentence-transformers）
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. 连接你的本地数据库
engine = create_engine("postgresql://admin:mysecretpassword@localhost:5432/personal_vault")

# 3. 输入你想搜索的内容（哪怕笔记里没这些词也能搜到）
user_query = "我想找找关于电脑硬件或者高性能设备的内容" 

# 4. 把搜索词也转化成向量
query_vector = model.encode(user_query).tolist()

# 5. 使用 pgvector 的特殊操作符 <=> (计算余弦距离) 进行搜索
# 这里的含义是：按向量相似度排序，取最接近的前 3 条
search_query = text("""
    SELECT title, content, 1 - (embedding <=> :v) AS similarity
    FROM my_notes
    ORDER BY embedding <=> :v
    LIMIT 3;
""")

with engine.connect() as conn:
    result = conn.execute(search_query, {"v": str(query_vector)})
    print(f"\n🔍 搜索词: '{user_query}'")
    print("-" * 40)
    for row in result:
        print(f"匹配度: {row.similarity:.4f} | 标题: {row.title}")
        print(f"内容: {row.content}\n")