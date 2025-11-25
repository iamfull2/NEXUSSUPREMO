import os
import codecs

def remove_bom(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        if content.startswith(codecs.BOM_UTF8):
            print(f"Removing BOM from: {filepath}")
            with open(filepath, 'wb') as f:
                f.write(content[3:])
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return False

def scan_and_fix(directory):
    for root, dirs, files in os.walk(directory):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.json') or file.endswith('.js') or file.endswith('.jsx') or file.endswith('.ts') or file.endswith('.tsx'):
                remove_bom(os.path.join(root, file))

if __name__ == "__main__":
    scan_and_fix('.')
