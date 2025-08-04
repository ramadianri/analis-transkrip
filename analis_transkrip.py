import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
import sys
import os
import glob

def extract_table_to_dataframe(html_content):
    """
    Mengurai konten html untuk menemukan tabel dan mengubahnya menjadi DataFrame pandas.
    
    Args:
        html_content (str): Konten html sebagai string.
    Returns:
        pd.DataFrame
    """
    # Membuat objek BeautifulSoup untuk mengurai html
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Temukan tabel berdasarkan kelasnya. HTML memiliki tabel dengan kelas ‘table table-hover table-bordered’.
    table = soup.find('table', class_='table table-hover table-bordered')
    if not table:
        print("[INFO] Tabel tidak ditemukan dalam konten HTML.")
        return None
    
    # Ekstrak header tabel dari bagian <thead>
    headers = [th.get_text(strip=True) for th in table.find('thead').find_all('th')]
    # Ekstrak baris tabel dari bagian <tbody>
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        # Ekstrak teks dari setiap sel (td) di baris
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        rows.append(cells)
    
    # Membuat pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)
    
    return df

def extract_specific_values(html_content):
    """
    Mengurai konten HTML untuk menemukan nilai tertentu seperti 
    Tahun Masuk dan Total SKS dari tabel yang relevan.
    
    Args:
        html_content (str): Konten html sebagai string.
    Returns:
        dict
    """
    # Membuat objek BeautifulSoup untuk mengurai html
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Dictionary untuk menyimpan nilai yang diekstrak
    extracted_data = {}
    
    # Temukan tabel yang berisi Tahun Masuk dan Total SKS
    academic_table = soup.find('table', class_='table table-hover table-krs-head')
    
    if academic_table:
        # Temukan baris untuk Tahun Masuk
        tahun_masuk_th = academic_table.find('th', string='Tahun Masuk')
        if tahun_masuk_th:
            # Nilai tersebut ada di elemen berikutnya <td>
            tahun_masuk_td = tahun_masuk_th.find_next_sibling('td')
            if tahun_masuk_td:
                extracted_data['Tahun Masuk'] = tahun_masuk_td.get_text(strip=True)
        
        # Temukan baris untuk Total SKS
        total_sks_th = academic_table.find('th', string='Total SKS')
        if total_sks_th:
            # Nilai tersebut ada di elemen berikutnya <td>
            total_sks_td = total_sks_th.find_next_sibling('td')
            if total_sks_td:
                extracted_data['Total SKS'] = total_sks_td.get_text(strip=True)
        
        # Temukan baris untuk IPK
        ipk_th = academic_table.find('th', string='IPK')
        if ipk_th:
            # Nilai tersebut ada di elemen berikutnya <td>
            ipk_td = ipk_th.find_next_sibling('td')
            if ipk_td:
                extracted_data['IPK'] = ipk_td.get_text(strip=True)
    
    # Temukan tabel yang berisi Nama dan No. HP
    biodata_table = soup.find('div', class_='col-md-6').find('table', class_='table table-hover')
    if biodata_table:
        # Temukan baris untuk Nama
        nama_th = biodata_table.find('th', string='Nama')
        if nama_th:
            # Nilai tersebut ada di elemen berikutnya <td>
            nama_td = nama_th.find_next_sibling('td')
            if nama_td:
                extracted_data['Nama'] = nama_td.get_text(strip=True)
        
        # Temukan baris untuk No. HP
        nohp_th = biodata_table.find('th', string='No. HP')
        if nohp_th:
            # Nilai tersebut ada di elemen berikutnya <td>
            nohp_td = nohp_th.find_next_sibling('td')
            if nohp_td:
                extracted_data['No. HP'] = nohp_td.get_text(strip=True)
                
    return extracted_data

