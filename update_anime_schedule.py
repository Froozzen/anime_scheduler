import requests
import datetime
import os
from pytz import timezone

# Discord webhook details (using environment variables)
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
MESSAGE_ID = os.getenv('MESSAGE_ID')

# Anime release schedules
anime_releases = {
    "Solo Leveling": {
        "total_episodes": 13,
        "current_episode": 7,
        "next_release": datetime.datetime(2025, 2, 22, 18, 30, tzinfo=timezone("Europe/Berlin")),
        "release_interval": datetime.timedelta(weeks=1)
    },
    "One Piece": {
        "total_episodes": 1122,
        "current_episode": 1122,
        "next_release": datetime.datetime(2025, 4, 6, 4, 45, tzinfo=timezone("Europe/Berlin")),
        "release_interval": datetime.timedelta(weeks=1)
    }
}

def update_countdown():
    now = datetime.datetime.now(timezone("Europe/Berlin"))
    message = "📅 **Anime Release Schedule**\n\n"

    for anime, details in anime_releases.items():
        next_release = details["next_release"]
        if now > next_release:
            while now > next_release:
                next_release += details["release_interval"]
            details["current_episode"] += 1

        time_left = next_release - now
        days, remainder = divmod(time_left.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        message += (
            f"**{anime}**\n"
            f"Next Episode: {details['current_episode'] + 1}/{details['total_episodes']}\n"
            f"Time Left: {int(days)}d {int(hours)}h {int(minutes)}m\n"
            f"Release Date: {next_release.strftime('%Y-%m-%d %H:%M %Z')}\n\n"
        )
# Add URLs for airing and next season
    message += "Currently Airing:\n"
    message += "https://myanimelist.net/topanime.php?type=airing\n\n"

    message += "Next Season:\n"
    message += "https://myanimelist.net/topanime.php?type=upcoming\n\n"
    
    last_edited = now.strftime("%Y-%m-%d %H:%M %Z")
    message += f"Last Edited: {last_edited}"

    data = {"content": message}
    response = requests.patch(f"{WEBHOOK_URL}/messages/{MESSAGE_ID}", json=data)
    if response.status_code == 200:
        print("Message updated successfully.")
    else:
        print(f"Failed to update message: {response.status_code} - {response.text}")

if __name__ == "__main__":
    update_countdown()
