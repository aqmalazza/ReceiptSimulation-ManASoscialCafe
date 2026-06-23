-- =========================================================
-- 02_seed.sql
-- Data awal untuk menjalankan aplikasi.
-- Tidak berisi riwayat transaksi.
-- =========================================================

USE `mana_social_cafe`;

INSERT INTO `cabang`
(`id_cabang`, `nama_cabang`, `alamat_cabang`, `no_telp_cabang`, `instagram_cabang`) VALUES
('CBG001', 'ManA Social Cafe', 'Alamat tidak tercantum pada struk', NULL, '@mana.bandung');

INSERT INTO `meja`
(`id_meja`, `nomor_meja`, `status_meja`, `id_cabang`) VALUES
('MJ001', 6, 'terisi', 'CBG001'),
('MJ002', 1, 'tersedia', 'CBG001'),
('MJ003', 2, 'tersedia', 'CBG001'),
('MJ004', 3, 'tersedia', 'CBG001'),
('MJ005', 4, 'tersedia', 'CBG001'),
('MJ006', 5, 'tersedia', 'CBG001'),
('MJ007', 7, 'tersedia', 'CBG001'),
('MJ008', 8, 'tersedia', 'CBG001'),
('MJ009', 9, 'tersedia', 'CBG001'),
('MJ010', 10, 'tersedia', 'CBG001');

INSERT INTO `pegawai`
(`id_pegawai`, `nama_pegawai`, `jabatan`, `id_cabang`) VALUES
('PGW001', 'Kasir ManA', 'Kasir', 'CBG001');

INSERT INTO `pelanggan`
(`id_pelanggan`, `nama_pelanggan`, `no_telp`, `status_member`) VALUES
('PLG001', 'KASIR *****5388', NULL, 'non-member');

INSERT INTO `menu`
(`id_menu`, `nama_menu`, `kategori_menu`, `harga_menu`, `status_menu`) VALUES
('MNU001', 'Yamien Manis', 'Makanan', 40000.00, 'tersedia'),
('MNU002', 'Mango Midori', 'Minuman', 38000.00, 'tersedia'),
('MNU003', 'Panna Cotta', 'Dessert', 26000.00, 'tersedia'),
('MNU004', 'Es Kopi Susu', 'Minuman', 28000.00, 'tersedia'),
('MNU005', 'Americano', 'Minuman', 25000.00, 'tersedia'),
('MNU006', 'Cappuccino', 'Minuman', 32000.00, 'tersedia'),
('MNU007', 'Cafe Latte', 'Minuman', 33000.00, 'tersedia'),
('MNU008', 'Matcha Latte', 'Minuman', 35000.00, 'tidak tersedia'),
('MNU009', 'Croissant', 'Snack', 22000.00, 'tersedia'),
('MNU010', 'French Fries', 'Snack', 24000.00, 'tersedia'),
('MNU011', 'Chicken Wings', 'Makanan', 42000.00, 'tersedia'),
('MNU012', 'Nasi Goreng Spesial', 'Makanan', 38000.00, 'tersedia'),
('MNU013', 'Spaghetti Carbonara', 'Makanan', 45000.00, 'tidak tersedia'),
('MNU014', 'Cheesecake', 'Dessert', 30000.00, 'tersedia'),
('MNU015', 'Chocolate Lava Cake', 'Dessert', 34000.00, 'tidak tersedia');
