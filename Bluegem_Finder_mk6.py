import pytesseract
import pyautogui
import time
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Tesseract yolu belirtmeniz gerekebilir
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows için örnek yol

# Paint Seed'ler için örnek diziler (değiştirilebilir)
de_pattern_1 = ["490", "148", "69", "704"]
de_rank_1 = ["16", "48", "66", "67", "96", "111", "117", "159", "259", "263", "273", "297", "308", "321", "324", "341",
             "347", "461", "482", "517", "530", "567", "587", "674", "695", "723", "764", "772", "781", "790", "792",
             "843", "880", "885", "904", "948", "990"]
de_rank_2 = ["09", "116", "134", "158", "168", "225", "338", "354", "356", "365", "370", "386", "406", "426", "433",
             "441", "483", "537", "542", "592", "607", "611", "651", "668", "673", "696", "730", "743", "820", "846",
             "856", "857", "870", "876", "878", "882", "898", "900", "925", "942", "946", "951", "953", "970", "998"]
de_purple = ["29", "31", "33", "43", "72", "85", "88", "99", "104", "105", "128", "133", "136", "139", "140", "146",
             "146", "156", "172", "174", "176", "189", "216", "217", "249", "265", "290", "293", "310", "310", "322",
             "339", "340", "343", "363", "395", "404", "411", "437", "449", "451", "453", "458", "463", "487", "496",
             "509", "532", "550", "572", "572", "574", "598", "599", "605", "606", "614", "621", "627", "631", "653",
             "666", "667", "672", "683", "707", "710", "717", "727", "734", "740", "750", "766", "778", "795", "800",
             "804", "806", "811", "815", "816", "817", "839", "842", "848", "849", "850", "862", "877", "891", "913",
             "926", "927", "944", "952", "969", "971", "989"]
de_gold = ["4", "6", "14", "24", "37", "74", "78", "79", "80", "87", "102", "103", "124", "132", "135", "144", "167",
           "177", "180", "181", "182", "184", "184", "184", "205", "243", "247", "248", "252", "256", "256", "264",
           "269", "270", "277", "289", "292", "301", "323", "325", "334", "360", "362", "367", "374", "382", "392",
           "403", "428", "432", "443", "446", "466", "491", "492", "495", "505", "511", "527", "549", "555", "555",
           "558", "564", "568", "568", "577", "594", "604", "608", "623", "624", "629", "637", "638", "645", "646",
           "646", "686", "692", "733", "735", "738", "746", "783", "798", "802", "803", "813", "837", "868", "868",
           "887", "903", "907", "911", "914", "921", "923", "945", "986", "994"]


# OCR ile Paint Seed verilerini alacak fonksiyon
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


# Ekran görüntüsü alma fonksiyonu
def capture_full_screenshot():
    # Ekran görüntüsünü al
    screenshot = pyautogui.screenshot()

    # Ekran görüntüsünü geçici bir dosyaya kaydet
    file_name = "temp_screenshot.png"
    screenshot.save(file_name)

    # Dosya yolunu döndür
    return file_name


# Paint Seed'leri sınıflandırma
def process_and_classify_paint_seeds(paint_seeds):
    classified_data = []
    for seed in paint_seeds:
        if seed in de_pattern_1:
            classified_data.append({"Paint Seed": seed, "Category": "Blue-Gem", "type": "BLUE GEM!!!"})
        elif seed in de_rank_1:
            classified_data.append({"Paint Seed": seed, "Category": "Rank 1","type": "RANK 1!!!"})
        elif seed in de_rank_2:
            classified_data.append({"Paint Seed": seed, "Category": "Rank 2"})
        elif seed in de_purple:
            classified_data.append({"Paint Seed": seed, "Category": "Purple"})
        elif seed in de_gold:
            classified_data.append({"Paint Seed": seed, "Category": "Gold"})
    return classified_data


# Verileri CSV dosyasına kaydet
def save_to_csv(classified_data):
    # Verileri pandas DataFrame formatına dönüştür
    df = pd.DataFrame(classified_data)

    # 'Color' sütununu eklemek
    color_mapping = {
        "Blue-Gem": "Magenta",
        "Rank 1": "Red",
        "Rank 2": "Yellow",
        "Purple": "Purple",
        "Gold": "Gold"
    }
    df['Color'] = df['Category'].map(color_mapping).fillna('Unknown')  # Unknown olmayanlara renk ekle

    # CSV dosyasına kaydet
    file_name = f"bluegem_finder_{time.strftime('%Y%m%d%H%M%S')}.csv"
    df.to_csv(file_name, index=False)
    print(f"Paint Seed verileri {file_name} dosyasına kaydedildi.")

    # Sadece Unknown olmayanları içeren filtreli liste
    filtered_data = [f"{row['Category']} - Paint Seed: {row['Paint Seed']}, Color: {row['Color']}" for index, row in df.iterrows() if row['Category'] != 'Unknown']

    # Listeyi yazdır
    print("\n** Paint Seed Kategorileri ve Renkleri **")
    for item in filtered_data:
        print(item)



# Ana monitörün çözünürlüğü (örnek çözünürlük)
screen_width = 1920  # Ana monitör genişliği
screen_height = 1080  # Ana monitör yüksekliği

# Sayfa kaydırma ve verileri işleme fonksiyonu
def scroll_page_on_main_monitor():
    paint_seed_list = []

    for _ in range(16):  # Sayfayı 15 kez kaydırıyoruz
        pyautogui.moveTo(screen_width // 2, screen_height // 2)  # Ana monitörde ortalama bir yere tıkla
        pyautogui.scroll(-700)  # Sayfayı kaydır
        time.sleep(4)  # İçeriğin yüklenmesini beklemek için

        # Kaydırma sonrası ekran görüntüsü al
        print(f"Kaydırma {_ + 1}. işlemi tamamlandı, ekran görüntüsü alınıyor...")
        image_path = capture_full_screenshot()

        # OCR ile Paint Seed bilgilerini çıkart
        paint_seeds = extract_text_from_image(image_path)

        if paint_seeds:
            for seed in paint_seeds:
                print(f"Paint Seed: {seed}")
            # Sınıflandırılmış veriyi ekle
            classified_data = process_and_classify_paint_seeds(paint_seeds)
            paint_seed_list.extend(classified_data)
        else:
            print("Paint Seed bilgisi tespit edilemedi.")

    print("Tüm sayfa kaydırma işlemi tamamlandı.")
    save_to_csv(paint_seed_list)


# Ana fonksiyon
if __name__ == "__main__":
    scroll_page_on_main_monitor()
