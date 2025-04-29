"""
A module for creating desktop notifications using the notify-send command.
"""

import logging
import os
import subprocess
from pathlib import Path

# Ensure the DBUS session bus is set correctly (optional, depending on your environment)
os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"


class DesktopNotification:
    """
    A class for creating desktop notifications using the notify-send command.

    Attributes:
        title (str): The title of the notification.
        message (str): The message body of the notification.
        image_path (str): The path to the image to be displayed in the notification.
    """

    def __init__(self, title: str, message: str, image_path: str = "No"):
        """
        Initializes a desktop notification with the given title and message.

        Parameters:
            title (str): The title of the notification.
            message (str): The message body of the notification.
            image_path (str): The path to the image to be displayed in the notification.

        Returns:
            None
        """
        try:
            if image_path != "No" and Path(image_path).exists():
                icon = Path(image_path).as_posix()
            else:
                icon = None 

            notify_send_args = ["notify-send", title, message, "-t", "10000"]

            if icon:
                notify_send_args.extend(["-i", icon])

            subprocess.run(notify_send_args, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to send notification: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Example usage
    DesktopNotification("Test Notification", "This is a test notification.", "danger.png")
    print("done")