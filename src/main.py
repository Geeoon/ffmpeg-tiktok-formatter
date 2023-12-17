import math
from ffmpy import FFmpeg

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
ASPECT_RATIO = OUTPUT_WIDTH / OUTPUT_HEIGHT
OUTPUT_FILE_NAME = 'output.mp4'
VIDEO_BITRATE = '512k'
AUDIO_BITRATE= '192k'


# vertical video
# ff = FFmpeg(
#     inputs={'test_files/primary.mp4': '-y', 'test_files/secondary.mp4': None},
#     outputs={   'output.mp4': f'-shortest -filter_complex " \
#                 [0]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={OUTPUT_WIDTH}:ih [primary]; \
#                 [1]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={OUTPUT_WIDTH}:ih [secondary]; \
#                 [primary][secondary] vstack=inputs=2 [outv];" \
#                 -map [outv]:v -map 0:a -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE}'}
# )

# horizontal video
ff = FFmpeg(
    inputs={'test_files/primary.mp4': '-y', 'test_files/secondary.mp4': None},
    outputs={   'output.mp4': f'-shortest -filter_complex " \
                [0]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={math.trunc(OUTPUT_WIDTH / 2)}:{math.trunc(OUTPUT_HEIGHT / 2)} [primary]; \
                [1]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={math.trunc(OUTPUT_WIDTH / 2)}:{math.trunc(OUTPUT_HEIGHT / 2)} [secondary]; \
                [primary][secondary] hstack=inputs=2 [combined]; \
                [combined]pad=w={OUTPUT_WIDTH}:h={OUTPUT_HEIGHT}:y=(oh-ih)/2:color=black [outv];" \
                -map [outv]:v -map 0:a -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE}'}
)

print(ff.cmd)

ff.run()