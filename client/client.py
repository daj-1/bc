import tkinter as tk
from tkinter import messagebox
import requests

class BookCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Catalog")
        
        self.create_widgets()
        self.load_books()

    def create_widgets(self):
        self.root.configure(bg="#f1f8ff")
        self.root.geometry("600x400")

        self.title_label = tk.Label(self.root, text="Book Catalog", font=("Helvetica", 24, "bold"), fg="#004b8d", bg="#f1f8ff")
        self.title_label.pack(pady=20)

        self.book_listbox = tk.Listbox(self.root, width=50, height=10, font=("Arial", 12), bg="#e6f0ff", fg="#333", 
                                       selectbackground="#0066cc", selectforeground="white", bd=0)
        self.book_listbox.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#f1f8ff")
        button_frame.pack(pady=10)

        self.add_button = self.create_button(button_frame, "Add Book", self.add_book)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.edit_button = self.create_button(button_frame, "Edit Book", self.edit_book)
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = self.create_button(button_frame, "Delete Book", self.delete_book)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.refresh_button = self.create_button(button_frame, "Refresh", self.load_books)
        self.refresh_button.pack(side=tk.LEFT, padx=10)

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command, font=("Helvetica", 12, "bold"), 
                           bg="#007bff", fg="white", relief="flat", width=12, height=2)
        button.config(activebackground="#0056b3", activeforeground="white")
        button.bind("<Enter>", lambda event: button.config(bg="#0056b3"))
        button.bind("<Leave>", lambda event: button.config(bg="#007bff"))
        return button

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
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Book")
        add_window.geometry("400x400")

        fields = ["Title", "Author", "Genre", "Year", "Description", "Copies"]
        entries = {}

        for i, field in enumerate(fields):
            label = tk.Label(add_window, text=field, font=("Helvetica", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

            entry = tk.Entry(add_window, font=("Helvetica", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry

        def save_book():
            try:
                book_data = {
                    "title": entries["Title"].get(),
                    "author": entries["Author"].get(),
                    "genre": entries["Genre"].get(),
                    "year": int(entries["Year"].get()),
                    "description": entries["Description"].get(),
                    "copies": int(entries["Copies"].get())
                }

                response = requests.post("http://127.0.0.1:5000/api/books", json=book_data)
                response.raise_for_status()
                self.load_books()
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check your entries.")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to add book: {e}")

        save_button = tk.Button(add_window, text="Save", command=save_book, bg="#007bff", fg="white", font=("Helvetica", 12, "bold"))
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=20)

    def edit_book(self):
        pass  # Implementation for editing a book with a similar dialog

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
