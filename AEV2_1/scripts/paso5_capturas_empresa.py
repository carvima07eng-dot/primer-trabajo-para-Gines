from playwright.sync_api import sync_playwright
from comun import *

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = nueva_pagina(b, h=900)
    login(pg, *ADMIN)
    # Formulario de la compañía
    pg.goto(URL + "/odoo/action-base.action_res_company_form/1")
    pg.wait_for_selector(".o_form_view")
    esperar(pg)
    shot(pg, "07_datos_empresa.png")
    # Ajustes generales: tarjeta de la compañía
    pg.goto(URL + "/odoo/settings#general_settings")
    pg.wait_for_selector(".o_setting_container, .settings")
    esperar(pg)
    el = pg.locator("#companies").first
    if el.count():
        el.scroll_into_view_if_needed()
        esperar(pg, 800)
    shot(pg, "08_ajustes_compania.png")
    # Aplicaciones instaladas
    pg.goto(URL + "/odoo/action-base.open_module_tree")
    pg.wait_for_selector(".o_kanban_view")
    esperar(pg)
    s = pg.locator(".o_searchview_input")
    s.click()
    pg.keyboard.press("Backspace")  # quita el filtro 'Aplicaciones'
    esperar(pg, 800)
    pg.locator(".o_searchview_dropdown_toggler").click()
    esperar(pg, 800)
    pg.get_by_text("Instalado", exact=True).first.click()
    esperar(pg, 800)
    pg.locator(".o_searchview_dropdown_toggler").click()
    s.fill("")
    pg.keyboard.press("Escape")
    esperar(pg)
    shot(pg, "09_modulos_instalados.png")
    b.close()
