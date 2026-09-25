from playwright.sync_api import sync_playwright
from comun import *

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = nueva_pagina(b, h=640)
    login(pg, *ADMIN)
    pg.goto(URL + "/odoo/action-hr.hr_employee_public_action")
    pg.wait_for_selector(".o_view_controller")
    esperar(pg)
    pg.goto(URL + "/odoo/employees")
    pg.wait_for_selector(".o_kanban_view, .o_list_view")
    esperar(pg)
    shot(pg, "16_empleados_departamentos.png")
    b.close()
