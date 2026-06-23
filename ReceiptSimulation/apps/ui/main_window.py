from __future__ import annotations

from decimal import Decimal
import tkinter as tk
from tkinter import ttk, messagebox

from config import APP_TITLE, DB_CONFIG, DEFAULT_SERVICE_CHARGE, PAYMENT_METHODS
from database import Database
from formatters import display_cabang, display_meja, display_menu, display_pegawai, extract_id, money, rupiah, safe_decimal
from receipt import build_receipt
from repositories import MasterRepository, TransactionRepository
from ui.widgets import ScrollableFrame


class StrukApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1280x760")
        self.minsize(1040, 640)

        self.db = Database(DB_CONFIG)
        self.master_repo = MasterRepository(self.db)
        self.transaction_repo = TransactionRepository(self.db)
        self.master_data = {"cabang": [], "meja": [], "pegawai": [], "menu": []}
        self.cart: list[dict] = []

        self._setup_style()
        self._build_layout()
        self._load_master_data()
        self._search_transactions()
        self._refresh_totals()

    def _setup_style(self):
        self.configure(bg="#F6F7FB")
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background="#F6F7FB")
        style.configure("Card.TFrame", background="#FFFFFF")
        style.configure("Title.TLabel", background="#F6F7FB", foreground="#111827", font=("Segoe UI", 20, "bold"))
        style.configure("Section.TLabel", background="#FFFFFF", foreground="#111827", font=("Segoe UI", 10, "bold"))
        style.configure("Field.TLabel", background="#FFFFFF", foreground="#374151", font=("Segoe UI", 9))
        style.configure("Value.TLabel", background="#FFFFFF", foreground="#111827", font=("Segoe UI", 12, "bold"))
        style.configure("Danger.TLabel", background="#FFFFFF", foreground="#DC2626", font=("Segoe UI", 9, "bold"))
        style.configure("Success.TLabel", background="#FFFFFF", foreground="#15803D", font=("Segoe UI", 9, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"), padding=(12, 7))
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 9), background="#FFFFFF", fieldbackground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _build_layout(self):
        root = ttk.Frame(self, style="App.TFrame", padding=14)
        root.pack(fill=tk.BOTH, expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        header = ttk.Frame(root, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text="ManA Social Cafe", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(header, text="Refresh Data", command=self._load_master_data).grid(row=0, column=1, sticky="e")

        pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        pane.grid(row=1, column=0, sticky="nsew")

        left = ttk.Frame(pane, style="App.TFrame")
        right = ttk.Frame(pane, style="App.TFrame")
        pane.add(left, weight=3)
        pane.add(right, weight=2)

        self.notebook = ttk.Notebook(left)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        input_tab = ttk.Frame(self.notebook, style="App.TFrame")
        history_tab = ttk.Frame(self.notebook, style="App.TFrame")
        self.notebook.add(input_tab, text="Input Transaksi")
        self.notebook.add(history_tab, text="Cari Struk Lama")

        scroll = ScrollableFrame(input_tab)
        scroll.pack(fill=tk.BOTH, expand=True)
        self._build_transaction_form(scroll.inner)
        self._build_cart_table(scroll.inner)
        self._build_payment_form(scroll.inner)
        self._build_history_tab(history_tab)
        self._build_receipt_panel(right)

    def _card(self, parent, title: str):
        outer = ttk.Frame(parent, style="Card.TFrame", padding=14)
        outer.pack(fill=tk.X, pady=(0, 10), padx=1)
        outer.columnconfigure(0, weight=1)
        ttk.Label(outer, text=title, style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))
        body = ttk.Frame(outer, style="Card.TFrame")
        body.grid(row=1, column=0, sticky="ew")
        return body

    def _build_transaction_form(self, parent):
        frame = self._card(parent, "Data Transaksi")
        for col in (1, 3):
            frame.columnconfigure(col, weight=1)

        self.cabang_var = tk.StringVar()
        self.meja_var = tk.StringVar()
        self.pegawai_var = tk.StringVar()
        self.menu_var = tk.StringVar()
        self.qty_var = tk.IntVar(value=1)
        self.nama_pelanggan_var = tk.StringVar()
        self.no_telp_var = tk.StringVar()
        self.catatan_var = tk.StringVar()

        self._label(frame, "Cabang", 0, 0)
        self.cabang_cb = self._combo(frame, self.cabang_var, 0, 1)
        self._label(frame, "Meja", 0, 2)
        self.meja_cb = self._combo(frame, self.meja_var, 0, 3)

        self._label(frame, "Pegawai/Kasir", 1, 0)
        self.pegawai_cb = self._combo(frame, self.pegawai_var, 1, 1)
        self._label(frame, "Nama Pelanggan", 1, 2)
        self.nama_pelanggan_entry = self._entry(frame, self.nama_pelanggan_var, 1, 3)

        self._label(frame, "Telepon", 2, 0)
        self.no_telp_entry = self._entry(frame, self.no_telp_var, 2, 1)
        self._label(frame, "Menu", 2, 2)
        self.menu_cb = self._combo(frame, self.menu_var, 2, 3)

        self._label(frame, "Qty", 3, 0)
        self.qty_spin = ttk.Spinbox(frame, from_=1, to=99, textvariable=self.qty_var, width=8)
        self.qty_spin.grid(row=3, column=1, sticky="w", padx=6, pady=6)
        self._label(frame, "Catatan Item", 3, 2)
        self.catatan_entry = self._entry(frame, self.catatan_var, 3, 3)

        ttk.Button(frame, text="Tambah ke Keranjang", style="Accent.TButton", command=self._add_to_cart).grid(
            row=4, column=0, columnspan=4, sticky="ew", padx=6, pady=(10, 0)
        )

    def _build_cart_table(self, parent):
        frame = self._card(parent, "Keranjang Pesanan")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        columns = ("id_menu", "nama_menu", "qty", "harga", "subtotal", "catatan")
        self.cart_tree = ttk.Treeview(frame, columns=columns, show="headings", height=7)
        settings = {
            "id_menu": ("ID Menu", 80, "w"),
            "nama_menu": ("Nama Menu", 190, "w"),
            "qty": ("Qty", 60, "center"),
            "harga": ("Harga", 105, "e"),
            "subtotal": ("Subtotal", 115, "e"),
            "catatan": ("Catatan", 160, "w"),
        }
        for col, (title, width, anchor) in settings.items():
            self.cart_tree.heading(col, text=title)
            self.cart_tree.column(col, width=width, anchor=anchor, stretch=True)
        self.cart_tree.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.cart_tree.configure(yscrollcommand=scroll.set)

        actions = ttk.Frame(frame, style="Card.TFrame")
        actions.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(actions, text="Hapus Item Terpilih", command=self._remove_selected_item).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(actions, text="Kosongkan Keranjang", command=self._clear_cart).pack(side=tk.LEFT)

    def _build_payment_form(self, parent):
        frame = self._card(parent, "Pembayaran")
        for col in range(4):
            frame.columnconfigure(col, weight=1)

        self.biaya_var = tk.StringVar(value=DEFAULT_SERVICE_CHARGE)
        self.nominal_var = tk.StringVar(value="0")
        self.metode_var = tk.StringVar(value=PAYMENT_METHODS[0])

        self._label(frame, "Biaya Tambahan", 0, 0)
        self.biaya_entry = self._entry(frame, self.biaya_var, 0, 1)
        self.biaya_entry.bind("<KeyRelease>", lambda _event: self._refresh_totals())

        self._label(frame, "Metode Bayar", 0, 2)
        self.metode_cb = ttk.Combobox(frame, textvariable=self.metode_var, values=PAYMENT_METHODS, state="readonly")
        self.metode_cb.grid(row=0, column=3, sticky="ew", padx=6, pady=6)

        self._label(frame, "Nominal Bayar", 1, 0)
        self.nominal_entry = self._entry(frame, self.nominal_var, 1, 1)
        self.nominal_entry.bind("<KeyRelease>", lambda _event: self._refresh_totals())

        summary = ttk.Frame(frame, style="Card.TFrame")
        summary.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        for col in range(5):
            summary.columnconfigure(col, weight=1)

        self.summary_vars = {}
        for index, label in enumerate(["Subtotal", "Biaya", "Total Bayar", "Nominal", "Kembalian"]):
            box = ttk.Frame(summary, style="Card.TFrame", padding=8)
            box.grid(row=0, column=index, sticky="ew", padx=3)
            ttk.Label(box, text=label, style="Field.TLabel").pack(anchor="w")
            var = tk.StringVar(value="Rp0")
            self.summary_vars[label] = var
            ttk.Label(box, textvariable=var, style="Value.TLabel").pack(anchor="w")

        self.payment_status = ttk.Label(frame, text="", style="Success.TLabel")
        self.payment_status.grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 0))

        actions = ttk.Frame(frame, style="Card.TFrame")
        actions.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(12, 0))
        self.save_btn = ttk.Button(actions, text="Simpan Transaksi & Cetak Struk", style="Accent.TButton", command=self._save_transaction)
        self.save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ttk.Button(actions, text="Bersihkan Form", command=self._clear_form).pack(side=tk.LEFT)

    def _build_history_tab(self, parent):
        wrapper = ttk.Frame(parent, style="App.TFrame", padding=12)
        wrapper.pack(fill=tk.BOTH, expand=True)
        wrapper.columnconfigure(0, weight=1)
        wrapper.rowconfigure(1, weight=1)

        search = ttk.Frame(wrapper, style="App.TFrame")
        search.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search.columnconfigure(0, weight=1)
        self.search_var = tk.StringVar()
        entry = ttk.Entry(search, textvariable=self.search_var)
        entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        entry.bind("<Return>", lambda _event: self._search_transactions())
        ttk.Button(search, text="Cari", command=self._search_transactions).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(search, text="Tampilkan Struk Terpilih", command=self._show_selected_history_receipt).grid(row=0, column=2)

        columns = ("id", "order", "tanggal", "meja", "pelanggan", "total")
        self.history_tree = ttk.Treeview(wrapper, columns=columns, show="headings")
        settings = {
            "id": ("ID", 90),
            "order": ("No Pesanan", 180),
            "tanggal": ("Tanggal", 135),
            "meja": ("Meja", 60),
            "pelanggan": ("Pelanggan", 150),
            "total": ("Total", 100),
        }
        for col, (title, width) in settings.items():
            self.history_tree.heading(col, text=title)
            self.history_tree.column(col, width=width, anchor="w", stretch=True)
        self.history_tree.grid(row=1, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(wrapper, orient=tk.VERTICAL, command=self.history_tree.yview)
        scroll.grid(row=1, column=1, sticky="ns")
        self.history_tree.configure(yscrollcommand=scroll.set)

    def _build_receipt_panel(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)
        ttk.Label(parent, text="Output Struk", style="Field.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.receipt_text = tk.Text(
            parent,
            font=("Consolas", 10),
            wrap=tk.NONE,
            bg="#FFFFFF",
            fg="#111827",
            insertbackground="#111827",
            relief=tk.FLAT,
            borderwidth=1,
        )
        self.receipt_text.grid(row=1, column=0, sticky="nsew")
        y_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.receipt_text.yview)
        x_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.receipt_text.xview)
        y_scroll.grid(row=1, column=1, sticky="ns")
        x_scroll.grid(row=2, column=0, sticky="ew")
        self.receipt_text.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    def _label(self, parent, text: str, row: int, column: int):
        ttk.Label(parent, text=text, style="Field.TLabel").grid(row=row, column=column, sticky="w", padx=6, pady=6)

    def _combo(self, parent, variable, row: int, column: int):
        combo = ttk.Combobox(parent, textvariable=variable, state="readonly")
        combo.grid(row=row, column=column, sticky="ew", padx=6, pady=6)
        return combo

    def _entry(self, parent, variable, row: int, column: int):
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=column, sticky="ew", padx=6, pady=6)
        return entry

    def _load_master_data(self):
        try:
            self.master_data = self.master_repo.load_all()
        except Exception as exc:
            messagebox.showerror("Koneksi Database Gagal", str(exc))
            return

        self.cabang_cb["values"] = [display_cabang(row) for row in self.master_data["cabang"]]
        self.meja_cb["values"] = [display_meja(row) for row in self.master_data["meja"]]
        self.pegawai_cb["values"] = [display_pegawai(row) for row in self.master_data["pegawai"]]
        self.menu_cb["values"] = [display_menu(row) for row in self.master_data["menu"]]
        for combo in (self.cabang_cb, self.meja_cb, self.pegawai_cb, self.menu_cb):
            if combo["values"] and not combo.get():
                combo.current(0)

    def _find_row(self, collection_name: str, key_name: str, key_value: str) -> dict | None:
        return next((row for row in self.master_data[collection_name] if row[key_name] == key_value), None)

    def _add_to_cart(self):
        if not self.menu_var.get():
            messagebox.showwarning("Menu Kosong", "Pilih menu terlebih dahulu.")
            return
        try:
            qty = int(self.qty_var.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Qty Tidak Valid", "Qty harus berupa angka lebih dari 0.")
            return

        id_menu = extract_id(self.menu_var.get())
        menu = self._find_row("menu", "id_menu", id_menu)
        if not menu:
            messagebox.showerror("Menu Tidak Ditemukan", "Data menu tidak ditemukan di database.")
            return
        if str(menu.get("status_menu", "")).lower() != "tersedia":
            messagebox.showwarning("Menu Tidak Tersedia", f"{menu['nama_menu']} sedang tidak tersedia.")
            return

        harga = Decimal(menu["harga_menu"])
        catatan = self.catatan_var.get().strip() or None
        for item in self.cart:
            if item["id_menu"] == id_menu:
                item["qty"] += qty
                item["subtotal_item"] = item["harga_satuan"] * item["qty"]
                if catatan:
                    item["catatan_item"] = catatan
                self._render_cart()
                self._refresh_totals()
                self.catatan_var.set("")
                return

        self.cart.append({
            "id_menu": id_menu,
            "nama_menu": menu["nama_menu"],
            "qty": qty,
            "harga_satuan": harga,
            "subtotal_item": harga * qty,
            "catatan_item": catatan,
        })
        self._render_cart()
        self._refresh_totals()
        self.catatan_var.set("")

    def _render_cart(self):
        for row_id in self.cart_tree.get_children():
            self.cart_tree.delete(row_id)
        for item in self.cart:
            self.cart_tree.insert("", tk.END, values=(
                item["id_menu"],
                item["nama_menu"],
                item["qty"],
                money(item["harga_satuan"]),
                money(item["subtotal_item"]),
                item.get("catatan_item") or "-",
            ))

    def _remove_selected_item(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showinfo("Pilih Item", "Pilih item yang ingin dihapus.")
            return
        selected_id = self.cart_tree.item(selected[0], "values")[0]
        self.cart = [item for item in self.cart if item["id_menu"] != selected_id]
        self._render_cart()
        self._refresh_totals()

    def _clear_cart(self):
        self.cart.clear()
        self._render_cart()
        self._refresh_totals()

    def _subtotal(self) -> Decimal:
        return sum((item["subtotal_item"] for item in self.cart), Decimal("0"))

    def _refresh_totals(self):
        try:
            biaya = safe_decimal(self.biaya_var.get())
            nominal = safe_decimal(self.nominal_var.get())
        except ValueError:
            self.payment_status.configure(text="Input biaya atau nominal tidak valid.", style="Danger.TLabel")
            self.save_btn.state(["disabled"])
            return

        subtotal = self._subtotal()
        total = subtotal + biaya
        kembalian = nominal - total
        values = {
            "Subtotal": subtotal,
            "Biaya": biaya,
            "Total Bayar": total,
            "Nominal": nominal,
            "Kembalian": kembalian,
        }
        for key, value in values.items():
            self.summary_vars[key].set(rupiah(value))

        if total <= 0:
            self.payment_status.configure(text="Tambahkan menu ke keranjang terlebih dahulu.", style="Danger.TLabel")
            self.save_btn.state(["disabled"])
        elif nominal < total:
            self.payment_status.configure(text=f"Kurang bayar {rupiah(total - nominal)}", style="Danger.TLabel")
            self.save_btn.state(["disabled"])
        else:
            self.payment_status.configure(text=f"Pembayaran cukup. Kembalian {rupiah(kembalian)}", style="Success.TLabel")
            self.save_btn.state(["!disabled"])

    def _save_transaction(self):
        if not self.cart:
            messagebox.showwarning("Keranjang Kosong", "Tambahkan minimal satu menu ke keranjang.")
            return
        try:
            biaya = safe_decimal(self.biaya_var.get())
            nominal = safe_decimal(self.nominal_var.get())
            total = self._subtotal() + biaya
        except ValueError:
            messagebox.showwarning("Input Tidak Valid", "Biaya tambahan dan nominal bayar harus berupa angka.")
            return
        if nominal < total:
            messagebox.showwarning("Pembayaran Kurang", "Nominal bayar lebih kecil dari total bayar.")
            return

        try:
            id_transaksi = self.transaction_repo.create_transaction(
                id_cabang=extract_id(self.cabang_var.get()),
                id_meja=extract_id(self.meja_var.get()),
                id_pegawai=extract_id(self.pegawai_var.get()),
                nama_pelanggan=self.nama_pelanggan_var.get(),
                no_telp=self.no_telp_var.get(),
                cart=self.cart,
                biaya=biaya,
                metode_pembayaran=self.metode_var.get(),
                nominal_bayar=nominal,
            )
            self._print_receipt(id_transaksi)
            self._search_transactions()
            messagebox.showinfo("Berhasil", f"Transaksi {id_transaksi} berhasil disimpan.")
            self._clear_form(keep_receipt=True)
        except Exception as exc:
            messagebox.showerror("Gagal Menyimpan Transaksi", str(exc))

    def _print_receipt(self, id_transaksi: str):
        header, items, biaya_rows = self.transaction_repo.get_receipt_data(id_transaksi)
        if not header:
            messagebox.showerror("Struk Tidak Ditemukan", "Data transaksi tidak ditemukan.")
            return
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(tk.END, build_receipt(header, items, biaya_rows))

    def _search_transactions(self):
        if not hasattr(self, "history_tree"):
            return
        for row_id in self.history_tree.get_children():
            self.history_tree.delete(row_id)
        try:
            rows = self.transaction_repo.search_transactions(self.search_var.get() if hasattr(self, "search_var") else "")
        except Exception as exc:
            messagebox.showerror("Gagal Mencari Transaksi", str(exc))
            return
        for row in rows:
            tanggal = row["tanggal_waktu"].strftime("%d-%m-%Y %H:%M") if row.get("tanggal_waktu") else "-"
            self.history_tree.insert("", tk.END, values=(
                row["id_transaksi"],
                row["no_pesanan"],
                tanggal,
                row.get("nomor_meja") or "-",
                row.get("nama_pelanggan") or "Pelanggan Umum",
                money(row["total_bayar"]),
            ))

    def _show_selected_history_receipt(self):
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showinfo("Pilih Transaksi", "Pilih transaksi yang ingin ditampilkan ulang.")
            return
        self._print_receipt(self.history_tree.item(selected[0], "values")[0])

    def _clear_form(self, keep_receipt: bool = False):
        self.cart.clear()
        self._render_cart()
        self.nama_pelanggan_var.set("")
        self.no_telp_var.set("")
        self.catatan_var.set("")
        self.nominal_var.set("0")
        self._refresh_totals()
        if not keep_receipt:
            self.receipt_text.delete("1.0", tk.END)
