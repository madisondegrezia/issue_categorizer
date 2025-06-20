import os
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

# Setup Slack and OpenAI
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = App(token=SLACK_BOT_TOKEN)
# openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

if not TARGET_CHANNEL_ID:
    print("Error: Channel ID not found.")
    exit()


@app.event("message")
def handle_all_channel_messages(body, logger):
    print(body)

    event = body["event"]

    # filter out messages from bots
    if "subtype" in event and event["subtype"] == "bot_message":
        return  # ignore messages
    if "bot_id" in event:
        return  # ignore messages from itself (bot)
    if event.get("type") != "message" or event.get("subtype") is not None:
        return

    channel_id = event.get("channel")
    if channel_id != TARGET_CHANNEL_ID:
        print(
            f"Ignoring message from channel: {channel_id} (not {TARGET_CHANNEL_ID})")
        return  # ignore messages not from targeted channel

    # relevant message details
    user_id = event.get("user")
    text = event.get("text", "")
    timestamp = event.get("ts")  # timestamp of message

    try:
        channel_info = app.client.conversations_info(channel=channel_id)
        channel_name = channel_info["channel"]["name"] if channel_info and channel_info["ok"] else channel_id
    except Exception as e:
        channel_name = channel_id
        print(f"Error fetching channel info for {channel_id}: {e}")

    print(f"\n--- All Message Detected in #{channel_name}")
    print(f"From: {user_id}")
    print(f"Text: '{text}'")
    print(f"Timestamp: {timestamp}")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
