import os
# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Add functionality here
# @app.event("app_home_opened") etc
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )

  except Exception as e:
    logger.error(f"Error opening modal: {e}")

@app.message("^.*こんにちは.*")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"こんにちは！ <@{message['user']}>さん！"},
                # "accessory": {
                #     "type": "button",
                #     "text": {"type": "plain_text", "text":"Click Me"},
                #     "action_id": "button_click"
                # }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

# @app.action("button_click")
# def action_button_click(body, ack, say):
#     # アクションを確認したことを即時で応答します
#     ack()
#     # チャンネルにメッセージを投稿します
#     say(f"<@{body['user']['id']}> クリックありがとう！何もないけど、")

@app.message("^.*")
def react_thank(message, say):
    channel_id = message['channel']
    timestamp = message['ts']
    client.reactions_add(channel=channel_id, timestamp=timestamp, name='guruguru-good')


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))