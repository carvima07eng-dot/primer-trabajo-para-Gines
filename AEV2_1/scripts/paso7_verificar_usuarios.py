"""Inicia sesión con cada usuario, captura su menú de aplicaciones y
guarda las apps visibles en ../evidencias/menus_por_usuario.txt"""
from playwright.sync_api import sync_playwright
from comun import *
from usuarios_datos import USUARIOS

res = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for i, (nombre, login_, pwd, *_rest) in enumerate(USUARIOS, 1):
        ctx = b.new_context(viewport={"width": 1366, "height": 700}, locale="es-ES")
        pg = ctx.new_page()
        login(pg, login_, pwd)
        esperar(pg, 2500)
        abrir_menu_apps(pg)
        apps = [t.strip() for t in pg.locator(".o_navbar_apps_menu .dropdown-item, .o-dropdown--menu .o_app").all_inner_texts() if t.strip()]
        slug = login_.split("@")[0].replace(".", "_")
        shot(pg, f"u{i}_{slug}_menu.png")
        res.append((nombre, login_, apps, aviso_tiempo_real(pg)))
        ctx.close()
    b.close()

with open("../evidencias/menus_por_usuario.txt", "w") as f:
    for nombre, login_, apps, aviso in res:
        linea = f"{nombre:15} {login_:28} -> {', '.join(apps)}"
        print(linea, "(aviso ws)" if aviso else "")
        f.write(linea + "\n")
