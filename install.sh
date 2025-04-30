#!/bin/bash

# Verifica se é root
if [ "$(id -u)" -ne 0 ]; then
    echo "Este script deve ser executado como root" >&2
    exit 1
fi

# Versão do aplicativo
VERSION="1.0"
INSTALL_DIR="/opt/template_complete"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"

# Criar diretórios
echo "Criando diretórios de instalação..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$ICON_DIR"

# Copiar arquivos
echo "Copiando arquivos do aplicativo..."
cp -r src/* "$INSTALL_DIR/"
cp data/icons/template_complete.png "$ICON_DIR/"

# Criar executável principal
echo "Criando executável..."
cat > "$INSTALL_DIR/template_complete" <<EOF
#!/usr/bin/env python3
import sys
from src.main import main

if __name__ == "__main__":
    main()
EOF

chmod +x "$INSTALL_DIR/template_complete"

# Criar link simbólico
echo "Criando link simbólico..."
ln -sf "$INSTALL_DIR/template_complete" "$BIN_DIR/template_complete"

# Adicionar entrada no menu
echo "Instalando entrada no menu..."
cp data/template_complete.desktop "$DESKTOP_DIR/"

# Atualizar banco de dados de ícones
echo "Atualizando banco de dados de ícones..."
gtk-update-icon-cache -f -t /usr/share/icons/hicolor

# Atualizar banco de dados desktop
update-desktop-database

echo "Instalação concluída com sucesso!"
echo "Template Complete $VERSION foi instalado em $INSTALL_DIR"