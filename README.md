# TempoTweak - Video Frame Rate Converter

A simple Python GUI application for modifying the frame rate (FPS) of video files.

*Inspired by the Ekko and Jinx dancing scene at 4fps - sometimes you just need to see things at different frame rates! 😄*

## Features

- **User-friendly GUI**: Built with tkinter for easy interaction
- **Video format support**: Supports MP4, AVI, MOV, MKV, WMV, FLV, WebM, and M4V formats
- **Custom FPS**: Enter any desired frame rate or use quick-select buttons (24, 30, 60, 120)
- **Video information**: Display current video duration, FPS, and resolution
- **Progress tracking**: Real-time progress bar during video processing
- **Smart naming**: Automatically names output files as `originalfilename_fps.extension`
- **Overwrite protection**: Warns before overwriting existing files

## Sample Results

### Before and After Comparison

Check out the `samples/` folder to see TempoTweak in action:

**Original Video (test.mp4)**
- File: `samples/test.mp4`
- Original FPS: 30fps
- Smooth, natural motion

**After Processing (test_4fps.mp4)**
- File: `samples/test_4fps.mp4` 
- Modified FPS: 4fps
- Choppy, artistic stop-motion effect

*The dramatic difference in frame rate creates unique visual effects - perfect for artistic expression, meme creation, or just experimenting with different visual styles! 🎬*

## Project Structure

```
TempoTweak/
├── tempo_tweak.py          # Main application
├── requirements.txt        # Dependencies
├── README.md              # This file
└── samples/               # Sample videos demonstrating the effect
    ├── test.mp4           # Original video sample (30fps)
    └── test_4fps.mp4      # 4fps converted sample
```

## Requirements

- Python 3.6 or higher
- moviepy library
- tkinter (usually included with Python)

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python tempo_tweak.py
   ```

2. **Select Input Video**: Click "Browse" to choose your video file
3. **Select Output Folder**: Click "Browse" to choose where to save the converted video
4. **Set Target FPS**: Enter the desired frame rate or click one of the preset buttons
5. **Start Processing**: Click "Start Processing" to begin the conversion

The output file will be saved with the format: `originalfilename_targetfps.extension`

For example: `video.mp4` converted to 30 FPS becomes `video_30fps.mp4`

## Supported Video Formats

- MP4 (recommended)
- AVI
- MOV
- MKV
- WMV
- FLV
- WebM
- M4V

## Notes

- The application uses the moviepy library for video processing
- Processing time depends on video length, resolution, and target FPS
- The application maintains video quality while changing the frame rate
- You can cancel processing at any time using the "Cancel" button

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed correctly
2. Ensure the input video file is not corrupted
3. Check that you have write permissions for the output folder
4. For large video files, processing may take considerable time

## License

This project is open source and available under the MIT License.
