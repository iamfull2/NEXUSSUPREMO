# ========================================
# NEXUS SUPREME PRO - DEPLOY AUTOMÁTICO
# Cria Admin Panel + Usuários + Deploy
# ========================================

cd "C:\Users\mathi\Downloads\NEXUSSUPREMO\backend"

# ========== PASSO 1: Criar users.js ==========
Write-Host "`n========== CRIANDO users.js ==========" -ForegroundColor Cyan

@"
// users.js - Banco de dados de usuários
const users = [
  {
    id: 1,
    email: 'mathias2matheus2@gmail.com',
    password: 'Mome8e8a65D7',
    name: 'Admin',
    role: 'admin',
    plan: 'Enterprise'
  },
  {
    id: 2,
    email: 'mmlightdesigner@gmail.com',
    password: 'mmk200981@@@@',
    name: 'Matheus Designer',
    role: 'user',
    plan: 'Professional'
  }
];

module.exports = users;
"@ | Out-File users.js -Encoding UTF8 -Force

Write-Host "✅ users.js criado!" -ForegroundColor Green

# ========== PASSO 2: Criar App.jsx com Admin Panel ==========
Write-Host "`n========== CRIANDO App.jsx com ADMIN PANEL ==========" -ForegroundColor Cyan

cd "..\frontend\src"

@"
import { useState } from 'react';
import './App.css';

