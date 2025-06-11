from db_connection import get_db_connection
import pandas as pd

class BookDAO:
    def __init__(self):
        self.engine = get_db_connection()
    
    def add_book(self, title, author, isbn, publish_date=None, quantity=1):
        with self.engine.connect() as conn:
            conn.execute(
                "INSERT INTO books (title, author, isbn, publish_date, quantity) "
                "VALUES (%s, %s, %s, %s, %s)",
                (title, author, isbn, publish_date, quantity)
            )
    
    def get_all_books(self):
        return pd.read_sql("SELECT * FROM books", self.engine)
    
    def search_books(self, keyword):
        query = """
            SELECT * FROM books 
            WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s
        """
        return pd.read_sql(query, self.engine, params=(f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    
    def update_book(self, book_id, title=None, author=None, isbn=None, publish_date=None, quantity=None):
        updates = []
        params = []
        
        if title:
            updates.append("title = %s")
            params.append(title)
        if author:
            updates.append("author = %s")
            params.append(author)
        if isbn:
            updates.append("isbn = %s")
            params.append(isbn)
        if publish_date:
            updates.append("publish_date = %s")
            params.append(publish_date)
        if quantity is not None:
            updates.append("quantity = %s")
            params.append(quantity)
        
        if updates:
            params.append(book_id)
            with self.engine.connect() as conn:
                conn.execute(
                    f"UPDATE books SET {', '.join(updates)} WHERE id = %s",
                    params
                )
    
    def delete_book(self, book_id):
        with self.engine.connect() as conn:
            conn.execute("DELETE FROM books WHERE id = %s", (book_id,))