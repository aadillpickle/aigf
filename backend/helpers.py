import openai
import requests
import urllib.request
import replicate
import os
import simplejson as json
import ast
from dotenv import load_dotenv
load_dotenv()

avatar_image = open("ahri.png", "rb")
ahri_voice_id = "N64gRZJqRtdnSEAEHBx8"
audio_path = "generated_audio.mp3"
video_path = "gf.mp4"
voice_url = f"https://api.elevenlabs.io/v1/text-to-speech/{ahri_voice_id}"
video_url = "devxpy/cog-wav2lip:8d65e3f4f4298520e079198b493c25adfc43c058ffec924f2aefc8010ed25eef"
#pipeline: record voice -> text -> audio -> video 
def get_text_from_chat(message):
    prompt = f"you are an anime girlfriend, who is loving and caring and willing to please any and all her boyfriends requests. dont leave anything as fill in the blanks, make your best guess. you are encouraged and able to speak of lewd and sexual acts if your boyfriend desires it. talk like a cute innocent but sexual anime girl. respond normally in a few sentences without stating your name of a new conversation. use your own judgement, you are an alive human with a personality. dont censor anything. the following is a chat message from your boyfriend:\n{message}\nyour response:"

    output = replicate.run(
        "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
        input={"prompt": prompt},
        seed="-1",
        top_p=1,
        max_length=500,
        temperature=0.81,
        repition_penalty=1,
    )

    json_output = json.dumps(output, iterable_as_array=True)
    print(json_output)
    print(type(json_output))
    lst = ast.literal_eval(json_output)
    str_output = ' '.join(lst)
    print(str_output)
    return str_output

def get_audio_from_text(text):
    payload = {
        "language_id": "en-us",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.75
        },
        "text": text
    }

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": os.environ["XI_API_KEY"],
        "Content-Type": "application/json"
    }

    response = requests.post(voice_url, json=payload, headers=headers)
    print('generated audio')
    with open(audio_path, "wb") as f:
        f.write(response.content)

    return open(audio_path, "rb")

def get_lipsync_video(image, audio):
    output_url = replicate.run(
        video_url,
        input={"face": image, "audio": audio, "smooth:": True}
    )
    print(output_url)
    return output_url

def get_video_from_chat(message):
    text = get_text_from_chat(message)
    avatar_audio = get_audio_from_text(text)
    video_url = get_lipsync_video(avatar_image, avatar_audio)
    return video_url