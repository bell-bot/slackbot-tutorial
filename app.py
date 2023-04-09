import os

import logging

from flask_ngrok import run_with_ngrok

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

from slashCommand import Slash

import openai
from flask import Flask, redirect, render_template, request, url_for, make_response, Response

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
run_with_ngrok(app)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(),
            temperature=0.6,
        )
        print(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return result

def chat_gpt_request():
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(),
            temperature=0.6,
        )

    return response.choices[0].text

@app.route("/slack/clickbait", methods=["POST"])
def command():
  if not verifier.is_valid_request(request.get_data(), request.headers):
    return make_response("invalid request", 403)
  info = request.form

  clickbait_title = chat_gpt_request()

  try:
    response = slack_client.chat_postMessage(
      channel='#{}'.format(info["channel_name"]), 
      text=Slash(clickbait_title).getMessage()
    )#.get()
  except SlackApiError as e:
    logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
    logging.error(e.response)
    return make_response("", e.response.status_code)

  return make_response("", response.status_code)

def generate_prompt():
    return "Generate a random clickbait title."

# Start the Flask server
if __name__ == "__main__":

  SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
  SLACK_SIGNATURE = os.environ['SLACK_SIGNATURE']
  slack_client = WebClient(SLACK_BOT_TOKEN)
  verifier = SignatureVerifier(SLACK_SIGNATURE)

  app.run()