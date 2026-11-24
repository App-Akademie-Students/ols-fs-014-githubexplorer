[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Za-z0-9-]+/[A-Za-z0-9_.-]+$')]
    [string]$Repo,

    [string]$CsvPath = (Join-Path $PSScriptRoot 'github-explorer-backlog.csv'),

    [string[]]$OnlyId,

    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$items = @(Import-Csv -LiteralPath $CsvPath -Delimiter ';' -Encoding UTF8)
if (-not $items.Count) { throw 'Die CSV enthält keine Einträge.' }

$ids = @{}
foreach ($item in $items) {
    if ($item.ID -notmatch '^[FNE]\d{2}$' -or $ids.ContainsKey($item.ID) -or
        -not $item.Titel -or -not $item.Abnahmekriterien -or
        $item.Typ -notin @('functional', 'non-functional', 'decision') -or
        ($item.Typ -eq 'decision' -and $item.Prioritaet) -or
        ($item.Typ -ne 'decision' -and $item.Prioritaet -notin @('must', 'nice-to-have'))) {
        throw "Ungültiger oder doppelter CSV-Eintrag: $($item.ID)"
    }
    $ids[$item.ID] = $true
}
foreach ($id in $OnlyId) {
    if (-not $ids.ContainsKey($id)) { throw "Unbekannte Backlog-ID: $id" }
}
if ($OnlyId) { $items = @($items | Where-Object { $_.ID -in $OnlyId }) }

if (-not $Apply) {
    $items | Format-Table ID, Titel, Prioritaet, Typ -AutoSize
    Write-Host "$($items.Count) ausgewählte Einträge. Mit -Apply werden fehlende Issues angelegt."
    return
}

if (-not (Get-Command gh -CommandType Application -ErrorAction SilentlyContinue)) {
    throw 'Installiere zuerst die GitHub CLI (gh).'
}

function Invoke-GitHubCli {
    param([string[]]$CliArgs)
    $result = & gh @CliArgs
    if ($LASTEXITCODE -ne 0) {
        throw "GitHub CLI meldet Fehlercode $LASTEXITCODE. Prüfe die Ausgabe und starte den Import bei Bedarf erneut."
    }
    return $result
}

$existingIds = @{}
$issueTitles = Invoke-GitHubCli -CliArgs @(
    'api', '--paginate', "repos/$Repo/issues?state=all&per_page=100",
    '--jq', '.[] | select(has("pull_request") | not) | .title'
)
foreach ($title in $issueTitles) {
    if ($title -match '^\[([FNE]\d{2})\]') { $existingIds[$Matches[1]] = $true }
}

$pending = @($items | Where-Object { -not $existingIds.ContainsKey($_.ID) })
foreach ($item in $items) {
    if ($existingIds.ContainsKey($item.ID)) { Write-Host "Übersprungen: $($item.ID) existiert bereits." }
}
if (-not $pending.Count) { return }

$colors = @{
    'must' = 'B60205'
    'nice-to-have' = '0E8A16'
    'functional' = '0052CC'
    'non-functional' = '5319E7'
    'decision' = 'FBCA04'
}
$existingLabels = Invoke-GitHubCli -CliArgs @(
    'api', '--paginate', "repos/$Repo/labels?per_page=100", '--jq', '.[].name'
)
$neededLabels = @($pending | ForEach-Object { $_.Typ; $_.Prioritaet } |
    Where-Object { $_ } | Sort-Object -Unique)
foreach ($label in $neededLabels) {
    if ($label -notin $existingLabels) {
        Invoke-GitHubCli -CliArgs @('label', 'create', $label, '--repo', $Repo, '--color', $colors[$label])
    }
}

$bodyFile = [IO.Path]::GetTempFileName()
try {
    foreach ($item in $pending) {
        $title = "[$($item.ID)] $($item.Titel)"
        $body = "## Abnahmekriterien`n`n- [ ] $($item.Abnahmekriterien)`n"
        [IO.File]::WriteAllText($bodyFile, $body, [Text.UTF8Encoding]::new($false))
        $createArgs = @('issue', 'create', '--repo', $Repo, '--title', $title,
            '--body-file', $bodyFile, '--label', $item.Typ)
        if ($item.Prioritaet) { $createArgs += @('--label', $item.Prioritaet) }
        $url = Invoke-GitHubCli -CliArgs $createArgs
        Write-Host "$($item.ID) angelegt: $url"
    }
}
finally {
    Remove-Item -LiteralPath $bodyFile -Force
}
