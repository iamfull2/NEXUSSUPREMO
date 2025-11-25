# 🏆 NEXUS SUPREME PRO - Setup Completo

## ⚡ INSTALAÇÃO RÁPIDA (5 MINUTOS)

### PASSO 1: Abra PowerShell como Administrador

```powershell
# Clique direito no menu Iniciar e selecione "Windows PowerShell (Admin)"
```

### PASSO 2: Execute o Script de Setup

```powershell
# Navegue até a pasta NEXUSSUPREMO
cd C:\Users\mathi\Downloads\NEXUSSUPREMO

# Execute o setup
powershell -ExecutionPolicy Bypass -File setup.ps1
```

### PASSO 3: Aguarde a Instalação

O script irá:
- ✅ Verificar Node.js e NPM
- ✅ Criar estrutura de pastas
- ✅ Gerar arquivo .env
- ✅ Instalar dependências
- ✅ Criar servidor Express

### PASSO 4: Inicie o Backend

Após o setup, escolha uma opção:

**Opção A: Duplo clique no arquivo**
```
C:\Users\mathi\Downloads\NEXUSSUPREMO\start-backend.bat
```

**Opção B: Via PowerShell**
```powershell
cd C:\Users\mathi\Downloads\NEXUSSUPREMO\backend
npm start
```

### PASSO 5: Abra no Navegador

```
http://localhost:3000
```

---

## 🔐 CREDENCIAIS DE ACESSO

### Usuário 1 (Admin)
```
Email: admin@nexus.com
Senha: admin123
Plano: Enterprise
```

### Usuário 2 (Você)
```
Email: mmlightdesigner@gmail.com
Senha: admin mmk200981@@@@
Plano: Professional
```

---

## 📊 O QUE ESTÁ CONFIGURADO

### Backend (Node.js + Express)
- ✅ Server rodando em http://localhost:3000
- ✅ API REST completa
- ✅ Autenticação JWT
- ✅ CORS configurado
- ✅ Health check
- ✅ Logging automático

### Frontend (React)
- ✅ Login funcional
- ✅ Dashboard profissional
- ✅ Tabela de domínios
- ✅ Busca em tempo real
- ✅ Paginação
- ✅ Responsivo

### Banco de Dados
- ✅ Dados em memória (demo)
- ✅ Pronto para conectar PostgreSQL

### Segurança
- ✅ JWT tokens
- ✅ CORS habilitado
- ✅ Variáveis de ambiente
- ✅ Proteção HTTPS-ready

---

## 🔗 ENDPOINTS DA API

### Autenticação
```bash
POST /api/auth/login
Body: { "email": "user@email.com", "password": "senha" }
Response: { "token": "jwt_token", "user": {...} }
```

### Domínios
```bash
GET /api/domains
Response: { "domains": {...} }
```

### Estatísticas
```bash
GET /api/stats
Response: { "stats": {...} }
```

### Health Check
```bash
GET /health
Response: { "status": "ok" }
```

---

## 🛠️ ARQUITETURA

```
NEXUSSUPREMO/
├── backend/
│   ├── server.js          ← Servidor Express
│   ├── .env               ← Variáveis de ambiente
│   └── node_modules/      ← Dependências
├── frontend/
│   ├── public/
│   │   └── index.html     ← React App
│   └── (arquivos estáticos)
├── database/              ← Dados (quando usar real DB)
├── logs/                  ← Arquivos de log
├── start-backend.bat      ← Iniciar (Windows)
├── start-backend.ps1      ← Iniciar (PowerShell)
└── setup.ps1              ← Script de setup
```

---

## 🚀 PRÓXIMOS PASSOS

### Para Usar Banco de Dados Real (PostgreSQL)

1. **Instale PostgreSQL**
   - Baixe em: https://www.postgresql.org/download/

2. **Configure no .env**
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=nexus_supreme_db
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   ```

3. **Conecte no backend**
   - O servidor usará PostgreSQL em vez de dados em memória

### Para Aceitar Pagamentos (Stripe)

1. **Crie conta em: https://stripe.com**

2. **Adicione no .env**
   ```
   STRIPE_SECRET_KEY=sk_live_sua_chave
   STRIPE_PUBLIC_KEY=pk_live_sua_chave
   ```

### Para Deploy

```bash
# Build da aplicação
npm run build

# Deploy em produção
npm run start
```

---

## 📱 ACESSAR DE OUTRO COMPUTADOR

Se você quer acessar de outro PC na rede:

1. **Encontre o IP do seu computador**
   ```powershell
   ipconfig
   # Procure por "IPv4 Address" (ex: 192.168.1.100)
   ```

2. **Acesse via:**
   ```
   http://192.168.1.100:3000
   ```

---

## ⚠️ TROUBLESHOOTING

### "Node.js não encontrado"
- Instale em: https://nodejs.org/
- Reinicie o PowerShell após instalar

### "Porta 3000 já em uso"
- Mude no .env: `PORT=3001` (ou outra porta)
- Ou finalize o processo usando a porta:
  ```powershell
  netstat -ano | findstr :3000
  taskkill /PID <PID> /F
  ```

### "Erro de permissão no PowerShell"
- Execute como administrador
- Ou use: `powershell -ExecutionPolicy Bypass -File setup.ps1`

### "npm: comando não encontrado"
- Instale Node.js e NPM
- https://nodejs.org/

---

## 📞 SUPORTE

Se algo não funcionar:

1. Verifique o console do PowerShell para erros
2. Veja os logs em: `C:\Users\mathi\Downloads\NEXUSSUPREMO\logs\`
3. Tente novamente com:
   ```powershell
   cd backend
   npm install
   npm start
   ```

---

## ✅ CHECKLIST PÓS-SETUP

- [ ] Node.js e NPM instalados
- [ ] Script setup.ps1 executado com sucesso
- [ ] Backend iniciado (porta 3000)
- [ ] Frontend carrega em http://localhost:3000
- [ ] Login funciona com admin@nexus.com
- [ ] Login funciona com mmlightdesigner@gmail.com
- [ ] Dashboard carrega com dados
- [ ] Busca de domínios funciona

---

## 🎉 PARABÉNS!

Seu NEXUS SUPREME PRO está:
- ✅ Instalado
- ✅ Configurado
- ✅ Funcionando
- ✅ Pronto para usar

**Aproveite seu sistema profissional!** 🚀

---

**NEXUS SUPREME v3.0 | Enterprise Cookie Management System**
