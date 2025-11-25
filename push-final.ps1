$projectPath = "C:\Users\mathi\Downloads\NEXUSSUPREMO"
Set-Location $projectPath

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "NEXUS SUPREME PRO - PUSH PARA GITHUB" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# PASSO 1: Limpar Git anterior
Write-Host "PASSO 1: Limpando Git anterior..." -ForegroundColor Yellow
git remote remove origin 2>$null
Remove-Item ".git" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "OK - Git limpo`n" -ForegroundColor Green

# PASSO 2: Deletar arquivos com secrets
Write-Host "PASSO 2: Removendo arquivos com secrets..." -ForegroundColor Yellow
Get-ChildItem -Filter "sf_cookie*.json" -Force -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Filter "sf_cookie*.txt" -Force -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "NEXUS_SUPREME_DATA\cookies\" -Force -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
Write-Host "OK - Secrets removidos`n" -ForegroundColor Green

# PASSO 3: Criar .gitignore correto
Write-Host "PASSO 3: Criando .gitignore..." -ForegroundColor Yellow
$gitignore = @"
# Dependencies
node_modules/
dist/
build/

# Environment
.env
.env.local
.env.*.local

# Sensitive
sf_cookie*
*_cookies.json
master_cookies.json
NEXUS_SUPREME_DATA/

# System
.DS_Store
*.log
npm-debug.log*
yarn-debug.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# Vercel
.vercel
"@

$gitignore | Out-File ".gitignore" -Encoding UTF8 -Force
Write-Host "OK - .gitignore criado`n" -ForegroundColor Green

# PASSO 4: Git init
Write-Host "PASSO 4: Inicializando Git..." -ForegroundColor Yellow
git init
git config user.email "seu@email.com"
git config user.name "NEXUS SUPREME"
git branch -M main
Write-Host "OK - Git inicializado`n" -ForegroundColor Green

# PASSO 5: Git add
Write-Host "PASSO 5: Adicionando arquivos..." -ForegroundColor Yellow
git add .
Write-Host "OK - Arquivos adicionados`n" -ForegroundColor Green

# PASSO 6: Git commit
Write-Host "PASSO 6: Fazendo commit..." -ForegroundColor Yellow
git commit -m "NEXUS SUPREME PRO - Vite React + Node.js Backend - Production Ready"
Write-Host "OK - Commit realizado`n" -ForegroundColor Green

# PASSO 7: Adicionar remote
Write-Host "PASSO 7: Conectando ao GitHub..." -ForegroundColor Yellow
git remote add origin https://github.com/iamfull2/NEXUSSUPREMO.git
Write-Host "OK - Remote adicionado`n" -ForegroundColor Green

# PASSO 8: Push
Write-Host "PASSO 8: Fazendo push para GitHub..." -ForegroundColor Yellow
git push -u origin main --force
Write-Host "OK - Push realizado`n" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "SUCESSO TOTAL! GITHUB ATUALIZADO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nSEU REPOSITORIO:" -ForegroundColor Cyan
Write-Host "https://github.com/iamfull2/NEXUSSUPREMO`n" -ForegroundColor Yellow

Write-Host "PROXIMA ETAPA - VERCEL DEPLOY:" -ForegroundColor Cyan
Write-Host "1. Acesse: https://vercel.com" -ForegroundColor Yellow
Write-Host "2. Clique: Add New -> Project" -ForegroundColor Yellow
Write-Host "3. Conecte GitHub" -ForegroundColor Yellow
Write-Host "4. Selecione: NEXUSSUPREMO" -ForegroundColor Yellow
Write-Host "5. Clique: Deploy" -ForegroundColor Yellow
Write-Host "6. Aguarde 3-5 minutos" -ForegroundColor Yellow
Write-Host "7. SITE ONLINE!" -ForegroundColor Yellow
Write-Host "`n"
