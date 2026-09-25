"""Crea los 8 usuarios de TechParts S.L. con sus permisos exactos,
los 5 departamentos y la ficha de empleado de cada uno."""
from comun import rpc

uid, call = rpc()


def g(xmlid):
    m, n = xmlid.split(".")
    return call("ir.model.data", "search_read", [["module", "=", m], ["name", "=", n]], fields=["res_id"])[0]["res_id"]


from usuarios_datos import USUARIOS

# Departamentos
deps = {}
for nombre in ["Dirección", "Ventas", "Almacén", "Compras", "Administración"]:
    ex = call("hr.department", "search", [["name", "=", nombre]])
    deps[nombre] = ex[0] if ex else call("hr.department", "create", {"name": nombre})

for nombre, login, pwd, grupos, dep, puesto in USUARIOS:
    ids = [g(x) for x in BASE + grupos]
    vals = {"name": nombre, "login": login, "email": login, "password": pwd,
            "group_ids": [(6, 0, ids)], "tz": "Europe/Madrid", "lang": "es_ES"}
    ex = call("res.users", "search", [["login", "=", login]])
    if ex:
        u = ex[0]
        call("res.users", "write", [u], vals)
    else:
        u = call("res.users", "create", vals)
    # Ficha de empleado vinculada
    emp = call("hr.employee", "search", [["user_id", "=", u]])
    evals = {"name": nombre, "user_id": u, "department_id": deps[dep], "job_title": puesto,
             "work_email": login}
    if emp:
        call("hr.employee", "write", emp, evals)
    else:
        call("hr.employee", "create", evals)
    print(f"OK  {nombre:15} {login:28} {dep}")

# Responsables de departamento
jefes = {"Dirección": "carlos@techparts.es", "Ventas": "ana.garcia@techparts.es",
         "Almacén": "javier.romero@techparts.es", "Compras": "elena.vidal@techparts.es",
         "Administración": "marcos.soler@techparts.es"}
for dep, login in jefes.items():
    e = call("hr.employee", "search", [["user_id.login", "=", login]])
    call("hr.department", "write", [deps[dep]], {"manager_id": e[0]})
