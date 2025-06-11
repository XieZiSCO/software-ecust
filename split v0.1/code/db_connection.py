import pymysql
from sqlalchemy import create_engine

def get_db_connection():
    # 创建数据库连接
    engine = create_engine(
        "mysql+pymysql://root:280204353jyc@localhost/software?charset=utf8mb4"
    )
    return engine

def get_raw_connection():
    # 获取原始连接用于执行SQL
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='280204353jyc',
        database='software',
        charset='utf8mb4'
    )
    return connection

def init_database():
    # 初始化数据库表
    conn = get_raw_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    author VARCHAR(50) NOT NULL,
                    isbn VARCHAR(20) UNIQUE,
                    publish_date DATE,
                    quantity INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    finally:
        conn.close()