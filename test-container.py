#!/usr/bin/env python3
"""
Script de teste para verificar se o container está funcionando corretamente
"""

import subprocess
import sys
import time

def run_test(name, command, expected_exit_code=0):
    """Executa um teste e verifica o resultado"""
    print(f"\n🧪 Testando: {name}")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == expected_exit_code:
            print(f"✅ PASSOU - Exit code: {result.returncode}")
            if result.stdout.strip():
                print(f"📄 Output: {result.stdout.strip()[:200]}...")
            return True
        else:
            print(f"❌ FALHOU - Exit code esperado: {expected_exit_code}, obtido: {result.returncode}")
            if result.stderr:
                print(f"❌ Erro: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT - Comando demorou mais de 30 segundos")
        return False
    except Exception as e:
        print(f"💥 ERRO - {str(e)}")
        return False

def main():
    print("🐳 Testando Container Lead Scraper")
    print("=" * 50)
    
    tests = [
        ("Verificar se o container existe", "docker images lead-scraper-base"),
        ("Testar Python", "docker run --rm lead-scraper-base python --version"),
        ("Testar Chrome", "docker run --rm lead-scraper-base google-chrome --version"),
        ("Testar conectividade", "docker run --rm lead-scraper-base curl -s -o /dev/null -w \"%{http_code}\" https://httpbin.org/get"),
        ("Testar Chrome headless", "docker run --rm lead-scraper-base google-chrome --headless --disable-gpu --no-sandbox --dump-dom https://httpbin.org/get"),
        ("Testar pip", "docker run --rm lead-scraper-base pip --version"),
        ("Testar estrutura de arquivos", "docker run --rm lead-scraper-base bash -c \"ls -la /usr/local/bin/python*\""),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, command in tests:
        if run_test(name, command):
            passed += 1
        time.sleep(1)  # Pequena pausa entre testes
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO FINAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! Container está funcionando perfeitamente.")
        return 0
    else:
        print(f"⚠️  {total - passed} teste(s) falharam. Verifique os logs acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())