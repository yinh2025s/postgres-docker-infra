import sqlalchemy
from sqlalchemy import text
from sqlalchemy import create_engine

# 连接数据库
DB_URL = "postgresql://admin:mysecretpassword@localhost:5432/personal_vault"
engine = create_engine(DB_URL)

with engine.connect() as conn:
    # 1. 在数据库中启用 pgvector 扩展
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    # 2. 给 notes 表增加一个名为 embedding 的列，维度设为 384（适合本地轻量级模型）
    conn.execute(text("ALTER TABLE my_notes ADD COLUMN IF NOT EXISTS embedding vector(384)"))
    conn.commit()
    print("✅ 向量字段已添加！")