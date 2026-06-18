# Load .env file and collect keys
$keys = @()
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        $key = $Matches[1].Trim()
        $val = $Matches[2].Trim().Trim('"').Trim("'")
        [System.Environment]::SetEnvironmentVariable($key, $val, "Process")
        $keys += $key
    }
}

# Display all loaded env vars
foreach ($key in $keys) {
    $val = [System.Environment]::GetEnvironmentVariable($key, "Process")
    if ($val.Length -gt 10) {
        Write-Host "$key = $($val.Substring(0,10))..." -ForegroundColor Green
    } else {
        Write-Host "$key = $val" -ForegroundColor Green
    }
}
Write-Host "Starting LiteLLM Proxy..." -ForegroundColor Cyan

litellm --config config.yaml --port 4000
