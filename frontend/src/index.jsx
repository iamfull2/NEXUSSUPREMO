import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// ===================================================================
// CONFIGURAÇÃO INICIAL
// ===================================================================

// Tema padrão (dark mode)
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
if (prefersDark) {
  document.documentElement.setAttribute('data-color-scheme', 'dark');
} else {
  document.documentElement.setAttribute('data-color-scheme', 'light');
}

// Listen para mudanças de tema do sistema
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (e.matches) {
    document.documentElement.setAttribute('data-color-scheme', 'dark');
  } else {
    document.documentElement.setAttribute('data-color-scheme', 'light');
  }
});

// ===================================================================
// RENDERIZAÇÃO
// ===================================================================

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// ===================================================================
// PERFORMANCE: Service Worker (PWA)
// ===================================================================

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // Uncommment para ativar PWA
    // navigator.serviceWorker.register('/service-worker.js').then(
    //   (registration) => {
    //     console.log('Service Worker registrado:', registration);
    //   },
    //   (error) => {
    //     console.log('Service Worker erro:', error);
    //   }
    // );
  });
}

// ===================================================================
// ANALYTICS & ERROR TRACKING
// ===================================================================

// Error boundary global
window.addEventListener('error', (event) => {
  console.error('❌ Erro capturado:', event.error);
  // Enviar para analytics service
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('❌ Promise rejeitada:', event.reason);
  // Enviar para analytics service
});

// ===================================================================
// LOGS
// ===================================================================

console.log('%c🏆 NEXUS SUPREME PRO v1.0.0', 'color: #3b82f6; font-size: 16px; font-weight: bold;');
console.log('%cEnvironment: ' + (process.env.NODE_ENV || 'development'), 'color: #10b981;');
console.log('%cAPI URL: ' + (process.env.REACT_APP_API_URL || 'http://localhost:3000'), 'color: #f59e0b;');
console.log('%c© 2024 NEXUS SUPREME PRO. All rights reserved.', 'color: #6b7280; font-style: italic;');
