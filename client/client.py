import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

class BookCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Catalog")
        
        self.create_widgets()
        self.load_books()

    def create_widgets(self):
        self.book_listbox = tk.Listbox(self.root, width=50, height=20)
        self.book_listbox.pack(pady=20)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.add_button = tk.Button(button_frame, text="Add Book", command=self.add_book)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = tk.Button(button_frame, text="Edit Book", command=self.edit_book)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = tk.Button(button_frame, text="Delete Book", command=self.delete_book)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_books)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

    def load_books(self):
        try:
            response = requests.get("http://127.0.0.1:5000/api/books")
            response.raise_for_status()
            books = response.json()
            self.book_listbox.delete(0, tk.END)
            for book in books:
                self.book_listbox.insert(tk.END, f"{book['title']} by {book['author']}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def add_book(self):
        title = simpledialog.askstring("Input", "Enter book title:")
        author = simpledialog.askstring("Input", "Enter book author:")
        genre = simpledialog.askstring("Input", "Enter book genre:")
        year = simpledialog.askinteger("Input", "Enter book year:")
        description = simpledialog.askstring("Input", "Enter book description:")
        copies = simpledialog.askinteger("Input", "Enter number of copies:")

        if title and author and genre and year and copies is not None:
            book_data = {
                "title": title,
                "author": author,
                "genre": genre,
                "year": year,
                "description": description,
                "copies": copies
            }
            try:
                response = requests.post("http://127.0.0.1:5000/api/books", json=book_data)
                response.raise_for_status()
                self.load_books()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to add book: {e}")

    def edit_book(self):
        selected_index = self.book_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No book selected")
            return

        selected_book = self.book_listbox.get(selected_index)
        book_id = self.get_book_id_by_title(selected_book.split(' by ')[0])

        title = simpledialog.askstring("Input", "Enter new book title:", initialvalue=selected_book.split(' by ')[0])
        author = simpledialog.askstring("Input", "Enter new book author:", initialvalue=selected_book.split(' by ')[1])
        genre = simpledialog.askstring("Input", "Enter new book genre:")
        year = simpledialog.askinteger("Input", "Enter new book year:")
        description = simpledialog.askstring("Input", "Enter new book description:")
        copies = simpledialog.askinteger("Input", "Enter new number of copies:")

        if title and author and genre and year and copies is not None:
            book_data = {
                "title": title,
                "author": author,
                "genre": genre,
                "year": year,
                "description": description,
                "copies": copies
            }
            try:
                response = requests.put(f"http://127.0.0.1:5000/api/books/{book_id}", json=book_data)
                response.raise_for_status()
                self.load_books()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to edit book: {e}")

    def delete_book(self):
        selected_index = self.book_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No book selected")
            return

        selected_book = self.book_listbox.get(selected_index)
        book_id = self.get_book_id_by_title(selected_book.split(' by ')[0])

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            try:
                response = requests.delete(f"http://127.0.0.1:5000/api/books/{book_id}")
                response.raise_for_status()
                self.load_books()
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to delete book: {e}")

    def get_book_id_by_title(self, title):
        try:
            response = requests.get("http://127.0.0.1:5000/api/books")
            response.raise_for_status()
            books = response.json()
            for book in books:
                if book['title'] == title:
                    return book['id']
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to get book ID: {e}")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = BookCatalogApp(root)
    root.mainloop()
