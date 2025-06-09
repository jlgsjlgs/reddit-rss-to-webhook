import requests
import json
import os
import logging
import praw
import firebase_admin
from datetime import datetime, timezone, timedelta
from firebase_admin import credentials, firestore

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Discord:
    def __init__(self):
        self.webhookURL = os.getenv("WEBHOOK_URL")

        if not self.webhookURL:
            logging.error("WEBHOOK_URL not provided in environment variables")
            raise ValueError("Missing required environment variable: WEBHOOK_URL")
    
    def send(self, title, url):
        headers = {"Content-Type": "application/json"}
        data = {
            "content": "**{}**\n\n{}".format(title, url),
            "username": "HSR Leaks",
            "avatar_url": "https://static.wikia.nocookie.net/houkai-star-rail/images/4/44/Sticker_PPG_13_Acheron_03.png/revision/latest/scale-to-width-down/250?cb=20240802015945"
        }

        try:
            res = requests.post(self.webhookURL, data=json.dumps(data), headers=headers)

            if res.status_code == 204:
                logging.info(f"Sent to Discord: {title}")
            else:
                logging.error(f"Failed to send '{title}' to Discord, status code: {res.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception sending '{title}': {e}")


class Database:
    def __init__(self):
        self.key = json.loads(os.environ['FIREBASE_CREDENTIALS'])

        if not self.key:
            logging.error("FIREBASE_CREDENTIALS not provided in environment variables")
            raise ValueError("Missing required environment variable: FIREBASE_CREDENTIALS")

        try:
            cred = credentials.Certificate(self.key)
            app = firebase_admin.initialize_app(cred)
            self.db = firestore.client()
        except Exception as e:
            logging.error(f"Error initializing Firebase Admin SDK: {e}")
            raise
    
    def getTime(self):
        try:
            doc_ref = self.db.collection("timestamp").document("last_read")
            doc = doc_ref.get()
            data = doc.to_dict()
            return data.get("time").timestamp()
        except Exception as e:
            logging.error(f"Error getting timestamp from Firebase {e}")
            raise
    
    def updateTime(self):
        try:
            current_time = datetime.now(timezone.utc)
            doc_ref = self.db.collection("timestamp").document("last_read")
            doc_ref.set({"time": current_time})
            logging.info("Updated timestamp in Firestore")
        except Exception as e:
            logging.error(f"Error updating timestamp in Firebase: {e}")
            raise

class Reddit:
    def __init__(self):
        try:
            self.connection = praw.Reddit(
                client_id=os.getenv("CLIENT_ID"),
                client_secret=os.getenv("CLIENT_SECRET"),
                user_agent="rss-to-discord"
            )
        except Exception as e:
            logging.error(f"Error authenticating to Reddit: {e}")
            raise ValueError("Error authenticating to Reddit")

        self.discord = Discord()
    
    def checkPosts(self, last_checked_timestamp):
        stk = []
        subreddit = self.connection.subreddit("HonkaiStarRail_leaks")

        for submission in subreddit.new():
            if submission.created_utc >= last_checked_timestamp:
                stk.append(submission)
            else:
                break
        
        if not stk:
            logging.info("No new posts")
        
        while stk:
            post = stk.pop()
            self.discord.send(post.title, post.url)

if __name__ == "__main__":
    fb = Database()
    rdt = Reddit()

    rdt.checkPosts(fb.getTime())
    fb.updateTime()

    logging.info("Script execution completed")
