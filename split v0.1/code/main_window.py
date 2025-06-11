import tkinter as tk
from tkinter import ttk, messagebox
from book_dao import BookDAO

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("图书管理系统")
        self.root.geometry("800x600")
        
        self.dao = BookDAO()
        
        self.create_widgets()
        self.load_books()
    
    def create_widgets(self):
        # 顶部搜索框
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10, fill=tk.X)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, text="搜索", command=self.search_books)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        add_btn = tk.Button(search_frame, text="添加图书", command=self.show_add_dialog)
        add_btn.pack(side=tk.RIGHT, padx=5)
        
        # 图书表格
        self.tree = ttk.Treeview(self.root, columns=('id', 'title', 'author', 'isbn', 'publish_date', 'quantity'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='书名')
        self.tree.heading('author', text='作者')
        self.tree.heading('isbn', text='ISBN')
        self.tree.heading('publish_date', text='出版日期')
        self.tree.heading('quantity', text='数量')
        
        self.tree.column('id', width=50)
        self.tree.column('title', width=150)
        self.tree.column('author', width=100)
        self.tree.column('isbn', width=120)
        self.tree.column('publish_date', width=100)
        self.tree.column('quantity', width=50)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 底部操作按钮
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        edit_btn = tk.Button(btn_frame, text="编辑", command=self.show_edit_dialog)
        edit_btn.pack(side=tk.LEFT, padx=10)
        
        delete_btn = tk.Button(btn_frame, text="删除", command=self.delete_book)
        delete_btn.pack(side=tk.LEFT, padx=10)
        
        refresh_btn = tk.Button(btn_frame, text="刷新", command=self.load_books)
        refresh_btn.pack(side=tk.LEFT, padx=10)
    
    def load_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        books = self.dao.get_all_books()
        for _, row in books.iterrows():
            self.tree.insert('', tk.END, values=(
                row['id'],
                row['title'],
                row['author'],
                row['isbn'],
                row['publish_date'],
                row['quantity']
            ))
    
    def search_books(self):
        keyword = self.search_var.get()
        if not keyword:
            self.load_books()
            return
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        books = self.dao.search_books(keyword)
        for _, row in books.iterrows():
            self.tree.insert('', tk.END, values=(
                row['id'],
                row['title'],
                row['author'],
                row['isbn'],
                row['publish_date'],
                row['quantity']
            ))
    
    def show_add_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("添加图书")
        
        # 创建表单控件...
        # 保存按钮调用 self.dao.add_book()
    
    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择一本书")
            return
            
        book_id = self.tree.item(selected[0])['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑图书")
        
        # 创建表单控件并填充选中图书的数据...
        # 保存按钮调用 self.dao.update_book()
    
    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择一本书")
            return
            
        book_id = self.tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("确认", "确定要删除这本书吗？"):
            self.dao.delete_book(book_id)
            self.load_books()
            messagebox.showinfo("成功", "图书已删除")