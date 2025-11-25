#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║    🔥 NEXUS SUPREME v2.0 - NAVEGADOR COMPLETO DE COOKIES                ║
║                                                                            ║
║       Navegue por todos os 1.282 domínios com paginação                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import json
import time
from pathlib import Path
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

init(autoreset=True)

class NEXUSSUPREMEv20:
    """Sistema v2.0 - Navegador completo com paginação"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        self.master_db_file = self.script_dir / "NEXUS_SUPREME_DATA" / "cookies" / "master_cookies.json"
        
        self.master_db = {}
        self.load_cookies()
        self.domains_list = sorted(self.master_db.keys())
    
    def load_cookies(self):
        """Carrega banco de dados"""
        try:
            with open(self.master_db_file, 'r', encoding='utf-8') as f:
                self.master_db = json.load(f)
            print(f"\n{Fore.GREEN}✅ Banco de dados carregado!{Style.RESET_ALL}")
            print(f"   Domínios: {len(self.master_db)}")
            print(f"   Total de cookies: {sum(len(v) for v in self.master_db.values()):,}\n")
        except Exception as e:
            print(f"{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}\n")
    
    def list_domains_paginated(self, page=1, per_page=50):
        """Lista domínios com paginação"""
        total_domains = len(self.domains_list)
        total_pages = (total_domains + per_page - 1) // per_page
        
        if page < 1 or page > total_pages:
            print(f"{Fore.RED}❌ Página inválida{Style.RESET_ALL}\n")
            return
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_domains = self.domains_list[start_idx:end_idx]
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"🌐 DOMÍNIOS DISPONÍVEIS - PÁGINA {page}/{total_pages}")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        for i, domain in enumerate(page_domains, start_idx + 1):
            cookies = len(self.master_db[domain])
            print(f"  [{i:4d}] {domain:50s} ({cookies:3d} cookies)")
        
        print(f"\n{Fore.CYAN}Página {page} de {total_pages}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Mostrando {len(page_domains)} domínios (total: {total_domains})\n")
    
    def navigate_domains(self):
        """Navegação completa de domínios"""
        total_domains = len(self.domains_list)
        total_pages = (total_domains + 50 - 1) // 50
        current_page = 1
        
        while True:
            self.list_domains_paginated(current_page, 50)
            
            print(f"{Fore.CYAN}Opções:{Style.RESET_ALL}")
            print(f"  [1-{total_pages}] Ir para página")
            print(f"  [P] Próxima")
            print(f"  [A] Anterior")
            print(f"  [B] Buscar domínio")
            print(f"  [S] Selecionar domínio")
            print(f"  [0] Voltar\n")
            
            choice = input(f"{Fore.CYAN}Escolha: {Style.RESET_ALL}").strip().upper()
            
            if choice == "0":
                break
            
            elif choice == "P":
                if current_page < total_pages:
                    current_page += 1
                else:
                    print(f"{Fore.RED}Você já está na última página{Style.RESET_ALL}\n")
            
            elif choice == "A":
                if current_page > 1:
                    current_page -= 1
                else:
                    print(f"{Fore.RED}Você já está na primeira página{Style.RESET_ALL}\n")
            
            elif choice == "B":
                self.search_and_select()
                break
            
            elif choice == "S":
                domain = input(f"\n{Fore.CYAN}Digite o domínio exato: {Style.RESET_ALL}").strip()
                if domain in self.master_db:
                    self.open_with_cookies(domain)
                else:
                    print(f"{Fore.RED}Domínio não encontrado{Style.RESET_ALL}\n")
                break
            
            elif choice.isdigit():
                page_num = int(choice)
                if 1 <= page_num <= total_pages:
                    current_page = page_num
                else:
                    print(f"{Fore.RED}Página inválida (1-{total_pages}){Style.RESET_ALL}\n")
            
            else:
                print(f"{Fore.RED}Opção inválida{Style.RESET_ALL}\n")
    
    def search_and_select(self):
        """Busca e seleciona domínio"""
        query = input(f"\n{Fore.CYAN}Digite parte do domínio (ex: google, adobe): {Style.RESET_ALL}").strip().lower()
        
        results = [d for d in self.domains_list if query in d.lower()]
        
        if not results:
            print(f"{Fore.RED}Nenhum domínio encontrado para '{query}'{Style.RESET_ALL}\n")
            return
        
        print(f"\n{Fore.GREEN}Encontrados {len(results)} domínio(s):{Style.RESET_ALL}\n")
        
        for i, domain in enumerate(results[:100], 1):
            cookies = len(self.master_db[domain])
            print(f"  [{i:3d}] {domain:50s} ({cookies:3d} cookies)")
        
        if len(results) > 100:
            print(f"\n  {Fore.YELLOW}... e mais {len(results) - 100} domínios{Style.RESET_ALL}")
        
        print()
        choice = input(f"{Fore.CYAN}Digite o número ou domínio exato (0 para cancelar): {Style.RESET_ALL}").strip()
        
        if choice == "0":
            return
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                selected = results[idx]
                self.open_with_cookies(selected)
            else:
                print(f"{Fore.RED}Número inválido{Style.RESET_ALL}\n")
        else:
            if choice in self.master_db:
                self.open_with_cookies(choice)
            else:
                print(f"{Fore.RED}Domínio não encontrado{Style.RESET_ALL}\n")
    
    def open_with_cookies(self, domain):
        """Abre navegador com cookies"""
        if domain not in self.master_db:
            print(f"{Fore.RED}❌ Domínio não encontrado{Style.RESET_ALL}\n")
            return
        
        cookies = self.master_db[domain]
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"🚀 ABRINDO: {domain} COM {len(cookies)} COOKIES")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            print(f"{Fore.YELLOW}⏳ Inicializando Chrome...{Style.RESET_ALL}")
            driver = webdriver.Chrome(options=options)
            
            url = f"https://{domain}"
            print(f"{Fore.YELLOW}⏳ Navegando para {url}...{Style.RESET_ALL}")
            driver.get(url)
            
            time.sleep(2)
            
            print(f"{Fore.YELLOW}💉 Injetando {len(cookies)} cookies...{Style.RESET_ALL}\n")
            
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
                    
                    driver.add_cookie(cookie_dict)
                    
                    if i % 20 == 0:
                        print(f"  ✅ {i}/{len(cookies)} cookies")
                except:
                    pass
            
            print(f"\n{Fore.GREEN}✅ {len(cookies)} cookies injetados!{Style.RESET_ALL}\n")
            
            print(f"{Fore.YELLOW}🔄 Recarregando...{Style.RESET_ALL}\n")
            driver.refresh()
            
            time.sleep(3)
            
            print(f"{Fore.GREEN}{'='*70}")
            print(f"🎉 PRONTO! Você está logado em {domain}!")
            print(f"{'='*70}{Style.RESET_ALL}\n")
            
            try:
                input("Pressione ENTER para fechar...")
            except:
                pass
            
            driver.quit()
        
        except Exception as e:
            print(f"{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}\n")
    
    def show_main_menu(self):
        """Menu principal"""
        while True:
            print(f"\n{Fore.GREEN}{'='*70}")
            print("🔥 NEXUS SUPREME v2.0 - MENU PRINCIPAL")
            print(f"{'='*70}{Style.RESET_ALL}\n")
            
            print(f"  Total de domínios: {len(self.domains_list)}")
            print(f"  Total de cookies: {sum(len(v) for v in self.master_db.values()):,}\n")
            
            print("  [1] 📋 Navegar por Domínios (com paginação)")
            print("  [2] 🔍 Buscar e Acessar Domínio")
            print("  [3] 📊 Mostrar Estatísticas")
            print("  [0] ❌ Sair\n")
            
            choice = input(f"{Fore.CYAN}Escolha: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.navigate_domains()
            
            elif choice == "2":
                self.search_and_select()
            
            elif choice == "3":
                self.show_stats()
                input(f"\n{Fore.YELLOW}Pressione ENTER...{Style.RESET_ALL}")
            
            elif choice == "0":
                print(f"\n{Fore.CYAN}👋 Até logo!{Style.RESET_ALL}\n")
                break
            
            else:
                print(f"{Fore.RED}❌ Opção inválida{Style.RESET_ALL}")
    
    def show_stats(self):
        """Mostra estatísticas"""
        print(f"\n{Fore.GREEN}{'='*70}")
        print("📊 ESTATÍSTICAS")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        total_cookies = sum(len(v) for v in self.master_db.values())
        avg_cookies = total_cookies // len(self.master_db) if self.master_db else 0
        
        print(f"  Total de Domínios: {len(self.domains_list)}")
        print(f"  Total de Cookies: {total_cookies:,}")
        print(f"  Média por Domínio: {avg_cookies}")
        print(f"\n  Top 10 Domínios:\n")
        
        top_domains = sorted(self.master_db.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        
        for i, (domain, cookies) in enumerate(top_domains, 1):
            print(f"    {i}. {domain:40s} ({len(cookies):3d} cookies)")

def main():
    try:
        system = NEXUSSUPREMEv20()
        system.show_main_menu()
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
