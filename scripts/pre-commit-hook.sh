#!/bin/sh
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
