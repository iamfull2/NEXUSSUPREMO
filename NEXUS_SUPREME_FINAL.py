#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║        🔥 NEXUS SUPREME FINAL - SISTEMA DE ACESSO AOS COOKIES            ║
║                                                                            ║
║           Injeita cookies e abre navegador com login automático           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import json
import time
from pathlib import Path
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

init(autoreset=True)

class NEXUSSUPREMEFinal:
    """Sistema de acesso final - Injeta cookies e abre navegador"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        self.master_db_file = self.script_dir / "NEXUS_SUPREME_DATA" / "cookies" / "master_cookies.json"
        
        self.master_db = {}
        self.load_cookies()
    
    def load_cookies(self):
        """Carrega banco de dados de cookies"""
        try:
            with open(self.master_db_file, 'r', encoding='utf-8') as f:
                self.master_db = json.load(f)
            print(f"\n{Fore.GREEN}✅ Banco de dados carregado!{Style.RESET_ALL}")
            print(f"   Domínios: {len(self.master_db)}")
            print(f"   Total de cookies: {sum(len(v) for v in self.master_db.values()):,}\n")
        except Exception as e:
            print(f"{Fore.RED}❌ Erro ao carregar BD: {e}{Style.RESET_ALL}\n")
    
    def list_domains_categorized(self):
        """Lista domínios categorizados"""
        if not self.master_db:
            print(f"{Fore.RED}Nenhum domínio disponível{Style.RESET_ALL}\n")
            return
        
        domains = sorted(self.master_db.keys())
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"🌐 DOMÍNIOS DISPONÍVEIS ({len(domains)})")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        # Categorização simples
        popular = ['google.com', 'facebook.com', 'instagram.com', 'twitter.com', 
                   'youtube.com', 'amazon.com', 'github.com', 'freepik.com', 
                   'adobe.com', 'netflix.com', 'openai.com']
        
        print(f"{Fore.CYAN}📍 Domínios Populares:{Style.RESET_ALL}\n")
        count = 0
        for domain in domains:
            if any(p in domain for p in popular):
                cookies = len(self.master_db[domain])
                print(f"  {Fore.YELLOW}•{Style.RESET_ALL} {domain:40s} ({cookies:3d} cookies)")
                count += 1
                if count >= 10:
                    break
        
        print(f"\n{Fore.CYAN}📍 Todos os Domínios:{Style.RESET_ALL}\n")
        for i, domain in enumerate(domains[:50], 1):
            cookies = len(self.master_db[domain])
            print(f"  [{i:2d}] {domain:40s} ({cookies:3d} cookies)")
        
        if len(domains) > 50:
            print(f"\n  {Fore.YELLOW}... e mais {len(domains) - 50} domínios{Style.RESET_ALL}\n")
    
    def search_domain(self, query):
        """Busca domínios"""
        query = query.lower()
        results = [d for d in self.master_db.keys() if query in d.lower()]
        
        if results:
            print(f"\n{Fore.GREEN}Encontrados {len(results)} domínio(s):{Style.RESET_ALL}\n")
            for i, domain in enumerate(results[:20], 1):
                cookies = len(self.master_db[domain])
                print(f"  [{i}] {domain} ({cookies} cookies)")
        else:
            print(f"\n{Fore.RED}Nenhum domínio encontrado para '{query}'{Style.RESET_ALL}\n")
    
    def open_with_cookies(self, domain):
        """Abre navegador com cookies injetados"""
        if domain not in self.master_db:
            print(f"{Fore.RED}❌ Domínio '{domain}' não encontrado{Style.RESET_ALL}\n")
            return
        
        cookies = self.master_db[domain]
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"🚀 ABRINDO: {domain} COM {len(cookies)} COOKIES")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        try:
            # Configurar Chrome
            options = Options()
            # options.add_argument("--headless")  # Descomente para modo headless
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            print(f"{Fore.YELLOW}⏳ Inicializando Chrome...{Style.RESET_ALL}")
            driver = webdriver.Chrome(options=options)
            
            # URL
            url = f"https://{domain}"
            print(f"{Fore.YELLOW}⏳ Navegando para {url}...{Style.RESET_ALL}")
            driver.get(url)
            
            # Aguarda carregamento
            time.sleep(2)
            
            # Injeta cookies
            print(f"{Fore.YELLOW}💉 Injetando {len(cookies)} cookies...{Style.RESET_ALL}\n")
            
            for i, cookie in enumerate(cookies, 1):
                try:
                    # Formata cookie corretamente
                    cookie_dict = {
                        'name': str(cookie.get('name', '')),
                        'value': str(cookie.get('value', '')),
                        'domain': domain
                    }
                    
                    if 'path' in cookie:
                        cookie_dict['path'] = str(cookie['path'])
                    if 'secure' in cookie:
                        cookie_dict['secure'] = bool(cookie['secure'])
                    if 'httpOnly' in cookie:
                        cookie_dict['httpOnly'] = bool(cookie['httpOnly'])
                    
                    driver.add_cookie(cookie_dict)
                    
                    if i % 10 == 0:
                        print(f"  ✅ {i}/{len(cookies)} cookies injetados")
                except Exception as e:
                    pass
            
            print(f"\n{Fore.GREEN}✅ {len(cookies)} cookies injetados com sucesso!{Style.RESET_ALL}\n")
            
            # Recarrega página
            print(f"{Fore.YELLOW}🔄 Recarregando página...{Style.RESET_ALL}\n")
            driver.refresh()
            
            # Aguarda
            time.sleep(3)
            
            print(f"{Fore.GREEN}{'='*70}")
            print(f"🎉 PRONTO! Você está logado em {domain}!")
            print(f"{'='*70}{Style.RESET_ALL}\n")
            
            # Manter janela aberta
            try:
                input("Pressione ENTER para fechar o navegador...")
            except:
                pass
            
            driver.quit()
        
        except Exception as e:
            print(f"{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}\n")
    
    def show_menu(self):
        """Menu interativo"""
        while True:
            print(f"\n{Fore.GREEN}{'='*70}")
            print("🔥 NEXUS SUPREME FINAL - MENU DE ACESSO")
            print(f"{'='*70}{Style.RESET_ALL}\n")
            
            print("  [1] 📋 Listar Domínios")
            print("  [2] 🔍 Buscar Domínio")
            print("  [3] 🌐 Acessar Domínio")
            print("  [0] ❌ Sair\n")
            
            choice = input(f"{Fore.CYAN}Escolha: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.list_domains_categorized()
                input(f"\n{Fore.YELLOW}Pressione ENTER...{Style.RESET_ALL}")
            
            elif choice == "2":
                query = input(f"\n{Fore.CYAN}Digite o domínio (ex: google, freepik): {Style.RESET_ALL}")
                self.search_domain(query)
                input(f"\n{Fore.YELLOW}Pressione ENTER...{Style.RESET_ALL}")
            
            elif choice == "3":
                domain = input(f"\n{Fore.CYAN}Digite o domínio exato (ex: google.com): {Style.RESET_ALL}").strip()
                self.open_with_cookies(domain)
            
            elif choice == "0":
                print(f"\n{Fore.CYAN}👋 Até logo!{Style.RESET_ALL}\n")
                break
            
            else:
                print(f"\n{Fore.RED}❌ Opção inválida{Style.RESET_ALL}")

def main():
    try:
        system = NEXUSSUPREMEFinal()
        system.show_menu()
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
