# Windows Native TTS - NO hanging!
$folder = "voice-rag-system_clean"
Get-ChildItem "$folder\**\*_explanation\audio_script.txt" -Recurse | ForEach-Object {
    $txtPath = $_.FullName
    $mp3Path = $txtPath -replace 'audio_script.txt$', 'explanation.mp3'
    $text = Get-Content $txtPath -Raw
    
    Add-Type -AssemblyName System.Speech
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $speak.SetOutputToWaveFile($mp3Path)
    $speak.Speak($text)
    $speak.Dispose()
    Write-Host "✅ $mp3Path"
}
Write-Host "🎉 All MP3s created!"
