$ErrorActionPreference = 'SilentlyContinue'
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$html = Join-Path $root 'handbook\trading-handbook.html'
$out = Join-Path $root '_dom_dump2.html'
$uri = ([System.Uri]$html).AbsoluteUri
& 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' --headless --disable-gpu '--user-data-dir=C:\Users\18315\AppData\Local\Temp\edgedom2' "--dump-dom=$uri" 2>$null | Out-File -FilePath $out -Encoding utf8
Start-Sleep -Seconds 4
$f = Get-Item $out
Write-Output "DOM: $($f.Length) bytes"
