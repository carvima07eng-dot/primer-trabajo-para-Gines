"""Convierte las salidas de terminal guardadas en evidencias/*.txt en capturas PNG
con aspecto de consola (prompt en verde, errores en rojo, avisos en amarillo)."""
import glob
import html
import os
import re
from playwright.sync_api import sync_playwright

CAPTURAS = {
    "t00_docker_daemon.txt": ("T00_terminal_docker_daemon.png", "carlos@dam2: ~/techparts-odoo"),
    "t01_versiones.txt": ("T01_terminal_versiones.png", "carlos@dam2: ~/techparts-odoo"),
    "t02_estructura.txt": ("T02_terminal_estructura.png", "carlos@dam2: ~/AEV2_1"),
    "t03a_pull.txt": ("T03_terminal_pull.png", "carlos@dam2: ~/techparts-odoo/proyecto"),
    "t03b_pull_error_429.txt": ("T03b_terminal_error_429.png", "carlos@dam2: ~/techparts-odoo/proyecto"),
    "t04_up.txt": ("T04_terminal_up.png", "carlos@dam2: ~/techparts-odoo/proyecto"),
    "t05_ps.txt": ("T05_terminal_ps.png", "carlos@dam2: ~/techparts-odoo/proyecto"),
    "t06_errores_arranque.txt": ("T06_terminal_errores_arranque.png", "carlos@dam2: ~/techparts-odoo/proyecto"),
    "t07_odoo_conf.txt": ("T07_terminal_odoo_conf.png", "carlos@dam2: ~/techparts-odoo/proyecto"),
    "t08_backup.txt": ("T08_terminal_backup.png", "carlos@dam2: ~/techparts-odoo/proyecto"),
    "salida_restauracion.txt": ("T09_terminal_restauracion.png", "carlos@dam2: ~/techparts-odoo/proyecto"),
    "matriz_accesos.txt": ("T10_terminal_matriz_accesos.png", "carlos@dam2: ~/AEV2_1/scripts"),
}

CSS = """
body{margin:0;background:#fff;font-family:'DejaVu Sans Mono',monospace}
.win{width:1180px;border-radius:9px;overflow:hidden;box-shadow:0 4px 18px #0005;margin:14px}
.bar{background:#3a3f4b;color:#ddd;font:13px 'DejaVu Sans',sans-serif;padding:8px 12px;display:flex;align-items:center;gap:7px}
.dot{width:12px;height:12px;border-radius:50%}
.t{flex:1;text-align:center;margin-right:50px}
pre{margin:0;background:#1e2127;color:#d7dae0;padding:14px 16px;font-size:13.5px;line-height:1.45;white-space:pre-wrap;word-break:break-all}
.p{color:#98c379;font-weight:bold}.e{color:#e06c75}.w{color:#e5c07b}.c{color:#7f848e}.ok{color:#56b6c2}
"""


def colorear(linea):
    h = html.escape(linea)
    if linea.startswith("$ "):
        cmd, _, com = h[2:].partition("   #")
        return f'<span class="p">$</span> {cmd}' + (f'<span class="c">   #{com}</span>' if com else "")
    if re.search(r"ERROR|Error|error:|failed|429", linea):
        return f'<span class="e">{h}</span>'
    if "WARNING" in linea:
        return f'<span class="w">{h}</span>'
    if re.search(r"\b(Started|Healthy|Pulled|200 OK|completada|OK)\b", linea):
        return f'<span class="ok">{h}</span>'
    return h


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1210, "height": 400}, device_scale_factor=1.5)
    for txt, (png, titulo) in CAPTURAS.items():
        lineas = open(os.path.join("../evidencias", txt)).read().rstrip("\n").split("\n")
        cuerpo = "\n".join(colorear(l) for l in lineas)
        pg.set_content(f"""<html><head><style>{CSS}</style></head><body><div class="win"><div class="bar">
            <span class="dot" style="background:#ff5f56"></span><span class="dot" style="background:#ffbd2e"></span>
            <span class="dot" style="background:#27c93f"></span><span class="t">{titulo}</span></div>
            <pre>{cuerpo}</pre></div></body></html>""")
        pg.locator(".win").screenshot(path="../capturas/" + png)
        print("captura:", png)
    b.close()
