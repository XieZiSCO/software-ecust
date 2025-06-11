# config.py
DEEPSEEK_API_KEY = "sk-83027fc164114fa6bfaa98254f887aec"

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:280204353jyc@localhost/software?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False

TEST_MODE = False  # 改成 False 即可切换为真实模式 改成 Ture 会输出预设内容而不调用大模型
