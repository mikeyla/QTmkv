#!/bin/bash
set -e

# Configuration
APP_NAME="QTmkv"
BUILD_DIR="build"
SRC_DIR="src"
SCRIPTS_DIR="scripts"
ASSETS_DIR="assets"

# Clean previous build
echo "Cleaning build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Compile AppleScript
echo "Compiling AppleScript..."
osacompile -o "$BUILD_DIR/$APP_NAME.app" "$SRC_DIR/$APP_NAME.applescript"

# Copy Resources
echo "Copying resources..."
cp "$SRC_DIR/play_mkv.py" "$BUILD_DIR/$APP_NAME.app/Contents/Resources/"

# Check for ffmpeg/ffprobe in root or system
if [ -f "ffmpeg" ]; then
    cp "ffmpeg" "$BUILD_DIR/$APP_NAME.app/Contents/Resources/"
elif [ -f "/opt/homebrew/bin/ffmpeg" ]; then
    cp "/opt/homebrew/bin/ffmpeg" "$BUILD_DIR/$APP_NAME.app/Contents/Resources/"
else
    echo "Error: ffmpeg not found. Please place it in the root directory."
    exit 1
fi

if [ -f "ffprobe" ]; then
    cp "ffprobe" "$BUILD_DIR/$APP_NAME.app/Contents/Resources/"
elif [ -f "/opt/homebrew/bin/ffprobe" ]; then
    cp "/opt/homebrew/bin/ffprobe" "$BUILD_DIR/$APP_NAME.app/Contents/Resources/"
else
    echo "Error: ffprobe not found. Please place it in the root directory."
    exit 1
fi

# Make binaries executable
chmod +x "$BUILD_DIR/$APP_NAME.app/Contents/Resources/ffmpeg"
chmod +x "$BUILD_DIR/$APP_NAME.app/Contents/Resources/ffprobe"

# Generate Icon
echo "Generating Icon..."
bash "$SCRIPTS_DIR/make_icon_v2.sh" "$ASSETS_DIR/icon.png" "$BUILD_DIR/QTmkv.iconset"
iconutil -c icns "$BUILD_DIR/QTmkv.iconset" -o "$BUILD_DIR/$APP_NAME.app/Contents/Resources/AppIcon.icns"
rm -rf "$BUILD_DIR/QTmkv.iconset"

# Update Info.plist
echo "Updating Info.plist..."
python3 "$SRC_DIR/update_plist.py" "$BUILD_DIR/$APP_NAME.app/Contents/Info.plist"

# Sign App
echo "Signing App..."
xattr -cr "$BUILD_DIR/$APP_NAME.app"
codesign --force --deep --sign - "$BUILD_DIR/$APP_NAME.app"

# Create DMG
echo "Creating DMG..."
# We need to pass the app path and background image to the DMG script
# Or we can just run the DMG script and let it handle things if we set it up right.
# Let's modify create_dmg.sh to accept arguments or variables.
# For now, I'll call it with environment variables.
export APP_PATH="$BUILD_DIR/$APP_NAME.app"
export BG_IMAGE="$ASSETS_DIR/right_arrow.png"
export OUTPUT_DMG="$APP_NAME""_Installer.dmg"

bash "$SCRIPTS_DIR/create_dmg.sh"

echo "Build Complete!"
