#!/usr/bin/env bash
# Restaura una copia (SQL + filestore) en una base de datos NUEVA.
# Uso: ./restore.sh <fichero.sql> <filestore.tar.gz> <bd_destino>
set -euo pipefail
SQL="$1"; FS="$2"; DB="$3"
echo "[1/4] Creando base de datos '$DB'..."
docker exec techparts_db createdb -U odoo "$DB"
echo "[2/4] Cargando el volcado SQL..."
docker exec -i techparts_db psql -q -U odoo -d "$DB" -v ON_ERROR_STOP=1 < "$SQL" > /dev/null
echo "[3/4] Restaurando el filestore..."
docker exec -i -u root techparts_odoo bash -c \
  "mkdir -p /var/lib/odoo/filestore/$DB && tar -xzf - -C /var/lib/odoo/filestore/$DB --strip-components=1 && chown -R odoo: /var/lib/odoo/filestore/$DB" < "$FS"
echo "[4/4] Reiniciando Odoo..."
docker restart techparts_odoo > /dev/null
echo "Restauración completada en '$DB'."