def analyze_transcript(html_file_path):
    """
    Fungsi utama untuk menganalisis transkrip akademik dan mengembalikan 
    string dari hasil analisis.
    
    Args:
        html_file_path (str): Path ke file transkrip HTML.
    
    Returns:
        str: String yang berisi hasil analisis yang akan ditulis ke file.
    """
    output_lines = []

    # Load data dari file html
    print(f'[INFO] Memproses file: {os.path.basename(html_file_path)}... ', end='')
    try:
        html_content = open(html_file_path, 'r', encoding='utf-8').read()
        print('berhasil')
    except FileNotFoundError:
        print('Gagal: File tidak ditemukan. Pastikan path dan nama file sudah benar.')
        return None
    except Exception as e:
        print(f'Gagal: Terjadi kesalahan lain. Detail kesalahan: {e}')
        return None

    # Ekstrak nilai-nilai yang diperlukan
    values = extract_specific_values(html_content)
    # Cek apakah ekstraksi berhasil atau gagal
    if values:
        tahun_masuk = values.get('Tahun Masuk', 'Not found')
        # Handle cases where `tahun_masuk` might be "Not found"
        if tahun_masuk != 'Not found':
            tahun_masuk = int(tahun_masuk.split()[0])
        else:
            output_lines.append("[ERROR] Tahun Masuk tidak ditemukan.")
            return "\n".join(output_lines)

        total_sks = values.get('Total SKS', 'Not found')
        if total_sks != 'Not found':
            total_sks = int(total_sks)
        else:
            output_lines.append("[ERROR] Total SKS tidak ditemukan.")
            return "\n".join(output_lines)

        ipk = values.get('IPK', 'Not found')
        if ipk != 'Not found':
            ipk = float(ipk)
        else:
            output_lines.append("[ERROR] IPK tidak ditemukan.")
            return "\n".join(output_lines)

        nama = values.get('Nama', 'Not found')
        no_hp = values.get('No. HP', 'Not found')
        
        # Menghitung semester (karena tidak ada di html)
        today = date.today()
        if today.month <= 6:
            semester = 2 * (today.year - tahun_masuk)
        else:
            semester = 2 * (today.year - tahun_masuk) + 1
        
        output_lines.append(" ")
        output_lines.append("Biodata:")
        output_lines.append('---------------------')
        output_lines.append(f"Nama        : {nama}")
        output_lines.append(f"No. HP      : {no_hp}")
        output_lines.append(f"Tahun Masuk : {tahun_masuk}")
        output_lines.append(f"Semester    : {semester}")
        output_lines.append(f"Total SKS   : {total_sks}")
        output_lines.append(f"IPK         : {ipk}")
        
    else:
        print("[INFO] Tidak dapat menemukan nilai-nilai yang diperlukan")
        return None

    # Gunakan kurikulum sesuai tahun masuk pada transkrip
    if tahun_masuk < 2021:
        kurikulum_file = kurikulum_files[0]
    elif tahun_masuk < 2025:
        kurikulum_file = kurikulum_files[1]
    
    # Mengkonversi tabel pada file kurikulum ke dataframe
    print(f'[INFO] Menggunakan kurikulum: {os.path.basename(kurikulum_file)}... ', end='')
    try:
        df_kurikulum = pd.read_excel(kurikulum_file)
        print('berhasil')
    except FileNotFoundError:
        print('Gagal: File tidak ditemukan. Pastikan path dan nama file sudah benar.')
        return None
    except Exception as e:
        print(f'Gagal: Terjadi kesalahan lain. Detail kesalahan: {e}')
        return None

    # Mengkonversi tabel pada file htlm ke dataframe
    df_transkrip = extract_table_to_dataframe(html_content)
    if df_transkrip is None:
        print("[ERROR] Gagal mengkonversi transkrip ke DataFrame.")
        return None

    # Menghilangkan data yang sama
    df_transkrip.drop_duplicates(inplace=True)

    # Merubah nama kolom
    df_transkrip.rename(columns={'Nilai': 'Nilai Huruf'}, inplace=True)

    # Mengkonversi nilai huruf ke angka
    nilai_mapping = {
        'A': 4.0,
        'B+': 3.5,
        'B': 3.0,
        'C+': 2.5,
        'C': 2.0,
        'D+': 1.5,
        'D': 1.0,
        'E': 0.0,
        'T': 0.0
    }
    df_transkrip['Nilai Angka'] = df_transkrip['Nilai Huruf'].map(nilai_mapping)

    # Menghilangkan duplikasi mata kuliah yang pernah diulang (diambil nilai tertinggi)
    if df_transkrip['Nama'].duplicated().any() == True:
        duplicated_mask = df_transkrip['Nama'].duplicated(keep=False)
        for nama_mk in df_transkrip[duplicated_mask]['Nama'].unique():
            matkul_mask = df_transkrip['Nama'] == nama_mk
            nilai_tertinggi = df_transkrip[matkul_mask]['Nilai Angka'].max()
            nilai_mask = df_transkrip['Nilai Angka'] < nilai_tertinggi
            mask_to_drop = matkul_mask & nilai_mask
            df_transkrip = df_transkrip[~mask_to_drop]

    # Menghapus kolom
    df_transkrip.drop(['Nilai Angka'], axis=1, inplace=True)

    # Merubah nama kolom
    df_transkrip.rename(columns={'Nilai Huruf': 'Nilai'}, inplace=True)

    # Memilih hanya semester yang pernah dilalui dari dataframe kurikulum
    df_kurikulum = df_kurikulum[df_kurikulum['Semester'] < semester]

    # Menggabungkan dataframe
    df = pd.merge(df_transkrip, df_kurikulum, on='Kode MK', how='outer')

    # Memperbaiki kolom Nama
    df['Nama_x'] = df.apply(
        lambda row: row['Nama_y'] if pd.isna(row['Nama_x']) else row['Nama_x'],
        axis=1
    )
    df.drop(['Nama_y'], axis=1, inplace=True)
    df.rename(columns={'Nama_x': 'Nama'}, inplace=True)

    # Memperbaiki kolom SKS
    df['SKS_x'] = df.apply(
        lambda row: row['SKS_y'] if pd.isna(row['SKS_x']) else row['SKS_x'],
        axis=1
    )
    df.drop(['SKS_y'], axis=1, inplace=True)
    df.rename(columns={'SKS_x': 'SKS'}, inplace=True)

    # Mengisi nilai-nilai kosong
    df.fillna({'Semester': 0}, inplace=True)
    df.fillna({'Sifat': 'Pilihan'}, inplace=True)

    # Memperbaiki tipe data
    df['Semester'] = df['Semester'].apply(lambda x: int(x))
    df['SKS'] = df['SKS'].apply(lambda x: int(x))

    # cross-check jumlah SKS pada dataframe dan html
    nilai_non_T_mask = df['Nilai'] != 'T'
    nila_not_nan_mask = ~df['Nilai'].isna()
    if df[nilai_non_T_mask & nila_not_nan_mask]['SKS'].sum() != total_sks:
        print(" ")
        print("[ERROR] Total SKS tidak sesuai. Keluar dari program")
        return None

    # Cek proporsi Mata Kuliah wajib dan pilihan
    output_lines.append(" ")
    output_lines.append('Proporsi Mata Kuliah wajib dan pilihan:')
    output_lines.append('---------------------------------------')
    wajib_mask = df['Sifat'] == 'Wajib'
    nilai_not_nan_mask = ~df['Nilai'].isna()
    output_lines.append(f'Total SKS Mata Kuliah wajib   : {df[wajib_mask & nilai_not_nan_mask]['SKS'].sum()} SKS')
    output_lines.append(f'Total SKS Mata Kuliah pilihan : {df[df['Sifat'] == 'Pilihan']['SKS'].sum()} SKS')

    # Cek Mata Kuliah wajib yang belum diambil
    output_lines.append(" ")
    output_lines.append('Mata Kuliah wajib yang belum diambil (berdasarkan semester):')
    output_lines.append('------------------------------------------------------------')
    output_lines.append(df[df['Nilai'].isna()][['Kode MK','Nama','SKS','Semester']].to_string(index=False))

    # Cek Mata Kuliah dengan nilai di bawah C
    nilai_T_mask = df['Nilai'] == 'T'
    nilai_E_mask = df['Nilai'] == 'E'
    nilai_D_mask = df['Nilai'] == 'D'
    nilai_Dp_mask = df['Nilai'] == 'D+'
    output_lines.append(" ")
    output_lines.append('Mata Kuliah dengan nilai di bawah C:')
    output_lines.append(f'Total : {df[nilai_T_mask | nilai_E_mask | nilai_D_mask | nilai_Dp_mask]['SKS'].sum()} SKS')
    output_lines.append('------------------------------------')
    output_lines.append(df[nilai_T_mask | nilai_E_mask | nilai_D_mask | nilai_Dp_mask].to_string(index=False))

    # Kesesuian antara jumlah SKS yang sudah ditempuh dan jumlah SKS yang seharusnya sudah ditempuh
    jumlah_sks_semester = [0, 20, 40, 60, 80, 101, 121, 136, 144]
    if semester > 8:
        semester = 8
    output_lines.append(" ")
    output_lines.append('Kesesuaian jumlah SKS:')
    output_lines.append('(total yang sudah ditempuh / total seharusnya (berdasarkan semester)')
    output_lines.append('Catatan: Perhatikan total SKS wajib yg belum diambil di atas (jika ada)')
    output_lines.append('-----------------------------------------------------------------------')
    output_lines.append(f'{total_sks} / {jumlah_sks_semester[semester-1]}')
    output_lines.append("")
    
    return "\n".join(output_lines)

