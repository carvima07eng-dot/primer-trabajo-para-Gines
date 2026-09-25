"""Utilidades comunes: conexión XML-RPC y capturas con Playwright."""
import xmlrpc.client

URL = "http://localhost:8069"
DB = "techparts"
CAP = "../capturas/"
ADMIN = ("carlos@techparts.es", "Carlos2025!")


def rpc(login=ADMIN[0], pwd=ADMIN[1]):
    common = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/common")
    uid = common.authenticate(DB, login, pwd, {})
    models = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/object", allow_none=True)

    def call(model, method, *args, **kw):
        return models.execute_kw(DB, uid, pwd, model, method, list(args), kw)
    return uid, call


def nueva_pagina(browser, w=1366, h=800):
    return browser.new_page(viewport={"width": w, "height": h}, locale="es-ES")


def esperar(pg, ms=2500):
    # Odoo mantiene abierta una conexión de longpolling (bus), por eso no se
    # usa "networkidle": se espera a que cargue la interfaz y un margen fijo.
    pg.wait_for_load_state("load")
    pg.wait_for_timeout(ms)


def login(pg, user, pwd):
    pg.goto(URL + "/web/login?db=" + DB)
    esperar(pg, 800)
    pg.fill("input[name=login]", user)
    pg.fill("input[name=password]", pwd)
    pg.click("button[type=submit]")
    pg.wait_for_selector(".o_main_navbar, .o_home_menu", timeout=60000)
    esperar(pg)


def logout(pg):
    pg.goto(URL + "/web/session/logout")
    esperar(pg, 800)


def shot(pg, nombre, full=False, apartar_raton=True):
    if apartar_raton:  # evita tooltips del ratón en la captura
        pg.mouse.move(pg.viewport_size["width"] - 5, pg.viewport_size["height"] - 5)
        pg.wait_for_timeout(700)
    pg.screenshot(path=CAP + nombre, full_page=full)
    print("captura:", nombre)


def abrir_menu_apps(pg):
    """Despliega el menú de aplicaciones (icono de cuadrícula) y aparta el ratón."""
    pg.locator(".o_navbar_apps_menu button").first.click()
    pg.mouse.move(1300, 700)
    esperar(pg, 1200)


def aviso_tiempo_real(pg):
    return pg.get_by_text("Se perdió la conexión en tiempo real").count() > 0
