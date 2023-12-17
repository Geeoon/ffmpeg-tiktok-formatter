import ffmpeg

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
ASPECT_RATIO = OUTPUT_WIDTH / OUTPUT_HEIGHT

primary_vid = ffmpeg.input('test_files/primary.mp4')
secondary_vid = ffmpeg.input('test_files/secondary.mp4')
