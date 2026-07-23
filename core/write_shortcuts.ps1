param([Parameter(Mandatory = $true)][string]$Json)

# Create or update Windows .lnk shortcuts from a JSON spec list.
# Called by core/shortcuts.py — never run by hand.
# Each spec: { path, target, args, workdir, icon, existed }

$ErrorActionPreference = "Stop"
$specs = Get-Content -Raw -Encoding UTF8 $Json | ConvertFrom-Json
$shell = New-Object -ComObject WScript.Shell

foreach ($s in $specs) {
    $dir = Split-Path -Parent $s.path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $lnk = $shell.CreateShortcut($s.path)
    $lnk.TargetPath = $s.target
    $lnk.Arguments = $s.args
    if ($s.workdir) { $lnk.WorkingDirectory = $s.workdir }
    $lnk.IconLocation = $s.icon
    $lnk.Save()

    $verb = if ($s.existed) { "updated" } else { "created" }
    Write-Output ("  {0,-8} {1}" -f $verb, (Split-Path -Leaf $s.path))
}