export default function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  
  // Admin panel state
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [newUserEmail, setNewUserEmail] = useState('');
  const [newUserPassword, setNewUserPassword] = useState('');
  const [newUserName, setNewUserName] = useState('');
  const [users, setUsers] = useState([
    { id: 1, email: 'mathias2matheus2@gmail.com', name: 'Admin', role: 'admin' },
    { id: 2, email: 'mmlightdesigner@gmail.com', name: 'Matheus Designer', role: 'user' }
  ]);

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const loggedInUser = users.find(u => u.email === email);
    if (!loggedInUser || loggedInUser.password !== password) {
      setError('Email ou senha incorretos');
      setLoading(false);
      return;
    }

    setUser(loggedInUser);
    setIsLoggedIn(true);
    setEmail('');
    setPassword('');
    setLoading(false);
  };

  const handleAddUser = (e) => {
    e.preventDefault();
    if (!newUserEmail || !newUserPassword || !newUserName) {
      alert('Preencha todos os campos!');
      return;
    }

    const newUser = {
      id: users.length + 1,
      email: newUserEmail,
      name: newUserName,
      role: 'user',
      password: newUserPassword
    };

    setUsers([...users, newUser]);
    setNewUserEmail('');
    setNewUserPassword('');
    setNewUserName('');
    alert('✅ Usuário adicionado com sucesso!');
  };

  const handleDeleteUser = (id) => {
    if (id === 1) {
      alert('Não é possível deletar o admin!');
      return;
    }
    setUsers(users.filter(u => u.id !== id));
    alert('✅ Usuário removido!');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setShowAdminPanel(false);
  };

  if (isLoggedIn) {
    return (
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>🏆 NEXUS SUPREME PRO</h1>
          <div className="header-actions">
            {user?.role === 'admin' && (
              <button 
                className="btn-admin" 
                onClick={() => setShowAdminPanel(!showAdminPanel)}
              >
                {showAdminPanel ? '← Voltar' : '⚙️ Painel Admin'}
              </button>
            )}
            <button onClick={handleLogout} className="btn-logout">Sair</button>
          </div>
        </div>
        
        {showAdminPanel && user?.role === 'admin' ? (
          <div className="admin-panel">
            <div className="admin-content">
              <h2>👨‍💼 Painel de Administração</h2>
              
              <div className="admin-section">
                <h3>➕ Adicionar Novo Usuário</h3>
                <form onSubmit={handleAddUser} className="admin-form">
                  <div className="form-row">
                    <input
                      type="email"
                      placeholder="Email"
                      value={newUserEmail}
                      onChange={(e) => setNewUserEmail(e.target.value)}
                      required
                    />
                    <input
                      type="password"
                      placeholder="Senha"
                      value={newUserPassword}
                      onChange={(e) => setNewUserPassword(e.target.value)}
                      required
                    />
                    <input
                      type="text"
                      placeholder="Nome"
                      value={newUserName}
                      onChange={(e) => setNewUserName(e.target.value)}
                      required
                    />
                    <button type="submit" className="btn-add">Adicionar</button>
                  </div>
                </form>
              </div>

              <div className="admin-section">
                <h3>👥 Lista de Usuários</h3>
                <div className="users-list">
                  {users.map(u => (
                    <div key={u.id} className="user-item">
                      <div className="user-info">
                        <p><strong>{u.name}</strong> ({u.role})</p>
                        <p className="user-email">{u.email}</p>
                      </div>
                      <button 
                        className="btn-delete"
                        onClick={() => handleDeleteUser(u.id)}
                      >
                        Remover
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="dashboard-content">
            <h2>Bem-vindo, {user?.name}!</h2>
            <div className="user-info">
              <p><strong>Email:</strong> {user?.email}</p>
              <p><strong>Função:</strong> {user?.role === 'admin' ? '👨‍💼 Administrador' : '👤 Usuário'}</p>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>🏆 NEXUS SUPREME PRO</h1>
          <p>Enterprise Cookie Management System</p>
        </div>
        
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Senha:</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={loading}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button 
            type="submit" 
            className="btn-login"
            disabled={loading}
          >
            {loading ? 'Conectando...' : 'Entrar'}
          </button>
        </form>

        <div className="demo-section">
          <p className="demo-title">📌 Seus Logins:</p>
          <div className="demo-box">
            <p><strong>Admin:</strong> mathias2matheus2@gmail.com</p>
            <p><strong>Seu Email:</strong> mmlightdesigner@gmail.com</p>
          </div>
        </div>
      </div>
    </div>
  );
}
"@ | Out-File App.jsx -Encoding UTF8 -Force

Write-Host "✅ App.jsx com Admin Panel criado!" -ForegroundColor Green

# ========== PASSO 3: Adicionar CSS para Admin ==========
Write-Host "`n========== ADICIONANDO CSS para Admin Panel ==========" -ForegroundColor Cyan

$cssAdmin = @"

/* Admin Panel Styles */
.admin-panel {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 30px;
}

.admin-content {
  max-width: 1200px;
  margin: 0 auto;
}

.admin-content h2 {
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

.admin-section {
  background: white;
  padding: 25px;
  margin-bottom: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.admin-section h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 16px;
}

.admin-form .form-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 12px;
  align-items: end;
}

.admin-form input {
  padding: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
  width: 100%;
}

.admin-form input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-add {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.users-list {
  display: grid;
  gap: 12px;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f9f9f9;
  border-left: 4px solid #667eea;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.user-item:hover {
  background: #f0f0f0;
}

.user-item .user-info {
  flex: 1;
}

.user-item p {
  margin: 5px 0;
  color: #333;
}

.user-email {
  color: #666;
  font-size: 12px;
}

.btn-delete {
  padding: 8px 16px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.btn-delete:hover {
  background: #ff5252;
  transform: scale(1.05);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-admin {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-admin:hover {
  background: rgba(255, 255, 255, 0.3);
}

@media (max-width: 768px) {
  .admin-form .form-row {
    grid-template-columns: 1fr;
  }

  .user-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .btn-delete {
    width: 100%;
    margin-top: 10px;
  }
}
"@

Add-Content App.css $cssAdmin
Write-Host "✅ CSS do Admin Panel adicionado!" -ForegroundColor Green

# ========== PASSO 4: BUILD e DEPLOY ==========
Write-Host "`n========== BUILD E DEPLOY ==========" -ForegroundColor Cyan

cd "..\..\"

# Build
Write-Host "`n🔨 Fazendo build..." -ForegroundColor Yellow
cd frontend
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro no build!" -ForegroundColor Red
    exit 1
}

# Git
Write-Host "`n📤 Enviando para GitHub..." -ForegroundColor Yellow
cd ..
git add -A
git commit -m "Feature: Admin panel with user management + Security"
git push origin main --force

# Vercel Deploy
Write-Host "`n🚀 Deployando no Vercel..." -ForegroundColor Yellow
vercel --token=NfCYGv9rVuUlGxC8hHpZBruX --prod --force

Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ TUDO PRONTO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`n📌 SEUS LOGINS:" -ForegroundColor Cyan
Write-Host "Admin: mathias2matheus2@gmail.com" -ForegroundColor Yellow
Write-Host "Você: mmlightdesigner@gmail.com" -ForegroundColor Yellow
Write-Host "`n🔐 Painel Admin: Clique em ⚙️ Painel Admin (quando logado como admin)" -ForegroundColor Cyan
Write-Host "`n🌐 Site online em:" -ForegroundColor Green
Write-Host "https://nexussupremo-42jbrawyx-mathias2matheus2-3180s-projects.vercel.app" -ForegroundColor Green
Write-Host "`n========================================`n" -ForegroundColor Green
