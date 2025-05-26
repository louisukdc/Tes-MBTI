import json
from collections import deque

# Fungsi untuk membaca file JSON soal MBTI
def load_pertanyaan(filename='soal_mbtix.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


# Fungsi validasi nomor HP Indonesia (contoh sederhana)
def validasi_nomor_hp(nomor):
    return nomor.startswith('08') and 10 <= len(nomor) <= 13 and nomor.isdigit()

# Fungsi mendapatkan input pengguna
def input_data_user():
    nama = input("Masukkan Nama Anda: ").strip()
    while True:
        no_hp = input("Masukkan Nomor HP Anda (format Indonesia): ").strip()
        if validasi_nomor_hp(no_hp):
            print("✅ Nomor HP valid.")
            break
        else:
            print("❌ Nomor tidak valid. Harus dimulai dengan '08' dan 10–13 digit.")
    return nama, no_hp


# Fungsi untuk mendapatkan jawaban dari pengguna
def dapatkan_jawaban_user(pertanyaan_list):
    jawaban_user = []
    print("Silakan jawab pertanyaan berikut dengan memilih A atau B:\n")
    for i, p in enumerate(pertanyaan_list, 1):
        print(f"{i}. {p['pertanyaan']}")
        print(f"   A. {p['opsi']['A']['jawaban']}")
        print(f"   B. {p['opsi']['B']['jawaban']}")
        while True:
            jawaban = input("Jawaban Anda (A/B): ").strip().upper()
            if jawaban in ['A', 'B']:
                nilai_dimensi = p['opsi'][jawaban]['nilai']
                jawaban_user.append(nilai_dimensi)
                break
            else:
                print("Masukkan hanya A atau B.")
    return jawaban_user


from collections import Counter

def hitung_mbti_dari_jawaban(jawaban_user, pertanyaan_list):
    # Kelompokkan jawaban berdasarkan dimensi
    dimensi_jawaban = {
        'E/I': [],
        'S/N': [],
        'T/F': [],
        'J/P': []
    }

    for i, dimensi in enumerate(pertanyaan_list):
        kode = dimensi["kode"]  # E/I, S/N, dst
        nilai = jawaban_user[i]
        if kode in dimensi_jawaban:
            dimensi_jawaban[kode].append(nilai)

    # Ambil mayoritas dari masing-masing dimensi
    hasil_akhir = ""
    for kode in ['E/I', 'S/N', 'T/F', 'J/P']:
        counter = Counter(dimensi_jawaban[kode])
        if not counter:
            continue
        if counter['E'] > counter['I']:
            hasil_akhir += 'E'
        elif counter['I'] > counter['E']:
            hasil_akhir += 'I'
        elif counter['S'] > counter['N']:
            hasil_akhir += 'S'
        elif counter['N'] > counter['S']:
            hasil_akhir += 'N'
        elif counter['T'] > counter['F']:
            hasil_akhir += 'T'
        elif counter['F'] > counter['T']:
            hasil_akhir += 'F'
        elif counter['J'] > counter['P']:
            hasil_akhir += 'J'
        elif counter['P'] > counter['J']:
            hasil_akhir += 'P'
        else:
            hasil_akhir += list(counter.keys())[0]  # jika seri, ambil acak

    return hasil_akhir



# Fungsi BFS MBTI – menelusuri jalur dimensi berdasarkan urutan jawaban
def bfs_mbti_search(pertanyaan_list, jawaban_user):
    queue = deque()
    queue.append(([], 0))  # (jalur saat ini, indeks pertanyaan)
    
    while queue:
        path, idx = queue.popleft()
        if idx == len(pertanyaan_list):
            return ''.join(path)
        
        nilai_dimensi = jawaban_user[idx]
        next_path = path + [nilai_dimensi]
        queue.append((next_path, idx + 1))

    return None

# Fungsi utama program
def main():
    print("🧪 Selamat datang di Tes MBTI Berbasis AI (Algoritma Pencarian) 🎯\n")
    nama, no_hp = input_data_user()
    pertanyaan = load_pertanyaan()
    jawaban_user = dapatkan_jawaban_user(pertanyaan)
    hasil_mbti = hitung_mbti_dari_jawaban(jawaban_user, pertanyaan)

    print("\n🎉 Hasil Tes MBTI untuk", nama)
    print("📱 Nomor HP:", no_hp)
    print("🧠 Tipe Kepribadian MBTI Anda adalah:", hasil_mbti)

if __name__ == "__main__":
    main()
