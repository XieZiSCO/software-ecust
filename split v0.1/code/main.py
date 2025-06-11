from main_window import MainWindow
import tkinter as tk
from db_connection import init_database

def main():
    # 初始化数据库
    init_database()
    
    # 创建主窗口
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()