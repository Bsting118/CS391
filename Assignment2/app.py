#================================#
# CS-391: Assignment 2
# Brendan Sting
# Kettering University
#================================#

from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, render_template # New imports to support web app version

import config
import json

client = OpenAI(api_key=config.OPENAI_API_KEY) # ADD YOUR OWN CONFIG.PY IN SAME DIRECTORY AS APP.PY, WITH AN OPENAI_API_KEY VAR THAT HAS YOUR API KEY!
app = Flask(__name__) # Add a Flask instance

def ask_chatgpt(messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return (response.choices[0].message.content)

# Download the transcript from the YouTube video (transformed into method)
def process_URL_for_transcript_list(videoID):
    transcript_list = YouTubeTranscriptApi.list_transcripts(videoID)
    return transcript_list

# Transformed text processing of transcript list to method:
def parse_transcript_list_to_text(transcriptList):
    transcript = transcriptList.find_generated_transcript(['en']).fetch()
    # Read/Extract the transcript and concatenate all text elements
    concatenated_text = " ".join(item['text'] for item in transcript)
    return concatenated_text

# Transformed system prompting to method:
def assist_with_youtube_summary(parsedTranscriptText):
    # Call the openai ChatCompletion endpoint, with the ChatGPT model
    msgs=[
        {"role": "system", "content":"You are a helpful assistant."},
        {"role": "user", "content": "Summarize the following text."},
        {"role": "assistant", "content": "Yes."},
        {"role": "user", "content": parsedTranscriptText}
    ]
    return ask_chatgpt(msgs)

# Helper method provided by ChatGPT:
def extract_substring(input_string):
    delimiter = "?v="
    start_index = input_string.find(delimiter)
    
    if start_index != -1:
        return input_string[start_index + len(delimiter):]
    else:
        return None

# Method to return final transcript summary string:
def onSubmitButtonPressed():
    inputString = request.form["URL"]
    inputVideoID = extract_substring(inputString)
    inputTranscriptList = process_URL_for_transcript_list(inputVideoID)
    parsedInpTranscriptText = parse_transcript_list_to_text(inputTranscriptList)
    response = assist_with_youtube_summary(parsedInpTranscriptText)
    return response


# Add an index route:
@app.route("/")
def index():
    return render_template("index.html")

# Add a submit route:
@app.route("/submit", methods=["POST"])
def submit():
    ai_response = onSubmitButtonPressed()

    # Render the AI response into the context of {{article}} placeholder
    return render_template("index.html", transcript=ai_response)

# Main method check:
if __name__ == "__main__":
    app.run()