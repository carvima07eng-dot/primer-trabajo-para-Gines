#!/usr/bin/env bash
# Copia de seguridad de Odoo 19 (TechParts S.L.): base de datos + filestore.
# Uso: ./backup.sh [nombre_bd]     (por defecto: techparts)
set -euo pipefail
DB="${1:-techparts}"
FECHA="$(date +%Y%m%d_%H%M)"
DEST="$(dirname "$0")/../backup"
mkdir -p "$DEST"

echo "[1/3] Volcado SQL de la base de datos '$DB'..."
docker exec techparts_db pg_dump -U odoo -d "$DB" --no-owner --no-privileges \
  > "$DEST/${DB}_${FECHA}.sql"

echo "[2/3] Empaquetando el filestore..."
docker exec techparts_odoo tar -czf - -C /var/lib/odoo/filestore "$DB" \
  > "$DEST/filestore_${DB}_${FECHA}.tar.gz"

echo "[3/3] Sumas de verificación..."
( cd "$DEST" && sha256sum "${DB}_${FECHA}.sql" "filestore_${DB}_${FECHA}.tar.gz" > "SHA256SUMS_${FECHA}.txt" )
ls -lh "$DEST"
