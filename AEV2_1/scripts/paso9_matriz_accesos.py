"""Comprueba en el servidor (XML-RPC, con las credenciales de cada usuario)
qué puede leer (L) y crear (C) cada uno en los modelos principales."""
from comun import rpc
from usuarios_datos import USUARIOS

MODELOS = [("crm.lead", "CRM"), ("sale.order", "Ventas"), ("stock.picking", "Inventario"),
           ("purchase.order", "Compras"), ("account.move", "Facturación"),
           ("hr.employee", "Empleados"), ("res.users", "Usuarios")]


def puede(call, modelo, op):
    try:
        return bool(call(modelo, "has_access", [], op))
    except Exception:
        return False


lineas = ["Usuario".ljust(16) + "".join(n.ljust(13) for _, n in MODELOS)]
for nombre, login, pwd, *_ in USUARIOS:
    _, call = rpc(login, pwd)
    fila = nombre.ljust(16)
    for modelo, _n in MODELOS:
        l, c = puede(call, modelo, "read"), puede(call, modelo, "create")
        fila += ("L+C" if l and c else "L" if l else "-").ljust(13)
    lineas.append(fila)
txt = "\n".join(lineas)
print(txt)
open("../evidencias/matriz_accesos.txt", "w").write(txt + "\n\nL = lectura, C = creación, - = sin acceso (AccessError)\n")
