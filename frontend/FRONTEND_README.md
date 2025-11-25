# 🎨 FRONTEND REACT - NEXUS SUPREME PRO

## 📋 Estrutura

```
frontend/
├── src/
│   ├── App.jsx              # Componente principal
│   ├── App.css              # Estilos
│   ├── index.js             # Entry point
│   └── index.css            # Estilos globais
├── public/
│   └── index.html           # HTML principal
├── package.json             # Dependências
├── .env.example             # Variáveis de ambiente
└── README.md                # Este arquivo
```

## 🚀 Quick Start

### 1. Instale dependências

```bash
npm install
```

### 2. Configure variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env` e configure:
```
REACT_APP_API_URL=http://localhost:3000
```

### 3. Inicie o servidor local

```bash
npm start
```

Acesse: `http://localhost:3000`

## 🔐 Credenciais de Teste

```
Email: mmlightdesigner@gmail.com
Senha: admin mmk200981@@@@
```

## 📊 Features

✅ **Login JWT** - Autenticação segura com tokens
✅ **Dashboard** - Visualização de estatísticas
✅ **Domínios** - Listagem de domínios gerenciados
✅ **Perfil** - Gerenciamento de perfil do usuário
✅ **Responsive** - Funciona em desktop e mobile
✅ **Dark Mode** - Interface escura profissional
✅ **API Integration** - Conecta com seu backend Python

## 🔗 Conectando com Backend Python

O frontend se conecta automaticamente com o backend via:

```javascript
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3000';
```

### Endpoints esperados:

- `POST /api/auth/login` - Fazer login
- `POST /api/auth/logout` - Fazer logout
- `GET /api/me` - Obter perfil do usuário
- `GET /api/domains` - Listar domínios
- `GET /api/stats` - Obter estatísticas

## 📱 Deploy

### Vercel

1. **Crie conta em:** https://vercel.com

2. **Configure variável de ambiente:**
   ```
   REACT_APP_API_URL = https://seu-backend.vercel.app
   ```

3. **Deploy automático:**
   ```bash
   vercel
   ```

### GitHub Pages

```bash
npm run build
# Deploy a pasta 'build'
```

## 🛠️ Desenvolvimento

### Estrutura do Projeto

**App.jsx** - Componente principal com:
- Estado global (token, usuário, dados)
- Funções de login/logout
- Fetch de dados da API
- Navegação entre abas

**App.css** - Estilos com:
- Design system coerente
- Variáveis CSS
- Componentes reutilizáveis
- Responsividade total

### Adicionar novas páginas

```jsx
// Adicione em App.jsx
const [activeTab, setActiveTab] = useState('nova-aba');

// Adicione tab button em <nav>
<button 
  className={`tab ${activeTab === 'nova-aba' ? 'active' : ''}`}
  onClick={() => setActiveTab('nova-aba')}
>
  📄 Nova Aba
</button>

// Adicione em <main>
{activeTab === 'nova-aba' && (
  <div className="nova-aba-section">
    {/* Seu conteúdo */}
  </div>
)}
```

## 🎨 Customização

### Cores

Edite `:root` em `App.css`:

```css
:root {
  --primary: #3b82f6;
  --primary-dark: #2563eb;
  --bg-primary: #0f172a;
  /* etc */
}
```

### Fontes

Mude em `App.css`:

```css
body {
  font-family: 'Sua fonte aqui';
}
```

### Layout

Ajuste em cada seção CSS:

```css
.stats-grid {
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
```

## ⚙️ Troubleshooting

### ❌ "Cannot find module 'react'"
```bash
npm install
```

### ❌ "CORS error"
Verifique se o backend permite CORS:
```javascript
res.setHeader('Access-Control-Allow-Origin', '*');
```

### ❌ "Login não funciona"
1. Verifique se backend está rodando
2. Verifique `REACT_APP_API_URL` em `.env`
3. Abra DevTools → Network e veja requisição

### ❌ "Deploy no Vercel falha"
1. Verifique `npm run build` localmente
2. Configure variáveis de ambiente no Vercel
3. Veja logs: `vercel logs`

## 📚 Recursos

- React Docs: https://react.dev
- Vercel Docs: https://vercel.com/docs
- JavaScript Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

## 🔄 Próximas Melhorias

- [ ] Integração com mais endpoints
- [ ] Temas customizáveis
- [ ] Modo offline com IndexedDB
- [ ] Notificações em tempo real (WebSocket)
- [ ] Mobile app (React Native)
- [ ] PWA (Progressive Web App)

## 📝 Licença

MIT - Use como quiser

---

**NEXUS SUPREME PRO** - Frontend React Professional
Desenvolvido com ❤️ para integração perfeita com seu backend Python
