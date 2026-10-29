$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$taskRoot = Split-Path -Parent $PSScriptRoot
$taskNarration = Get-Content -Raw -LiteralPath (Join-Path $taskRoot 'tmp\narration.json') | ConvertFrom-Json
$taskSynth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$taskSynth.Rate = 1
for ($taskIndex = 0; $taskIndex -lt $taskNarration.Count; $taskIndex++) {
    $taskAudio = Join-Path $taskRoot ('tmp\scene-{0}.wav' -f ($taskIndex + 1))
    $taskSynth.SetOutputToWaveFile($taskAudio)
    $taskSynth.Speak($taskNarration[$taskIndex])
    $taskSynth.SetOutputToNull()
}
$taskSynth.Dispose()
Write-Output 'Seven narration tracks created.'
