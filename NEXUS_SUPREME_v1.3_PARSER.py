#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║     🔥 NEXUS_SUPREME v1.3 - PARSER ROBUSTO PARA MÚLTIPLOS JSONs         ║
║                                                                            ║
║  Processa JSONs quebrados, múltiplos JSONs, e formatos variados           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import json
import re
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

class NEXUSSUPREMEv13:
    """Parser robusto - v1.3"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        print(f"\n{Fore.CYAN}📍 Pasta do Script: {self.script_dir}{Style.RESET_ALL}\n")
        
        self.data_dir = self.script_dir / "NEXUS_SUPREME_DATA"
        self.cookies_dir = self.data_dir / "cookies"
        self.data_dir.mkdir(exist_ok=True)
        self.cookies_dir.mkdir(exist_ok=True)
        
        self.master_db_file = self.cookies_dir / "master_cookies.json"
        self.master_db = {}
    
    def extract_multiple_jsons(self, text):
        """Extrai múltiplos JSONs de um texto"""
        jsons = []
        
        # Tenta encontrar todos os JSONs usando regex
        # Procura por padrão: [ ... ]
        
        depth = 0
        current_json = ""
        in_string = False
        escape_next = False
        
        for i, char in enumerate(text):
            if escape_next:
                current_json += char
                escape_next = False
                continue
            
            if char == '\\' and in_string:
                escape_next = True
                current_json += char
                continue
            
            if char == '"' and not escape_next:
                in_string = not in_string
                current_json += char
                continue
            
            if not in_string:
                if char == '[':
                    if depth == 0:
                        current_json = ""
                    depth += 1
                    current_json += char
                
                elif char == ']':
                    current_json += char
                    depth -= 1
                    
                    if depth == 0 and current_json.strip():
                        try:
                            data = json.loads(current_json)
                            if isinstance(data, list):
                                jsons.append(data)
                        except:
                            pass
                        current_json = ""
                
                elif depth > 0:
                    current_json += char
            else:
                current_json += char
        
        return jsons
    
    def parse_file_robust(self, filepath):
        """Parse robusto com suporte a múltiplos JSONs"""
        filepath = Path(filepath)
        cookies = []
        
        try:
            print(f"  Lendo: {filepath.name}...", end=" ")
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                print(f"⚠️ Arquivo vazio")
                return []
            
            file_size_mb = len(content) / (1024*1024)
            
            # Método 1: JSON único (padrão)
            if content.strip().startswith('['):
                try:
                    data = json.loads(content)
                    if isinstance(data, list):
                        cookies = data
                        print(f"✅ JSON Único ({len(cookies)} cookies, {file_size_mb:.1f} MB)")
                        return cookies
                except json.JSONDecodeError:
                    print(f"⚠️ JSON Único falhou, tentando múltiplos...", end=" ")
            
            # Método 2: Múltiplos JSONs
            json_arrays = self.extract_multiple_jsons(content)
            
            if json_arrays:
                for array in json_arrays:
                    if isinstance(array, list):
                        cookies.extend(array)
                
                print(f"✅ {len(json_arrays)} JSON(s) ({len(cookies)} cookies, {file_size_mb:.1f} MB)")
                return cookies
            
            # Método 3: Netscape Format
            print(f"⚠️ Nenhum JSON encontrado, tentando Netscape...", end=" ")
            for line in content.splitlines():
                if line.strip().startswith('#') or not line.strip():
                    continue
                parts = line.split('\t')
                if len(parts) >= 7:
                    try:
                        cookie = {
                            'domain': parts[0],
                            'path': parts[2],
                            'secure': parts[3].upper() == 'TRUE',
                            'expiry': parts[4],
                            'name': parts[5],
                            'value': parts[6].strip()
                        }
                        cookies.append(cookie)
                    except:
                        continue
            
            if cookies:
                print(f"✅ Netscape ({len(cookies)} cookies, {file_size_mb:.1f} MB)")
                return cookies
            
            print(f"⚠️ Nenhum cookie extraído")
            return []
        
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    def import_all_cookies(self):
        """Importa com parser robusto"""
        print(f"\n{Fore.GREEN}{'='*70}")
        print("📥 IMPORTAÇÃO v1.3 - PARSER ROBUSTO PARA MÚLTIPLOS JSONs")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        # Encontra JSONs
        json_files = sorted(self.script_dir.glob("sf_cookie Matheus*.json"))
        
        if not json_files:
            print(f"{Fore.RED}⚠️ Nenhum arquivo sf_cookie Matheus*.json encontrado{Style.RESET_ALL}\n")
            return
        
        print(f"{Fore.CYAN}Encontrados {len(json_files)} arquivo(s):{Style.RESET_ALL}\n")
        
        total_cookies = 0
        total_domains = set()
        
        for filepath in json_files:
            cookies = self.parse_file_robust(filepath)
            
            if cookies:
                total_cookies += len(cookies)
                
                for cookie in cookies:
                    domain = str(cookie.get('domain', '')).strip().lstrip('.')
                    
                    if domain:
                        if domain not in self.master_db:
                            self.master_db[domain] = []
                        
                        self.master_db[domain].append(cookie)
                        total_domains.add(domain)
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print("✅ IMPORTAÇÃO CONCLUÍDA")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        print(f"  {Fore.CYAN}Total de Cookies: {total_cookies:,}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Domínios Únicos: {len(total_domains)}{Style.RESET_ALL}\n")
        
        # Salva
        if total_cookies > 0:
            with open(self.master_db_file, 'w', encoding='utf-8') as f:
                json.dump(self.master_db, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}💾 Banco de dados salvo!{Style.RESET_ALL}\n")
            
            # Mostra top 30 domínios
            print(f"{Fore.YELLOW}Top 30 Domínios:{Style.RESET_ALL}\n")
            domains = sorted(total_domains)
            for i, domain in enumerate(domains[:30], 1):
                count = len(self.master_db.get(domain, []))
                print(f"  {i:2d}. {domain:40s} ({count:3d} cookies)")
            
            if len(domains) > 30:
                print(f"\n  {Fore.YELLOW}... e mais {len(domains) - 30} domínios{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}⚠️ Nenhum cookie foi importado{Style.RESET_ALL}\n")

def main():
    try:
        system = NEXUSSUPREMEv13()
        system.import_all_cookies()
        print(f"\n{Fore.GREEN}✅ Pronto! Seus cookies estão salvos.{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
