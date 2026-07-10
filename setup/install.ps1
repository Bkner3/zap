$ErrorActionPreference = "Stop"

$AppName = "ZAP"
$RootDir = "$env:LOCALAPPDATA\$AppName"

$SlDir = "$RootDir\sl"

Write-Host "Installing $AppName..."

# Criar estrutura
foreach ($dir in @($RootDir, $SlDir)) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

# Obter releases
Write-Host "Finding latest release..."

$release = Invoke-RestMethod `
    "https://api.github.com/repos/Bkner3/zap/releases"

$asset = $release[0].assets | Where-Object {
    $_.name -eq "zap.exe"
}

if (!$asset) {
    throw "Could not find zap.exe in release."
}

# Download
$ExePath = "$RootDir\zap.exe"

Write-Host "Downloading ZAP..."

Invoke-WebRequest `
    -Uri $asset.browser_download_url `
    -OutFile $ExePath


$Shim = @"
@echo off
"$ExePath" %*
"@

Set-Content `
    -Path "$SlDir\zap.cmd" `
    -Value $Shim `
    -Encoding ASCII


Write-Host "Adding ZAP to PATH..."

$userPath = [Environment]::GetEnvironmentVariable(
    "Path",
    "User"
)

if ($userPath -notlike "*$SlDir*") {

    if ([string]::IsNullOrEmpty($userPath)) {
        $newPath = $SlDir
    }
    else {
        $newPath = "$userPath;$SlDir"
    }

    [Environment]::SetEnvironmentVariable(
        "Path",
        $newPath,
        "User"
    )
}


Write-Host ""
Write-Host "Installation completed!"
Write-Host ""
Write-Host "Restart your terminal and run:"
Write-Host "  zap"