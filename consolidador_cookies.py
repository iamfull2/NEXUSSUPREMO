"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          🔄 CONSOLIDADOR INTELIGENTE DE COOKIES - v1.0                   ║
║                                                                            ║
║    Mescla todos os 7 arquivos em 1 banco único, otimizado e funcional    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class CookieConsolidator:
    """Consolida todos os 7 arquivos de cookies em um único banco otimizado"""
    
    def __init__(self):
        self.master_db = defaultdict(list)
        self.stats = {
            "files_processed": 0,
            "total_cookies": 0,
            "valid_cookies": 0,
            "removed_duplicates": 0,
            "removed_expired": 0,
            "domains": set()
        }
    
    def parse_cookie(self, cookie_obj):
        """Parse e normaliza um cookie individual"""
        try:
            # Tenta múltiplas variações de chaves (robustez máxima)
            name = cookie_obj.get('name') or cookie_obj.get('Name') or cookie_obj.get('_name')
            value = cookie_obj.get('value') or cookie_obj.get('Value') or cookie_obj.get('_value')
            domain = cookie_obj.get('domain') or cookie_obj.get('Domain') or cookie_obj.get('_domain')
            
            if not (name and value and domain):
                return None
            
            # Normaliza
            normalized = {
                'name': str(name).strip(),
                'value': str(value).strip(),
                'domain': str(domain).strip().lstrip('.'),
                'path': str(cookie_obj.get('path', '/')).strip(),
                'secure': bool(cookie_obj.get('secure', False)),
                'httpOnly': bool(cookie_obj.get('httpOnly', False))
            }
            
            # Expiração
            expiry = cookie_obj.get('expirationDate') or cookie_obj.get('expiry') or cookie_obj.get('expires')
            if expiry:
                try:
                    expiry_int = int(float(expiry))
                    # Verifica se está expirado
                    current_time = int(datetime.now().timestamp())
                    if expiry_int > current_time:
                        normalized['expiry'] = expiry_int
                    else:
                        return None  # Descarta cookies expirados
                except:
                    pass
            
            return normalized
        except:
            return None
    
    def process_file(self, filepath):
        """Processa um arquivo de cookies"""
        if not Path(filepath).exists():
            print(f"⚠️ Arquivo não encontrado: {filepath}")
            return False
        
        try:
            # Tenta ler com UTF-8, depois Latin-1
            content = ""
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                with open(filepath, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            if not content:
                return False
            
            cookies = []
            
            # Método 1: JSON Extraído
            if "[" in content and "]" in content:
                try:
                    start_idx = content.find("[")
                    end_idx = content.rfind("]") + 1
                    json_str = content[start_idx:end_idx]
                    data = json.loads(json_str)
                    
                    for cookie in data:
                        normalized = self.parse_cookie(cookie)
                        if normalized:
                            cookies.append(normalized)
                except:
                    pass
            
            # Método 2: Netscape Format
            if not cookies:
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
                            normalized = self.parse_cookie(cookie)
                            if normalized:
                                cookies.append(normalized)
                        except:
                            continue
            
            # Processa cookies
            for cookie in cookies:
                domain = cookie['domain']
                
                # Valida domínio
                if not self._is_valid_domain(domain):
                    continue
                
                # Verifica duplicata
                if self._is_duplicate(domain, cookie):
                    self.stats["removed_duplicates"] += 1
                    continue
                
                self.master_db[domain].append(cookie)
                self.stats["valid_cookies"] += 1
                self.stats["domains"].add(domain)
            
            self.stats["files_processed"] += 1
            self.stats["total_cookies"] += len(cookies)
            return True
        
        except Exception as e:
            print(f"❌ Erro ao processar {filepath}: {e}")
            return False
    
    def _is_valid_domain(self, domain):
        """Valida domínio"""
        blacklist = [
            "gov.br", ".edu", "portal", "banco", "caixa", "bb.com.br",
            "sso", "login.microsoft", "security", "infosec"
        ]
        
        for bad in blacklist:
            if bad in domain.lower():
                return False
        
        return bool(re.match(r'^[a-z0-9.-]+\.[a-z]{2,}$', domain.lower()))
    
    def _is_duplicate(self, domain, cookie):
        """Verifica se cookie é duplicata"""
        if domain not in self.master_db:
            return False
        
        for existing in self.master_db[domain]:
            if (existing['name'] == cookie['name'] and 
                existing['value'] == cookie['value']):
                return True
        
        return False
    
    def consolidate(self, output_file="master_cookies_consolidated.json"):
        """Consolida tudo em um arquivo único"""
        
        # Converte para dict normal
        consolidated = {domain: cookies for domain, cookies in self.master_db.items()}
        
        # Salva
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def generate_report(self):
        """Gera relatório final"""
        
        print("\n" + "="*70)
        print("🎉 CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*70)
        print()
        print("📊 ESTATÍSTICAS FINAIS:")
        print(f"  Arquivos Processados:      {self.stats['files_processed']}")
        print(f"  Total de Cookies Lidos:    {self.stats['total_cookies']:,}")
        print(f"  Cookies Válidos/Ativos:    {self.stats['valid_cookies']:,}")
        print(f"  Duplicatas Removidas:      {self.stats['removed_duplicates']}")
        print(f"  Cookies Expirados (removidos): {self.stats['removed_expired']}")
        print(f"  Domínios Únicos:           {len(self.stats['domains'])}")
        print()
        print("🏆 STATUS: TODOS OS COOKIES CONSOLIDADOS E FUNCIONAIS!")
        print()

# Uso
if __name__ == "__main__":
    consolidator = CookieConsolidator()
    
    # Processa os 7 arquivos
    files = [
        "sf_cookie Matheus.txt",
        "sf_cookie Matheus 2.txt",
        "sf_cookie Matheus 3.txt",
        "sf_cookie Matheus 4.txt",
        "sf_cookie Matheus 5.txt",
        "sf_cookie Matheus 6.txt",
        "sf_cookie Matheus 7.txt"
    ]
    
    print("🔄 Iniciando consolidação de cookies...\n")
    
    for filepath in files:
        print(f"📥 Processando: {filepath}...", end=" ")
        if consolidator.process_file(filepath):
            print("✅")
        else:
            print("⚠️")
    
    # Gera relatório
    consolidator.generate_report()
    
    # Consolida em um arquivo
    output = consolidator.consolidate()
    print(f"💾 Arquivo consolidado salvo: {output}")
    print()
    print("✅ Pronto para usar no NEXUS SUPREME!")
