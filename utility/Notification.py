import logging
import os

import plyer

os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"


# print(icon_image)


class DesktopNotification:

    def __init__(self, title: str, message: str, image_path: str = "No"):
        """
        Initializes a Birthday notification with the given title and message.

        Parameters:
            title (str): The title of the notification.
            message (str): The message body of the notification.

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
        except Exception as e:
            logging.error(e)
        # Not working cause of X11 and cron job issue have to add cron username to group of either video or x11 don't
        # know much about .


if __name__ == "__main__":
    DesktopNotification("test", "test", "danger.png")
    print("done")
