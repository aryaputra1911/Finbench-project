import os
import json
import requests
import pandas as pd
from tqdm import tqdm

def setup_project():
    # 1. Membuat Struktur Folder
    folders = [
        'data/raw',
        'data/processed',
        'src',
        'notebooks',
        'app',
        'tests',
        'scripts'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✔ Folder created: {folder}")

    # 2. Membaca Dataset untuk mengambil Link PDF
    jsonl_file = r"C:\Users\ARYA\Downloads\financebench_merged.jsonl"
    
    if not os.path.exists(jsonl_file):
        print(f"❌ Error: File {jsonl_file} tidak ditemukan!")
        return

    print(f"\n--- Memulai Proses Download PDF ---")
    
    # Membaca file JSONL
    df = pd.read_json(jsonl_file, lines=True)
    
    # Mengambil URL unik agar tidak download file yang sama berulang kali
    unique_docs = df[['doc_name', 'doc_link']].drop_duplicates()
    
    success_count = 0
    fail_count = 0

    # 3. Proses Download
    for index, row in tqdm(unique_docs.iterrows(), total=len(unique_docs), desc="Downloading PDFs"):
        doc_name = row['doc_name']
        url = row['doc_link']
        
        # Nama file tujuan
        file_path = f"data/raw/{doc_name}.pdf"
        
        # Cek jika file sudah ada, jangan download lagi
        if os.path.exists(file_path):
            continue
            
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"\n⚠️ Gagal download {doc_name}: {e}")
            fail_count += 1

    print(f"\n--- Selesai! ---")
    print(f"✅ Berhasil download: {success_count} file")
    print(f"❌ Gagal: {fail_count} file")
    print(f"📂 Semua PDF tersimpan di: data/raw/")

if __name__ == "__main__":
    setup_project()