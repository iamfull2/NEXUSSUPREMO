const http = require('http');
const url = require('url');
const crypto = require('crypto');

const PORT = process.env.PORT || 3000;

// ===================================================================
// DATABASE SIMULADO (Em produção usar PostgreSQL)
// ===================================================================

let users = [
  {
    id: 1,
    email: 'mathias2matheus2@gmail.com',
    password: 'mome200981@',
    name: 'Admin User',
    plan: 'Enterprise',
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    id: 2,
    email: 'mmlightdesigner@gmail.com',
    password: 'admin mmk200981@@@@',
    name: 'Light Designer',
    plan: 'Professional',
    createdAt: new Date(),
    updatedAt: new Date()
  }
];

let sessions = {};
let nextUserId = 3;

// ===================================================================
// UTILITY FUNCTIONS
// ===================================================================

function generateToken() {
  return crypto.randomBytes(32).toString('hex');
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', chunk => {
      data += chunk;
      if (data.length > 1e6) {
        reject(new Error('Payload too large'));
      }
    });
    req.on('end', () => {
      try {
        resolve(JSON.parse(data || '{}'));
      } catch (e) {
        reject(new Error('Invalid JSON'));
      }
    });
  });
}

function sendJSON(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
  });
  res.end(JSON.stringify(data));
}

function getAuthToken(req) {
  const authHeader = req.headers.authorization || '';
  return authHeader.replace('Bearer ', '');
}

function getUserFromToken(token) {
  if (sessions[token]) {
    return users.find(u => u.id === sessions[token].userId);
  }
  return null;
}

// ===================================================================
// ROUTES
// ===================================================================

