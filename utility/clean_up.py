
import logging
from utility.get_image_from_url import IMAGE_PATH



def clean_up():
    """
    Cleans up the images directory.

    Parameters:
        None

    Returns:
        None
    """
    if IMAGE_PATH.exists():
        for file_path in IMAGE_PATH.iterdir():
            try:
                if file_path.is_file():
                    file_path.unlink()
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
