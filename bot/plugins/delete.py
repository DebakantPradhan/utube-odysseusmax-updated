import os
import shutil
import logging
from pyrogram import filters as Filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction

from ..config import Config
from ..utubebot import UtubeBot

log = logging.getLogger(__name__)

@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("delete")
    & Filters.user(Config.AUTH_USERS)
)
async def _delete_downloads(c: UtubeBot, m: Message):
    """Delete all files from the downloads directory"""
    await m.reply_chat_action(ChatAction.TYPING)
    
    downloads_path = os.path.join(os.getcwd(), "bot", "downloads")
    
    if not os.path.exists(downloads_path):
        await m.reply_text("Downloads directory does not exist.", True)
        return
    
    # Check if optional argument is provided for specific deletion
    if len(m.command) > 1 and m.command[1] == "list":
        # List files but don't delete
        files = os.listdir(downloads_path)
        if not files:
            await m.reply_text("Downloads directory is already empty.", True)
            return
        
        file_list = "\n".join([f"- {f}" for f in files])
        await m.reply_text(f"Files in downloads directory:\n\n{file_list}\n\nTo delete use /delete", True)
        return
    
    try:
        # Count files before deletion
        files = os.listdir(downloads_path)
        file_count = len(files)
        
        if file_count == 0:
            await m.reply_text("Downloads directory is already empty.", True)
            return
        
        # Delete everything in the downloads directory
        for item in files:
            item_path = os.path.join(downloads_path, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        # Create a .gitkeep file to ensure directory remains in git
        open(os.path.join(downloads_path, ".gitkeep"), "w").close()
        
        # Get disk space info
        disk_info = os.popen("df -h / | tail -1").read().strip().split()
        if len(disk_info) >= 5:
            available_space = disk_info[3]
            used_percentage = disk_info[4]
        else:
            available_space = "Unknown"
            used_percentage = "Unknown"
        
        await m.reply_text(
            f"✅ Successfully deleted {file_count} items from downloads directory.\n\n"
            f"Available space: {available_space}\n"
            f"Disk usage: {used_percentage}", 
            True
        )
        log.info(f"User {m.from_user.id} deleted {file_count} files from downloads directory")
    
    except Exception as e:
        log.error(e, exc_info=True)
        await m.reply_text(f"❌ Error occurred while deleting files: {str(e)}", True)