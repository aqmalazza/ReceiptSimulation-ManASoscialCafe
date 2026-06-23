-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 23, 2026 at 02:01 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.30

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mana_social_cafe`
--
CREATE DATABASE IF NOT EXISTS `mana_social_cafe` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `mana_social_cafe`;

-- --------------------------------------------------------

--
-- Table structure for table `biaya_tambahan`
--

DROP TABLE IF EXISTS `biaya_tambahan`;
CREATE TABLE `biaya_tambahan` (
  `id_biaya` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_transaksi` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_biaya` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nominal_biaya` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cabang`
--

DROP TABLE IF EXISTS `cabang`;
CREATE TABLE `cabang` (
  `id_cabang` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_cabang` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alamat_cabang` text COLLATE utf8mb4_unicode_ci,
  `no_telp_cabang` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `instagram_cabang` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cabang`
--

INSERT INTO `cabang` (`id_cabang`, `nama_cabang`, `alamat_cabang`, `no_telp_cabang`, `instagram_cabang`) VALUES
('CBG001', 'ManA Social Cafe', 'Alamat tidak tercantum pada struk', NULL, '@mana.bandung');

-- --------------------------------------------------------

--
-- Table structure for table `detail_transaksi`
--

DROP TABLE IF EXISTS `detail_transaksi`;
CREATE TABLE `detail_transaksi` (
  `id_transaksi` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_menu` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `qty` int NOT NULL,
  `harga_satuan` decimal(12,2) NOT NULL,
  `subtotal_item` decimal(12,2) NOT NULL,
  `catatan_item` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `meja`
--

DROP TABLE IF EXISTS `meja`;
CREATE TABLE `meja` (
  `id_meja` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nomor_meja` int NOT NULL,
  `status_meja` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT 'tersedia',
  `id_cabang` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `meja`
--

INSERT INTO `meja` (`id_meja`, `nomor_meja`, `status_meja`, `id_cabang`) VALUES
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

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu` (
  `id_menu` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_menu` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `kategori_menu` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `harga_menu` decimal(12,2) NOT NULL,
  `status_menu` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT 'tersedia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`id_menu`, `nama_menu`, `kategori_menu`, `harga_menu`, `status_menu`) VALUES
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

-- --------------------------------------------------------

--
-- Table structure for table `pegawai`
--

DROP TABLE IF EXISTS `pegawai`;
CREATE TABLE `pegawai` (
  `id_pegawai` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_pegawai` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `jabatan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_cabang` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pegawai`
--

INSERT INTO `pegawai` (`id_pegawai`, `nama_pegawai`, `jabatan`, `id_cabang`) VALUES
('PGW001', 'Kasir ManA', 'Kasir', 'CBG001');

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

DROP TABLE IF EXISTS `pelanggan`;
CREATE TABLE `pelanggan` (
  `id_pelanggan` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_pelanggan` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `no_telp` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status_member` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT 'non-member'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`id_pelanggan`, `nama_pelanggan`, `no_telp`, `status_member`) VALUES
('PLG001', 'KASIR *****5388', NULL, 'non-member');

-- --------------------------------------------------------

--
-- Table structure for table `pembayaran`
--

DROP TABLE IF EXISTS `pembayaran`;
CREATE TABLE `pembayaran` (
  `id_pembayaran` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_transaksi` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `metode_pembayaran` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status_pembayaran` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nominal_bayar` decimal(12,2) NOT NULL,
  `kembalian` decimal(12,2) NOT NULL DEFAULT '0.00',
  `tanggal_pembayaran` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

DROP TABLE IF EXISTS `transaksi`;
CREATE TABLE `transaksi` (
  `id_transaksi` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `no_pesanan` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `jenis_transaksi` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tanggal_waktu` datetime NOT NULL,
  `subtotal` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total_biaya_tambahan` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total_bayar` decimal(12,2) NOT NULL DEFAULT '0.00',
  `id_cabang` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_meja` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_pegawai` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_pelanggan` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `biaya_tambahan`
--
ALTER TABLE `biaya_tambahan`
  ADD PRIMARY KEY (`id_biaya`),
  ADD KEY `fk_biaya_transaksi` (`id_transaksi`);

--
-- Indexes for table `cabang`
--
ALTER TABLE `cabang`
  ADD PRIMARY KEY (`id_cabang`);

--
-- Indexes for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD PRIMARY KEY (`id_transaksi`,`id_menu`),
  ADD KEY `fk_detail_menu` (`id_menu`);

--
-- Indexes for table `meja`
--
ALTER TABLE `meja`
  ADD PRIMARY KEY (`id_meja`),
  ADD KEY `fk_meja_cabang` (`id_cabang`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id_menu`);

--
-- Indexes for table `pegawai`
--
ALTER TABLE `pegawai`
  ADD PRIMARY KEY (`id_pegawai`),
  ADD KEY `fk_pegawai_cabang` (`id_cabang`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id_pelanggan`);

--
-- Indexes for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD PRIMARY KEY (`id_pembayaran`),
  ADD UNIQUE KEY `id_transaksi` (`id_transaksi`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD UNIQUE KEY `no_pesanan` (`no_pesanan`),
  ADD KEY `fk_transaksi_cabang` (`id_cabang`),
  ADD KEY `fk_transaksi_meja` (`id_meja`),
  ADD KEY `fk_transaksi_pegawai` (`id_pegawai`),
  ADD KEY `fk_transaksi_pelanggan` (`id_pelanggan`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `biaya_tambahan`
--
ALTER TABLE `biaya_tambahan`
  ADD CONSTRAINT `fk_biaya_transaksi` FOREIGN KEY (`id_transaksi`) REFERENCES `transaksi` (`id_transaksi`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD CONSTRAINT `fk_detail_menu` FOREIGN KEY (`id_menu`) REFERENCES `menu` (`id_menu`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_detail_transaksi` FOREIGN KEY (`id_transaksi`) REFERENCES `transaksi` (`id_transaksi`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `meja`
--
ALTER TABLE `meja`
  ADD CONSTRAINT `fk_meja_cabang` FOREIGN KEY (`id_cabang`) REFERENCES `cabang` (`id_cabang`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Constraints for table `pegawai`
--
ALTER TABLE `pegawai`
  ADD CONSTRAINT `fk_pegawai_cabang` FOREIGN KEY (`id_cabang`) REFERENCES `cabang` (`id_cabang`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Constraints for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD CONSTRAINT `fk_pembayaran_transaksi` FOREIGN KEY (`id_transaksi`) REFERENCES `transaksi` (`id_transaksi`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `fk_transaksi_cabang` FOREIGN KEY (`id_cabang`) REFERENCES `cabang` (`id_cabang`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_transaksi_meja` FOREIGN KEY (`id_meja`) REFERENCES `meja` (`id_meja`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_transaksi_pegawai` FOREIGN KEY (`id_pegawai`) REFERENCES `pegawai` (`id_pegawai`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_transaksi_pelanggan` FOREIGN KEY (`id_pelanggan`) REFERENCES `pelanggan` (`id_pelanggan`) ON DELETE SET NULL ON UPDATE CASCADE;
SET FOREIGN_KEY_CHECKS=1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
