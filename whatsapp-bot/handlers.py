"""
Handler untuk memproses pesan masuk dan generate response
"""
import random
from datetime import datetime

# Database sederhana untuk auto-reply (bisa dikembangkan dengan database sungguhan)
AUTO_REPLIES = {
    # Sapaan
    "halo": [
        "Halo juga! 👋",
        "Hai! Apa kabar? 😊",
        "Halo! Ada yang bisa saya bantu?",
        "Yo! Selamat datang! 🎉",
    ],
    "hai": [
        "Hai juga! 😄",
        "Halo! Ada yang perlu bantuan?",
        "Hai hai! 👋",
    ],
    "hi": [
        "Hi! 👋",
        "Hello! 😊",
    ],
    "pagi": [
        "Selamat pagi! ☀️",
        "Pagi juga! Semoga hari kamu menyenangkan!",
    ],
    "siang": [
        "Selamat siang! 🌞",
        "Siang! Panas ya di luar!",
    ],
    "sore": [
        "Selamat sore! 🌅",
        "Sore! Semoga harimu menyenangkan!",
    ],
    "malam": [
        "Selamat malam! 🌙",
        "Malam! Tidur yang nyenyak ya!",
    ],
    
    # Pertanyaan umum
    "kabar": [
        "Kabar baik! 😊 Terima kasih sudah bertanya!",
        "Alhamdulillah baik! Kamu bagaimana?",
        "Kabar baik dong! Ada yang bisa saya bantu?",
    ],
    "siapa kamu": [
        "Saya adalah bot WhatsApp! 🤖",
        "Saya adalah asisten virtual yang siap membantu Anda 24/7!",
    ],
    "help": [
        "Ketik !menu untuk melihat semua perintah yang tersedia.",
    ],
    "menu": [
        "📋 *Menu Bot*\n\n"
        "!menu - Menampilkan menu\n"
        "!help - Bantuan\n"
        "!info - Info bot\n"
        "!ping - Cek bot hidup\n"
        "!joke - Dapatkan lelucon\n"
        "!time - Waktu sekarang\n"
        "!date - Tanggal hari ini",
    ],
    "thanks": [
        "Sama-sama! 😊",
        "Terima kasih kembali! 🙏",
        "Ups, tidak perlu mengucapkan terima kasih! 😄",
    ],
    "terima kasih": [
        "Sama-sama! 😊",
        "Sangat membantu ya! 🙏",
        "Senang bisa membantu! 💪",
    ],
}

# Command handlers
COMMANDS = {
    "!ping": lambda: "🏓 Pong! Bot sedang aktif!",
    "!info": lambda: "ℹ️ Bot WhatsApp v1.0\nDibuat dengan Python",
    "!joke": lambda: random.choice([
        "Kenapa programmer selalu hujan-hinanan? Karena dia suka debugging! 😄",
        "Apa bedanya programmer sama tukang bakso? Kalau programmer加班 (lembur), kalau tukang bakso加班 (juga lembur)! 😂",
        "Ada 10 jenis programmer: yang tahu biner dan yang tidak. 🤓",
        "Kenapa programmer tidak bisa buat aplikasi cuaca? Karena selalu ada 'bug' di forecast! 😂",
    ]),
    "!time": lambda: f"🕐 Waktu sekarang: {datetime.now().strftime('%H:%M:%S')}",
    "!date": lambda: f"📅 Tanggal hari ini: {datetime.now().strftime('%d-%m-%Y')}",
    "!menu": lambda: AUTO_REPLIES["menu"][0],
    "!help": lambda: AUTO_REPLIES["help"][0],
}

def get_auto_reply(message: str) -> str | None:
    """Cek apakah pesan cocok dengan auto-reply yang ada"""
    message_lower = message.lower().strip()
    
    for keyword, responses in AUTO_REPLIES.items():
        if keyword in message_lower:
            return random.choice(responses)
    
    return None

def get_command_reply(command: str) -> str | None:
    """Handle command khusus"""
    handler = COMMANDS.get(command.lower())
    if handler:
        return handler()  # Call the lambda function
    return None

def handle_message(message: str) -> str:
    """
    Main handler untuk memproses pesan
    Returns: Response string atau None jika tidak perlu reply
    """
    message = message.strip()
    
    # Cek command dulu
    command_reply = get_command_reply(message)
    if command_reply:
        return command_reply
    
    # Cek auto-reply
    auto_reply = get_auto_reply(message)
    if auto_reply:
        return auto_reply
    
    # Default: tidak ada response
    return None