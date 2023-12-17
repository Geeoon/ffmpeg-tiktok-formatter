import math
import whisper
import os, tempfile
from datetime import timedelta
from ffmpy import FFmpeg

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
INPUT_FILE_DIRECTORY = "test_files"
OUTPUT_FILE_NAME = 'output.mp4'
PRIMARY_FILE_NAME= 'primary_speech.mp4'
SECONDARY_FILE_NAME= 'secondary.mp4'
VIDEO_BITRATE = '512k'
AUDIO_BITRATE= '192k'
ADDITIONAL_LENGTH = 300  # pixels of additional width/height for a primary video, can be negative
NO_SPEECH_THRESHOLD = 0.4


# grab audio
ff = FFmpeg(
    inputs={f'{INPUT_FILE_DIRECTORY}/{PRIMARY_FILE_NAME}': '-y'},
    outputs={f'{PRIMARY_FILE_NAME[:-2]}_audio.mp3': '-q:a 0 -map a'}
)
ff.run()

# generate subtitles
model = whisper.load_model("base.en")
result = model.transcribe(audio=f'{PRIMARY_FILE_NAME[:-2]}_audio.mp3', no_speech_threshold=NO_SPEECH_THRESHOLD)

srt_tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.srt')
segments = result["segments"]
for seg in segments:
    start = str(0) + str(timedelta(seconds=int(seg["start"]))) + ",000"
    end = str(0) + str(timedelta(seconds=int(seg["end"]))) + ",000"
    text = seg["text"]
    segment_id = seg["id"] + 1
    segment = f"{segment_id}\n{start} --> {end}\n{text[1:] if text[0] == ' ' else text}\n\n"
    with open(srt_tmp.name, "a", encoding="utf-8") as f:
        f.write(segment)
    srt_tmp.close()

# vertical video
ff = FFmpeg(
    inputs={f'{INPUT_FILE_DIRECTORY}/{PRIMARY_FILE_NAME}': '-y', f'{INPUT_FILE_DIRECTORY}/{SECONDARY_FILE_NAME}': None},
    outputs={   f'{OUTPUT_FILE_NAME}': f'-shortest -filter_complex " \
                [0]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) + ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [primary]; \
                [1]scale=-2:{math.trunc(OUTPUT_HEIGHT / 2) - ADDITIONAL_LENGTH}, crop={OUTPUT_WIDTH}:ih [secondary]; \
                [primary][secondary] vstack=inputs=2 [combined]; \
                [combined] subtitles={srt_tmp.name}:force_style=\'Fontsize=24,PrimaryColor=&H00000FF&\' [outv];" \
                -map [outv]:v -map 0:a -r 30 -b:a {AUDIO_BITRATE} -b:v {VIDEO_BITRATE}'}
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
    
# clean up
os.unlink(srt_tmp.name)    