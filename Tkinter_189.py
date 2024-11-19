# Mengimpor modul sqlite3 untuk bekerja dengan database SQLite
import sqlite3
# Mengimpor modul tkinter untuk membuat GUI
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    # Membuka atau membuat database bernama 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Membuat tabel jika belum ada, dengan kolom-kolom sesuai kebutuhan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()   # Menutup koneksi

# Fungsi untuk mengambil semua data dari tabel nilai_siswa
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Query untuk mengambil semua data
    rows = cursor.fetchall()  # Mengambil hasil query
    conn.close()
    return rows  # Mengembalikan data dalam bentuk list of tuples

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Query untuk menyisipkan data baru ke tabel
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data di database berdasarkan ID
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Query untuk memperbarui data yang sudah ada
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data dari database berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Query untuk menghapus data
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    # Logika untuk menentukan fakultas berdasarkan nilai tertinggi
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Fungsi untuk menyimpan data dari form ke database
def submit():
    try:
        # Mengambil nilai dari form input
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Validasi jika nama kosong
        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        # Menghitung prediksi fakultas
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Menyimpan data ke database
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Membersihkan input form
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        # Menampilkan pesan error jika input tidak valid
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data di database
def update():
    try:
        # Validasi jika tidak ada data yang dipilih dari tabel
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        # Mengambil data dari form input dan ID data yang dipilih
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Validasi jika nama kosong
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        # Menghitung prediksi fakultas
        prediksi = calculate_prediction(biologi, fisika, inggris)
        # Memperbarui data di database
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()  # Membersihkan input form
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        # Menampilkan pesan error jika input tidak valid
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data dari database
def delete():
    try:
        # Validasi jika tidak ada data yang dipilih dari tabel
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        # Mengambil ID data yang dipilih
        record_id = int(selected_record_id.get())
        # Menghapus data dari database
        delete_database(record_id)
        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()  # Membersihkan input form
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        # Menampilkan pesan error jika terjadi kesalahan
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk membersihkan input form
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk memperbarui isi tabel dengan data dari database
def populate_table():
    # Menghapus semua data di tabel tkinter
    for row in tree.get_children():
        tree.delete(row)
    # Menambahkan data dari database ke tabel
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi form input berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        # Mendapatkan item yang dipilih dari tabel
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        # Mengisi form input dengan data yang dipilih
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        # Menampilkan pesan error jika tidak ada data yang valid dipilih
        messagebox.showerror("Error", "Pilih data yang valid!")
# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter untuk form input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Membuat label dan input untuk nama siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

# Membuat label dan input untuk nilai Biologi
Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

# Membuat label dan input untuk nilai Fisika
Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

# Membuat label dan input untuk nilai Inggris
Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol untuk menyimpan, memperbarui, dan menghapus data
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Mengikat event klik pada tabel untuk mengisi form input
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Memuat data awal ke tabel
populate_table()
# Menjalankan loop utama GUI
root.mainloop()