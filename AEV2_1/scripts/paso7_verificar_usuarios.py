"""Inicia sesión con cada usuario y guarda:
  - uN_<login>_menu.png : menú de aplicaciones que ve
  - uN_<login>_id.png   : diálogo 'Mis preferencias' (nombre + email) para identificar la sesión
  - uN_<login>_app.png  : barra de menús dentro de su aplicación principal
y un resumen en ../evidencias/menus_por_usuario.txt"""
from playwright.sync_api import sync_playwright
from comun import *
from usuarios_datos import USUARIOS

APP_PRINCIPAL = {"carlos@techparts.es": "Ajustes", "ana.garcia@techparts.es": "Ventas",
                 "pedro.lopez@techparts.es": "Ventas", "sofia.torres@techparts.es": "CRM",
                 "javier.romero@techparts.es": "Inventario", "lucia.herrero@techparts.es": "Inventario",
                 "elena.vidal@techparts.es": "Compra", "marcos.soler@techparts.es": "Facturación"}

res = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for i, (nombre, login_, pwd, *_rest) in enumerate(USUARIOS, 1):
        ctx = b.new_context(viewport={"width": 1366, "height": 700}, locale="es-ES")
        pg = ctx.new_page()
        login(pg, login_, pwd)
        esperar(pg, 2500)
        slug = f"u{i}_" + login_.split("@")[0].replace(".", "_")
        # 1) Menú de aplicaciones
        abrir_menu_apps(pg)
        apps = [t.strip() for t in pg.locator(".o-dropdown--menu .o_app").all_inner_texts() if t.strip()]
        shot(pg, f"{slug}_menu.png")
        pg.keyboard.press("Escape")
        esperar(pg, 600)
        # 2) Menú de usuario (identidad)
        pg.locator(".o_user_menu button").first.click()
        esperar(pg, 1000)
        pg.locator(".o-dropdown--menu").get_by_text("Mis preferencias").click()
        pg.wait_for_selector(".modal .o_form_view")
        esperar(pg, 1500)
        pg.locator(".modal .modal-content").screenshot(path=CAP + f"{slug}_id.png")
        pg.keyboard.press("Escape")
        esperar(pg, 600)
        # 3) Aplicación principal
        app = APP_PRINCIPAL[login_]
        pg.goto(URL + "/odoo")
        esperar(pg, 2500)
        abrir_menu_apps(pg)
        pg.locator(".o-dropdown--menu .o_app", has_text=app).first.click()
        esperar(pg, 4000)
        menus = [t.strip() for t in pg.locator(".o_menu_sections > *").all_inner_texts() if t.strip()]
        shot(pg, f"{slug}_app.png")
        res.append((nombre, login_, apps, app, menus, aviso_tiempo_real(pg)))
        ctx.close()
    b.close()

with open("../evidencias/menus_por_usuario.txt", "w") as f:
    for nombre, login_, apps, app, menus, aviso in res:
        txt = f"{nombre} <{login_}>\n  Apps visibles : {', '.join(apps)}\n  Menús en {app}: {' | '.join(menus)}\n"
        print(txt + ("  (aviso websocket)\n" if aviso else ""))
        f.write(txt + "\n")
