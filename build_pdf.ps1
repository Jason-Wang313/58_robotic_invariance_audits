$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PaperDir = Join-Path $Root "paper"
$DownloadsPdf = "C:\Users\wangz\Downloads\58.pdf"
$LocalPdf = Join-Path $PaperDir "main.pdf"
$BuildStatus = Join-Path $Root "data\build_status.json"
$ValidationPath = Join-Path $Root "results\full_scale\experiment_validation.json"

if (-not (Test-Path -LiteralPath $ValidationPath)) {
    throw "Missing full-scale validation file: $ValidationPath"
}

$Validation = Get-Content -Raw -LiteralPath $ValidationPath | ConvertFrom-Json
if (-not $Validation.row_count_ok) {
    throw "Full-scale validation row_count_ok is false."
}
if (-not $Validation.audit_observer_only_ok) {
    throw "Full-scale validation audit_observer_only_ok is false."
}
if ([int64]$Validation.condition_rows -ne 201600) {
    throw "Unexpected condition row count: $($Validation.condition_rows)"
}
if ([int64]$Validation.represented_evaluations -ne 105696460800) {
    throw "Unexpected represented evaluation count: $($Validation.represented_evaluations)"
}

Push-Location $PaperDir
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
}
finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $LocalPdf)) {
    throw "Expected local PDF was not produced: $LocalPdf"
}

$PdfInfo = & pdfinfo $LocalPdf
$PagesLine = $PdfInfo | Select-String -Pattern "^Pages:\s+(\d+)" | Select-Object -First 1
if (-not $PagesLine) {
    throw "Could not read page count from $LocalPdf"
}
$Pages = [int]$PagesLine.Matches[0].Groups[1].Value
if ($Pages -lt 25) {
    throw "Final PDF has $Pages pages; expected at least 25 pages."
}

$LocalLength = (Get-Item -LiteralPath $LocalPdf).Length
$Hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $LocalPdf).Hash

Copy-Item -LiteralPath $LocalPdf -Destination $DownloadsPdf -Force
Remove-Item -LiteralPath $LocalPdf -Force

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $BuildStatus) | Out-Null
$Status = [ordered]@{
    paper = 58
    decision = "final_v3_full_scale_submission_candidate"
    canonical_pdf = $DownloadsPdf
    pages = $Pages
    file_size_bytes = $LocalLength
    sha256 = $Hash
    condition_rows = [int64]$Validation.condition_rows
    represented_evaluations = [int64]$Validation.represented_evaluations
    represented_planning_tick_decisions = [int64]$Validation.represented_planning_tick_decisions
    audit_observer_only_ok = [bool]$Validation.audit_observer_only_ok
    local_pdf_removed = -not (Test-Path -LiteralPath $LocalPdf)
    built_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")
}
$Status | ConvertTo-Json | Set-Content -Path $BuildStatus -Encoding ASCII

Get-Item -LiteralPath $DownloadsPdf | Select-Object FullName,Length,LastWriteTime
Write-Host "pages=$Pages"
Write-Host "sha256=$Hash"
Write-Host "local_pdf_removed=$(-not (Test-Path -LiteralPath $LocalPdf))"
