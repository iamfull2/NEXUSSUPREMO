Write-Host "`n"
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host "NEXUS SUPREME PRO - DIAGNOSTICO COMPLETO" -ForegroundColor Cyan
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host "`n"

$projectPath = "C:\Users\mathi\Downloads\NEXUSSUPREMO"

if (-not (Test-Path $projectPath)) {
    Write-Host "ERRO: Pasta nao encontrada: $projectPath" -ForegroundColor Red
    exit
}

Set-Location $projectPath
Write-Host "Localizacao: $projectPath`n" -ForegroundColor Yellow

# PASSO 1: Verificar estrutura de pastas
Write-Host "1. VERIFICANDO ESTRUTURA DE PASTAS" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

$folders = @("frontend", "backend", "frontend/src", "frontend/public")
foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Write-Host "  OK - Pasta existe: $folder" -ForegroundColor Green
    } else {
        Write-Host "  FALTA - Pasta nao existe: $folder" -ForegroundColor Red
    }
}

Write-Host "`n"

# PASSO 2: Verificar arquivos raiz
Write-Host "2. VERIFICANDO ARQUIVOS NA RAIZ" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

$rootFiles = @("vercel.json", "package.json", ".gitignore", "README.md")
foreach ($file in $rootFiles) {
    if (Test-Path $file) {
        Write-Host "  OK - Arquivo existe: $file" -ForegroundColor Green
    } else {
        Write-Host "  FALTA - Arquivo nao existe: $file" -ForegroundColor Red
    }
}

Write-Host "`n"

# PASSO 3: Verificar arquivos frontend
Write-Host "3. VERIFICANDO ARQUIVOS FRONTEND" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

$frontendFiles = @(
    "frontend/package.json",
    "frontend/vite.config.js",
    "frontend/public/index.html",
    "frontend/src/App.jsx",
    "frontend/src/App.css",
    "frontend/src/index.jsx",
    "frontend/src/index.css"
)

foreach ($file in $frontendFiles) {
    if (Test-Path $file) {
        Write-Host "  OK - Arquivo existe: $file" -ForegroundColor Green
    } else {
        Write-Host "  FALTA - Arquivo nao existe: $file" -ForegroundColor Red
    }
}

Write-Host "`n"

# PASSO 4: Verificar arquivos backend
Write-Host "4. VERIFICANDO ARQUIVOS BACKEND" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

$backendFiles = @(
    "backend/server-online.js",
    "backend/package.json"
)

foreach ($file in $backendFiles) {
    if (Test-Path $file) {
        Write-Host "  OK - Arquivo existe: $file" -ForegroundColor Green
    } else {
        Write-Host "  FALTA - Arquivo nao existe: $file" -ForegroundColor Red
    }
}

Write-Host "`n"

# PASSO 5: Verificar conteudo do vercel.json
Write-Host "5. VERIFICANDO CONTEUDO DO vercel.json" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

if (Test-Path "vercel.json") {
    $vercelContent = Get-Content vercel.json -Raw
    
    if ($vercelContent -match '"buildCommand": "cd frontend && npm install && npm run build"') {
        Write-Host "  OK - buildCommand esta correto para Vite" -ForegroundColor Green
    } else {
        Write-Host "  ERRO - buildCommand nao esta correto!" -ForegroundColor Red
        Write-Host "  Deve ser: cd frontend && npm install && npm run build" -ForegroundColor Yellow
    }
    
    if ($vercelContent -match '"outputDirectory": "frontend/dist"') {
        Write-Host "  OK - outputDirectory esta correto" -ForegroundColor Green
    } else {
        Write-Host "  ERRO - outputDirectory nao esta correto!" -ForegroundColor Red
    }
    
    if ($vercelContent -match '@vercel/node') {
        Write-Host "  OK - Usando @vercel/node" -ForegroundColor Green
    } else {
        Write-Host "  ERRO - Nao esta usando @vercel/node!" -ForegroundColor Red
    }
} else {
    Write-Host "  FALTA - vercel.json nao existe!" -ForegroundColor Red
}

Write-Host "`n"

# PASSO 6: Verificar conteudo do frontend/package.json
Write-Host "6. VERIFICANDO frontend/package.json" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

