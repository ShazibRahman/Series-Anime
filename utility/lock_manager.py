import io
import os
import pathlib
import time
from functools import wraps
import logging
from typing import Any

import psutil


def check_pid_exists(pid):
    """
    Check if a process with the given PID exists.

    Args:
        pid (int): The PID of the process to check.

    Returns:
        bool: True if a process with the given PID exists, False otherwise.
    """
    return psutil.pid_exists(pid)


class LockError(Exception):
    pass


class LockManager:
    def __init__(self, file_path):
        self.lock_file = file_path

    def acquire_control(self):
        """
        Acquires control by checking if a lock file exists. If the lock file does not exist, it creates one and
        writes the current process ID to it. If the lock file exists, it reads the process ID from it and compares it
        with the current process ID. If the process IDs match, it logs a message indicating that control is already
        acquired. If the process IDs do not match, it logs a message indicating that another instance of the program
        is already running with the process ID and exits.

        Parameters:
        - None

        Returns:
        - None | Bool
        """
        while os.path.exists(self.lock_file):
            with open(self.lock_file, "r", encoding="utf-8") as file:
                pid = file.read().strip()

                if pid == "":
                    # Remove stale lock file
                    os.remove(self.lock_file)
                    continue

                if pid == str(os.getpid()):
                    logging.info("Control already acquired.")
                    return True
                elif check_pid_exists(int(pid)):
                    logging.info(
                        "Another instance of the program is already running with pid %s exiting...",
                        pid,
                    )
                    return False
                else:
                    # Remove stale lock file
                    os.remove(self.lock_file)

        with open(self.lock_file, "w", encoding="utf-8") as file:
            file.write(str(os.getpid()))
        logging.info("Control acquired.")
        return True

    def release_control(self):
        """
        Removes the lock file and prints a message indicating that control has been released.
        """

        if not os.path.exists(self.lock_file):
            raise LockError("Lock does not exist.")

        with io.open(self.lock_file, "r", encoding="utf-8") as file:
            pid = file.read()
            if os.getpid() == int(pid):
                os.remove(self.lock_file)
                logging.info("Control released.")

    def __enter__(self):
        return self.acquire_control()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release_control()


def lock_manager_decorator(file_name: str | pathlib.Path) -> Any:

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs):
            lock_manager = LockManager(file_name)
            if not lock_manager.acquire_control():
                return
            try:
                return func(*args, **kwargs)
            finally:
                lock_manager.release_control()

        return wrapper

    return decorator


if __name__ == "__main__":
    # lock_manager = LockManager(
    #     "/home/shazib/Desktop/Folder/python/wallpaper_updates/wallpaper_updator.lock"
    # )

    logging.basicConfig(level=logging.INFO)

    # @lock_manager_decorator("wallpaper_updator.lock")
    # def main():
    #     time.sleep(10)
    #     print("Hello World")
    #
    # main()

    with LockManager("wallpaper_updator.lock") as lock_acquired:
        if lock_acquired:
            time.sleep(10)
            print("Hello World")
        else:
            print("Lock not acquired")
