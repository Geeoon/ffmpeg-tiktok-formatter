import math  # to trunacate
import uuid  # to generate unique name
import os  # to clean up files
import argparse  # to get command line arugments
import whisper  # to generate subtitles
from whisper.utils import get_writer  # to generate subtitles
from ffmpy import FFmpeg  # to use FFmpeg

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
OUTPUT_FILE_NAME = 'output.mp4'
PRIMARY_FILE_PATH = 'test_files/matrix.mp4'
SECONDARY_FILE_PATH = 'test_files/secondary.mp4'
VIDEO_BITRATE = '2M'
AUDIO_BITRATE = '192k'
ADDITIONAL_LENGTH = 0
NO_SPEECH_THRESHOLD = 0.6
FONT_SIZE = 16
OUTPUT_FPS = 30
RENDERING_PRESET = 'ultrafast'  # medium by default
MAX_WORDS_PER_LINE = 3  # 0 for default/off, 3 is good for short action events, but not good for slower dialogue
MODEL_NAME = 'base.en'
IS_HORIZONTAL = True
SUBTITLE_PATH = ''


# parser = argparse.ArgumentParser("video_formatter")
# parser.add_argument('primary_video', help='The path to the primary video. This video will be the one used to make automatic subtitles and will be the output audio.  Must be an mp4.', type=str)
# parser.add_argument('secondary_video', help='The path to the secondary video.  Must be an mp4.', type=str)
# parser.add_argument('-l', '--subtitle_path', help='The path to the .srt subtitles file. If this is used, the `-a` flag will be ignored.', type=str, default='')
# parser.add_argument('-k', '--horizontal', help='Make a horizontally stacked video.', action='store_true')
# parser.add_argument('-a', '--automatic_subtitles', help='Automatically generate subtitles.', action='store_true')
# parser.add_argument('-o', '--offset', help='Offset primary video size by a number of pixels. Can be negative. If used with `-s`, it will control the secondary video.', type=int, default=0)
# parser.add_argument('-s', '--swap', help='Swap the primary and secondary vidoes, but keep everything else the same.', action='store_true')
# parser.add_argument('--video_bitrate', help='The bitrate of the ouput video. `2M` by default', type=str, default='2M')
# parser.add_argument('--audio_bitrate', help='The bitrate of the output audio. `192k` by default', type=str, default='192k')
# parser.add_argument('--preset', help='The FFmpeg video encoding preset. `medium` by default.', type=str, default='medium')
# parser.add_argument('-f', '--font_size', help='The subtitle font size, defaults to 16', type=str, default=16)
# parser.add_argument('--fps', help='The output video frame rate, defaults to 30.', type=int, default=30)
# parser.add_argument('--whisper_model', help='The OpenAI Whisper model to use. Defaults to `base`.', type=str, default='base')
# parser.add_argument('--max_words', help='The maximum number of words per line when automatically generating subtitles.', type=int, default=0)
# parser.add_argument('--set_dimensions', help='The dimensions of the output video, width x height. Default is 1080 1920', type=int, nargs=2, default=[1080, 1920])
# args = parser.parse_args()

# OUPTUT_WIDTH = args.set_dimentions[0]
# OUPTUT_HEIGHT = args.set_dimentions[1]
# OUTPUT_FILE_NAME = 'output.mp4'
# PRIMARY_FILE_PATH = args.primary_video
# SECONDARY_FILE_PATH = args.secondary_video
# VIDEO_BITRATE = args.video_bitrate
# AUDIO_BITRATE = args.audio_bitrate
# ADDITIONAL_LENGTH = args.offset
# NO_SPEECH_THRESHOLD = 0.6
# FONT_SIZE = args.font_size
# OUTPUT_FPS = args.fps
# RENDERING_PRESET = args.preset
# MAX_WORDS_PER_LINE = args.max_words
# MODEL_NAME = args.whisper_model
# IS_HORIZONTAL = args.horizontal
# SUBTITLE_PATH = args.subtitle_path
AUTOMATIC_SUBTITLES = False

PRIMARY_FILE_DIR, PRIMARY_FILE_NAME = os.path.split(PRIMARY_FILE_PATH)
SECONDARY_FILE_DIR, SECONDARY_FILE_NAME = os.path.split(SECONDARY_FILE_PATH)


def clean_up(random):
    try:
        os.remove(f'{PRIMARY_FILE_NAME[:-4]}_{random}_audio.mp3')
    except OSError:
        pass
    
    try:
        os.remove(f'{PRIMARY_FILE_NAME[:-4]}_{random}_audio.srt')
    except OSError:
        pass


