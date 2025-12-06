import subprocess
import sys
import os
import shutil
import json
import time
import signal
import atexit

def get_codec_info(input_file, ffmpeg_path="ffmpeg"):
    """
    Returns a dictionary with video and audio codec info using ffprobe.
    """
    # Use ffprobe from the same dir as ffmpeg if possible
    ffprobe_cmd = "ffprobe"
    if os.path.isabs(ffmpeg_path):
        possible_ffprobe = os.path.join(os.path.dirname(ffmpeg_path), "ffprobe")
        if os.path.exists(possible_ffprobe):
            ffprobe_cmd = possible_ffprobe

    cmd = [
        ffprobe_cmd,
        "-v", "error",
        "-show_entries", "stream=index,codec_name,codec_type",
        "-of", "json",
        input_file
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        video_codec = None
        audio_codec = None
        
        for stream in data.get("streams", []):
            if stream["codec_type"] == "video" and not video_codec:
                video_codec = stream["codec_name"]
            elif stream["codec_type"] == "audio" and not audio_codec:
                audio_codec = stream["codec_name"]
                
        return video_codec, audio_codec
    except Exception as e:
        print(f"Warning: Could not analyze codecs: {e}")
        return None, None

def play_mkv(input_file):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    # Generate temp file path
    filename = os.path.basename(input_file)
    name, _ = os.path.splitext(filename)
    # Use /tmp for temporary storage to avoid cluttering user's folder
    temp_dir = "/tmp" 
    output_file = os.path.join(temp_dir, f"{name}_{int(time.time())}.mov")

    # Cleanup old temp files (older than 1 hour)
    try:
        current_time = time.time()
        for f in os.listdir(temp_dir):
            if f.endswith(".mov") and "_" in f:
                # Check if it looks like our file (timestamp at end)
                parts = f.rsplit("_", 1)
                if len(parts) == 2 and parts[1].replace(".mov", "").isdigit():
                    file_path = os.path.join(temp_dir, f)
                    # Delete if older than 1 hour (3600 seconds)
                    if os.path.getmtime(file_path) < current_time - 3600:
                        try:
                            os.remove(file_path)
                            print(f"Cleaned up old temp file: {f}")
                        except OSError:
                            pass
    except Exception as e:
        print(f"Warning: Cleanup failed: {e}")

    # Check for bundled ffmpeg
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bundled_ffmpeg = os.path.join(script_dir, "ffmpeg")
    
    if os.path.exists(bundled_ffmpeg):
        ffmpeg_cmd = bundled_ffmpeg
    elif shutil.which("ffmpeg"):
        ffmpeg_cmd = "ffmpeg"
    else:
        print("Error: ffmpeg is not installed or not in PATH.")
        return

    print(f"Analyzing '{filename}'...")
    video_codec, audio_codec = get_codec_info(input_file, ffmpeg_cmd)
    print(f"Detected: Video={video_codec}, Audio={audio_codec}")

    # Build ffmpeg command
    cmd = [ffmpeg_cmd, "-i", input_file]

    # Video handling
    if video_codec == "hevc":
        # HEVC needs hvc1 tag for QuickTime
        print("Applying HEVC fix (hvc1 tag)...")
        cmd.extend(["-c:v", "copy", "-tag:v", "hvc1"])
    elif video_codec in ["h264", "prores", "mjpeg"]:
        cmd.extend(["-c:v", "copy"])
    else:
        # Unsupported video (vp9, av1, etc) -> Transcode
        # ultrafast preset for speed
        print(f"Unsupported video codec '{video_codec}'. Transcoding to h264 (this may take time)...")
        cmd.extend(["-c:v", "libx264", "-preset", "ultrafast"])

    # Audio handling
    # QuickTime supports: aac, ac3, eac3, pcm, mp3, alac
    if audio_codec in ["aac", "ac3", "eac3", "mp3", "alac", "pcm_s16le", "pcm_s24le"]:
        cmd.extend(["-c:a", "copy"])
    else:
        # Unsupported audio (dts, vorbis, flac, opus) -> Transcode to AAC
        print(f"Unsupported audio codec '{audio_codec}'. Transcoding to AAC...")
        cmd.extend(["-c:a", "aac", "-b:a", "192k"])

    # Drop subtitles (often cause issues in MOV)
    cmd.append("-sn")

    # Output options
    # -y: overwrite
    # -movflags +faststart: optimize for playback (though less critical for local file)
    cmd.extend(["-y", "-movflags", "+faststart", "-loglevel", "warning", output_file])

    print(f"Converting to temporary file: {output_file}")
    print("Please wait...")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Error: Conversion failed.")
        if os.path.exists(output_file):
            os.remove(output_file)
        return

    print("Conversion complete. Opening QuickTime Player...")
    subprocess.run(["open", "-a", "QuickTime Player", output_file])

    print("\n" + "="*40)
    print(f"Playing: {filename}")
    print(f"Temp file created at: {output_file}")
    print("="*40)
    # We exit immediately so no Terminal window is needed. 
    # The file is in /tmp and will be cleaned up by the OS eventually.

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 play_mkv.py <mkv_file>")
    else:
        play_mkv(sys.argv[1])
