import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
import PyPDF2
import os

def create_watermark(watermark_text, output_filename):
    c = canvas.Canvas(output_filename)
    c.setFont("Helvetica", 40)
    c.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.3)
    width, height = c._pagesize

    # Position the text in the center with a rotation
    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, watermark_text)
    c.restoreState()

    c.save()

def add_watermark(input_pdf, output_pdf, watermark_pdf):
    with open(input_pdf, "rb") as input_file, open(watermark_pdf, "rb") as watermark_file:
        # Read the input PDF and watermark PDF
        input_pdf_reader = PyPDF2.PdfReader(input_file)
        watermark_pdf_reader = PyPDF2.PdfReader(watermark_file)
        watermark_page = watermark_pdf_reader.pages[0]

        # Create a PDF writer to save the result
        pdf_writer = PyPDF2.PdfWriter()

        # Iterate through the pages and merge with the watermark
        for page in input_pdf_reader.pages:
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)

        # Write the output PDF
        with open(output_pdf, "wb") as output_file:
            pdf_writer.write(output_file)

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def process_files():
    input_pdf = input_entry.get()
    output_pdf = output_entry.get()
    watermark_text = watermark_entry.get()

    if not input_pdf or not output_pdf or not watermark_text:
        messagebox.showwarning("Input Error", "Please fill out all fields.")
        return

    watermark_pdf = "temp_watermark.pdf"
    create_watermark(watermark_text, watermark_pdf)
    add_watermark(input_pdf, output_pdf, watermark_pdf)
    os.remove(watermark_pdf)

    messagebox.showinfo("Success", f"Watermark added successfully to {output_pdf}")

# Set up the main window
root = tk.Tk()
root.title("PDF Watermarker")

# Input PDF file selection
tk.Label(root, text="Input PDF:").grid(row=0, column=0, padx=10, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=5)
input_button = tk.Button(root, text="Browse", command=select_input_file)
input_button.grid(row=0, column=2, padx=10, pady=5)

# Watermark text input
tk.Label(root, text="Watermark Text:").grid(row=1, column=0, padx=10, pady=5)
watermark_entry = tk.Entry(root, width=50)
watermark_entry.grid(row=1, column=1, padx=10, pady=5)

# Output PDF file selection
tk.Label(root, text="Output PDF:").grid(row=2, column=0, padx=10, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=2, column=1, padx=10, pady=5)
output_button = tk.Button(root, text="Browse", command=select_output_file)
output_button.grid(row=2, column=2, padx=10, pady=5)

# Process button
process_button = tk.Button(root, text="Add Watermark", command=process_files)
process_button.grid(row=3, column=1, padx=10, pady=20)

# Run the application
root.mainloop()