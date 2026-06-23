# ManA Social Cafe - Tkinter + MySQL

Demo sederhana untuk tugas Basis Data. Aplikasi ini mengambil data master dari MySQL, menyimpan transaksi, dan menampilkan struk berdasarkan relasi tabel.

## Menjalankan Aplikasi

```bash
pip install -r requirements.txt
python app.py
```

Pastikan MySQL/Laragon aktif dan database `mana_social_cafe` sudah berisi tabel yang dibuat pada tugas.

## Struktur Kode

```text
app.py              Entry point aplikasi
config.py           Konfigurasi database dan data statis struk
database.py         Helper koneksi dan eksekusi query MySQL
formatters.py       Format angka, rupiah, dan label dropdown
repositories.py     Query data master dan transaksi
receipt.py          Penyusun format struk
ui/main_window.py   Layout dan event UI Tkinter
ui/widgets.py       Widget reusable
```

## Catatan

- Nama pelanggan boleh dikosongkan. Jika kosong, transaksi memakai pelanggan default `PLG001`.
- WiFi, password, dan Instagram ditulis langsung di `config.py`, bukan disimpan di database.
- Menu dengan status `tidak tersedia` tetap tampil, tetapi tidak bisa ditambahkan ke keranjang.
- Tab **Cari Struk Lama** dipakai untuk menampilkan ulang struk transaksi yang sudah tersimpan.
