# Database ManA Social Cafe

Folder ini berisi file SQL yang sudah dipisahkan dari hasil export phpMyAdmin.

## Isi File

| File | Fungsi |
|---|---|
| `00_reset.sql` | Menghapus database lama. Jalankan hanya jika ingin mulai dari awal. |
| `01_schema.sql` | Membuat database, tabel, primary key, unique key, foreign key, dan relasi. |
| `02_seed.sql` | Mengisi data awal: cabang, meja, pegawai, pelanggan default, dan menu. |
| `03_queries.sql` | Query untuk mengecek jumlah data, relasi foreign key, dan pencarian struk lama. |
| `99_full_setup.sql` | Gabungan reset, schema, dan seed dalam satu file. |
| `mana_social_cafe.sql` | File hasil export dari phpMyAdmin. |

## Urutan Import Manual

Jika ingin menjalankan satu per satu di phpMyAdmin:

1. Import `00_reset.sql` jika ingin menghapus database lama.
2. Import `01_schema.sql`.
3. Import `02_seed.sql`.
4. Jalankan `03_queries.sql` jika ingin mengecek hasil.

## Cara Cepat

Jika ingin langsung membuat ulang database dari awal, import:

```sql
99_full_setup.sql
```

File ini akan menghapus database lama, membuat struktur baru, lalu mengisi data awal.

## Catatan

Data transaksi tidak dimasukkan karena pada export terakhir tabel transaksi, detail_transaksi, biaya_tambahan, dan pembayaran sudah dikosongkan.
