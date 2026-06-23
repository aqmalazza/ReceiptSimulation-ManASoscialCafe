from config import RECEIPT_STATIC_INFO, RECEIPT_WIDTH
from formatters import money


def center(text: str) -> str:
    return text.center(RECEIPT_WIDTH)


def line(char: str = "=") -> str:
    return char * RECEIPT_WIDTH


def amount_line(label: str, amount) -> str:
    return f"{label:<26}{money(amount):>16}"[:RECEIPT_WIDTH]


def item_line(qty, name: str, amount) -> str:
    left = f"{qty:<2} {name[:24]:<24}"
    return f"{left}{money(amount):>14}"[:RECEIPT_WIDTH]


def build_receipt(header: dict, items: list[dict], biaya_rows: list[dict]) -> str:
    total_qty = sum(int(item["qty"] or 0) for item in items)
    meja = header.get("nomor_meja") or "-"
    tanggal = header["tanggal_waktu"].strftime("%d-%m-%Y %H:%M")
    metode_status = f"{header['metode_pembayaran']} {header['status_pembayaran']}".upper()
    telepon = header.get("no_telp") or "-"

    lines = [
        line(),
        center(header["nama_cabang"]),
        center(f"{header['jenis_transaksi'].upper()} - MEJA {meja}"),
        center(tanggal),
        line(),
        f"Pesanan  : {header['no_pesanan']}",
        f"Pelayan  : {header['nama_pegawai']}",
        f"Pelanggan: {header.get('nama_pelanggan') or 'Pelanggan Umum'}",
        f"Telepon  : {telepon}",
        line("-"),
    ]

    for item in items:
        lines.append(item_line(item["qty"], item["nama_menu"], item["subtotal_item"]))
        if item.get("catatan_item"):
            lines.append(f"   *{item['catatan_item']:<27}{'0':>10}"[:RECEIPT_WIDTH])

    lines.append(line("-"))
    lines.append(amount_line("Subtotal", header["subtotal"]))
    for biaya in biaya_rows:
        lines.append(amount_line(biaya["nama_biaya"], biaya["nominal_biaya"]))
    lines.append(line("-"))
    lines.append(amount_line(f"TOTAL ({total_qty} ITEM)", header["total_bayar"]))
    lines.append(amount_line(metode_status, header["nominal_bayar"]))
    if header.get("kembalian"):
        lines.append(amount_line("Kembalian", header["kembalian"]))
    lines.append(line("-"))
    lines.append(f"Wifi     : {RECEIPT_STATIC_INFO['wifi_name']}")
    lines.append(f"Password : {RECEIPT_STATIC_INFO['wifi_password']}")
    lines.append(center("Follow our IG:"))
    for account in RECEIPT_STATIC_INFO["instagram_accounts"]:
        lines.append(center(account))
    lines.append(line())
    return "\n".join(lines)
