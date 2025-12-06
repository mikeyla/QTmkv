APP_NAME="QTmkv"
DMG_NAME="${OUTPUT_DMG:-QTmkv_Installer.dmg}"
VOL_NAME="QTmkv Installer"
BG_IMAGE="${BG_IMAGE:-../assets/right_arrow.png}"
APP_SOURCE="${APP_PATH:-../QTmkv.app}"

# Prepare source folder
rm -rf dmg_root
mkdir dmg_root
cp -r "$APP_SOURCE" dmg_root/
ln -s /Applications dmg_root/Applications
mkdir dmg_root/.background
cp "$BG_IMAGE" dmg_root/.background/background.png

# Create temporary RW DMG
rm -f temp.dmg
hdiutil create -srcfolder dmg_root -volname "$VOL_NAME" -fs HFS+ -fsargs "-c c=64,a=16,e=16" -format UDRW -ov temp.dmg

# Mount it
DEVICE=$(hdiutil attach -readwrite -noverify -noautoopen "temp.dmg" | egrep '^/dev/' | sed 1q | awk '{print $1}')

# Wait a bit for mounting
sleep 2

# AppleScript to set view options
echo "Setting view options..."
osascript <<EOF
tell application "Finder"
    tell disk "$VOL_NAME"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {400, 100, 1000, 500}
        set theViewOptions to the icon view options of container window
        set arrangement of theViewOptions to not arranged
        set icon size of theViewOptions to 128
        set background picture of theViewOptions to file ".background:background.png"
        
        -- Create alias if it doesn't exist (it should from the ln -s, but Finder sees it as a file)
        -- We just position the items
        
        -- Wait for Finder to update
        delay 1
        
        set position of item "${APP_NAME}" of container window to {100, 150}
        set position of item "Applications" of container window to {500, 150}
        
        close
        open
        update without registering applications
        delay 1
        close
    end tell
end tell
EOF

# Unmount
hdiutil detach "$DEVICE"

# Convert to final compressed DMG
rm -f "$DMG_NAME"
hdiutil convert "temp.dmg" -format UDZO -imagekey zlib-level=9 -o "$DMG_NAME"

# Clean up
rm -f temp.dmg
rm -rf dmg_root
