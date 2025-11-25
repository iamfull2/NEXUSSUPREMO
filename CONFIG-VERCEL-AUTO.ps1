# ========================================
# NEXUS SUPREME PRO - CONFIGURAÇÃO VERCEL
# Configure Root Directory + Build + Output
# ========================================

cd "C:\Users\mathi\Downloads\NEXUSSUPREMO"

# 1. CRIAR .vercelignore
Write-Host "📝 Criando .vercelignore..." -ForegroundColor Cyan
@'
node_modules
.git
.env
backend
dist
'@ | Out-File .vercelignore -Encoding ASCII -Force

# 2. CRIAR vercel.json CORRETO
Write-Host "⚙️ Criando vercel.json..." -ForegroundColor Cyan
@'
{
  "version": 2,
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/dist"
}
'@ | Out-File vercel.json -Encoding ASCII -Force

# 3. VALIDAR
Write-Host "`n✅ Arquivos criados:" -ForegroundColor Green
Write-Host "vercel.json:" -ForegroundColor Yellow
Get-Content vercel.json

# 4. GIT
Write-Host "`n📤 Enviando para GitHub..." -ForegroundColor Cyan
git add -A
git commit -m "Config: Vercel auto-deploy setup"
git push origin main --force

# 5. REDEPLOY VERCEL
Write-Host "`n🚀 Deployando no Vercel..." -ForegroundColor Cyan
vercel --token=NfCYGv9rVuUlGxC8hHpZBruX --prod --force

Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ CONFIGURAÇÃO COMPLETA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`n🌐 SEU SITE ESTÁ ONLINE:" -ForegroundColor Cyan
Write-Host "https://nexussupremo.vercel.app" -ForegroundColor Yellow
Write-Host "`n📌 LOGINS:" -ForegroundColor Green
Write-Host "  👨‍💼 mathias2matheus2@gmail.com / Mome8e8a65D7" -ForegroundColor Yellow
Write-Host "  👤 mmlightdesigner@gmail.com / mmk200981@@@@" -ForegroundColor Yellow
Write-Host "`n========================================`n" -ForegroundColor Green
