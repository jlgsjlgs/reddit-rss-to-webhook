# reddit-to-webhook

[![Reddit to Discord webhook](https://github.com/jlgsjlgs/reddit-to-webhook/actions/workflows/main.yml/badge.svg)](https://github.com/jlgsjlgs/reddit-to-webhook/actions/workflows/main.yml)

A lightweight Python script that monitors a specific subreddit for new posts and sends them to a Discord webhook. Uses Firebase's Firestore to keep track of the timestamp that we last checked.

## Features

- Monitors new submissions from a chosen subreddit
- Sends a notification to the specified Discord webhook for any new posts 
- Keeps track of script last ran timestamp in Firebase Firestore
- Runs automatically on a schedule using GitHub Actions (cron)  

## Environment Variables

These can be set locally or through GitHub Actions secrets.

| Variable            | Description                                |
| ------------------- | ------------------------------------------ |
| `CLIENT_ID`         | Reddit app client ID                       |
| `CLIENT_SECRET`     | Reddit app client secret                   |
| `WEBHOOK_URL`       | Your Discord channel webhook URL           |
| `FIREBASE_CREDENTIALS` | JSON string of Firebase service account credentials |

## Logging

The script uses Python’s logging module to provide structured logs:

- Success and error responses from the webhook
- Errors related to Firebase or Reddit API usage
- A message when no new posts are found

Logs are visible in the GitHub Actions job output.
