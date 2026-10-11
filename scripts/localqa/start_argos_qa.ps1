$ErrorActionPreference = "Stop"
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
$python = Join-Path $repoRoot ".venv\Scripts\python.exe"
$manage = Join-Path $repoRoot "manage.py"
$settingsModule = "scripts.localqa.settings"
$port = 8765
$server = $null

function Test-PortAvailable {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Parse("127.0.0.1"), $port)
    try {
        $listener.Start()
        return $true
    } catch [System.Net.Sockets.SocketException] {
        return $false
    } finally {
        $listener.Stop()
    }
}

try {
    if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
        throw "Não encontrei o Python do projeto em .venv\Scripts\python.exe."
    }
    if (-not (Test-Path -LiteralPath $manage -PathType Leaf)) {
        throw "Não encontrei manage.py na raiz deste projeto."
    }
    if (-not (Test-PortAvailable)) {
        throw "A porta local 8765 já está em uso. Feche o servidor existente antes de iniciar outro."
    }

    $env:ARGOS_QA_ROOT = $repoRoot
    $env:ARGOS_LOCAL_QA_LAUNCHER = "1"
    $env:DJANGO_SETTINGS_MODULE = $settingsModule
    $env:ARGOS_DEBUG = "true"
    $env:ARGOS_ALLOWED_HOSTS = "127.0.0.1,localhost"
    $env:ARGOS_VISUAL_QA_ENABLED = "true"
    $env:ARGOS_VISUAL_QA_USERNAME = "qa-visual-hom01"
    $env:ARGOS_QA_SECRET_KEY = & $python -c "import secrets; print(secrets.token_urlsafe(48))"
    if ($LASTEXITCODE -ne 0 -or $env:ARGOS_QA_SECRET_KEY.Length -lt 32) {
        throw "Não foi possível gerar a chave temporária do QA."
    }
    $env:ARGOS_OPERATIONAL_QA_PASSWORD = & $python -c "import secrets; print(secrets.token_urlsafe(32))"
    if ($LASTEXITCODE -ne 0 -or $env:ARGOS_OPERATIONAL_QA_PASSWORD.Length -lt 24) {
        throw "Não foi possível gerar a senha temporária operacional do QA."
    }

    Write-Host "Preparando banco SQLite isolado, migrations e dados fictícios..."
    & $python (Join-Path $PSScriptRoot "prepare_qa.py")
    if ($LASTEXITCODE -ne 0) { throw "A preparação local de QA falhou." }

    if (-not (Test-PortAvailable)) {
        throw "A porta local 8765 foi ocupada durante a preparação; nenhum servidor novo foi iniciado."
    }

    Write-Host ""
    Write-Host "ARGOS QA fictício pronto para inspeção local"
    Write-Host "Endereço: http://127.0.0.1:8765/"
    Write-Host "Conta visual preservada: qa-visual-hom01 (senha existente mantida)."
    Write-Host "Conta operacional: qa-operacional-hom01"
    Write-Host "Senha operacional desta execução: $env:ARGOS_OPERATIONAL_QA_PASSWORD"
    Write-Host "A senha operacional anterior deixou de valer nesta inicialização."
    Write-Host "A senha nova aparece somente neste terminal e não é salva em arquivo."
    Write-Host "Pressione Ctrl+C nesta janela para encerrar o servidor."

    $server = Start-Process -FilePath $python -ArgumentList @(
        "`"$manage`"", "runserver", "127.0.0.1:$port", "--noreload"
    ) -WorkingDirectory $repoRoot -NoNewWindow -PassThru

    $ready = $false
    for ($attempt = 0; $attempt -lt 60; $attempt++) {
        if ($server.HasExited) {
            throw "O Django encerrou antes de responder. Revise a mensagem de erro acima."
        }
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:$port/" -TimeoutSec 2 -UseBasicParsing
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
                $ready = $true
                break
            }
        } catch {
            $httpResponse = $_.Exception.Response
            if ($httpResponse -and [int]$httpResponse.StatusCode -lt 500) {
                $ready = $true
                break
            }
        }
        Start-Sleep -Milliseconds 500
    }
    if (-not $ready) { throw "O Django não respondeu em http://127.0.0.1:$port/ no tempo esperado." }

    Write-Host "Servidor HTTP local respondeu. Abrindo o navegador..."
    Start-Process "http://127.0.0.1:$port/"
    $server.WaitForExit()
    if ($server.ExitCode -ne 0) { throw "O servidor Django terminou com erro (código $($server.ExitCode))." }
} catch {
    Write-Host "ERRO: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    if ($server -and -not $server.HasExited) {
        Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
        $server.WaitForExit()
    }
    Remove-Item Env:ARGOS_OPERATIONAL_QA_PASSWORD -ErrorAction SilentlyContinue
    Remove-Item Env:ARGOS_QA_SECRET_KEY -ErrorAction SilentlyContinue
}
