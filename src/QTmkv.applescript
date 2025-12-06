use AppleScript version "2.4"
use scripting additions

on run
	try
		set theFile to choose file with prompt "Select an MKV file to play:" of type {"mkv"}
		processFile(POSIX path of theFile)
	on error
		return
	end try
end run

on open theFiles
	repeat with aFile in theFiles
		processFile(POSIX path of aFile)
	end repeat
end open

on processFile(filePath)
	set myPath to POSIX path of (path to me)
	set pyPath to myPath & "Contents/Resources/play_mkv.py"
	
	-- Build the command
	-- We export PATH to ensure standard tools are found (though our script uses bundled ffmpeg mostly)
	set shellCmd to "export PATH=\"/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH\"; "
	set shellCmd to shellCmd & "python3 " & quoted form of pyPath & " " & quoted form of filePath
	
	-- Run it in the background (&> /dev/null &) so the app exits immediately and doesn't block
	-- We don't need 'do script' (Terminal), we use 'do shell script' (Background)
	try
		do shell script shellCmd
	on error errMsg
		display alert "Error running QTmkv" message errMsg
	end try
end processFile
