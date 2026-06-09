# Cara Install dan Jalankan Bot WhatsApp

## Prerequisites (Prasyarat)

### 1. Python 3.8+
```bash
# Cek versi Python
python3 --version

# Install jika belum ada
# Windows: download dari python.org
# Linux: sudo apt install python3 python3-pip
# Mac: brew install python
```

### 2. Node.js 16+
```bash
# Cek versi Node.js
node --version

# Install jika belum ada
# Windows: download dari nodejs.org
# Linux: sudo apt install nodejs npm
# Mac: brew install node
```

## Instalasi

### Step 1: Clone/Download Project
```bash
cd whatsapp-bot
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Node.js Dependencies
```bash
npm install
```

### Step 4: Jalankan Bot
```bash
python main.py
```

## Penggunaan

### Pertama Kali (Setup)
1. Jalankan `python main.py`
2. Akan muncul QR Code di terminal
3. Buka WhatsApp di HP
4. WhatsApp > Settings > Linked Devices > Link a Device
5. Scan QR Code

### Setelah Terhubung
1. Kirim pesan ke nomor yang terhubung dengan bot
2. Bot akan auto-reply berdasarkan keyword
3. Gunakan command dengan prefix `!`

## Command yang Tersedia

| Command | Fungsi |
|---------|--------|
| `!menu` | Tampilkan semua menu |
| `!help` | Bantuan |
| `!ping` | Cek bot aktif |
| `!info` | Info bot |
| `!joke` | Dapatkan lelucon |
| `!time` | Waktu sekarang |
| `!date` | Tanggal hari ini |

## Customization (Kustomisasi)

### Tambah Auto-Reply
Edit file `handlers.py`, tambahkan keyword di dictionary `AUTO_REPLIES`:

```python
"keyword_baru": [
    "Respon pertama",
    "Respon alternatif",
]
```

### Tambah Command
Tambahkan di dictionary `COMMANDS` dalam `handlers.py`:

```python
"!nama_command": lambda: "Isi response",
```

### Ubah Prefix Command
Edit `config.py`:
```python
COMMAND_PREFIX = "!"
```

## Troubleshooting

### QR Code tidak muncul
- Pastikan terminal mendukung warna/warna tidak dimatikan
- Coba resize window terminal
- Gunakan terminal yang mendukung ANSI color

### Bot tidak mau connect
- Hapus folder `session` dan scan QR lagi
- Pastikan WhatsApp tidak terhubung ke web lain
- Cek koneksi internet

### Error "Node.js not found"
- Install Node.js dari https://nodejs.org/

### Error module not found
```bash
pip install -r requirements.txt
npm install
```

## Struktur Project

```
whatsapp-bot/
├── main.py          # File utama bot
├── handlers.py      # Logic auto-reply
├── config.py        # Konfigurasi
├── requirements.txt # Python dependencies
├── package.json     # Node.js dependencies
├── src/
│   └── bot.js       # WhatsApp Web client
├── session/         # Session storage (auto-generated)
└── README.md        # Dokumentasi
```

## Keamanan

⚠️ **Penting:**
- Jangan share folder `session/` ke orang lain
- Bot ini menggunakan WhatsApp Web protocol
- Resiko banned oleh WhatsApp, gunakan dengan bijak
- Jangan gunakan untuk spam atau aktivitas ilegal

## Lisensi

MIT License - Bebas digunakan dan dimodifikasi