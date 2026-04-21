from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

model = SentenceTransformer('all-MiniLM-L6-v2')
engine = create_engine("postgresql://admin:mysecretpassword@localhost:5432/personal_vault")

with engine.connect() as conn:
    # 1. 找出所有没有向量的笔记
    result = conn.execute(text("SELECT id, content FROM my_notes WHERE embedding IS NULL"))
    rows = result.fetchall()
    
    print(f"🛠 发现 {len(rows)} 条旧笔记需要 AI 处理...")
    
    for row in rows:
        # 2. 为旧内容生成向量
        vector = model.encode(row.content).tolist()
        # 3. 更新回数据库
        conn.execute(
            text("UPDATE my_notes SET embedding = :v WHERE id = :id"),
            {"v": str(vector), "id": row.id}
        )
        print(f"✅ 已完成 ID 为 {row.id} 的笔记向量化")
    
    conn.commit()
print("🎉 所有数据已升级为最前沿的向量格式！")