if (Test-Path "frontend/package.json") {
    $packageContent = Get-Content frontend/package.json -Raw
    
    if ($packageContent -match '"build": "vite build"') {
        Write-Host "  OK - Script build esta correto" -ForegroundColor Green
    } else {
        Write-Host "  ERRO - Script build nao esta correto!" -ForegroundColor Red
    }
    
    if ($packageContent -match '"vite"') {
        Write-Host "  OK - Vite esta nas dependencias" -ForegroundColor Green
    } else {
        Write-Host "  ERRO - Vite nao esta instalado!" -ForegroundColor Red
    }
    
    if ($packageContent -match '@vitejs/plugin-react') {
        Write-Host "  OK - Plugin React do Vite esta configurado" -ForegroundColor Green
    } else {
        Write-Host "  ERRO - Plugin React nao esta instalado!" -ForegroundColor Red
    }
} else {
    Write-Host "  FALTA - frontend/package.json nao existe!" -ForegroundColor Red
}

Write-Host "`n"

# PASSO 7: Verificar Git
Write-Host "7. VERIFICANDO GIT" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green

if (Test-Path ".git") {
    Write-Host "  OK - Repositorio Git inicializado" -ForegroundColor Green
    
    $gitRemote = git remote -v 2>$null
    if ($gitRemote) {
        Write-Host "  OK - Git remote configurado" -ForegroundColor Green
        Write-Host "  Remotes: `n$gitRemote" -ForegroundColor Cyan
    } else {
        Write-Host "  AVISO - Git remotes nao configurados" -ForegroundColor Yellow
    }
} else {
    Write-Host "  FALTA - .git nao existe (repositorio nao inicializado)" -ForegroundColor Red
}

Write-Host "`n"

# PASSO 8: Mostrar estrutura geral
Write-Host "8. ESTRUTURA GERAL DO PROJETO" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

Write-Host "`nArquivos na raiz:" -ForegroundColor Cyan
Get-ChildItem -Path . -MaxDepth 1 -File | ForEach-Object { Write-Host "  - $($_.Name)" }

Write-Host "`nPastas principais:" -ForegroundColor Cyan
Get-ChildItem -Path . -MaxDepth 1 -Directory | ForEach-Object { Write-Host "  - $($_.Name)/" }

Write-Host "`n"

# PASSO 9: Resumo
Write-Host "9. RESUMO E PROXIMOS PASSOS" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Green
Write-Host "`n"

$errors = @()
$warnings = @()

if (-not (Test-Path "vercel.json")) { $errors += "vercel.json falta" }
if (-not (Test-Path "frontend/package.json")) { $errors += "frontend/package.json falta" }
if (-not (Test-Path "frontend/vite.config.js")) { $errors += "frontend/vite.config.js falta" }
if (-not (Test-Path "frontend/public/index.html")) { $errors += "frontend/public/index.html falta" }
if (-not (Test-Path ".git")) { $warnings += "Git nao inicializado" }
if (-not (Test-Path ".gitignore")) { $warnings += ".gitignore nao existe" }

if ($errors.Count -gt 0) {
    Write-Host "ERROS ENCONTRADOS:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
}

if ($warnings.Count -gt 0) {
    Write-Host "`nAVISOS:" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "  - $warning" -ForegroundColor Yellow
    }
}

if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "TUDO OK! Seu projeto esta pronto!" -ForegroundColor Green
    Write-Host "`nProximos passos:" -ForegroundColor Cyan
    Write-Host "  1. git init (se nao fez)" -ForegroundColor Cyan
    Write-Host "  2. git add ." -ForegroundColor Cyan
    Write-Host "  3. git commit -m 'Initial commit - NEXUS SUPREME PRO with Vite'" -ForegroundColor Cyan
    Write-Host "  4. git remote add origin https://github.com/SEU_USUARIO/NEXUSSUPREMO.git" -ForegroundColor Cyan
    Write-Host "  5. git push -u origin main" -ForegroundColor Cyan
    Write-Host "  6. Ir no Vercel e fazer deploy" -ForegroundColor Cyan
}

Write-Host "`n"
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host "FIM DO DIAGNOSTICO" -ForegroundColor Cyan
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host "`n"
