import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


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


def generate_prompt():
    return "Generate a random clickbait title."