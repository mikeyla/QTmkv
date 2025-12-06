import plistlib
import os
import sys

if len(sys.argv) > 1:
    plist_path = sys.argv[1]
else:
    plist_path = "QTmkv.app/Contents/Info.plist"

with open(plist_path, 'rb') as f:
    plist = plistlib.load(f)

# Add MKV document type
plist['CFBundleDocumentTypes'] = [
    {
        'CFBundleTypeExtensions': ['mkv'],
        'CFBundleTypeIconFile': 'AppIcon',
        'CFBundleTypeName': 'Matroska Video File',
        'CFBundleTypeRole': 'Viewer',
        'LSHandlerRank': 'Alternate'
    }
]

# Ensure icon file is set
plist['CFBundleIconFile'] = 'AppIcon'

with open(plist_path, 'wb') as f:
    plistlib.dump(plist, f)
