import math
import whisper
from ffmpy import FFmpeg

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
INPUT_FILE_DIRECTORY = "test_files"
OUTPUT_FILE_NAME = 'output.mp4'
PRIMARY_FILE_NAME= 'primary_speech.mp4'
SECONDARY_FILE_NAME='secondary.mp4'
VIDEO_BITRATE = '512k'
AUDIO_BITRATE= '192k'
ADDITIONAL_LENGTH = 300  # pixels of additional width/height for a primary video, can be negative


# model = whisper.load_model("tiny.en")


# vertical video
ff = FFmpeg(
    inputs={f'{INPUT_FILE_DIRECTORY}/{PRIMARY_FILE_NAME}': '-y -r 30', f'{INPUT_FILE_DIRECTORY}/{SECONDARY_FILE_NAME}': '-r 30'},
    outputs={   f'{OUTPUT_FILE_NAME}': f'-shortest -filter_complex " \
                [0]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) + ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [primary]; \
                [1]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) - ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [secondary]; \
                [primary][secondary] vstack=inputs=2 [outv];" \
                -map [outv]:v -map 0:a -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE}'}
)

# horizontal video
# ff = FFmpeg(
#     inputs={f'{INPUT_FILE_DIRECTORY}/{PRIMARY_FILE_NAME}': '-y', f'{INPUT_FILE_DIRECTORY}/{SECONDARY_FILE_NAME}': None},
#     outputs={   f'{OUTPUT_FILE_NAME}': f'-shortest -filter_complex " \
#                 [0]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={math.trunc(OUTPUT_WIDTH / 2) + ADDITIONAL_LENGTH}:{math.trunc(OUTPUT_HEIGHT / 2)} [primary]; \
#                 [1]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={math.trunc(OUTPUT_WIDTH / 2) - ADDITIONAL_LENGTH}:{math.trunc(OUTPUT_HEIGHT / 2)} [secondary]; \
#                 [primary][secondary] hstack=inputs=2 [combined]; \
#                 [combined]pad=w={OUTPUT_WIDTH}:h={OUTPUT_HEIGHT}:y=(oh-ih)/2:color=black [outv];" \
#                 -map [outv]:v -map 0:a -r 30 -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE}'}
# )

print(ff.cmd)

ff.run()