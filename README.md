# FFmpeg TikTok Formatter
This project takes a widescreen or vertical clip and adds another clip so that it can be uploaded to TikTok, or any short-form content site, in a format that helps it retain attention longer.

This repo is similar to the [TikTokClipReup](github.com/Geeoon/TikTokClipReup) repo, but uses FFmpeg directly through the ffmpy Python wrapper.

## Dependencies:
Use the following command to install all the dependencies:

`sudo apt update && sudo apt install ffmpeg && pip install -U openai-whisper ffmpy`

Alternatively, you can use pip to install the packages from the `requirements.txt` file.  In the base directory, run:

`pip install -r requirements.txt`