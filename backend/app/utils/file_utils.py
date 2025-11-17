import logging
import os
import aiofiles
from typing import Optional

logger = logging.getLogger(__name__)

async def save_uploaded_file(file, destination: str) -> bool:
    """
    Save uploaded file asynchronously
    """
    try:
        async with aiofiles.open(destination, 'wb') as buffer:
            content = await file.read()
            await buffer.write(content)
        return True
    except Exception as e:
        logger.exception("Error saving file to %s: %s", destination, e)
        return False

def ensure_directory_exists(directory: str):
    """
    Create directory if it doesn't exist
    """
    os.makedirs(directory, exist_ok=True)

def get_file_extension(filename: str) -> Optional[str]:
    """
    Extract file extension from filename
    """
    return os.path.splitext(filename)[1].lower() if '.' in filename else None