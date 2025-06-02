# Video to ASCII Art Converter

A Python-based tool that transforms video files into ASCII/character art animations. Perfect for creative visualizations, terminal demos, or retro-style effects.

## ✨ Features
- **Video Conversion**: Convert any video file (e.g., MP4) into ASCII character art.
- **Customizable Output**: Adjust frame size, character density, and effects.
- **Effects**:
  - ☑️ High Contrast
  - ☑️ Edge Detection
  - ☑️ Colored Pencil Style
- **Time Control**: Select specific start/end times for partial conversion.

## 🛠️ Installation
1. **Requirements**:
   - Python 3.8+
   - Libraries: OpenCV (`opencv-python`), Pillow (`PIL`), NumPy (`numpy`)
   ```bash
   pip install opencv-python pillow numpy
   ```

2. **Download**:
   Clone this repository or download the `Bin/app.exe` (pre-built executable for Windows).

## 🚀 Usage
1. **Run the Tool**:
   - **For Python**: Execute `src/app.py`.
   - **For Executable**: Double-click `Bin/app.exe`.

2. **GUI Instructions**:
   - **Input Video**: Click *"Select File"* to choose a video (e.g., `MyGO.mp4`).
   - **Output Path**: Specify where to save the ASCII art video.
   - **Settings**:
     - **Frame Size**: Adjust `Overall Canvas Size` (4 = compact, 10 = detailed).
     - **Character Size**: Pixel-to-char ratio (`5` is balanced).
     - **Effects**: Toggle checkboxes for visual styles.
   - **Time Range**: Set `Start/End Time (seconds)` to convert a clip.
   - **Convert**: Click *"Start Conversion"*.

## 📂 Project Structure
```
Character_drawing/
├── Asset/               # Video/icon resources (e.g., saber.ico)
├── Bin/                 # Output executable (app.exe)
├── src/                 # Source code
│   ├── app.py           # Main GUI script
│   ├── filters.py       # Image effect algorithms
│   └── ...
└── app.spec             # PyInstaller configuration
```

## ❓ FAQ
**Q: Why is the output video laggy?**  
A: Reduce `Canvas Size` or shorten the time range for faster processing.

**Q: How to add custom characters?**  
Modify `src/filters.py` → `ASCII_CHARS` variable (e.g., `@#%&*`).

## 📜 License
MIT License. Feel free to modify and distribute.