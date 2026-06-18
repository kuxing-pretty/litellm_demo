@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Load .env file and collect keys
set "keys="
for /f "usebackq eol=# tokens=1,* delims==" %%a in (".env") do (
    set "val=%%b"
    set "val=!val:"=!"
    set "%%a=!val!"
    set "keys=!keys! %%a"
)

REM Display all loaded env vars
for %%k in (!keys!) do (
    set "display=!%%k!"
    if defined display (
        if !display:~10! neq "" (
            echo %%k = !display:~0,10!...
        ) else (
            echo %%k = !display!
        )
    )
)
echo Starting LiteLLM Proxy...

litellm --config config.yaml --port 4000
