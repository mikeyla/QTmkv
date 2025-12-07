import plistlib
import os
import sys

if len(sys.argv) > 1:
    plist_path = sys.argv[1]
else:
    plist_path = "QTmkv.app/Contents/Info.plist"

with open(plist_path, 'rb') as f:
    plist = plistlib.load(f)

# Ensure basic keys
plist['CFBundleName'] = 'QTmkv'
plist['CFBundleDisplayName'] = 'QTmkv'
plist['CFBundleShortVersionString'] = '1.1'
plist['CFBundleVersion'] = '1.1'

# Add MKV document type with UTType
plist['CFBundleDocumentTypes'] = [
    {
        'CFBundleTypeExtensions': ['mkv'],
        'CFBundleTypeIconFile': 'AppIcon',
        'CFBundleTypeName': 'Matroska Video File',
        'CFBundleTypeRole': 'Editor',
        'CFBundleTypeMIMETypes': ['video/x-matroska', 'video/mkv'],
        'LSHandlerRank': 'Owner',
        'LSItemContentTypes': [
            'org.matroska.mkv',
            'public.movie',
            'public.video',
            'public.audiovisual-content',
            'public.data'
        ]
    }
]

# Add UTImportedTypeDeclarations (Imported, not Exported, to avoid conflict with VLC)
plist['UTImportedTypeDeclarations'] = [
    {
        'UTTypeIdentifier': 'org.matroska.mkv',
        'UTTypeDescription': 'Matroska Video File',
        'UTTypeConformsTo': ['public.movie', 'public.video', 'public.audiovisual-content'],
        'UTTypeTagSpecification': {
            'public.filename-extension': ['mkv'],
            'public.mime-type': ['video/x-matroska', 'video/mkv']
        },
        'UTTypeIconFile': 'AppIcon'
    }
]

# Remove Exported types if present (to be safe)
if 'UTExportedTypeDeclarations' in plist:
    del plist['UTExportedTypeDeclarations']

# Ensure icon file is set
plist['CFBundleIconFile'] = 'AppIcon'

with open(plist_path, 'wb') as f:
    plistlib.dump(plist, f)
