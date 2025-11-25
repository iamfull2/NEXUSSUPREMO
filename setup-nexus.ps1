$projectPath = "C:\Users\mathi\Downloads\NEXUSSUPREMO"
Set-Location $projectPath

Write-Host "`nCriando arquivos necessarios...`n" -ForegroundColor Cyan

# 1. Criar vercel.json
Write-Host "Criando vercel.json..." -ForegroundColor Yellow
$vercelJson = @"
{
  "version": 2,
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "env": {
    "REACT_APP_API_URL": "@react_app_api_url"
  },
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/node",
      "config": {
        "zeroConfig": true
      }
    },
    {
      "src": "backend/server-online.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/server-online.js"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/dist/index.html"
    }
  ]
}
"@
$vercelJson | Out-File -FilePath "vercel.json" -Encoding UTF8 -Force
Write-Host "OK - vercel.json criado!" -ForegroundColor Green

# 2. Criar package.json na raiz
Write-Host "Criando package.json..." -ForegroundColor Yellow
$packageJson = @"
{
  "name": "nexus-supreme-pro",
  "version": "1.0.0",
  "description": "NEXUS SUPREME PRO - AntiDetect Browser System",
  "scripts": {
    "dev": "cd frontend && npm run dev",
    "build": "cd frontend && npm run build"
  }
}
"@
$packageJson | Out-File -FilePath "package.json" -Encoding UTF8 -Force
Write-Host "OK - package.json criado!" -ForegroundColor Green

# 3. Criar frontend/package.json
Write-Host "Criando frontend/package.json..." -ForegroundColor Yellow
$frontendPackageJson = @"
{
  "name": "nexus-supreme-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8"
  }
}
"@
$frontendPackageJson | Out-File -FilePath "frontend/package.json" -Encoding UTF8 -Force
Write-Host "OK - frontend/package.json criado!" -ForegroundColor Green

# 4. Criar frontend/vite.config.js
Write-Host "Criando frontend/vite.config.js..." -ForegroundColor Yellow
$viteConfig = @"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false
  }
})
"@
$viteConfig | Out-File -FilePath "frontend/vite.config.js" -Encoding UTF8 -Force
Write-Host "OK - frontend/vite.config.js criado!" -ForegroundColor Green

# 5. Criar frontend/public/index.html
Write-Host "Criando frontend/public/index.html..." -ForegroundColor Yellow
$indexHtml = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NEXUS SUPREME PRO</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/index.jsx"></script>
</body>
</html>
"@
$indexHtml | Out-File -FilePath "frontend/public/index.html" -Encoding UTF8 -Force
Write-Host "OK - frontend/public/index.html criado!" -ForegroundColor Green

# 6. Criar .gitignore
Write-Host "Criando .gitignore..." -ForegroundColor Yellow
$gitignore = @"
node_modules/
dist/
build/
.env
.env.local
.DS_Store
*.log
.vscode/
.idea/
.vercel
"@
$gitignore | Out-File -FilePath ".gitignore" -Encoding UTF8 -Force
Write-Host "OK - .gitignore criado!" -ForegroundColor Green

# 7. Inicializar Git
Write-Host "Inicializando Git..." -ForegroundColor Yellow
git init
git config user.email "seu@email.com"
git config user.name "NEXUS SUPREME"
git branch -M main
Write-Host "OK - Git inicializado!" -ForegroundColor Green

# 8. Fazer primeiro commit
Write-Host "Fazendo primeiro commit..." -ForegroundColor Yellow
git add .
git commit -m "Initial commit - NEXUS SUPREME PRO with Vite React"
Write-Host "OK - Commit realizado!" -ForegroundColor Green

# 9. Resumo final
Write-Host "`n" 
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "SUCESSO! Todos os arquivos foram criados e Git foi inicializado!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green

Write-Host "`nARQUIVOS CRIADOS:" -ForegroundColor Cyan
Write-Host "  - vercel.json" -ForegroundColor Green
Write-Host "  - package.json" -ForegroundColor Green
Write-Host "  - frontend/package.json" -ForegroundColor Green
Write-Host "  - frontend/vite.config.js" -ForegroundColor Green
Write-Host "  - frontend/public/index.html" -ForegroundColor Green
Write-Host "  - .gitignore" -ForegroundColor Green

Write-Host "`nPROXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host "  1. Criar repositorio em: https://github.com/new" -ForegroundColor Yellow
Write-Host "     Nome: NEXUSSUPREMO" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Executar no PowerShell:" -ForegroundColor Yellow
Write-Host "     git remote add origin https://github.com/SEU_USUARIO/NEXUSSUPREMO.git" -ForegroundColor Magenta
Write-Host "     git push -u origin main" -ForegroundColor Magenta
Write-Host ""
Write-Host "  3. Ir em https://vercel.com" -ForegroundColor Yellow
Write-Host "     - Add New -> Project" -ForegroundColor Yellow
Write-Host "     - Conectar GitHub" -ForegroundColor Yellow
Write-Host "     - Selecionar NEXUSSUPREMO" -ForegroundColor Yellow
Write-Host "     - Clicar Deploy" -ForegroundColor Yellow
Write-Host ""
Write-Host "  4. Aguardar 2-3 minutos" -ForegroundColor Yellow
Write-Host "     - Site ficara ONLINE!" -ForegroundColor Yellow

Write-Host "`nPronto para deploy! Sucesso total!" -ForegroundColor Green
Write-Host "`n"
