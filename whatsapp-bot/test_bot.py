"""
Unit tests untuk WhatsApp Bot
Run: python -m pytest test_bot.py -v
"""

import pytest
from handlers import get_auto_reply, get_command_reply, handle_message


class TestAutoReplies:
    """Test auto-reply functionality"""
    
    def test_halo_reply(self):
        """Test sapaan halo"""
        result = get_auto_reply("halo")
        assert result is not None
        # Check any valid response from "halo" keyword
        assert len(result) > 0
    
    def test_hai_reply(self):
        """Test sapaan hai"""
        result = get_auto_reply("hai")
        assert result is not None
    
    def test_pagi_reply(self):
        """Test sapaan pagi"""
        result = get_auto_reply("selamat pagi")
        assert result is not None
        assert "pagi" in result.lower()
    
    def test_kabar_reply(self):
        """Test pertanyaan kabar"""
        result = get_auto_reply("apa kabar")
        assert result is not None
    
    def test_unknown_message(self):
        """Test pesan yang tidak dikenal"""
        result = get_auto_reply("asjdklasjdlasjd")
        assert result is None


class TestCommands:
    """Test command functionality"""
    
    def test_ping_command(self):
        """Test !ping command"""
        result = get_command_reply("!ping")
        assert result is not None
        assert "pong" in result.lower() or "aktif" in result.lower()
    
    def test_info_command(self):
        """Test !info command"""
        result = get_command_reply("!info")
        assert result is not None
        assert "bot" in result.lower()
    
    def test_menu_command(self):
        """Test !menu command"""
        result = get_command_reply("!menu")
        assert result is not None
        assert "menu" in result.lower()
    
    def test_joke_command(self):
        """Test !joke command"""
        result = get_command_reply("!joke")
        assert result is not None
        assert len(result) > 10  # Joke should have content
    
    def test_time_command(self):
        """Test !time command"""
        result = get_command_reply("!time")
        assert result is not None
        assert "waktu" in result.lower() or ":" in result
    
    def test_date_command(self):
        """Test !date command"""
        result = get_command_reply("!date")
        assert result is not None
        assert "tanggal" in result.lower() or "-" in result


class TestHandleMessage:
    """Test main message handler"""
    
    def test_command_priority(self):
        """Test bahwa command diprioritaskan"""
        result = handle_message("!ping")
        assert result is not None
    
    def test_auto_reply_fallback(self):
        """Test auto-reply untuk pesan non-command"""
        result = handle_message("halo semua")
        assert result is not None
    
    def test_no_reply(self):
        """Test pesan yang tidak perlu di-reply"""
        result = handle_message("asdflkjhqweklrh")
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])