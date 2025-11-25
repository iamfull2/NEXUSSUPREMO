import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('mmlightdesigner@gmail.com');
  const [password, setPassword] = useState('admin mmk200981@@@@');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [domains, setDomains] = useState(null);
  const [stats, setStats] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');

  // API URL - mudar para sua URL do backend
  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:3000';

  useEffect(() => {
    if (token) {
      fetchUser();
      fetchDomains();
      fetchStats();
    }
  }, [token]);

  const fetchUser = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        localStorage.removeItem('token');
        setToken(null);
      }
    } catch (e) {
      console.error('Erro ao buscar usuário:', e);
    }
  };

  const fetchDomains = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/domains`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setDomains(data.domains);
      }
    } catch (e) {
      console.error('Erro ao buscar domínios:', e);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/stats`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setStats(data.stats);
      }
    } catch (e) {
      console.error('Erro ao buscar stats:', e);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (data.success) {
        localStorage.setItem('token', data.token);
        setToken(data.token);
        setUser(data.user);
        setError('');
      } else {
        setError('Credenciais inválidas');
      }
    } catch (e) {
      setError('Erro ao fazer login: ' + e.message);
    }
    setLoading(false);
  };

  const handleLogout = async () => {
    try {
      await fetch(`${API_BASE}/api/auth/logout`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
    } catch (e) {
      console.error('Erro ao fazer logout:', e);
    }
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setDomains(null);
    setStats(null);
  };

  if (!token) {
    return (
      <div className="login-container">
        <div className="login-card">
          <h1>🏆 NEXUS SUPREME PRO</h1>
          <p>Enterprise Cookie Management System</p>
          
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu-email@example.com"
              />
            </div>

            <div className="form-group">
              <label>Senha</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
              />
            </div>

            {error && <div className="error-message">{error}</div>}

            <button type="submit" disabled={loading} className="btn-login">
              {loading ? 'Entrando...' : 'Entrar'}
            </button>
          </form>

          <div className="demo-credentials">
            <p><strong>Demo:</strong></p>
            <p>📧 mmlightdesigner@gmail.com</p>
            <p>🔑 admin mmk200981@@@@</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-content">
          <h1>🏆 NEXUS SUPREME PRO</h1>
          <div className="user-info">
            <span>Bem-vindo, <strong>{user?.name}</strong></span>
            <button onClick={handleLogout} className="btn-logout">Sair</button>
          </div>
        </div>
      </header>

      <nav className="tabs">
        <button 
          className={`tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button 
          className={`tab ${activeTab === 'domains' ? 'active' : ''}`}
          onClick={() => setActiveTab('domains')}
        >
          🌐 Domínios
        </button>
        <button 
          className={`tab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          👤 Perfil
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'dashboard' && (
          <div className="dashboard">
            <h2>Dashboard</h2>
            
            {stats && (
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>Domínios Totais</h3>
                  <p className="stat-value">{stats.totalDomains?.toLocaleString()}</p>
                </div>
                <div className="stat-card">
                  <h3>Cookies Totais</h3>
                  <p className="stat-value">{stats.totalCookies?.toLocaleString()}</p>
                </div>
                <div className="stat-card">
                  <h3>Domínios Ativos</h3>
                  <p className="stat-value">{stats.activeDomains?.toLocaleString()}</p>
                </div>
                <div className="stat-card">
                  <h3>Uptime</h3>
                  <p className="stat-value">{stats.uptime}%</p>
                </div>
              </div>
            )}

            <div className="info-card">
              <h3>✅ Sistema Online!</h3>
              <p>Seu backend Python está conectado e funcionando perfeitamente.</p>
              <p><strong>Plano:</strong> {user?.plan}</p>
              <p><strong>Email:</strong> {user?.email}</p>
            </div>
          </div>
        )}

        {activeTab === 'domains' && (
          <div className="domains-section">
            <h2>Domínios</h2>
            
            {domains && (
              <div className="domains-list">
                {Object.entries(domains).map(([domain, data]) => (
                  <div key={domain} className="domain-card">
                    <div className="domain-header">
                      <h3>{domain}</h3>
                      <span className={`status ${data.status}`}>
                        {data.status === 'active' ? '🟢 Ativo' : '🔴 Inativo'}
                      </span>
                    </div>
                    <div className="domain-info">
                      <p><strong>Cookies:</strong> {data.cookies}</p>
                      <p><strong>Categoria:</strong> {data.category}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="profile-section">
            <h2>Meu Perfil</h2>
            
            <div className="profile-card">
              <div className="profile-field">
                <label>Nome</label>
                <p>{user?.name}</p>
              </div>
              
              <div className="profile-field">
                <label>Email</label>
                <p>{user?.email}</p>
              </div>
              
              <div className="profile-field">
                <label>Plano</label>
                <p><strong>{user?.plan}</strong></p>
              </div>

              <div className="profile-field">
                <label>Membro desde</label>
                <p>{new Date().toLocaleDateString('pt-BR')}</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