const routes = {
  // Preflight CORS
  OPTIONS: (req, res) => {
    res.writeHead(200, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    res.end();
  },

  // Health check
  GET_health: (req, res) => {
    sendJSON(res, 200, { status: 'ok', timestamp: new Date().toISOString() });
  },

  // Root
  GET_root: (req, res) => {
    sendJSON(res, 200, {
      message: 'NEXUS SUPREME PRO - Backend API',
      version: '1.0.0',
      endpoints: {
        auth: '/api/auth/login',
        profile: '/api/me',
        domains: '/api/domains',
        stats: '/api/stats'
      }
    });
  },

  // Login
  POST_api_auth_login: async (req, res) => {
    try {
      const body = await parseBody(req);
      const user = users.find(u => u.email === body.email && u.password === body.password);
      
      if (user) {
        const token = generateToken();
        sessions[token] = {
          userId: user.id,
          createdAt: new Date(),
          expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
        };
        
        return sendJSON(res, 200, {
          success: true,
          token: token,
          user: {
            id: user.id,
            email: user.email,
            name: user.name,
            plan: user.plan
          }
        });
      } else {
        return sendJSON(res, 401, { success: false, message: 'Credenciais inválidas' });
      }
    } catch (e) {
      return sendJSON(res, 400, { error: e.message });
    }
  },

  // Get profile
  GET_api_me: (req, res) => {
    const token = getAuthToken(req);
    const user = getUserFromToken(token);
    
    if (!user) {
      return sendJSON(res, 401, { error: 'Unauthorized' });
    }
    
    return sendJSON(res, 200, {
      id: user.id,
      email: user.email,
      name: user.name,
      plan: user.plan,
      createdAt: user.createdAt,
      updatedAt: user.updatedAt
    });
  },

  // Update profile
  PUT_api_me: async (req, res) => {
    const token = getAuthToken(req);
    const user = getUserFromToken(token);
    
    if (!user) {
      return sendJSON(res, 401, { error: 'Unauthorized' });
    }
    
    try {
      const body = await parseBody(req);
      const userIndex = users.findIndex(u => u.id === user.id);
      
      if (body.name) users[userIndex].name = body.name;
      users[userIndex].updatedAt = new Date();
      
      return sendJSON(res, 200, {
        success: true,
        user: users[userIndex]
      });
    } catch (e) {
      return sendJSON(res, 400, { error: e.message });
    }
  },

  // Logout
  POST_api_auth_logout: (req, res) => {
    const token = getAuthToken(req);
    if (token && sessions[token]) {
      delete sessions[token];
    }
    return sendJSON(res, 200, { success: true, message: 'Logged out' });
  },

  // Get domains
  GET_api_domains: (req, res) => {
    const token = getAuthToken(req);
    const user = getUserFromToken(token);
    
    if (!user) {
      return sendJSON(res, 401, { error: 'Unauthorized' });
    }
    
    return sendJSON(res, 200, {
      success: true,
      domains: {
        'adobe.com': { cookies: 224, category: 'Creative', status: 'active' },
        'google.com': { cookies: 152, category: 'Productivity', status: 'active' },
        'freepik.com': { cookies: 98, category: 'Creative', status: 'active' },
        'amazon.com.br': { cookies: 87, category: 'E-commerce', status: 'active' },
        'github.com': { cookies: 65, category: 'Development', status: 'active' },
        'vercel.com': { cookies: 42, category: 'Development', status: 'active' }
      }
    });
  },

  // Get stats
  GET_api_stats: (req, res) => {
    const token = getAuthToken(req);
    const user = getUserFromToken(token);
    
    if (!user) {
      return sendJSON(res, 401, { error: 'Unauthorized' });
    }
    
    return sendJSON(res, 200, {
      success: true,
      stats: {
        totalDomains: 1282,
        totalCookies: 22500,
        activeDomains: 1200,
        uptime: 99.99,
        lastSync: new Date(),
        users: users.length,
        sessions: Object.keys(sessions).length
      }
    });
  },

  // List users (admin only)
  GET_api_users: (req, res) => {
    const token = getAuthToken(req);
    const user = getUserFromToken(token);
    
    if (!user || user.plan !== 'Enterprise') {
      return sendJSON(res, 403, { error: 'Forbidden' });
    }
    
    return sendJSON(res, 200, {
      success: true,
      users: users.map(u => ({
        id: u.id,
        email: u.email,
        name: u.name,
        plan: u.plan,
        createdAt: u.createdAt
      }))
    });
  }
};

// ===================================================================
// SERVER
// ===================================================================

const server = http.createServer(async (req, res) => {
  const pathname = url.parse(req.url).pathname;
  const method = req.method;
  
  // Route key
  const routeKey = `${method}_${pathname.replace(/\//g, '_').slice(1)}`;
  
  // Preflight CORS
  if (method === 'OPTIONS') {
    return routes.OPTIONS(req, res);
  }
  
  // Try to find route
  const routeHandler = routes[routeKey];
  if (routeHandler) {
    try {
      return await routeHandler(req, res);
    } catch (e) {
      return sendJSON(res, 500, { error: e.message });
    }
  }
  
  // Root
  if (pathname === '/' && method === 'GET') {
    return routes.GET_root(req, res);
  }
  
  // 404
  return sendJSON(res, 404, { error: 'Not found' });
});

server.listen(PORT, () => {
  console.log('');
  console.log('====================================================================');
  console.log('');
  console.log('            🏆 NEXUS SUPREME PRO - Backend Running');
  console.log('');
  console.log('====================================================================');
  console.log('');
  console.log('✅ Servidor rodando em: http://localhost:' + PORT);
  console.log('');
  console.log('🔐 Credenciais de teste:');
  console.log('   Email: mmlightdesigner@gmail.com');
  console.log('   Senha: admin mmk200981@@@@');
  console.log('');
  console.log('📊 Endpoints disponíveis:');
  console.log('   GET  /');
  console.log('   GET  /health');
  console.log('   POST /api/auth/login');
  console.log('   POST /api/auth/logout');
  console.log('   GET  /api/me');
  console.log('   PUT  /api/me');
  console.log('   GET  /api/domains');
  console.log('   GET  /api/stats');
  console.log('   GET  /api/users (Enterprise only)');
  console.log('');
  console.log('💻 Teste com curl:');
  console.log('   curl -X POST http://localhost:' + PORT + '/api/auth/login \\');
  console.log('     -H "Content-Type: application/json" \\');
  console.log('     -d \'{"email":"mmlightdesigner@gmail.com","password":"admin mmk200981@@@@"}\'');
  console.log('');
  console.log('Pressione Ctrl+C para parar');
  console.log('');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n👋 Servidor encerrado');
  process.exit(0);
});
