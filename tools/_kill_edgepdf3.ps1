# 杀所有 headless msedge 进程（导出残留：主进程挂住会占 user-data-dir 导致 print-to-pdf 不写文件）
$procs = Get-CimInstance Win32_Process -Filter "Name = 'msedge.exe'" |
    Where-Object { $_.CommandLine -match 'headless' }
$ids = $procs | Select-Object -ExpandProperty ProcessId
if ($ids) {
    Write-Output ("kill: " + ($ids -join ','))
    $ids | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
} else {
    Write-Output "no residual headless msedge process"
}
