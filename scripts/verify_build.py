"""
Script de verificación simple para detectar errores de importación y sintaxis.
Ejecuta esto antes de hacer push.
"""
import sys
import os
import importlib
import pkgutil

# Añadir la raíz del proyecto al sys.path
sys.path.append(os.getcwd())

def verify_imports(package_name):
    print(f"Verificando paquete: {package_name}")
    try:
        package = importlib.import_module(package_name)
        for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            try:
                importlib.import_module(module_name)
                print(f"  OK: {module_name}")
            except Exception as e:
                print(f"  ERROR en {module_name}: {e}")
                return False
    except Exception as e:
        print(f"ERROR al importar el paquete raiz {package_name}: {e}")
        return False
    return True

if __name__ == "__main__":
    success = verify_imports("app")
    if success:
        print("\n¡Todo parece estar en orden! Puedes hacer push con confianza.")
        sys.exit(0)
    else:
        print("\nSe detectaron errores. Por favor corrigelos antes de subir el codigo.")
        sys.exit(1)
