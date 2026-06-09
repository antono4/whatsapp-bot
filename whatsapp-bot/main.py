#!/usr/bin/env python3
"""
WhatsApp Bot - Simple Auto-Reply Bot
Author: OpenHands
Version: 1.0.0

Penggunaan:
1. Install dependencies: pip install -r requirements.txt
2. Jalankan: python main.py
3. Scan QR Code yang muncul di terminal

Note: Bot ini menggunakan whatsapp-web.js (Node.js) yang berjalan di backend.
Python berperan sebagai interface dan logic handler.
"""

import asyncio
import json
import os
import sys
import subprocess
import platform
from datetime import datetime
from pathlib import Path

# Import handlers
from handlers import handle_message
import config

class WhatsAppBot:
    """Main WhatsApp Bot Class"""
    
    def __init__(self):
        self.session_dir = Path(__file__).parent / "session"
        self.session_dir.mkdir(exist_ok=True)
        self.is_connected = False
        self.node_process = None
        
    def print_banner(self):
        """Print startup banner"""
        banner = """
╔══════════════════════════════════════════╗
║         🤖 WhatsApp Bot v1.0.0           ║
║                                          ║
║  Bot WhatsApp dengan Auto-Reply          ║
║  Ketik !menu untuk melihat perintah       ║
╚══════════════════════════════════════════╝
        """
        print(banner)
    
    def check_nodejs(self):
        """Check if Node.js is installed"""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"✓ Node.js terinstall: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        print("✗ Node.js tidak ditemukan!")
        print("\n📦 Install Node.js:")
        print("   Windows: https://nodejs.org/")
        print("   Linux:   sudo apt install nodejs npm")
        print("   Mac:     brew install node")
        return False
    
    def install_npm_packages(self):
        """Install required npm packages for WhatsApp Web"""
        print("\n📦 Menginstall packages npm...")
        
        # Create package.json
        package_json = {
            "name": "whatsapp-bot",
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "start": "node src/bot.js"
            },
            "dependencies": {
                "whatsapp-web.js": "^1.23.0",
                "qrcode-terminal": "^0.12.0"
            }
        }
        
        with open("package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        # Create src directory
        os.makedirs("src", exist_ok=True)
        
        # Create bot.js
        bot_js = '''const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

// Initialize WhatsApp client
const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: 'session'
    }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// QR Code event
client.on('qr', (qr) => {
    console.log("\\n═══════════════════════════════════════");
    console.log("   📱 SCAN QR CODE DI BAWAH INI");
    console.log("═══════════════════════════════════════\\n");
    qrcode.generate(qr, { small: true });
    console.log("\\n═══════════════════════════════════════\\n");
});

// Ready event
client.on('ready', () => {
    console.log("✅ Bot WhatsApp aktif dan siap!");
    console.log("💬 Silakan kirim pesan ke bot...");
});

// Message event
client.on('message', async (message) => {
    const msgBody = message.body;
    
    // Skip status messages
    if (message.from === 'status@broadcast') return;
    
    // Get reply from Python handler via file-based IPC
    try {
        const { spawn } = require('child_process');
        const pythonProcess = spawn('python3', ['-c', `
import sys
sys.path.insert(0, '${__dirname}')
from handlers import handle_message
result = handle_message("${msgBody.replace(/"/g, '\\\\"')}")
print(result if result else '')
`]);
        
        let reply = '';
        pythonProcess.stdout.on('data', (data) => {
            reply += data.toString();
        });
        
        pythonProcess.on('close', () => {
            if (reply.trim()) {
                message.reply(reply.trim());
            }
        });
    } catch (error) {
        console.error('Error:', error);
    }
});

// Disconnect event
client.on('disconnected', (reason) => {
    console.log('⚠️ Bot terputus:', reason);
    console.log('🔄 Restarting dalam 5 detik...');
    setTimeout(() => {
        client.initialize();
    }, 5000);
});

// Start the client
console.log("⏳ Initializing bot...");
client.initialize();
'''
        
        with open("src/bot.js", "w") as f:
            f.write(bot_js)
        
        # Install npm packages
        print("⏳ Menginstall dependencies (akan memakan waktu)...")
        result = subprocess.run(
            ["npm", "install"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print("✅ Packages terinstall!")
            return True
        else:
            print(f"❌ Gagal install packages: {result.stderr}")
            return False
    
    def run(self):
        """Run the bot"""
        self.print_banner()
        
        # Check Node.js
        if not self.check_nodejs():
            print("\n⚠️ Bot tidak bisa jalan tanpa Node.js")
            print("💡 Install Node.js terlebih dahulu, lalu jalankan ulang bot")
            return
        
        # Setup npm packages
        if not Path("node_modules").exists():
            self.install_npm_packages()
        
        # Run the bot
        print("\n🚀 Menjalankan bot...")
        print("📱 Buka WhatsApp > Settings > Linked Devices\n")
        
        try:
            self.node_process = subprocess.Popen(
                ["node", "src/bot.js"],
                cwd=os.getcwd()
            )
            self.node_process.wait()
        except KeyboardInterrupt:
            print("\n\n👋 Bot dihentikan. Sampai jumpa!")
            if self.node_process:
                self.node_process.terminate()

def main():
    """Main entry point"""
    bot = WhatsAppBot()
    bot.run()

if __name__ == "__main__":
    main()