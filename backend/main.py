from helpers import get_video_from_chat

from flask import Flask, request, Response, send_file
from flask_cors import CORS
from dotenv import load_dotenv

import os
load_dotenv()

app = Flask(__name__)
CORS(app)

PORT = os.environ.get('PORT', 8001)

@app.route('/', methods=['GET'])
def index():
	return '<h1>Server is running</h1>'

@app.route('/get-video-from-chat', methods=['POST'])
def chat_with_avatar():
    data = request.get_json()
    message = data['input']
    video_url = get_video_from_chat(message)
    return {'video_url': video_url}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=PORT, debug=True)