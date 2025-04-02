import customtkinter as ctk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("PDF Protector Tool")
app.geometry("500x400")
app.resizable(False, False)

# Global PDF path
selected_pdf = None

# ----- Functions ----- #

def select_pdf():
    global selected_pdf
    filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if filepath:
        selected_pdf = filepath
        pdf_label.configure(text=os.path.basename(filepath))
    else:
        pdf_label.configure(text="No file selected")

def protect_pdf():
    if not selected_pdf:
        messagebox.showerror("Error", "Please select a PDF file.")
        return

    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    try:
        reader = PdfReader(selected_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="protected.pdf"
        )

        if save_path:
            with open(save_path, "wb") as f:
                writer.write(f)
            messagebox.showinfo("Success", "PDF has been password protected!")
        else:
            messagebox.showwarning("Cancelled", "Save operation was cancelled.")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# ----- UI Layout ----- #

title_label = ctk.CTkLabel(app, text="🔒 PDF Protector", font=("Segoe UI", 28, "bold"))
title_label.pack(pady=20)

select_btn = ctk.CTkButton(app, text="Select PDF", command=select_pdf)
select_btn.pack(pady=10)

pdf_label = ctk.CTkLabel(app, text="No file selected", font=("Segoe UI", 12))
pdf_label.pack(pady=5)

password_entry = ctk.CTkEntry(app, placeholder_text="Enter password", show="*", width=300)
password_entry.pack(pady=20)

protect_btn = ctk.CTkButton(app, text="Protect PDF", command=protect_pdf, fg_color="#3B82F6", hover_color="#2563EB")
protect_btn.pack(pady=20)

footer = ctk.CTkLabel(app, text="Made with ❤️ by Proxlight", font=("Segoe UI", 10))
footer.pack(side="bottom", pady=10)

app.mainloop()
 
