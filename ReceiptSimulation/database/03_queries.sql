-- =========================================================
-- 03_queries.sql
-- Query pengecekan database dan relasi.
-- File ini tidak wajib dijalankan untuk setup aplikasi.
-- =========================================================

USE `mana_social_cafe`;

-- Cek jumlah data setiap tabel
SELECT 'cabang' AS tabel, COUNT(*) AS jumlah_data FROM cabang
UNION ALL
SELECT 'meja', COUNT(*) FROM meja
UNION ALL
SELECT 'pegawai', COUNT(*) FROM pegawai
UNION ALL
SELECT 'pelanggan', COUNT(*) FROM pelanggan
UNION ALL
SELECT 'menu', COUNT(*) FROM menu
UNION ALL
SELECT 'transaksi', COUNT(*) FROM transaksi
UNION ALL
SELECT 'detail_transaksi', COUNT(*) FROM detail_transaksi
UNION ALL
SELECT 'biaya_tambahan', COUNT(*) FROM biaya_tambahan
UNION ALL
SELECT 'pembayaran', COUNT(*) FROM pembayaran;

-- Cek foreign key / relasi
SELECT
    TABLE_NAME AS tabel,
    COLUMN_NAME AS kolom_fk,
    REFERENCED_TABLE_NAME AS tabel_referensi,
    REFERENCED_COLUMN_NAME AS kolom_referensi
FROM information_schema.KEY_COLUMN_USAGE
WHERE
    TABLE_SCHEMA = 'mana_social_cafe'
    AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME, COLUMN_NAME;

-- Query pencarian struk lama
SELECT
    t.id_transaksi,
    t.no_pesanan,
    t.tanggal_waktu,
    m.nomor_meja,
    p.nama_pelanggan,
    t.total_bayar
FROM transaksi t
LEFT JOIN meja m ON t.id_meja = m.id_meja
LEFT JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
ORDER BY t.tanggal_waktu DESC;
