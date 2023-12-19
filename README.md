# FFmpeg TikTok Formatter
This project takes a widescreen or vertical clip and adds another clip so that it can be uploaded to TikTok, or any short-form content site, in a format that helps it retain attention longer.

This repo is similar to the [TikTokClipReup](http://github.com/Geeoon/TikTokClipReup) repo, but uses FFmpeg directly through the ffmpy Python wrapper.

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
```
usage: video_formatter [-h] [-l SUBTITLE_PATH] [-k] [-a] [-o OFFSET] [-s] [--video_bitrate VIDEO_BITRATE] [--audio_bitrate AUDIO_BITRATE]
                       [--preset PRESET] [-f FONT_SIZE] [--fps FPS] [--whisper_model WHISPER_MODEL] [--max_words MAX_WORDS]
                       [--set_dimensions SET_DIMENSIONS SET_DIMENSIONS]
                       primary_video secondary_video

positional arguments:
  primary_video         The path to the primary video. This video will be the one used to make automatic subtitles and will be the output audio. Must be
                        an mp4.
  secondary_video       The path to the secondary video. Must be an mp4.

options:
  -h, --help            show this help message and exit
  -l SUBTITLE_PATH, --subtitle_path SUBTITLE_PATH
                        The path to the .srt subtitles file. If this is used, the `-a` flag will be ignored.
  -k, --horizontal      Make a horizontally stacked video.
  -a, --automatic_subtitles
                        Automatically generate subtitles.
  -o OFFSET, --offset OFFSET
                        Offset primary video size by a number of pixels. Can be negative. If used with `-s`, it will control the secondary video.
  -s, --swap            Swap the primary and secondary vidoes, but keep everything else the same.
  --video_bitrate VIDEO_BITRATE
                        The bitrate of the ouput video. `2M` by default
  --audio_bitrate AUDIO_BITRATE
                        The bitrate of the output audio. `192k` by default
  --preset PRESET       The FFmpeg video encoding preset. `medium` by default.
  -f FONT_SIZE, --font_size FONT_SIZE
                        The subtitle font size, defaults to 16
  --fps FPS             The output video frame rate, defaults to 30.
  --whisper_model WHISPER_MODEL
                        The OpenAI Whisper model to use. Defaults to `base`.
  --max_words MAX_WORDS
                        The maximum number of words per line when automatically generating subtitles.
  --set_dimensions SET_DIMENSIONS SET_DIMENSIONS
                        The dimensions of the output video, width x height. Default is 1080 1920
```
