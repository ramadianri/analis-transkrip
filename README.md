# Analisis Transkrip Akademik
Proyek ini berisi skrip Python untuk menganalisis transkrip akademik dari file HTML dan membandingkannya dengan data kurikulum dari file Excel.

## Tujuan Proyek
Tujuan utama dari skrip ini adalah untuk:
- Mengurai data transkrip dari file HTML.
- Mengidentifikasi mata kuliah wajib yang belum diambil.
- Menemukan mata kuliah dengan nilai di bawah C dan menghitung total SKS-nya.
- Melakukan pemeriksaan silang antara total SKS yang ditempuh dengan total SKS yang seharusnya ditempuh berdasarkan semester berjalan.
- Menyimpan hasil analisis ke dalam file teks di folder output.

## Cara Mengkloning Repositori
Anda dapat mengkloning repositori ini ke komputer lokal Anda dengan menjalankan perintah berikut di terminal:
> git clone https://github.com/ramadianri/analis-transkrip.git

## Cara Menginstal Dependensi
Proyek ini membutuhkan beberapa pustaka Python yang dapat diinstal menggunakan file requirements.txt. Pastikan Anda memiliki Python dan pip terinstal, lalu jalankan perintah berikut:
> pip install -r requirements.txt

## Cara Menambahkan Transkrip Mahasiswa
- Login ke akun [SIA](http://sia.unram.ac.id/)
- Di sebelah kiri, klik `Mahasiswa`
- Pilih mahasiswa dengan cara klik `NIM' dari mahasiswa tersebut
- Pada bagian `Tahun Akademik` pilih `Transkrip Nilai`
- Klik kanan pada laman web, kemudian klik `Save as`
- Isi nama file dengan nama mahasiswa (opsional), pastikan kolom `save as type:` dipilih `HTML only`
- Simpan file tersebut di folder `transkrip` pada direktori utama

*Catatan : Anda bisa menyimpan lebih dari 1 file, secara otomatis skrip akan menganalisis semua file

## Cara Menjalankan Skrip
- Pastikan Anda telah menempatkan file transkrip yang ingin dianalisis dalam format HTML di dalam folder `transkrip`.
- Pastikan file kurikulum .xlsx Anda ada di dalam folder `kurikulum`.
- Jalankan skrip dari direktori utama dengan perintah:
    > python analis_transkrip.py
- Setelah selesai, hasil analisis akan disimpan sebagai file .txt di dalam folder `output`.