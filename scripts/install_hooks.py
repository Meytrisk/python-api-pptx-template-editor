import os
import shutil
import stat
import sys

def install_hooks():
    src = os.path.join('scripts', 'pre-commit-hook.sh')
    dst = os.path.join('.git', 'hooks', 'pre-commit')
    
    if not os.path.exists('.git'):
        print("Error: No se encontro la carpeta .git. Asegurate de estar en la raiz del repositorio.")
        return

    # Crear el script de hook en la carpeta scripts
    hook_content = """#!/bin/sh
echo "Ejecutando verificacion tecnica antes del commit..."

# Intentar usar el entorno virtual local si existe
if [ -f "./venv/Scripts/python.exe" ]; then
    PYTHON_CMD="./venv/Scripts/python.exe"
elif [ -f "./venv/Scripts/python" ]; then
    PYTHON_CMD="./venv/Scripts/python"
elif [ -f "./venv/bin/python" ]; then
    PYTHON_CMD="./venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "Usando: $PYTHON_CMD"
$PYTHON_CMD scripts/verify_build.py

RESULT=$?

if [ $RESULT -ne 0 ]; then
    echo "ERROR: La verificacion de build fallo."
    echo "El commit ha sido abortado. Por favor, corrige los errores de importacion o sintaxis."
    exit 1
fi

echo "Verificacion exitosa. Prosiguiendo con el commit..."
exit 0
"""
    
    os.makedirs('scripts', exist_ok=True)
    with open(src, 'w', newline='\n') as f:
        f.write(hook_content)
    
    print(f"Script de hook creado en {src}")
    
    # Copiar a .git/hooks
    try:
        shutil.copy(src, dst)
        # Hacerlo ejecutable
        st = os.stat(dst)
        os.chmod(dst, st.st_mode | stat.S_IEXEC)
        print(f"Hook instalado correctamente en {dst}")
    except Exception as e:
        print(f"Error al copiar el hook: {e}")

if __name__ == "__main__":
    install_hooks()
