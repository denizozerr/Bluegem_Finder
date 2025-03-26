import time
import pyautogui
import cv2
import pytesseract
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd ="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
def capture_screen(region=None):
    """Belirtilen ekrandan bir bölgeyi yakalar ve OpenCV formatına çevirir."""
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


def process_image(img):
    """OCR doğruluğunu artırmak için görüntüyü işler."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh


def extract_text(img):
    """Görüntüden yazıyı ayıklar."""
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text.strip()


def main():
    # Steam Pazarındaki item bölgesini belirle (koordinatlar değişebilir)
    region = (300, 400, 500, 200)  # Örnek koordinatlar (x, y, genişlik, yükseklik)

    while True:
        screenshot = capture_screen(region)
        processed = process_image(screenshot)
        text = extract_text(processed)

        print("OCR Çıktısı:", text)

        # Eğer belirli pattern ID'ler bulunursa renklendir
        important_patterns = [256, 211, 22, 6, 832]
        for pattern in important_patterns:
            if str(pattern) in text:
                print(f"⚠️ ÖNEMLİ BULUNDU: Pattern {pattern} detected!")

        time.sleep(5)  # 5 saniyede bir tekrar et


if __name__ == "__main__":
    main()
