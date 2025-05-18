import requests
import json
import os
import praw
from datetime import datetime, timezone, timedelta


class DiscordWebhook:
    def __init__(self):
        self.webhookURL = os.getenv("WEBHOOK_URL")
    
    def sendToDiscord(self, title, img, url):
        headers = {
            "Content-Type": "application/json"
        }
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

        res = requests.post(self.webhookURL, data=json.dumps(data), headers=headers)

        return res.status_code

cutoff_time = (datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()
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
    
while stk:
    post = stk.pop()
    if post.url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        webhook.sendToDiscord(post.title, post.url, f"https://reddit.com{post.permalink}")
    else:
        webhook.sendToDiscord(f"{post.title}\n{post.url}", "", f"https://reddit.com{post.permalink}")
    





    

