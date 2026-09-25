"""Crea la base de datos 'techparts' desde el gestor web de Odoo y toma capturas."""
from playwright.sync_api import sync_playwright

CAP = "../capturas/"
URL = "http://localhost:8069"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1366, "height": 800}, locale="es-ES")
    pg.goto(URL + "/web/database/manager")
    pg.wait_for_load_state("networkidle")
    form = pg.locator("form:visible").first
    form.locator("input[name=master_pwd]").fill("TechParts_Master_2025!")
    form.locator("input[name=name]").fill("techparts")
    form.locator("input[name=login]").fill("carlos@techparts.es")
    form.locator("input[name=password]").fill("Carlos2025!")
    form.locator("input[name=phone]").fill("+34 960 987 654")
    form.locator("select[name=lang]").select_option("es_ES")
    form.locator("select[name=country_code]").select_option("es")
    pg.screenshot(path=CAP + "04_crear_bd_formulario.png")
    form.locator("button[type=submit], input[type=submit]").first.click()
    pg.wait_for_url("**/odoo**", timeout=600000)
    pg.wait_for_load_state("networkidle")
    pg.wait_for_timeout(3000)
    pg.screenshot(path=CAP + "05_primer_acceso_odoo.png")
    print(pg.url)
    b.close()