if __name__ == "__main__":
    # Path ke direktori
    kurikulum_dir = 'kurikulum'
    transkrip_dir = 'transkrip'
    output_dir = 'output'

    # Buat direktori output jika belum ada
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dapatkan daftar semua file kurikulum (asumsi hanya satu)
    kurikulum_files = glob.glob(os.path.join(kurikulum_dir, '*.xlsx'))
    if not kurikulum_files:
        print("[INFO] Tidak ada file kurikulum (.xlsx) yang ditemukan. Keluar.")
        sys.exit()
    
    # Dapatkan daftar semua file transkrip
    transkrip_files = glob.glob(os.path.join(transkrip_dir, '*.html'))
    if not transkrip_files:
        print("[INFO] Tidak ada file transkrip (.html) yang ditemukan. Keluar.")
        sys.exit()

    # Loop melalui setiap file transkrip dan jalankan analisis
    for transkrip_file in transkrip_files:
        # Analisis transkrip dan dapatkan output dalam bentuk string
        analysis_result = analyze_transcript(transkrip_file)
        
        if analysis_result:
            # Tentukan nama file output
            filename_base = os.path.splitext(os.path.basename(transkrip_file))[0]
            output_file_path = os.path.join(output_dir, f'{filename_base}.txt')

            # Tulis hasil analisis ke file
            try:
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(analysis_result)
                print(f"[INFO] Analisis untuk '{os.path.basename(transkrip_file)}' berhasil disimpan di '{output_file_path}'")
                print(' ')
            except Exception as e:
                print(f"[ERROR] Gagal menulis ke file output '{output_file_path}'. Detail: {e}")
