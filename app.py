from flask import Flask, render_template, request, redirect, url_for, session, send_file
import requests
import json
from config import DEEPSEEK_API_KEY, TEST_MODE
from flask_sqlalchemy import SQLAlchemy
from module import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于 session 加密
app.config.from_pyfile('config.py')
db.init_app(app)

def call_deepseek_api(prompt):
    if TEST_MODE:
        return f"[测试模式] 您的请求是：{prompt}\n返回伪造内容用于前端调试。"
    
    print("正在调用 DeepSeek API...")
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个软件开发专家，请根据提示生成内容"},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        print("DeepSeek 返回成功")
        return result['choices'][0]['message']['content']
    except Exception as e:
        print("DeepSeek 调用失败:", e)
        return "生成失败，请稍后再试。"


@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/generate', methods=['POST'])
def generate():
    system_type = request.form['system_type']
    content_type = request.form['content_type']

    prompt_map = {
        "architecture": f"请为{system_type}生成系统架构设计。",
        "database": f"请为{system_type}生成数据库设计，包括表结构。",
        "code": f"请为{system_type}生成系统代码，使用python编写，后端与mysql连接，页面使用tkinter库制作，mysql连接信息为mysql+pymysql://root:280204353jyc@localhost/software?charset=utf8mb4，请按照:"\
                    "## 1. 模块名称（py文件名称.py）" \
                    "```python" \
                    "此文件代码内容" \
                    "```" \
                    "的格式输出,注意格式内使用的括号是（）",
        "test": f"请为{system_type}生成测试用例。",
    }

    #测试用
    # prompt = prompt_map.get(content_type, "请生成相关内容,只需要输出前100个字符" )
    # result = call_deepseek_api(prompt)

    prompt = prompt_map.get(content_type, "请生成相关内容，尽量精简，输出字符不要超过大模型的单次最大输出字符数，以便部署")
    result = call_deepseek_api(prompt)

    return result


@app.route('/export', methods=['POST'])
def export():
    export_content = request.form['export_content']
    filename = request.form.get('filename', 'exported.txt')

    os.makedirs('./exports', exist_ok=True)  # 确保目录存在
    path = f"./exports/{filename}"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(export_content)

    return send_file(path, as_attachment=True)



# 初始化数据库（首次运行）
#with app.app_context():
    if not os.path.exists('users.db'):
        db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "用户已存在"
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "登录失败，用户名或密码错误"
        
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
