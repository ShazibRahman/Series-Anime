"""
A module for creating desktop notifications using the plyer library.
"""

import logging
import os

import plyer

os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"


# print(icon_image)


class DesktopNotification:
    """
    A class for creating desktop notifications using the plyer library.

    Attributes:
        title (str): The title of the notification.
        message (str): The message body of the notification.
        image_path (str): The path to the image to be displayed in the notification.
    """

    def __init__(self, title: str, message: str, image_path: str = "No"):
        """
        Initializes a Birthday notification with the given title and message.

        Parameters:
            title (str): The title of the notification.
            message (str): The message body of the notification.
            image_path (str): The path to the image to be displayed in the notification.

        Returns:
            None
        """
        try:
            plyer.notification.notify(
                title=title,
                message=message,
                app_name="Series",
                timeout=10,
                ticker="Series",
                toast=True,
                app_icon=image_path,
            )
        except Exception as e:  # pylint: disable=broad-except
            logging.error(e)


if __name__ == "__main__":
    DesktopNotification("test", "test", "danger.png")
    print("done")
