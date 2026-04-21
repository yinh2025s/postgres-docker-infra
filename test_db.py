from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# 连接地址 (Mac 本地访问 Docker 容器)
DB_URL = "postgresql://admin:mysecretpassword@localhost:5432/personal_vault"

engine = create_engine(DB_URL)
Base = declarative_base()

class Note(Base):
    __tablename__ = 'my_notes'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 存入一条数据
new_note = Note(title="Mac 搭建成功", content="在 M3 Max 上运行真快！")
session.add(new_note)
session.commit()

print("✅ 成功！数据已进入数据库。")
session.close()