import math
import whisper
from whisper.utils import get_writer
import os, tempfile
from datetime import timedelta
from ffmpy import FFmpeg

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
INPUT_FILE_DIRECTORY = "test_files"
OUTPUT_FILE_NAME = 'output.mp4'
PRIMARY_FILE_NAME= 'primary_speech.mp4'
SECONDARY_FILE_NAME= 'secondary.mp4'
VIDEO_BITRATE = '2M'
AUDIO_BITRATE= '192k'
ADDITIONAL_LENGTH = 0  # pixels of additional width/height for a primary video, can be negative
NO_SPEECH_THRESHOLD = 0.6  # default 0.6
FONT_SIZE = 15
OUTPUT_FPS = 30
RENDERING_PRESET = 'ultrafast'  # medium by default
MAX_WORDS_PER_LINE = 3  # 0 for default/off, 3 is good for short action events, but not good for slower dialogue
IS_ENGLISH = True  # not used, for now


# grab audio
ff = FFmpeg(
    inputs={f'{INPUT_FILE_DIRECTORY}/{PRIMARY_FILE_NAME}': '-y'},
    outputs={f'{PRIMARY_FILE_NAME[:-4]}_audio.mp3': '-q:a 0 -map a -preset fast'}
)
ff.run()


# generate subtitles
model = whisper.load_model("base.en")
audio = whisper.load_audio(f'{PRIMARY_FILE_NAME[:-4]}_audio.mp3')
# word timestamps must be true for max word length
result = whisper.transcribe(model, audio, no_speech_threshold=NO_SPEECH_THRESHOLD, word_timestamps=(MAX_WORDS_PER_LINE != 0))

# create subtitle file
srt_writer = get_writer(output_format="srt", output_dir="./")
srt_writer(result, f'{PRIMARY_FILE_NAME[:-4]}_audio.mp3', {"max_words_per_line": MAX_WORDS_PER_LINE})


# vertical video
ff = FFmpeg(
    inputs={f'{INPUT_FILE_DIRECTORY}/{PRIMARY_FILE_NAME}': '-y', f'{INPUT_FILE_DIRECTORY}/{SECONDARY_FILE_NAME}': None},
    outputs={   f'{OUTPUT_FILE_NAME}': f'-shortest -filter_complex " \
                [0] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) + ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [primary]; \
                [primary] subtitles={PRIMARY_FILE_NAME[:-4]}_audio.srt:force_style=\'Fontsize={FONT_SIZE},PrimaryColor=&H00000FF&\' [subtitled]; \
                [1] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) - ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [secondary]; \
                [subtitled][secondary] vstack=inputs=2 [outv];" \
                -map [outv]:v -map 0:a -r {OUTPUT_FPS} -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE} -preset {RENDERING_PRESET}'}
)

# horizontal video
# ff = FFmpeg(
#     inputs={f'{INPUT_FILE_DIRECTORY}/{PRIMARY_FILE_NAME}': '-y', f'{INPUT_FILE_DIRECTORY}/{SECONDARY_FILE_NAME}': None},
#     outputs={   f'{OUTPUT_FILE_NAME}': f'-shortest -filter_complex " \
#                 [0] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={math.trunc(OUTPUT_WIDTH / 2) + ADDITIONAL_LENGTH}:{math.trunc(OUTPUT_HEIGHT / 2)} [primary]; \
#                 [1] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={math.trunc(OUTPUT_WIDTH / 2) - ADDITIONAL_LENGTH}:{math.trunc(OUTPUT_HEIGHT / 2)} [secondary]; \
#                 [primary][secondary] hstack=inputs=2 [combined]; \
#                 [combined] pad=w={OUTPUT_WIDTH}:h={math.trunc(OUTPUT_HEIGHT / 2) + 10 * FONT_SIZE}:y=(oh-ih)/2:color=black [padded]; \
#                 [padded] subtitles={PRIMARY_FILE_NAME[:-4]}_audio.srt:force_style=\'Alignment=2,MarginV=0,MarginL=0,Fontsize={FONT_SIZE},PrimaryColor=&H00000FF&\' [subtitled]; \
#                 [subtitled] pad=w={OUTPUT_WIDTH}:h={OUTPUT_HEIGHT}:y=(oh-ih)/2:color=black [final];" \
#                 -map [final]:v -map 0:a -r {OUTPUT_FPS} -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE} -preset {RENDERING_PRESET}'}
# )

print(ff.cmd)
ff.run()
