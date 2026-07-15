"""
Utility functions for background notification tasks.
"""

import time
from datetime import datetime


def log_activity(user_id: int, action: str) -> None:
    """
    Logs a user action to activity_log.txt.

    Args:
        user_id: The ID of the authenticated user.
        action: Description of the action performed.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("activity_log.txt", "a", encoding="utf-8") as file:
        file.write(
            f"[{timestamp}] User {user_id}: {action}\n"
        )


def send_notification(email: str, message: str) -> None:
    """
    Simulates sending an email notification.

    Sleeps for two seconds to imitate a slow external
    service, then records the notification in a log file.

    Args:
        email: Recipient email.
        message: Notification message.
    """
    time.sleep(2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(
        "notification_log.txt",
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            f"[{timestamp}] To: {email} | {message}\n"
        )