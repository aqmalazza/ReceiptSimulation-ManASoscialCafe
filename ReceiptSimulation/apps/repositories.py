from __future__ import annotations

from datetime import datetime
from decimal import Decimal
import random
import string

from config import DEFAULT_CUSTOMER_ID, DEFAULT_CUSTOMER_NAME, DEFAULT_MEMBER_STATUS, EXTRA_FEE_NAME


class MasterRepository:
    def __init__(self, db):
        self.db = db

    def load_all(self) -> dict[str, list[dict]]:
        return {
            "cabang": self.db.fetch_all("SELECT * FROM cabang ORDER BY id_cabang"),
            "meja": self.db.fetch_all("SELECT * FROM meja ORDER BY nomor_meja"),
            "pegawai": self.db.fetch_all("SELECT * FROM pegawai ORDER BY id_pegawai"),
            "menu": self.db.fetch_all(
                """
                SELECT * FROM menu
                ORDER BY CASE WHEN status_menu = 'tersedia' THEN 0 ELSE 1 END, id_menu
                """
            ),
        }


class TransactionRepository:
    def __init__(self, db):
        self.db = db

    def next_id(self, table: str, id_column: str, prefix: str, width: int = 3) -> str:
        start = len(prefix) + 1
        row = self.db.fetch_one(
            f"""
            SELECT {id_column} AS last_id
            FROM {table}
            WHERE {id_column} LIKE %s
            ORDER BY CAST(SUBSTRING({id_column}, {start}) AS UNSIGNED) DESC
            LIMIT 1
            """,
            (f"{prefix}%",),
        )
        if not row or not row.get("last_id"):
            return f"{prefix}{1:0{width}d}"
        digits = "".join(ch for ch in str(row["last_id"]) if ch.isdigit())
        return f"{prefix}{int(digits or 0) + 1:0{width}d}"

    def generate_order_number(self) -> str:
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        suffix = "".join(random.choices(string.digits, k=4))
        return f"ORD{stamp}{suffix}"

    def ensure_default_customer(self):
        row = self.db.fetch_one("SELECT id_pelanggan FROM pelanggan WHERE id_pelanggan = %s", (DEFAULT_CUSTOMER_ID,))
        if row:
            return
        self.db.execute_transaction([
            (
                """
                INSERT INTO pelanggan (id_pelanggan, nama_pelanggan, no_telp, status_member)
                VALUES (%s, %s, NULL, %s)
                """,
                (DEFAULT_CUSTOMER_ID, DEFAULT_CUSTOMER_NAME, DEFAULT_MEMBER_STATUS),
            )
        ])

    def resolve_customer(self, nama_pelanggan: str, no_telp: str | None) -> str:
        nama = (nama_pelanggan or "").strip()
        telp = (no_telp or "").strip() or None
        if not nama:
            self.ensure_default_customer()
            return DEFAULT_CUSTOMER_ID

        existing = self.db.fetch_one(
            """
            SELECT id_pelanggan
            FROM pelanggan
            WHERE LOWER(nama_pelanggan) = LOWER(%s)
              AND (no_telp <=> %s)
            LIMIT 1
            """,
            (nama, telp),
        )
        if existing:
            return existing["id_pelanggan"]

        id_pelanggan = self.next_id("pelanggan", "id_pelanggan", "PLG")
        self.db.execute_transaction([
            (
                """
                INSERT INTO pelanggan (id_pelanggan, nama_pelanggan, no_telp, status_member)
                VALUES (%s, %s, %s, %s)
                """,
                (id_pelanggan, nama, telp, DEFAULT_MEMBER_STATUS),
            )
        ])
        return id_pelanggan

    def create_transaction(
        self,
        *,
        id_cabang: str,
        id_meja: str,
        id_pegawai: str,
        nama_pelanggan: str,
        no_telp: str,
        cart: list[dict],
        biaya: Decimal,
        metode_pembayaran: str,
        nominal_bayar: Decimal,
    ) -> str:
        id_pelanggan = self.resolve_customer(nama_pelanggan, no_telp)
        subtotal = sum((item["subtotal_item"] for item in cart), Decimal("0"))
        total_bayar = subtotal + biaya
        kembalian = nominal_bayar - total_bayar
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id_transaksi = self.next_id("transaksi", "id_transaksi", "TRX")

        statements: list[tuple[str, tuple]] = [
            (
                """
                INSERT INTO transaksi (
                    id_transaksi, no_pesanan, jenis_transaksi, tanggal_waktu,
                    subtotal, total_biaya_tambahan, total_bayar,
                    id_cabang, id_meja, id_pegawai, id_pelanggan
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    id_transaksi,
                    self.generate_order_number(),
                    "Makan ditempat",
                    now,
                    subtotal,
                    biaya,
                    total_bayar,
                    id_cabang,
                    id_meja,
                    id_pegawai,
                    id_pelanggan,
                ),
            )
        ]

        for item in cart:
            statements.append(
                (
                    """
                    INSERT INTO detail_transaksi (
                        id_transaksi, id_menu, qty, harga_satuan, subtotal_item, catatan_item
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        id_transaksi,
                        item["id_menu"],
                        item["qty"],
                        item["harga_satuan"],
                        item["subtotal_item"],
                        item.get("catatan_item"),
                    ),
                )
            )

        if biaya > 0:
            statements.append(
                (
                    """
                    INSERT INTO biaya_tambahan (id_biaya, id_transaksi, nama_biaya, nominal_biaya)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (self.next_id("biaya_tambahan", "id_biaya", "BY"), id_transaksi, EXTRA_FEE_NAME, biaya),
                )
            )

        statements.append(
            (
                """
                INSERT INTO pembayaran (
                    id_pembayaran, id_transaksi, metode_pembayaran,
                    status_pembayaran, nominal_bayar, kembalian, tanggal_pembayaran
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    self.next_id("pembayaran", "id_pembayaran", "BYR"),
                    id_transaksi,
                    metode_pembayaran,
                    "Lunas",
                    nominal_bayar,
                    kembalian,
                    now,
                ),
            )
        )

        self.db.execute_transaction(statements)
        return id_transaksi

    def get_receipt_data(self, id_transaksi: str) -> tuple[dict | None, list[dict], list[dict]]:
        header = self.db.fetch_one(
            """
            SELECT
                t.id_transaksi, t.no_pesanan, t.jenis_transaksi, t.tanggal_waktu,
                t.subtotal, t.total_biaya_tambahan, t.total_bayar,
                c.nama_cabang, m.nomor_meja, pg.nama_pegawai,
                pl.nama_pelanggan, pl.no_telp,
                pb.metode_pembayaran, pb.status_pembayaran, pb.nominal_bayar, pb.kembalian
            FROM transaksi t
            JOIN cabang c ON t.id_cabang = c.id_cabang
            LEFT JOIN meja m ON t.id_meja = m.id_meja
            JOIN pegawai pg ON t.id_pegawai = pg.id_pegawai
            LEFT JOIN pelanggan pl ON t.id_pelanggan = pl.id_pelanggan
            JOIN pembayaran pb ON t.id_transaksi = pb.id_transaksi
            WHERE t.id_transaksi = %s
            """,
            (id_transaksi,),
        )
        items = self.db.fetch_all(
            """
            SELECT mn.nama_menu, dt.qty, dt.harga_satuan, dt.subtotal_item, dt.catatan_item
            FROM detail_transaksi dt
            JOIN menu mn ON dt.id_menu = mn.id_menu
            WHERE dt.id_transaksi = %s
            ORDER BY dt.id_menu
            """,
            (id_transaksi,),
        )
        biaya_rows = self.db.fetch_all(
            """
            SELECT nama_biaya, nominal_biaya
            FROM biaya_tambahan
            WHERE id_transaksi = %s
            ORDER BY id_biaya
            """,
            (id_transaksi,),
        )
        return header, items, biaya_rows

    def search_transactions(self, keyword: str = "") -> list[dict]:
        key = f"%{(keyword or '').strip()}%"
        return self.db.fetch_all(
            """
            SELECT
                t.id_transaksi, t.no_pesanan, t.tanggal_waktu,
                COALESCE(m.nomor_meja, '-') AS nomor_meja,
                COALESCE(pl.nama_pelanggan, 'Pelanggan Umum') AS nama_pelanggan,
                t.total_bayar
            FROM transaksi t
            LEFT JOIN meja m ON t.id_meja = m.id_meja
            LEFT JOIN pelanggan pl ON t.id_pelanggan = pl.id_pelanggan
            WHERE %s = '%%'
               OR t.id_transaksi LIKE %s
               OR t.no_pesanan LIKE %s
               OR pl.nama_pelanggan LIKE %s
               OR CAST(m.nomor_meja AS CHAR) LIKE %s
            ORDER BY t.tanggal_waktu DESC
            LIMIT 100
            """,
            (key, key, key, key, key),
        )
