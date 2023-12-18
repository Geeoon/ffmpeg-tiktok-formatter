# FFmpeg TikTok Formatter
This project takes a widescreen or vertical clip and adds another clip so that it can be uploaded to TikTok, or any short-form content site, in a format that helps it retain attention longer.

This repo is similar to the [TikTokClipReup](github.com/Geeoon/TikTokClipReup) repo, but uses FFmpeg directly through the ffmpy Python wrapper.

## Dependencies:
Use the following command to install all the dependencies:

`sudo apt update && sudo apt install ffmpeg && pip install -U openai-whisper ffmpy`

Alternatively, you can use pip to install the packages from the `requirements.txt` file.  In the base directory, run:

`pip install -r requirements.txt`

## Usage
To create videos, use the command line interface.
### Basic Usage
`main.py <primary_video> <secondary_video>`

This will create a simple vertical video with no subtitles.
### Advanced Usage
`main.py <primary_video> <secondary_video> [subtitle_path] [options]`

`primary_video, required` The path to the primary video. This video will be the one used to make automatic subtitles and will be the output audio.  Must be an mp4.

`secondary_video, required` The path to the secondary video.  Must be an mp4.

`subtitle_path, optional` The path to the .srt subtitles file. If this is used, the `-a` flag will be ignored.

`-h, --horizontal` Make a horizontally stacked video.

`-a, --automatic` Automatically generate subtitles.

`-o, --offset <number>` Offset primary video size by a number of pixels. Can be negative. If used with `-s`, it will control the secondary video.

`-s, --swap` Swap the primary and secondary vidoes, but keep everything else the same.

`--video_bitrate <bitrate>` The bitrate of the ouput video. `2M` by default

`--audio_bitrate <bitrate>` The bitrate of the output audio. `192k` by default

`--preset <setting>` The FFmpeg video encoding preset. `medium` by default.

`-f, --font_size <size>` The subtitle font size.

`--fps <frame_rate>` The output video frame rate.

`--whisper_model <model>` The OpenAI Whisper model to use. Default is `base`.

`--max_words <number>` The maximum number of words per line when automatically generating subtitles.