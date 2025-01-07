import tkinter as tk
from tkinter import ttk, messagebox
import requests

class BookCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Catalog")
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for adding a new book
        self.title_label = ttk.Label(self.root, text="Title")
        self.title_label.grid(row=0, column=0)
        self.title_entry = ttk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        self.author_label = ttk.Label(self.root, text="Author")
        self.author_label.grid(row=1, column=0)
        self.author_entry = ttk.Entry(self.root)
        self.author_entry.grid(row=1, column=1)

        self.genre_label = ttk.Label(self.root, text="Genre")
        self.genre_label.grid(row=2, column=0)
        self.genre_entry = ttk.Entry(self.root)
        self.genre_entry.grid(row=2, column=1)

        self.year_label = ttk.Label(self.root, text="Year")
        self.year_label.grid(row=3, column=0)
        self.year_entry = ttk.Entry(self.root)
        self.year_entry.grid(row=3, column=1)

        self.description_label = ttk.Label(self.root, text="Description")
        self.description_label.grid(row=4, column=0)
        self.description_entry = ttk.Entry(self.root)
        self.description_entry.grid(row=4, column=1)

        self.copies_label = ttk.Label(self.root, text="Copies")
        self.copies_label.grid(row=5, column=0)
        self.copies_entry = ttk.Entry(self.root)
        self.copies_entry.grid(row=5, column=1)

        self.add_button = ttk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_button.grid(row=6, column=1)

        # Create widgets for displaying and searching books
        self.search_label = ttk.Label(self.root, text="Search")
        self.search_label.grid(row=7, column=0)
        self.search_entry = ttk.Entry(self.root)
        self.search_entry.grid(row=7, column=1)

        self.search_button = ttk.Button(self.root, text="Search", command=self.search_books)
        self.search_button.grid(row=7, column=2)

        self.books_list = tk.Listbox(self.root)
        self.books_list.grid(row=8, column=0, columnspan=3)

        self.get_books()

    def get_books(self):
        response = requests.get("http://127.0.0.1:5000/api/books")
        if response.status_code == 200:
            books = response.json()
            self.books_list.delete(0, tk.END)
            for book in books:
                self.books_list.insert(tk.END, f"{book['title']} by {book['author']}")

    def add_book(self):
        book_data = {
            "title": self.title_entry.get(),
            "author": self.author_entry.get(),
            "genre": self.genre_entry.get(),
            "year": self.year_entry.get(),
            "description": self.description_entry.get(),
            "copies": self.copies_entry.get()
        }
        response = requests.post("http://127.0.0.1:5000/api/books", json=book_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Book added successfully!")
            self.get_books()
        else:
            messagebox.showerror("Error", "Failed to add book")

    def search_books(self):
        search_query = self.search_entry.get()
        response = requests.get(f"http://127.0.0.1:5000/api/books?search={search_query}")
        if response.status_code == 200:
            books = response.json()
            self.books_list.delete(0, tk.END)
            for book in books:
                self.books_list.insert(tk.END, f"{book['title']} by {book['author']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookCatalogApp(root)
    root.mainloop()