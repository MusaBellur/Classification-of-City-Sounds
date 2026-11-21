import os # Dosya yolu birlestirme, klasor olusturma gibi isletim sistemi islemleri icin
import zipfile # ZIP dosyalarini acmak icin. Bu kodda henuz kullanilmiyor, sonraki adimda (zip'i cikarma) kullanacaksin
import requests # İnternetten dosya indirmek icin HTTP istegi atar
from tqdm import tqdm # İndirme sirasinda ilerleme cubugu gosterir

DATASET_URL = "https://github.com/karolpiczak/ESC-50/archive/refs/heads/master.zip" # İndirilecek veri setinin adresi. ESC-50, 50 sinifli cevresel ses veri seti
RAW_DATA_DIR = "data/raw" # İndirilen ham verinin kaydedilecegi klasor
ZIP_DATA = os.path.join(RAW_DATA_DIR, "esc50.zip") # Zip dosyasinin tam yolunu olusturur: data/raw/esc50.zip

def download_file(url, save_path): # İndirme isini yapan fonksiyon. Adres ve kayit yolunu parametre olarak alır
    response = requests.get(url, stream=True) # Adrese istek atar. stream=True dosyayi tek seferde bellege yuklemek yerine parca parca indirmeyi saglar
    response.raise_for_status() # Istek başarisizsa (404, 500 gibi) hemen hata firlatir. Böylece bozuk bir dosya indirmiş olmazsin
    total_size = int(response.headers.get("content-length",0)) # Sunucunun bildirdigi toplam dosya boyutunu okur (ilerleme cubugunun yuzdesi icin). Bulamazsa 0 kullanır
    with open(save_path, "wb") as file: # Dosyayi wb (write binary, ikili yazma) modunda acar. with blogu bitince dosya otomatik kapanir
        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            desc= "Downloading the dataset"
            """
            İlerleme çubuğunu oluşturur:
            total: Toplam boyut
            unit: Birim adi. Hata: 8 değil "B" (byte) olmali, string beklenir
            unit_scale=True: Byte'lari otomatik KB, MB olarak gösterir
            desc: Çubuğun solundaki açiklama
            """
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024): # Veriyi 1024 byte'lık (1 KB) parçalar halinde döngüyle alır
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
                    """
                    Parça boş değilse dosyaya yazar ve çubuğu o parçanin boyutu kadar ilerletir
                    """