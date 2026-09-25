"""Instala los 6 módulos pedidos (equivale a pulsar 'Activar' en Aplicaciones)."""
import time
from comun import rpc

MODULOS = {
    "sale_management": "Ventas",
    "purchase": "Compras",
    "stock": "Inventario",
    "crm": "CRM",
    "account": "Facturación",
    "hr": "Empleados",
}
uid, call = rpc()
for tecnico, nombre in MODULOS.items():
    ids = call("ir.module.module", "search", [["name", "=", tecnico]])
    t = time.time()
    call("ir.module.module", "button_immediate_install", ids)
    print(f"{nombre:12} ({tecnico}) instalado en {time.time() - t:5.1f} s")

inst = call("ir.module.module", "search_read", [["name", "in", list(MODULOS)]], fields=["name", "state"])
print(inst)
