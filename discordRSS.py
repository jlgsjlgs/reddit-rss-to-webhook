import requests
import json
import os
import praw
import logging
from datetime import datetime, timezone, timedelta

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'
)

LAST_RUN_FILE = "last_run.txt"

def get_last_run_timestamp():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, "r") as f:
            return float(f.read().strip())
    return (datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()

def update_last_run_timestamp():
    with open(LAST_RUN_FILE, "w") as f:
        f.write(str(datetime.now(timezone.utc).timestamp()))

class DiscordWebhook:
    def __init__(self):
        self.webhookURL = os.getenv("WEBHOOK_URL")
    
    def sendToDiscord(self, title, img, url):
        headers = {"Content-Type": "application/json"}
        data = {
            "content": "**{}**\n\n".format(title),
            "embeds": [
                {   
                    "title": title,
                    "image": {"url": img},
                    "url": url
                }
            ]
        }

        try:
            res = requests.post(self.webhookURL, data=json.dumps(data), headers=headers)
            if res.status_code == 204:
                logging.info(f"Sent to Discord: {title}")
            else:
                logging.error(f"Failed to send '{title}' to Discord, status code: {res.status_code}")
            return res.status_code
        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception sending '{title}': {e}")
            return None

cutoff_time = get_last_run_timestamp()
stk = []
webhook = DiscordWebhook()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent="rss-to-discord"
)

subreddit = reddit.subreddit("HonkaiStarRail_leaks")

for submission in reddit.subreddit("HonkaiStarRail_leaks").new():
    if submission.created_utc >= cutoff_time:
        stk.append(submission)
    else:
        break

if not stk:
    logging.info("No new posts")
    
while stk:
    post = stk.pop()
    if post.url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        webhook.sendToDiscord(post.title, post.url, f"https://reddit.com{post.permalink}")
    else:
        webhook.sendToDiscord(f"{post.title}\n{post.url}", "", f"https://reddit.com{post.permalink}")

update_last_run_timestamp()