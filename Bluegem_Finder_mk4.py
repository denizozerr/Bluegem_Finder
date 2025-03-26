import pytesseract
from PIL import Image
import pyautogui
import time
import cv2
import numpy as np

# Tesseract yolu belirtmeniz gerekebilir
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows için örnek yol


def capture_full_screenshot():
    # Ekranın tamamını yakala
    screenshot = pyautogui.screenshot()
    screenshot.save("full_screenshot.png")
    return "full_screenshot.png"


def scroll_and_capture_screenshot():
    # Sayfayı kaydırarak ekran görüntüsü al
    # İlk olarak ekranın tamamını al
    screenshot = capture_full_screenshot()
    print(f"Sayfa kaydırıldı ve ekran görüntüsü alındı: {screenshot}")
    return screenshot


def extract_text_from_image(image_path):
    # Görüntüyü yükle
    img = cv2.imread(image_path)

    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Görüntüdeki metni tespit et
    text = pytesseract.image_to_string(gray)

    # Paint Seed değerini metinden çıkar
    paint_seeds = []
    if "Paint Seed" in text:
        lines = text.splitlines()
        for line in lines:
            if "Paint Seed" in line:
                # Paint Seed bilgilerini çıkart
                paint_seed = line.split(":")[-1].strip()
                paint_seeds.append(paint_seed)
    return paint_seeds


# Sayfanın tamamını veya kaydırarak birkaç görüntü al
for _ in range(3):  # Sayfayı 3 kez kaydırıyoruz, ihtiyaca göre arttırabilirsiniz
    image_path = scroll_and_capture_screenshot()

    # OCR ile Paint Seed bilgilerini çıkart
    paint_seeds = extract_text_from_image(image_path)

    if paint_seeds:
        for seed in paint_seeds:
            print(f"Paint Seed: {seed}")
    else:
        print("Paint Seed bilgisi tespit edilemedi.")


# Ana monitörün çözünürlüğü (örnek çözünürlük)
screen_width = 1920  # Ana monitör genişliği
screen_height = 1080  # Ana monitör yüksekliği

def scroll_page_on_main_monitor():
    # Monitörde kaydırma işlemi
    for _ in range(15):  # Sayfayı 5 kez kaydırıyoruz
        pyautogui.moveTo(screen_width // 2, screen_height // 2)  # Ana monitörde ortalama bir yere tıkla
        pyautogui.scroll(-500)  # Sayfayı kaydır
        time.sleep(4)  # İçeriğin yüklenmesini beklemek için
    print("Sayfa kaydırma tamamlandı.")

scroll_page_on_main_monitor()
# İstenilen kadar döngüyle ekranı kaydırarak tüm verileri işleyebilirsiniz
