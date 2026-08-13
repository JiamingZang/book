$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$html = Join-Path $root 'handbook\trading-handbook.html'
$pdf  = Join-Path $root 'handbook\trading-handbook.pdf'
$uri = ([System.Uri]$html).AbsoluteUri
Write-Output "URL: $uri"
& 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe' --headless --disable-gpu --no-pdf-header-footer '--user-data-dir=C:\Users\18315\AppData\Local\Temp\edgepdf2' "--print-to-pdf=$pdf" $uri
Start-Sleep -Seconds 3
$f = Get-Item $pdf
Write-Output "PDF: $($f.Length) bytes, $($f.LastWriteTime)"
