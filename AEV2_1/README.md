# AEV2.1 — Instalación y configuración de Odoo 19 (TechParts S.L.)

Carlos Vidal Marín · 2.º DAM

- **Entrega:** `entrega/AEV2_1_VidalMarinCarlos.zip` (proyecto + backup + manual en PDF)
- **Manual:** `Manual_Instalacion_TechParts.pdf`

Otras carpetas: `capturas/` (todas las capturas), `evidencias/` (salida de los comandos), `scripts/` (scripts en Python que usé) y `manual/` (para generar el PDF).

Para arrancarlo:
```bash
cd proyecto
sudo chown 100:101 logs
docker compose up -d
./restore.sh ../backup/techparts_20260925_1003.sql ../backup/filestore_techparts_20260925_1003.tar.gz techparts
# http://localhost:8069  ->  carlos@techparts.es / Carlos2025!
```
