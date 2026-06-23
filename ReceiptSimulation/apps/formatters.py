from decimal import Decimal, InvalidOperation


def money(value) -> str:
    number = Decimal(value or 0)
    return f"{number:,.0f}".replace(",", ".")


def rupiah(value) -> str:
    return f"Rp{money(value)}"


def safe_decimal(value: str) -> Decimal:
    clean = str(value or "").replace("Rp", "").replace(".", "").replace(",", "").strip()
    if not clean:
        return Decimal("0")
    try:
        return Decimal(clean)
    except InvalidOperation as exc:
        raise ValueError("Input angka tidak valid") from exc


def extract_id(display_value: str) -> str:
    return display_value.split(" - ")[0].strip()


def display_cabang(row: dict) -> str:
    return f"{row['id_cabang']} - {row['nama_cabang']}"


def display_meja(row: dict) -> str:
    return f"{row['id_meja']} - Meja {row['nomor_meja']}"


def display_pegawai(row: dict) -> str:
    return f"{row['id_pegawai']} - {row['nama_pegawai']}"


def display_menu(row: dict) -> str:
    label = f"{row['id_menu']} - {row['nama_menu']} - {rupiah(row['harga_menu'])}"
    if str(row.get("status_menu", "")).lower() != "tersedia":
        label += " [Tidak Tersedia]"
    return label
