import logging
import os
from pathlib import Path

from .utubebot import UtubeBot
from .config import Config


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG if Config.DEBUG else logging.INFO)
    logging.getLogger("pyrogram").setLevel(
        logging.INFO if Config.DEBUG else logging.WARNING
    )

    # Ensure downloads directory exists
    downloads_dir = Path(__file__).parent / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    
    # Create .gitkeep file
    gitkeep_file = downloads_dir / ".gitkeep"
    if not gitkeep_file.exists():
        gitkeep_file.touch()


    UtubeBot().run()
