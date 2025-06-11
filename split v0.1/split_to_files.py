import os
import re

# 创建存放目录
code_dir = os.path.join("C:/Users/ASUS/Desktop/分割/", "code")
os.makedirs(code_dir, exist_ok=True)

source_file = "source.txt"

with open(source_file, "r", encoding="utf-8") as f:
    text = f.read()

# 正则改用中文括号匹配
pattern = r'##\s*\d+\.\s+.+?（([\w\.]+)）\s*```python\n(.*?)```'

# 这里要确保匹配多行内容
matches = re.findall(pattern, text, re.DOTALL)

if not matches:
    print("⚠️ 未匹配到任何模块，请检查 source.txt 的格式。")
else:
    print(f"匹配到 {len(matches)} 个模块，正在保存...")
    for filename, code in matches:
        file_path = os.path.join(code_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code.strip())
        print(f"✅ 已保存: {filename}")

print("✅ 所有模块已分割并保存完成。")