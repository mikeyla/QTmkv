# QTmkv

**QTmkv** is a lightweight macOS application that allows you to play MKV files natively in QuickTime Player.

It works by acting as a "launcher" that instantly remuxes (copies streams without re-encoding) the MKV file into a temporary QuickTime-compatible container (`.mov`) and opening it. This process is usually near-instantaneous.

## Features

*   **Native Playback**: Uses QuickTime Player for playback.
*   **Instant Start**: Uses `ffmpeg` to remux streams on-the-fly.
*   **Smart Transcoding**:
    *   Automatically fixes "No Video" issues with HEVC files by applying the correct `hvc1` tag.
    *   Transcodes unsupported audio (DTS, Vorbis, etc.) to AAC while keeping video untouched.
*   **Zero Clutter**: Creates temporary files in `/tmp` and automatically cleans them up on the next launch.
*   **Standalone**: Comes bundled with `ffmpeg` and `ffprobe`, so no external dependencies are required.

## Installation

1.  Download the latest release (`QTmkv_Installer.dmg`).
2.  Open the DMG.
3.  Drag the **QTmkv** app to your **Applications** folder.

## Usage

### Set as Default Player
To make QTmkv the default player for all your MKV files:

1.  Right-click any `.mkv` file in Finder.
2.  Select **Get Info**.
3.  Under **Open with:**, select **QTmkv**.
4.  Click **Change All...**.

### Manual Use
*   **Double-click** the app to select a file.
*   **Drag and drop** an MKV file onto the app icon.

## How it Works

QTmkv is an AppleScript wrapper around a Python script.

1.  **AppleScript (`QTmkv.applescript`)**: Handles the app launch and drag-and-drop events. It executes the Python script in the background.
2.  **Python Script (`play_mkv.py`)**:
    *   Analyzes the file using bundled `ffprobe`.
    *   Constructs an optimized `ffmpeg` command.
    *   Converts the file to a temporary `.mov` in `/tmp`.
    *   Launches QuickTime Player.
    *   Performs cleanup of old temp files.

## Building from Source

Requirements:
*   macOS
*   `ffmpeg` and `ffprobe` binaries (for bundling)

Steps:
1.  Clone the repo.
2.  Place `ffmpeg` and `ffprobe` binaries in the root directory (or ensure they are in your path).
3.  Run the build script:
    ```bash
    ./build.sh
    ```
    This will compile the app, bundle the resources, and create the DMG installer in the `build/` directory.

## Troubleshooting

### App still appears in "Open With" after deleting
If you deleted the app but it still shows up in the "Open With" menu, or if macOS keeps reverting your default application choice, you may need to reset the Launch Services database.

Run this command in Terminal:
```bash
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
```
*Note: This will reset all file associations to their defaults.*

### "Damaged" or "Can't be opened" error
If you see an error saying the app is damaged, run this command to clear the quarantine attribute:
```bash
xattr -cr /Applications/QTmkv.app
```
