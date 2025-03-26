import cv2
import numpy as np
import pytesseract
import pyautogui
import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Tesseract OCR yolunu belirle
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Kategorilere göre belirlenmiş pattern ID'leri
categories = {
    "Blue-Gem": ["490", "148", "69", "704", "504"],
    "Rank 1": ["16", "48", "66", "67", "96", "111", "117", "159", "259", "263", "273", "297", "308", "321", "324",
               "341", "347", "461", "482", "517", "530", "567", "587", "674", "695", "723", "764", "772", "781", "790",
               "792", "843", "880", "885", "904", "948", "990"],
    "Rank 2": ["09", "116", "134", "158", "168", "225", "338", "354", "356", "365", "370", "386", "406", "426", "433",
               "441", "483", "537", "542", "592", "607", "611", "651", "668", "673", "696", "730", "743", "820", "846",
               "856", "857", "870", "876", "878", "882", "898", "900", "925", "942", "946", "951", "953", "970", "998"]
}

# Renk kodları
category_colors = {
    "Blue-Gem": "magenta",
    "Rank 1": "red",
    "Rank 2": "yellow",
    "Diğer": "white"
}


def capture_screen(region=None):
    """Belirtilen ekrandan bir bölgeyi yakalar ve OpenCV formatına çevirir."""
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


def extract_text_from_image(image):
    """Görüntüden OCR kullanarak metin çıkarır."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 6')
    return text.strip()


def categorize_numbers(text):
    """Tespit edilen numaraları kategorize eder."""
    extracted_numbers = text.split()
    categorized = {cat: [] for cat in categories.keys()}
    all_numbers = []

    for num in extracted_numbers:
        all_numbers.append(num)
        matched = False
        for cat, num_list in categories.items():
            if num in num_list:
                categorized[cat].append(num)
                matched = True
                break

        if not matched:
            if "Diğer" not in categorized:
                categorized["Diğer"] = []
            categorized["Diğer"].append(num)

    return categorized, all_numbers


def update_ui():
    image = capture_screen()
    extracted_text = extract_text_from_image(image)
    results, all_numbers = categorize_numbers(extracted_text)

    for widget in frame.winfo_children():  # Önceki verileri temizle
        widget.destroy()

    # Tarama sonuçlarını göster
    raw_label = tk.Label(frame, text=f"OCR Çıktısı: {', '.join(all_numbers)}", fg="cyan", bg='black',
                         font=("Arial", 10))
    raw_label.pack(anchor='w', padx=10, pady=5)

    if any(results.values()):  # Eğer eşleşen bir şey varsa göster
        for cat, nums in results.items():
            if nums:
                label = tk.Label(frame, text=f"{cat}: {', '.join(nums)}", fg=category_colors.get(cat, "white"),
                                 bg='black', font=("Arial", 12, "bold"))
                label.pack(anchor='w', padx=10, pady=2)
    else:
        label = tk.Label(frame, text="Eşleşen veri bulunamadı", fg="white", bg='black', font=("Arial", 12))
        label.pack()


# Tkinter GUI
tk_root = tk.Tk()
tk_root.title("CS2 Bluegem Finder")
tk_root.geometry("700x500")
tk_root.configure(bg='black')

title_label = tk.Label(tk_root, text="CS2 Bluegem Finder", fg="cyan", bg='black', font=("Arial", 14, "bold"))
title_label.pack(pady=10)

frame = tk.Frame(tk_root, bg='black')
frame.pack(fill='both', expand=True, padx=10, pady=10)

button = ttk.Button(tk_root, text="Güncelle", command=update_ui)
button.pack(pady=10)

tk_root.mainloop()