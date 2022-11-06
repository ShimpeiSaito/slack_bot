import os
import hashlib
import requests
import datetime
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

# Add functionality
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
  # イベントがトリガーされたチャンネルへ say() でメッセージを送信
  say(
      blocks=[
          {
              "type": "section",
              "text": {"type": "mrkdwn", "text": f"こんにちは！ <@{message['user']}>さん！"},
          }
      ],
      text=f"こんにちは！ <@{message['user']}>さん！"
  )


@app.message("出欠")
def attendance(message, say):
  dt_now = datetime.datetime.now().strftime('%Y年%m月%d日の出欠ログ')
  requests.post(f"https://maker.ifttt.com/trigger/Attendance_log/with/key/bF1sHuZb1lBwx62Q_d2tMA?value1=-----{dt_now}-----")
  say(
      blocks=[
          {
              "type": "section",
              "text": {"type": "mrkdwn", "text": f"みなさん！出欠をとります！"},
              "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"出席"},
                    "action_id": "attend_click"
              }
          },
          {
              "type": "section",
              "text": {"type": "mrkdwn", "text": f" "},
              "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"欠席"},
                    "action_id": "absence_click"
              }
          }
      ],
      text=f"<@{message['user']}>さんが出欠確認を開始しました！"
  )

@app.action("attend_click")
def action_attend_click(body, ack, say):
  # アクションを確認したことを即時で応答
  ack()
  # チャンネルにメッセージを投稿
  say(f"<@{body['user']['id']}> 出席しました！")
  requests.post(f"https://maker.ifttt.com/trigger/Attendance_log/with/key/bF1sHuZb1lBwx62Q_d2tMA?value1={body['user']['name']}&value2=出席")

@app.action("absence_click")
def action_absence_click(body, ack, say):
  # アクションを確認したことを即時で応答
  ack()
  # チャンネルにメッセージを投稿
  say(f"<@{body['user']['id']}> 欠席します。。")
  requests.post(f"https://maker.ifttt.com/trigger/Attendance_log/with/key/bF1sHuZb1lBwx62Q_d2tMA?value1={body['user']['name']}&value2=欠席")


@app.message("匿名アンケート")
def attendance(message, say):
  say(
      blocks=[
          {
              "type": "section",
              "text": {"type": "mrkdwn", "text": f"匿名アンケートをとります！！（水曜日は対面orオンラインどちらを希望しますか？）"},
              "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"対面"},
                    "action_id": "A_click"
              }
          },
          {
              "type": "section",
              "text": {"type": "mrkdwn", "text": f" "},
              "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"オンライン"},
                    "action_id": "B_click"
              }
          }
      ],
      text=f"<@{message['user']}>さんが匿名アンケートを開始しました！"
  )

@app.action("A_click")
def action_attend_click(body, ack, say):
  # アクションを確認したことを即時で応答
  ack()
  # チャンネルにメッセージを投稿
  uID_hash = hashlib.sha256((body['user']['id']).encode("utf-8")).hexdigest()
  say(f"{uID_hash[0:7]} 対面を希望します！")



@app.action("B_click")
def action_absence_click(body, ack, say):
  # アクションを確認したことを即時で応答
  ack()
  # チャンネルにメッセージを投稿
  uID_hash = hashlib.sha256((body['user']['id']).encode("utf-8")).hexdigest()
  say(f"{uID_hash[0:7]} オンラインを希望します！")



# @app.event("emoji_changed")
# def emoji_notice(say):
#   say(f"新しい絵文字が追加されたみたいだよ！")


@app.message("^.*")
def react_thank(message):
  channel_id = message['channel']
  timestamp = message['ts']
  client.reactions_add(channel=channel_id, timestamp=timestamp, name='guruguru-good')


from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)