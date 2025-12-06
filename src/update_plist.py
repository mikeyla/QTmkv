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
# Add MKV document type with UTType
plist['CFBundleDocumentTypes'] = [
    {
        'CFBundleTypeExtensions': ['mkv'],
        'CFBundleTypeIconFile': 'AppIcon',
        'CFBundleTypeName': 'Matroska Video File',
        'CFBundleTypeRole': 'Viewer',
        'LSHandlerRank': 'Owner',
        'LSItemContentTypes': ['org.matroska.mkv']
    }
]

# Add UTExportedTypeDeclarations to define the type
plist['UTExportedTypeDeclarations'] = [
    {
        'UTTypeIdentifier': 'org.matroska.mkv',
        'UTTypeDescription': 'Matroska Video File',
        'UTTypeConformsTo': ['public.movie'],
        'UTTypeTagSpecification': {
            'public.filename-extension': ['mkv'],
            'public.mime-type': ['video/x-matroska']
        },
        'UTTypeIconFile': 'AppIcon'
    }
]

# Ensure icon file is set
plist['CFBundleIconFile'] = 'AppIcon'

with open(plist_path, 'wb') as f:
    plistlib.dump(plist, f)
