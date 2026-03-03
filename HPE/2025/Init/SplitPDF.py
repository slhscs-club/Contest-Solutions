import fitz
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from CreatePy import create_file

BG = "#1a1a1a"
FG = "#e0e0e0"
ACCENT = "#2d2d2d"
BLUE = "#007acc"
GREEN = "#218838"

class PDFClipper:
    def __init__(self, win):
        self.win = win
        self.win.title("PDF Clipper")
        self.win.geometry("1000x900")
        self.win.configure(bg=BG)
        
        self.pdf = None
        self.path = ""
        self.idx = 0
        self.marks = {}

        self.ui()
        self.keys()

    def ui(self):
        self.top = tk.Frame(self.win, bg=ACCENT, pady=10)
        self.top.pack(fill=tk.X)

        tk.Button(self.top, text="OPEN", command=self.open_file, 
                  bg=BLUE, fg="white", font=("Arial", 9, "bold"),
                  relief="flat", padx=15).pack(side=tk.LEFT, padx=15)

        tk.Label(self.top, text="PROB:", bg=ACCENT, fg=FG).pack(side=tk.LEFT)
        self.id_box = tk.Entry(self.top, width=4, font=("Consolas", 14), bg=BG, fg=BLUE, 
                               insertbackground="white", justify='center', relief="flat")
        self.id_box.pack(side=tk.LEFT, padx=10)
        self.id_box.insert(0, "00")

        tk.Button(self.top, text="EXPORT", command=self.save, 
                  bg=GREEN, fg="white", font=("Arial", 9, "bold"),
                  relief="flat", padx=15).pack(side=tk.RIGHT, padx=15)

        self.bar = tk.Label(self.win, text="Ready", bg=BG, fg="#888888")
        self.bar.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.view = tk.Label(self.win, bg=BG)
        self.view.pack(expand=True)

    def keys(self):
        self.view.bind("<Button-1>", self.on_left)
        self.view.bind("<Button-2>", self.on_mid)
        self.view.bind("<Button-3>", self.on_right)
        self.win.bind("<Left>", lambda e: self.move(-1))
        self.win.bind("<Right>", lambda e: self.move(1))

    def open_file(self):
        self.path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if self.path:
            self.pdf = fitz.open(self.path)
            self.idx = 0
            self.marks = {}
            self.win.update()
            self.draw()

    def draw(self):
        if not self.pdf: return
        page = self.pdf[self.idx]
        
        w = self.win.winfo_width()
        h = self.win.winfo_height() - 120
        rect = page.rect
        zoom = min(w/rect.width, h/rect.height) * 0.95

        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.img = ImageTk.PhotoImage(img)
        self.view.config(image=self.img)
        
        tag = self.marks.get(self.idx, "NONE")
        self.bar.config(text=f"PAGE {self.idx + 1}/{len(self.pdf)} | TAG: {tag}")

    def move(self, d):
        if not self.pdf: return
        new = self.idx + d
        if 0 <= new < len(self.pdf):
            self.idx = new
            self.draw()

    def on_left(self, e):
        if not self.pdf: return
        num = self.id_box.get().strip().zfill(2)
        self.marks[self.idx] = f"problem{num}"
        self.move(1)

    def on_mid(self, e):
        self.move(1)

    def on_right(self, e):
        try:
            val = int(self.id_box.get())
            self.id_box.delete(0, tk.END)
            self.id_box.insert(0, str(val + 1).zfill(2))
        except: pass
        self.move(1)

    def save(self):
        if not self.marks: return
        groups = {}
        for pg, name in self.marks.items():
            groups.setdefault(name, []).append(pg)

        for name, pages in groups.items():
            out = fitz.open()
            for p in sorted(pages):
                out.insert_pdf(self.pdf, from_page=p, to_page=p)
            out.save(f"{name}.pdf")
            out.close()
            create_file(name)
        messagebox.showinfo("Saved", f"Exported {len(groups)} files to local folder.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFClipper(root)
    root.mainloop()