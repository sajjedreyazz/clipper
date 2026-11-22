# Clipper

Turns a long speech video into short vertical clips with burned-in captions. Runs fully on your own computer.

## What it does
1. Transcribes the video's speech (faster-whisper)
2. Picks the 3 best moments, starting and ending on full sentences
3. Cuts them into vertical 9:16 clips with captions (FFmpeg)

## Requirements
- Python 3.12
- FFmpeg
- `pip install faster-whisper "av==18.1.0"`

## Usage
1. Put your video in the folder as `input.mp4`
2. Run `python transcribe.py`
3. Run `python shorts_en.py`
4. Your clips appear as `final_1.mp4`, `final_2.mp4`, `final_3.mp4`

## Notes
- Works best on talking-head videos such as interviews and lectures
- Processing is slow on weak laptops, so a 3 to 5 minute video is a good start