#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          🏆 NEXUS SUPREME PRO - SISTEMA PROFISSIONAL FINAL               ║
║                                                                            ║
║     Cookie Management Engine | Multi-Domain Handler | Auto-Login Inject   ║
║                                                                            ║
║     Versão: 3.0 | Modo: Produção | Status: Enterprise-Ready              ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import json
import sqlite3
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURAÇÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

init(autoreset=True)

class Config:
    """Configuração centralizada"""
    SCRIPT_DIR = Path(__file__).parent.resolve()
    DATA_DIR = SCRIPT_DIR / "NEXUS_SUPREME_DATA"
    COOKIES_DIR = DATA_DIR / "cookies"
    LOGS_DIR = DATA_DIR / "logs"
    DB_FILE = COOKIES_DIR / "master_cookies.json"
    SQLITE_DB = DATA_DIR / "nexus.db"
    
    # Criar diretórios
    DATA_DIR.mkdir(exist_ok=True)
    COOKIES_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(LOGS_DIR / f"nexus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("NEXUS_PRO")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class Cookie:
    """Modelo de Cookie"""
    name: str
    value: str
    domain: str
    path: str = "/"
    secure: bool = False
    httpOnly: bool = False
    expiry: Optional[int] = None
    
    def to_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

class DomainCategory(Enum):
    """Categorias de domínios"""
    CREATIVE = "🎨 Creative"
    AI = "🤖 AI"
    SOCIAL = "🌐 Social"
    STREAMING = "📺 Streaming"
    PRODUCTIVITY = "💼 Productivity"
    ECOMMERCE = "🛒 E-commerce"
    DEV = "👨‍💻 Development"
    EDUCATION = "📚 Education"
    OTHER = "📌 Other"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CORE ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CookieDatabase:
    """Gerenciamento de banco de dados de cookies"""
    
    def __init__(self):
        self.db_file = Config.DB_FILE
        self.data: Dict[str, List[Dict]] = {}
        self.load()
    
    def load(self) -> bool:
        """Carrega BD"""
        try:
            if self.db_file.exists():
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                Config.logger.info(f"✅ BD carregado: {len(self.data)} domínios, {self._total_cookies()} cookies")
                return True
            return False
        except Exception as e:
            Config.logger.error(f"❌ Erro ao carregar BD: {e}")
            return False
    
    def save(self) -> bool:
        """Salva BD"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            Config.logger.info(f"💾 BD salvo: {len(self.data)} domínios")
            return True
        except Exception as e:
            Config.logger.error(f"❌ Erro ao salvar BD: {e}")
            return False
    
    def _total_cookies(self) -> int:
        return sum(len(v) for v in self.data.values())
    
    def get_domains(self, sort=True) -> List[str]:
        """Retorna lista de domínios"""
        domains = list(self.data.keys())
        return sorted(domains) if sort else domains
    
    def get_cookies_by_domain(self, domain: str) -> List[Dict]:
        """Retorna cookies de um domínio"""
        return self.data.get(domain, [])
    
    def search_domains(self, query: str) -> List[str]:
        """Busca domínios"""
        query = query.lower()
        return [d for d in self.get_domains() if query in d.lower()]
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        domains = self.get_domains()
        total_cookies = self._total_cookies()
        
        if not domains:
            return {}
        
        avg_cookies = total_cookies // len(domains)
        top_domains = sorted(self.data.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        
        return {
            "total_domains": len(domains),
            "total_cookies": total_cookies,
            "avg_cookies": avg_cookies,
            "top_domains": top_domains
        }
    
    def categorize_domain(self, domain: str) -> DomainCategory:
        """Categoriza domínio"""
        d = domain.lower()
        
        if any(x in d for x in ['adobe', 'freepik', 'canva', 'shutterstock', 'envato', 'figma']):
            return DomainCategory.CREATIVE
        elif any(x in d for x in ['openai', 'midjourney', 'leonardo', 'runway', 'chat']):
            return DomainCategory.AI
        elif any(x in d for x in ['facebook', 'instagram', 'twitter', 'linkedin']):
            return DomainCategory.SOCIAL
        elif any(x in d for x in ['netflix', 'youtube', 'twitch', 'hulu']):
            return DomainCategory.STREAMING
        elif any(x in d for x in ['google', 'microsoft', 'slack', 'dropbox', 'notion']):
            return DomainCategory.PRODUCTIVITY
        elif any(x in d for x in ['amazon', 'ebay', 'aliexpress', 'shopify']):
            return DomainCategory.ECOMMERCE
        elif any(x in d for x in ['github', 'gitlab', 'stackoverflow']):
            return DomainCategory.DEV
        elif any(x in d for x in ['udemy', 'coursera', 'skillshare']):
            return DomainCategory.EDUCATION
        else:
            return DomainCategory.OTHER

class BrowserEngine:
    """Motor de navegação e injeção de cookies"""
    
    def __init__(self):
        self.driver = None
    
    def init_chrome(self, headless=False) -> bool:
        """Inicializa Chrome com configurações profissionais"""
        try:
            options = Options()
            
            if headless:
                options.add_argument("--headless")
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--start-maximized")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            Config.logger.info("✅ Chrome inicializado")
            return True
        except Exception as e:
            Config.logger.error(f"❌ Erro ao inicializar Chrome: {e}")
            return False
    
    def inject_cookies(self, domain: str, cookies: List[Dict]) -> int:
        """Injeta cookies no navegador"""
        injected = 0
        
        for i, cookie in enumerate(cookies, 1):
            try:
                cookie_dict = {
                    'name': str(cookie.get('name', '')),
                    'value': str(cookie.get('value', '')),
                    'domain': domain
                }
                
                if 'path' in cookie:
                    cookie_dict['path'] = str(cookie['path'])
                if 'secure' in cookie:
                    cookie_dict['secure'] = bool(cookie['secure'])
                
                self.driver.add_cookie(cookie_dict)
                injected += 1
                
                if i % 50 == 0:
                    Config.logger.info(f"   {i}/{len(cookies)} cookies injetados")
            except Exception as e:
                pass
        
        Config.logger.info(f"✅ {injected}/{len(cookies)} cookies injetados")
        return injected
    
    def access_domain(self, domain: str, cookies: List[Dict]) -> bool:
        """Acessa domínio e injeta cookies"""
        try:
            url = f"https://{domain}"
            Config.logger.info(f"🚀 Acessando {url}...")
            
            self.driver.get(url)
            time.sleep(2)
            
            self.inject_cookies(domain, cookies)
            
            Config.logger.info("🔄 Recarregando página...")
            self.driver.refresh()
            time.sleep(3)
            
            Config.logger.info(f"🎉 Pronto! Logado em {domain}")
            return True
        except Exception as e:
            Config.logger.error(f"❌ Erro ao acessar {domain}: {e}")
            return False
    
    def close(self):
        """Fecha navegador"""
        if self.driver:
            self.driver.quit()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UI LAYER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class UIManager:
    """Gerenciador de interface"""
    
    def __init__(self, db: CookieDatabase):
        self.db = db
        self.browser = BrowserEngine()
    
    def show_banner(self):
        """Mostra banner"""
        print(f"\n{Fore.GREEN}{'='*70}")
        print("🏆 NEXUS SUPREME PRO v3.0")
        print(f"{'='*70}{Style.RESET_ALL}\n")
    
    def show_dashboard(self):
        """Dashboard principal"""
        stats = self.db.get_stats()
        
        if not stats:
            print(f"{Fore.RED}Nenhum dado disponível{Style.RESET_ALL}\n")
            return
        
        print(f"\n{Fore.CYAN}📊 DASHBOARD{Style.RESET_ALL}\n")
        print(f"  Domínios: {stats['total_domains']}")
        print(f"  Cookies Total: {stats['total_cookies']:,}")
        print(f"  Média por Domínio: {stats['avg_cookies']}\n")
        
        print(f"{Fore.YELLOW}Top 5 Domínios:{Style.RESET_ALL}\n")
        for i, (domain, cookies) in enumerate(stats['top_domains'][:5], 1):
            category = self.db.categorize_domain(domain)
            print(f"  {i}. {category.value} {domain:40s} ({len(cookies):3d} cookies)")
        print()
    
    def browse_paginated(self, page_size=50):
        """Navegação paginada"""
        domains = self.db.get_domains()
        total_pages = (len(domains) + page_size - 1) // page_size
        current_page = 1
        
        while True:
            start = (current_page - 1) * page_size
            end = start + page_size
            page_domains = domains[start:end]
            
            print(f"\n{Fore.GREEN}{'='*70}")
            print(f"📖 PÁGINA {current_page}/{total_pages}")
            print(f"{'='*70}{Style.RESET_ALL}\n")
            
            for i, domain in enumerate(page_domains, start + 1):
                cookies = len(self.db.get_cookies_by_domain(domain))
                category = self.db.categorize_domain(domain)
                print(f"  [{i:4d}] {category.value:20s} {domain:40s} ({cookies:3d})")
            
            print(f"\n{Fore.CYAN}[P]róxima [A]nterior [B]uscar [S]elecionar [Q]uit\n")
            choice = input(f"{Fore.CYAN}Escolha: {Style.RESET_ALL}").strip().upper()
            
            if choice == "Q":
                break
            elif choice == "P" and current_page < total_pages:
                current_page += 1
            elif choice == "A" and current_page > 1:
                current_page -= 1
            elif choice == "B":
                self.search_and_access()
                break
            elif choice == "S":
                domain = input(f"{Fore.CYAN}Domínio: {Style.RESET_ALL}").strip()
                self.access_domain(domain)
                break
    
    def search_and_access(self):
        """Busca e acessa"""
        query = input(f"\n{Fore.CYAN}Buscar (ex: google, adobe): {Style.RESET_ALL}").strip()
        results = self.db.search_domains(query)
        
        if not results:
            print(f"{Fore.RED}Nenhum resultado{Style.RESET_ALL}\n")
            return
        
        print(f"\n{Fore.GREEN}Encontrados {len(results)}:{Style.RESET_ALL}\n")
        
        for i, domain in enumerate(results[:50], 1):
            cookies = len(self.db.get_cookies_by_domain(domain))
            print(f"  [{i:2d}] {domain:50s} ({cookies:3d})")
        
        choice = input(f"\n{Fore.CYAN}Selecione (número ou domínio exato): {Style.RESET_ALL}").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                self.access_domain(results[idx])
        else:
            self.access_domain(choice)
    
    def access_domain(self, domain: str):
        """Acessa domínio"""
        cookies = self.db.get_cookies_by_domain(domain)
        
        if not cookies:
            print(f"{Fore.RED}Domínio não encontrado{Style.RESET_ALL}\n")
            return
        
        print(f"\n{Fore.CYAN}Injetando {len(cookies)} cookies em {domain}...{Style.RESET_ALL}")
        
        if self.browser.init_chrome():
            self.browser.access_domain(domain, cookies)
            
            try:
                input(f"\n{Fore.YELLOW}Pressione ENTER para fechar...{Style.RESET_ALL}")
            except:
                pass
            
            self.browser.close()
    
    def run(self):
        """Loop principal"""
        while True:
            self.show_banner()
            self.show_dashboard()
            
            print("  [1] 📖 Navegar Domínios")
            print("  [2] 🔍 Buscar e Acessar")
            print("  [3] 📊 Estatísticas Completas")
            print("  [0] ❌ Sair\n")
            
            choice = input(f"{Fore.CYAN}Escolha: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.browse_paginated()
            elif choice == "2":
                self.search_and_access()
            elif choice == "3":
                self.show_full_stats()
            elif choice == "0":
                print(f"\n{Fore.CYAN}👋 Até logo!\n{Style.RESET_ALL}")
                break
    
    def show_full_stats(self):
        """Estatísticas completas"""
        stats = self.db.get_stats()
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print("📊 ESTATÍSTICAS COMPLETAS")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        print(f"  Total de Domínios: {stats['total_domains']}")
        print(f"  Total de Cookies: {stats['total_cookies']:,}")
        print(f"  Média por Domínio: {stats['avg_cookies']}\n")
        
        print(f"{Fore.YELLOW}Top 10 Domínios:{Style.RESET_ALL}\n")
        for i, (domain, cookies) in enumerate(stats['top_domains'], 1):
            print(f"  {i:2d}. {domain:50s} ({len(cookies):4d})")
        
        input(f"\n{Fore.YELLOW}Pressione ENTER...{Style.RESET_ALL}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    """Entrada principal"""
    try:
        db = CookieDatabase()
        
        if not db.data:
            print(f"{Fore.RED}Nenhum cookie encontrado. Execute parser primeiro.{Style.RESET_ALL}\n")
            return
        
        ui = UIManager(db)
        ui.run()
    
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}⏹️  Interrompido pelo usuário\n{Style.RESET_ALL}")
    except Exception as e:
        Config.logger.error(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()
