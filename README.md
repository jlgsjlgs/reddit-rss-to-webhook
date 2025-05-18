# reddit-to-webhook

A lightweight Python script that monitors a specific subreddit for new posts and sends them to a Discord webhook. Ideal for creating subreddit-based RSS feeds in Discord channels.

## Features

- Monitors new submissions from a chosen subreddit
- Sends image posts with previews to a Discord channel via webhook
- Posts text or link submissions as embedded messages
- Runs automatically every hour (or stipulated timeframe) using GitHub Actions (cron)

## Environment Variables

These can be set locally or through GitHub Actions secrets.

| Variable        | Description                      |
| --------------- | -------------------------------- |
| `CLIENT_ID`     | Reddit app client ID             |
| `CLIENT_SECRET` | Reddit app client secret         |
| `WEBHOOK_URL`   | Your Discord channel webhook URL |

## Logging

The script uses Python’s logging module to provide structured logs:

- Success and error responses from the webhook

- A message when no new posts are found

Logs are visible in the GitHub Actions job output.
