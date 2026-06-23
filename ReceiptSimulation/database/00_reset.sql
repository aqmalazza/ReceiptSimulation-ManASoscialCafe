-- =========================================================
-- 00_reset.sql
-- Menghapus database lama agar setup dapat dimulai dari awal.
-- Gunakan hanya jika ingin reset total.
-- =========================================================

SET FOREIGN_KEY_CHECKS=0;
DROP DATABASE IF EXISTS `mana_social_cafe`;
SET FOREIGN_KEY_CHECKS=1;