def create_audio(random):
    # grab audio
    ff = FFmpeg(
        inputs={f'{PRIMARY_FILE_PATH}': '-y'},
        outputs={f'{PRIMARY_FILE_NAME[:-4]}_{random}_audio.mp3': '-q:a 0 -map a -preset fast'}
    )
    ff.run()


def create_subtitles(model_name, random, threshold, max_words):
    # generate subtitles
    model = whisper.load_model(model_name)
    audio = whisper.load_audio(f'{PRIMARY_FILE_NAME[:-4]}_{random}_audio.mp3')
    # word timestamps must be true for max word length
    result = whisper.transcribe(model, audio, no_speech_threshold=threshold, word_timestamps=(max_words != 0))

    # create subtitle file
    srt_writer = get_writer(output_format="srt", output_dir="./")
    srt_writer(result, f'{PRIMARY_FILE_NAME[:-4]}_{random}_audio.mp3', {"max_words_per_line": max_words})


def create_vertical(random):
    output_options = f'-shortest -filter_complex " \
                    [0] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) + ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [primary];'
    if SUBTITLE_PATH != '':
        output_options += f'[primary] subtitles={PRIMARY_FILE_NAME[:-4]}_{random}_audio.srt:force_style=\'Fontsize={FONT_SIZE},PrimaryColor=&H00000FF&\' [subtitled]; \
                        [1] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) - ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [secondary]; \
                        [subtitled][secondary] vstack=inputs=2 [outv];'
    else:
        output_options += f'[1] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) - ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [secondary]; \
                        [primary][secondary] vstack=inputs=2 [outv];'
    
    output_options += f'" -map [outv]:v -map 0:a -r {OUTPUT_FPS} -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE} -preset {RENDERING_PRESET}'
    
    ff = FFmpeg(
        inputs={f'{PRIMARY_FILE_PATH}': '-y', f'{SECONDARY_FILE_PATH}': None},
        outputs={f'{OUTPUT_FILE_NAME[:-4]}_{random}.mp4': output_options}
    )
    ff.run()


def create_horizontal(random):
    output_options = f'-shortest -filter_complex " \
                    [0] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={math.trunc(OUTPUT_WIDTH / 2) + ADDITIONAL_LENGTH}:{math.trunc(OUTPUT_HEIGHT / 2)} [primary]; \
                    [1] scale=-2:{math.trunc(OUTPUT_HEIGHT / 2)}, crop={math.trunc(OUTPUT_WIDTH / 2) - ADDITIONAL_LENGTH}:{math.trunc(OUTPUT_HEIGHT / 2)} [secondary]; \
                    [primary][secondary] hstack=inputs=2 [combined];'
    
    if SUBTITLE_PATH != '':
        output_options += f'[combined] pad=w={OUTPUT_WIDTH}:h={max(0, min(OUTPUT_HEIGHT, math.trunc(OUTPUT_HEIGHT / 2) + 10 * FONT_SIZE))}:y=(oh-ih)/2:color=black [padded]; \
                        [padded] subtitles={PRIMARY_FILE_NAME[:-4]}_{random}_audio.srt:force_style=\'Alignment=2,MarginV=0,MarginL=0,Fontsize={FONT_SIZE},PrimaryColor=&H00000FF&\' [subtitled]; \
                        [subtitled] pad=w={OUTPUT_WIDTH}:h={OUTPUT_HEIGHT}:y=(oh-ih)/2:color=black [final];'
    else:
        output_options += f'[combined] pad=w={OUTPUT_WIDTH}:h={OUTPUT_HEIGHT}:y=(oh-ih)/2:color=black [final];'

    output_options += f'" -map [final]:v -map 0:a -r {OUTPUT_FPS} -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE} -preset {RENDERING_PRESET}'
    ff = FFmpeg(
        inputs={f'{PRIMARY_FILE_PATH}': '-y', f'{SECONDARY_FILE_PATH}': None},
        outputs={   f'{OUTPUT_FILE_NAME[:-4]}_{random}.mp4': output_options}
    )
    ff.run()


random_name = str(uuid.uuid4())  # used to name temp files

# TODO: Clean up code
try:
    create_audio(random_name)
    if SUBTITLE_PATH == '' and AUTOMATIC_SUBTITLES:
        create_subtitles(MODEL_NAME, random_name, NO_SPEECH_THRESHOLD, MAX_WORDS_PER_LINE)
        SUBTITLE_PATH = f'{PRIMARY_FILE_NAME[:-4]}_{random_name}_audio.srt'
    if IS_HORIZONTAL:
        print('making final cut')
        create_horizontal(random_name)
    else:
        create_vertical(random_name)
except:
    print("An error occured")
finally:
    clean_up(random_name)