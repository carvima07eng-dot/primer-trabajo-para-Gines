"""Captura de Aplicaciones filtrada por 'Aplicaciones' + 'Instalado'."""
from playwright.sync_api import sync_playwright
from comun import *

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = nueva_pagina(b, h=700)
    login(pg, *ADMIN)
    pg.goto(URL + "/odoo/action-base.open_module_tree")
    pg.wait_for_selector(".o_kanban_view")
    esperar(pg)
    pg.locator(".o_searchview_dropdown_toggler").click()
    esperar(pg, 800)
    pg.locator(".o_search_bar_menu").get_by_text("Instalado", exact=True).click()
    esperar(pg, 800)
    pg.locator(".o_searchview_dropdown_toggler").click()
    esperar(pg)
    shot(pg, "09_modulos_instalados.png")
    # Menú principal del administrador con todas las apps
    pg.goto(URL + "/odoo")
    esperar(pg)
    esperar(pg, 5000)
    abrir_menu_apps(pg)
    print("aviso websocket:", aviso_tiempo_real(pg))
    shot(pg, "10_menu_apps_administrador.png")
    b.close()
