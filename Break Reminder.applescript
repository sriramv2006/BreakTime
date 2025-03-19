tell application "Terminal"
	activate
	do script "cd \"" & (POSIX path of (path to me as text)) & "/..\" && ./run_break_reminder.sh"
end tell 