#!/bin/bash

# Verifica se é root
if [ "$(id -u)" -ne 0 ]; then
    echo "Este script deve ser executado como root" >&2
    exit 1
fi

# Diretórios de instalação
INSTALL_DIR="/opt/template_complete"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"

# Remover arquivos
echo "Removendo arquivos do aplicativo..."
rm -rf "$INSTALL_DIR"
rm -f "$BIN_DIR/template_complete"
rm -f "$DESKTOP_DIR/template_complete.desktop"
rm -f "$ICON_DIR/template_complete.png"

# Atualizar bancos de dados
echo "Atualizando bancos de dados..."
gtk-update-icon-cache -f -t /usr/share/icons/hicolor
update-desktop-database

echo "Desinstalação concluída com sucesso!"
echo "Template Complete foi completamente removido do sistema"