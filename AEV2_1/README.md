# AEV2.1 — Instalación y configuración completa de Odoo 19 (TechParts S.L.)

**Alumno:** Carlos Vidal Marín · 2.º DAM · Sistemas de Gestión Empresarial

## Entrega
- **`entrega/AEV2_1_VidalMarinCarlos.zip`** → fichero para subir (proyecto/ + backup/ + manual PDF).
- `Manual_Instalacion_TechParts.pdf` → manual técnico (27 páginas, 46 figuras).

## Contenido de la carpeta
| Carpeta | Contenido |
|---|---|
| `proyecto/` | `docker-compose.yml`, `config/odoo.conf`, `addons/`, `logs/`, `backup.sh`, `restore.sh`, logotipo |
| `backup/` | Volcado `.sql`, filestore `.tar.gz`, copia web `.zip` y sumas SHA-256 |
| `capturas/` | Todas las capturas (navegador y terminal) |
| `evidencias/` | Salidas reales de los comandos y logs |
| `scripts/` | Scripts XML-RPC y Playwright usados para configurar y capturar |
| `manual/` | Generador del manual (HTML → PDF) |

## Arranque rápido
```bash
cd proyecto
sudo chown 100:101 logs
docker compose up -d
./restore.sh ../backup/techparts_20260925_1003.sql ../backup/filestore_techparts_20260925_1003.tar.gz techparts
# http://localhost:8069  ·  carlos@techparts.es / Carlos2025!
```
