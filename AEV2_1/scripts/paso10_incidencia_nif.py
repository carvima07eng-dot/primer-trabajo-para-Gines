"""Reproduce en la interfaz la validación del NIF (base_vat) y captura el aviso.
Se descarta el cambio, así que el NIF guardado no se modifica."""
from playwright.sync_api import sync_playwright
from comun import *

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = nueva_pagina(b, h=700)
    login(pg, *ADMIN)
    pg.goto(URL + "/odoo/action-base.action_res_company_form/1")
    pg.wait_for_selector(".o_form_view")
    esperar(pg)
    campo = pg.locator("div[name=vat] input")
    campo.fill("B-46098765")  # tal cual aparece en el enunciado
    pg.locator(".o_form_button_save").click()
    esperar(pg, 2500)
    shot(pg, "inc_nif_invalido.png")
    print(pg.locator(".modal-body, .o_notification").all_inner_texts())
    pg.keyboard.press("Escape")
    esperar(pg, 800)
    pg.locator(".o_form_button_cancel").first.click()
    esperar(pg, 1500)
    b.close()
