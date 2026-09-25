from playwright.sync_api import sync_playwright
from comun import *

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = nueva_pagina(b)
    pg.goto(URL + "/web/login?db=" + DB)
    esperar(pg, 1000)
    pg.fill("input[name=login]", ADMIN[0])
    pg.fill("input[name=password]", ADMIN[1])
    shot(pg, "05_pantalla_login.png")
    login(pg, *ADMIN)
    shot(pg, "06_primer_acceso_odoo.png")
    b.close()
