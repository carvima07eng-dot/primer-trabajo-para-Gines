from playwright.sync_api import sync_playwright
from comun import *

uid, call = rpc()
ids = {u["login"]: u["id"] for u in call("res.users", "search_read", [["share", "=", False]], fields=["login"])}

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = nueva_pagina(b, h=620)
    login(pg, *ADMIN)
    pg.goto(URL + "/odoo/action-base.action_res_users")
    pg.wait_for_selector(".o_list_view")
    esperar(pg)
    shot(pg, "11_lista_usuarios.png")
    pg.set_viewport_size({"width": 1366, "height": 1000})
    for login_, nombre in (("ana.garcia@techparts.es", "12_permisos_ana_garcia.png"),
                           ("javier.romero@techparts.es", "13_permisos_javier_romero.png"),
                           ("marcos.soler@techparts.es", "14_permisos_marcos_soler.png")):
        pg.goto(URL + f"/odoo/action-base.action_res_users/{ids[login_]}")
        pg.wait_for_selector(".o_form_view")
        esperar(pg)
        shot(pg, nombre)
    # Grupos técnicos de Marcos en modo desarrollador
    pg.goto(URL + f"/odoo/action-base.action_res_users/{ids['marcos.soler@techparts.es']}?debug=1")
    pg.wait_for_selector(".o_form_view")
    esperar(pg)
    pg.locator(".oe_stat_button", has_text="Grupos").first.click()
    pg.wait_for_selector(".o_list_view")
    esperar(pg)
    pg.set_viewport_size({"width": 1366, "height": 560})
    shot(pg, "15_marcos_grupos_modo_desarrollador.png")
    print(pg.locator(".o_list_view tbody").inner_text())
    b.close()
