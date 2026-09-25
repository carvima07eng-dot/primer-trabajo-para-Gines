"""Genera Manual_Instalacion_TechParts.pdf (HTML + Chromium/Playwright).

Uso:  cd AEV2_1/manual && python3 generar_manual.py
"""
import html
import pathlib
from playwright.sync_api import sync_playwright

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent
CAP = "../capturas/"

ALUMNO = "Carlos Vidal Marín"
CURSO = "2.º DAM — Desarrollo de Aplicaciones Multiplataforma"
MODULO = "Sistemas de Gestión Empresarial (SGE)"
FECHA = "25 de septiembre de 2026"

_n = {"fig": 0, "tab": 0}


def fig(src, pie, ancho="100%"):
    _n["fig"] += 1
    return (f'<figure style="width:{ancho}"><img src="{CAP}{src}">'
            f'<figcaption><b>Figura {_n["fig"]}.</b> {pie}</figcaption></figure>')


def par(a, b):
    """Dos figuras en paralelo."""
    return f'<div class="par">{a}{b}</div>'


def tab_pie(pie):
    _n["tab"] += 1
    return f'<p class="tabpie"><b>Tabla {_n["tab"]}.</b> {pie}</p>'


def code(txt):
    return f"<pre class='code'>{html.escape(txt.strip())}</pre>"


def leer(rel):
    return (RAIZ / rel).read_text(encoding="utf-8")


def cmd(txt):
    return f"<pre class='cmd'>{html.escape(txt.strip())}</pre>"


# --------------------------------------------------------------------------- #
USUARIOS = [
    ("1", "Carlos Méndez", "carlos@techparts.es", "Carlos2025!", "Dirección",
     "Administrador (acceso completo)",
     "Rol: <b>Administrador</b> + Administrador en Ventas, Compra, Inventario, Contabilidad y Empleados"),
    ("2", "Ana García", "ana.garcia@techparts.es", "Ana2025!", "Ventas",
     "Ventas: Responsable · CRM: Usuario",
     "Ventas: <b>Administrador</b> (incluye CRM)"),
    ("3", "Pedro López", "pedro.lopez@techparts.es", "Pedro2025!", "Ventas",
     "Ventas: Usuario · CRM: Usuario",
     "Ventas: <b>Usuario: Solo mostrar documentos propios</b> (incluye CRM)"),
    ("4", "Sofía Torres", "sofia.torres@techparts.es", "Sofia2025!", "Ventas",
     "Ventas: Usuario · CRM: Usuario",
     "Ventas: <b>Usuario: Solo mostrar documentos propios</b> (incluye CRM)"),
    ("5", "Javier Romero", "javier.romero@techparts.es", "Javier2025!", "Almacén",
     "Inventario: Responsable", "Inventario: <b>Administrador</b>"),
    ("6", "Lucía Herrero", "lucia.herrero@techparts.es", "Lucia2025!", "Almacén",
     "Inventario: Usuario", "Inventario: <b>Usuario</b>"),
    ("7", "Elena Vidal", "elena.vidal@techparts.es", "Elena2025!", "Compras",
     "Compras: Responsable", "Compra: <b>Administrador</b>"),
    ("8", "Marcos Soler", "marcos.soler@techparts.es", "Marcos2025!", "Administración",
     "Facturación: Contable",
     "Contabilidad: <b>Facturación</b> + grupo técnico <i>Mostrar características de contabilidad "
     "completas</i> (= Contable)"),
]

VERIF = [  # nombre, apps visibles (propias), menús dentro de la app principal
    ("Carlos Méndez", "Todas + Ajustes", "Ajustes", "Opciones generales · Usuarios y compañías"),
    ("Ana García", "CRM, Ventas", "Ventas", "Pedidos · A facturar · Productos · Informes · <b>Configuración</b>"),
    ("Pedro López", "CRM, Ventas", "Ventas", "Pedidos · A facturar · Productos"),
    ("Sofía Torres", "CRM, Ventas", "CRM", "Ventas · Informes"),
    ("Javier Romero", "Inventario", "Inventario", "Información general · Operaciones · Productos · Informes · <b>Configuración</b>"),
    ("Lucía Herrero", "Inventario", "Inventario", "Información general · Operaciones · Productos"),
    ("Elena Vidal", "Compra", "Compra", "Pedidos · Productos · Informes · <b>Configuración</b>"),
    ("Marcos Soler", "Facturación", "Facturación", "Tablero · Clientes · Proveedores · <b>Contabilidad</b> · <b>Revisión</b> · Informes"),
]

INCIDENCIAS = [
    ("I-01", "Instalación",
     "<code>docker info</code> da el error <i>failed to connect to the docker API at unix:///var/run/docker.sock</i>.",
     "El servicio de Docker no estaba arrancado.",
     "Lo arranqué con <code>sudo systemctl start docker</code> (y con <code>enable</code> para que arranque solo). "
     "Lo comprobé otra vez con <code>docker info</code> (figura 1)."),
    ("I-02", "Instalación",
     "Al volver a hacer <code>docker compose pull</code> salió <i>429 Too Many Requests</i>.",
     "Docker Hub limita las descargas que puedes hacer sin iniciar sesión.",
     "Como ya tenía las imágenes descargadas, <code>up -d</code> funcionaba igual. Añadí <code>pull_policy: missing</code> "
     "al <i>docker-compose.yml</i> para que no las vuelva a descargar. Otra opción es hacer <code>docker login</code>."),
    ("I-03", "Primer arranque",
     "<i>ERROR: couldn't create the logfile directory. Logging to the standard output.</i>",
     "La carpeta <code>./logs</code> era de root y Odoo, dentro del contenedor, se ejecuta con el usuario "
     "<code>odoo</code> (uid 100, gid 101), así que no podía escribir en ella.",
     "<code>sudo chown 100:101 logs && chmod 775 logs</code> y reiniciar. Ya se crea el fichero <code>logs/odoo.log</code>."),
    ("I-04", "Primer arranque",
     "<i>unknown option 'db_filter' in the config file</i>.",
     "Había escrito mal el nombre del parámetro en el <code>odoo.conf</code>.",
     "El nombre bueno es <code>dbfilter</code>, sin guion bajo. Lo cambié a <code>dbfilter = ^techparts$</code>."),
    ("I-05", "Primer arranque",
     "<i>missing --http-interface/http_interface, using 0.0.0.0 by default, will change to 127.0.0.1 in 20.0</i>.",
     "Odoo avisa de que en la versión 20 cambiará el valor por defecto. Con 127.0.0.1 no se podría entrar desde fuera "
     "del contenedor.",
     "Puse <code>http_interface = 0.0.0.0</code> y <code>http_port = 8069</code> en el <code>odoo.conf</code>."),
    ("I-06", "Primer arranque",
     "<i>option addons_path, invalid addons directory '/mnt/extra-addons', skipped</i>.",
     "La carpeta <code>addons</code> está vacía y Odoo 19 no usa carpetas sin módulos.",
     "No hace falta hacer nada. El aviso se irá cuando meta algún módulo en <code>addons/</code>."),
    ("I-07", "Uso",
     "Abajo a la derecha salía <i>Se perdió la conexión en tiempo real</i> (figura al final de esta sección).",
     "Con <code>workers = 2</code> la conexión en tiempo real (<code>/websocket</code>) va por el puerto 8072, pero el "
     "navegador la busca en el 8069 porque no hay un nginx que la redirija.",
     "Como es un entorno de prácticas, puse <code>workers = 0</code> y así todo va por el 8069. Para una empresa real "
     "habría que dejar los workers y poner nginx mandando <code>/websocket</code> al 8072."),
    ("I-08", "Empresa",
     "Al guardar el NIF: <i>Parece que el número NIF [B46098765] para contacto [TechParts S.L.] no es válido</i>.",
     "Al instalar Facturación se instala la localización española, que comprueba la última cifra del NIF. Haciendo la "
     "cuenta, para <code>B4609876</code> la última cifra debería ser <b>0</b> (B46098760). El CIF del enunciado es inventado.",
     "Yo ya había guardado el NIF del enunciado (ESB46098765) antes de instalar Facturación, así que se quedó guardado. "
     "Si lo vuelves a escribir, Odoo no lo acepta. Lo dejo como pide el enunciado y lo explico aquí."),
    ("I-09", "Permisos",
     "En el usuario no aparece la opción «Contable» en Facturación. Solo salen <i>Facturación</i> y <i>Administrador</i>.",
     "En la versión Community de Odoo el permiso de «Contable» existe, pero está oculto.",
     "Activé el modo desarrollador (<code>?debug=1</code>) y, en el usuario, en Grupos, añadí «Mostrar características "
     "de contabilidad completas». Así Marcos tiene los menús de Contabilidad y Revisión, pero no Configuración."),
    ("I-10", "Permisos",
     "No hay un permiso aparte para CRM.",
     "En Odoo 19 el acceso a CRM va con el permiso de <b>Ventas</b>.",
     "Con el permiso de Ventas ya tienen CRM. Comprobé que Ana, Pedro y Sofía ven la app CRM."),
    ("I-11", "Permisos",
     "Los usuarios que no son administradores ven el menú «Aplicaciones».",
     "Odoo 19 deja que cualquier usuario <i>pida</i> al administrador que instale una aplicación.",
     "Es normal. No pueden instalar nada porque no tienen permisos de administrador."),
    ("I-12", "Aspecto",
     "La foto del administrador seguía teniendo la letra «A».",
     "Se creó al principio, cuando el usuario se llamaba «Administrator».",
     "Borré la imagen del contacto y Odoo la volvió a crear con la «C» de Carlos Méndez."),
    ("I-13", "Copia de seguridad",
     "<code>dropdb techparts_restore</code> daba <i>database is being accessed by other users</i>.",
     "Odoo seguía conectado a la base de datos de prueba después de probar el login.",
     "Usé <code>dropdb --force</code>, que cierra las conexiones y luego la borra."),
]

# --------------------------------------------------------------------------- #
CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10pt; color: #1d2433; line-height: 1.45; }
h1 { font-size: 17pt; color: #124a80; border-bottom: 3px solid #f58c1e; padding-bottom: 4px; margin: 0 0 10px;
     page-break-before: always; }
h2 { font-size: 12.5pt; color: #124a80; margin: 16px 0 6px; }
h3 { font-size: 11pt; color: #333; margin: 12px 0 4px; }
p { margin: 5px 0; text-align: justify; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.6pt; background: #eef2f7; padding: 0 3px; border-radius: 3px; }
pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.2pt; line-height: 1.35; padding: 8px 10px;
      border-radius: 5px; white-space: pre-wrap; word-break: break-all; margin: 6px 0; page-break-inside: avoid; }
pre.cmd { background: #1e2127; color: #d7dae0; border-left: 4px solid #98c379; }
pre.code { background: #f5f7fa; border: 1px solid #d9dee6; }
figure { margin: 8px auto 12px; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; border: 1px solid #c9d0da; border-radius: 4px; }
figcaption { font-size: 8.4pt; color: #555; margin-top: 3px; }
.par { display: flex; gap: 10px; align-items: flex-start; page-break-inside: avoid; }
.par figure { flex: 1; margin: 6px 0 10px; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: 6px 0; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #124a80; color: #fff; text-align: left; padding: 5px 6px; }
td { border-bottom: 1px solid #d9dee6; padding: 4px 6px; vertical-align: top; }
tr:nth-child(even) td { background: #f5f7fa; }
table.inc { table-layout: fixed; }
table.inc td:first-child { white-space: nowrap; }
ul { margin: 4px 0 4px 18px; padding: 0; }
.tabpie { font-size: 8.4pt; color: #555; text-align: center; margin-bottom: 12px; }
.nota { background: #fff6e8; border-left: 4px solid #f58c1e; padding: 6px 10px; margin: 8px 0; font-size: 9pt; }
.ok { background: #eaf7ef; border-left: 4px solid #2e9e5b; padding: 6px 10px; margin: 8px 0; font-size: 9pt; }
/* Portada */
.portada { height: 255mm; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.portada img { width: 60mm; }
.portada .t1 { font-size: 24pt; font-weight: bold; color: #124a80; margin-top: 10mm; }
.portada .t2 { font-size: 14pt; color: #f58c1e; margin: 3mm 0 14mm; }
.portada table { width: 125mm; font-size: 10.5pt; }
.portada td { padding: 6px 10px; text-align: left; }
.portada td:first-child { font-weight: bold; color: #124a80; width: 42mm; }
.indice { font-size: 10.5pt; line-height: 1.9; }
.indice span { color: #888; }
.arq { display: flex; gap: 14px; justify-content: center; align-items: center; margin: 10px 0; font-size: 9pt; }
.caja { border: 2px solid #124a80; border-radius: 8px; padding: 8px 12px; text-align: center; background: #f5f9fd; }
.caja b { color: #124a80; }
.flecha { font-size: 18pt; color: #f58c1e; }
"""


def portada():
    return f"""
<div class="portada">
  <img src="../proyecto/logo_techparts.png">
  <div class="t1">Manual técnico de instalación<br>y configuración de Odoo 19</div>
  <div class="t2">TechParts S.L. — Actividad Evaluable AEV2.1</div>
  <table>
    <tr><td>Alumno</td><td>{ALUMNO}</td></tr>
    <tr><td>Curso</td><td>{CURSO}</td></tr>
    <tr><td>Módulo</td><td>{MODULO}</td></tr>
    <tr><td>Unidad / RA</td><td>UD2 · R2 — Implanta sistemas ERP-CRM (criterios a–f)</td></tr>
    <tr><td>Fecha</td><td>{FECHA}</td></tr>
    <tr><td>Entorno</td><td>Odoo 19.0 (Community) · PostgreSQL 16 · Docker Compose</td></tr>
  </table>
</div>"""


def indice():
    items = ["Introducción y entorno de trabajo", "Preparación del sistema anfitrión",
             "Estructura del proyecto y ficheros de configuración", "Despliegue con Docker Compose",
             "Creación de la base de datos", "Configuración de la empresa", "Instalación de módulos",
             "Usuarios y permisos", "Verificación de accesos por usuario", "Copia de seguridad y restauración",
             "Incidencias encontradas y resolución", "Conclusiones",
             "Anexo A. Contenido del ZIP entregado", "Anexo B. Scripts que he usado"]
    li = "".join(f"<div>{i + 1 if i < 12 else ''}{'.' if i < 12 else ''} {t}</div>" for i, t in enumerate(items))
    return f"<h1 style='page-break-before:always'>Índice</h1><div class='indice'>{li}</div>"


def cuerpo():
    compose = leer("proyecto/docker-compose.yml")
    conf = leer("proyecto/config/odoo.conf")
    backup_sh = leer("proyecto/backup.sh")
    restore_sh = leer("proyecto/restore.sh")
    curl_web = cmd("curl -X POST http://localhost:8069/web/database/backup \\\n"
                   "     -F master_pwd='********' -F name=techparts -F backup_format=zip -o backup/techparts_web.zip")

    s = []
    # 1 -------------------------------------------------------------------
    s.append(f"""
<h1>1. Introducción y entorno de trabajo</h1>
<p>En este manual explico cómo he instalado y configurado <b>Odoo 19</b> para la empresa <b>TechParts S.L.</b>,
que es la misma empresa de la UD1. He seguido la sección 2.4 de los apuntes y lo he montado con <b>Docker Compose</b>,
usando dos contenedores: uno para Odoo y otro para la base de datos PostgreSQL.</p>
<p>Para cada paso pongo los comandos que he usado y capturas de pantalla. Al final están la tabla con los usuarios y
sus permisos, la copia de seguridad y los problemas que me han ido saliendo y cómo los he solucionado.</p>
<h2>1.1 Esquema de la instalación</h2>
<div class="arq">
  <div class="caja"><b>Navegador</b><br>http://localhost:8069</div><div class="flecha">➜</div>
  <div class="caja"><b>techparts_odoo</b><br>imagen <code>odoo:19.0</code><br>puertos 8069 / 8072<br>vol. <code>odoo-web-data</code> (filestore)</div>
  <div class="flecha">➜</div>
  <div class="caja"><b>techparts_db</b><br>imagen <code>postgres:16</code><br>puerto interno 5432<br>vol. <code>odoo-db-data</code></div>
</div>
<h2>1.2 Versiones utilizadas</h2>
<table><tr><th>Componente</th><th>Versión</th><th>Función</th></tr>
<tr><td>Docker Engine</td><td>29.3.1</td><td>Motor de contenedores</td></tr>
<tr><td>Docker Compose</td><td>v5.1.1 (plugin <code>docker compose</code>)</td><td>Levantar los dos contenedores a la vez</td></tr>
<tr><td>Odoo</td><td>19.0-20260908 (Community)</td><td>ERP-CRM</td></tr>
<tr><td>PostgreSQL</td><td>16.15</td><td>Base de datos</td></tr>
<tr><td>Navegador</td><td>Chromium</td><td>Acceso web y capturas</td></tr></table>
{tab_pie("Versiones del software instalado.")}
""")
    # 2 -------------------------------------------------------------------
    s.append(f"""
<h1>2. Preparación del sistema anfitrión</h1>
<p>Lo primero que hice fue comprobar que tenía Docker y Docker Compose instalados. Al ejecutar
<code>docker info</code> me dio un error porque el servicio de Docker no estaba arrancado (incidencia <b>I-01</b>),
así que lo arranqué con <code>systemctl</code> y ya funcionó.</p>
{cmd('''sudo systemctl start docker
sudo systemctl enable docker
docker --version
docker compose version
docker info''')}
{fig("T00_terminal_docker_daemon.png", "Incidencia I-01: Docker no estaba arrancado. Lo arranco y compruebo que ya funciona.")}
{fig("T01_terminal_versiones.png", "Versiones de Docker Engine y Docker Compose.")}
""")
    # 3 -------------------------------------------------------------------
    s.append(f"""
<h1>3. Estructura del proyecto y ficheros de configuración</h1>
<h2>3.1 Carpetas</h2>
{cmd('''mkdir -p proyecto/{config,addons,logs} backup
cd proyecto
sudo chown 100:101 logs && chmod 775 logs   # usuario odoo del contenedor (ver I-03)''')}
<table><tr><th>Ruta</th><th>Contenido</th><th>Montaje en el contenedor</th></tr>
<tr><td><code>docker-compose.yml</code></td><td>Definición de los servicios <i>db</i> y <i>odoo</i></td><td>—</td></tr>
<tr><td><code>config/odoo.conf</code></td><td>Configuración del servidor Odoo</td><td><code>/etc/odoo</code></td></tr>
<tr><td><code>addons/</code></td><td>Para módulos propios (de momento está vacía)</td><td><code>/mnt/extra-addons</code></td></tr>
<tr><td><code>logs/</code></td><td>Fichero <code>odoo.log</code></td><td><code>/var/log/odoo</code></td></tr>
<tr><td><code>backup.sh</code> / <code>restore.sh</code></td><td>Scripts de copia y restauración (sección 10)</td><td>—</td></tr></table>
{tab_pie("Carpetas del proyecto.")}
{fig("T02_terminal_estructura.png", "Carpetas creadas y permisos de la carpeta logs (100:101 es el usuario odoo del contenedor).")}
<h2>3.2 docker-compose.yml</h2>
<p>Lo más importante del fichero: con <code>depends_on</code> y <code>service_healthy</code> hago que Odoo espere
a que la base de datos esté lista antes de arrancar. Los volúmenes sirven para no perder los datos aunque borre los
contenedores. <code>pull_policy: missing</code> lo añadí después por la incidencia I-02.</p>
{code(compose)}
<h2>3.3 config/odoo.conf</h2>
<p>Lo que he configurado: <code>admin_passwd</code> es la contraseña maestra para crear y hacer copias de las bases
de datos; <code>dbfilter</code> hace que solo se use la base de datos <i>techparts</i>; <code>without_demo</code> quita
los datos de ejemplo; <code>logfile</code> guarda el log en la carpeta logs; y <code>workers = 0</code> lo cambié por la
incidencia I-07.</p>
{code(conf)}
""")
    # 4 -------------------------------------------------------------------
    s.append(f"""
<h1>4. Despliegue con Docker Compose</h1>
{cmd('''docker compose pull        # descarga odoo:19.0 y postgres:16
docker compose up -d       # crea la red y los volúmenes y arranca los contenedores
docker compose ps
docker compose logs -f odoo''')}
{fig("T03_terminal_pull.png", "Descarga de las imágenes (odoo:19.0 ocupa unos 3,3 GB y postgres:16 unos 640 MB).")}
{fig("T04_terminal_up.png", "docker compose up -d: primero arranca la base de datos y, cuando está «Healthy», arranca Odoo.")}
{fig("T05_terminal_ps.png", "Los dos contenedores funcionando, Odoo responde con un 200 y los volúmenes están creados.")}
<h2>4.1 Primer arranque: avisos y errores</h2>
<p>Odoo arrancó a la primera, pero al mirar el log vi un error y tres avisos (incidencias I-03 a I-06). Los arreglé
cambiando el <code>odoo.conf</code> y los permisos de la carpeta <code>logs/</code>, y reinicié con
<code>docker compose restart odoo</code>. Ahora solo queda el aviso de la carpeta <code>addons</code> vacía, que no
afecta a nada.</p>
{fig("T06_terminal_errores_arranque.png", "Log del primer arranque con los errores y avisos que me salieron.")}
{fig("T07_terminal_odoo_conf.png", "Así quedó el odoo.conf después de corregirlo.")}
""")
    # 5 -------------------------------------------------------------------
    s.append(f"""
<h1>5. Creación de la base de datos</h1>
<p>Entré en <code>http://localhost:8069</code> y, como todavía no había ninguna base de datos, Odoo me llevó
directamente a la pantalla para crearla (<code>/web/database/manager</code>). Rellené estos datos:</p>
<table><tr><th>Campo</th><th>Valor</th></tr>
<tr><td>Master Password</td><td>la definida en <code>admin_passwd</code></td></tr>
<tr><td>Database Name</td><td><code>techparts</code></td></tr>
<tr><td>Email / Password</td><td><code>carlos@techparts.es</code> / <code>Carlos2025!</code> (será el usuario 1, Carlos Méndez)</td></tr>
<tr><td>Phone</td><td>+34 960 987 654</td></tr>
<tr><td>Language / Country</td><td>Spanish / Español · Spain</td></tr>
<tr><td>Demo Data</td><td>Sin marcar</td></tr></table>
{tab_pie("Parámetros de creación de la base de datos.")}
<div class="nota">El usuario administrador que se crea aquí lo he usado como <b>Carlos Méndez</b>
(Administrador). Así en total hay justo los 8 usuarios que pide el enunciado.</div>
{par(fig("03_gestor_bd_vacio.png", "Pantalla para crear la base de datos."), fig("04_crear_bd_formulario.png", "Formulario de creación de la BD techparts."))}
{par(fig("05_pantalla_login.png", "Pantalla de inicio de sesión."), fig("06_primer_acceso_odoo.png", "Primera vez que entro: todavía pone «My Company»."))}
""")
    # 6 -------------------------------------------------------------------
    s.append(f"""
<h1>6. Configuración de la empresa</h1>
<p>Los datos de la empresa se ponen en <b>Ajustes → Opciones generales → Compañías → Actualizar información</b>
(también se puede entrar desde <b>Ajustes → Usuarios y compañías → Compañías</b>). Puse estos datos:</p>
<table><tr><th>Campo</th><th>Valor</th></tr>
<tr><td>Nombre</td><td>TechParts S.L.</td></tr><tr><td>NIF</td><td>ESB46098765 (B-46098765) — ver I-08</td></tr>
<tr><td>Dirección</td><td>Polígono Industrial Fuente del Jarro<br>C/ de la Innovación, 7, nave 3</td></tr>
<tr><td>Ciudad / C.P.</td><td>Paterna · 46988</td></tr><tr><td>Provincia / País</td><td>València (Valencia) · España</td></tr>
<tr><td>Teléfono</td><td>+34 960 987 654</td></tr><tr><td>Email</td><td>admin@techparts.es</td></tr>
<tr><td>Sitio web</td><td>https://www.techparts.es</td></tr><tr><td>Moneda</td><td>EUR (Euro)</td></tr>
<tr><td>Zona horaria</td><td>Europe/Madrid (preferencias de los 8 usuarios y horario laboral de la empresa)</td></tr>
<tr><td>Logotipo</td><td>Un engranaje con un circuito dentro (<code>proyecto/logo_techparts.png</code>), hecho por mí</td></tr></table>
{tab_pie("Datos de la empresa TechParts S.L.")}
{fig("07_datos_empresa.png", "Ficha de la empresa con todos los datos, el logo y la moneda en EUR.", "92%")}
{fig("08_ajustes_compania.png", "Resumen de la empresa en Ajustes.", "92%")}
{fig("inc_nif_invalido.png", "Incidencia I-08: Odoo no acepta el CIF del enunciado porque la última cifra (dígito de control) no cuadra.", "92%")}
""")
    # 7 -------------------------------------------------------------------
    s.append(f"""
<h1>7. Instalación de módulos</h1>
<p>En el menú <b>Aplicaciones</b> le di a <b>Activar</b> en los 6 módulos. Odoo instala también otros módulos que
necesitan y, como la empresa es de España, instaló solo la localización española (<code>l10n_es</code>) con el plan
contable de <b>PYMEs 2008</b> y la comprobación del NIF (<code>base_vat</code>).</p>
<table><tr><th>Aplicación</th><th>Módulo técnico</th><th>Tiempo de instalación</th></tr>
<tr><td>Ventas</td><td><code>sale_management</code></td><td>44,4 s (el primero tarda más porque instala cosas comunes)</td></tr>
<tr><td>Compras</td><td><code>purchase</code></td><td>4,2 s</td></tr>
<tr><td>Inventario</td><td><code>stock</code></td><td>13,1 s</td></tr>
<tr><td>CRM</td><td><code>crm</code></td><td>7,5 s</td></tr>
<tr><td>Facturación</td><td><code>account</code> (+ <code>l10n_es</code>, <code>base_vat</code>)</td><td>3,5 s</td></tr>
<tr><td>Empleados</td><td><code>hr</code></td><td>10,8 s</td></tr></table>
{tab_pie("Módulos instalados.")}
{fig("09_modulos_instalados.png", "Aplicaciones filtrando por «Instalado»: salen los 6 módulos y algunos que se instalan con ellos.", "92%")}
{fig("10_menu_apps_administrador.png", "Menú de aplicaciones del administrador después de instalar todo.", "80%")}
""")
    # 8 -------------------------------------------------------------------
    filas = "".join(f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td><td><code>{u[3]}</code></td><td>{u[4]}</td>"
                    f"<td>{u[5]}</td><td>{u[6]}</td></tr>" for u in USUARIOS)
    s.append(f"""
<h1>8. Usuarios y permisos</h1>
<p>Los usuarios se crean en <b>Ajustes → Usuarios y compañías → Usuarios → Nuevo</b>. En cada uno puse el nombre y
el email (que es el login), la contraseña (<i>Acción → Cambiar contraseña</i>) y, en la pestaña
<b>Permisos de acceso</b>, el permiso de cada aplicación. En <b>Preferencias</b> puse el idioma en español y la zona
horaria Europe/Madrid. Además, en <b>Empleados</b> creé los 5 departamentos (Dirección, Ventas, Almacén, Compras y
Administración) con cada empleado en el suyo y un responsable por departamento.</p>
<h2>8.1 Tabla resumen de usuarios y permisos</h2>
<table><tr><th>#</th><th>Nombre</th><th>Login</th><th>Contraseña</th><th>Dpto.</th><th>Permiso pedido</th><th>Configuración en Odoo 19</th></tr>{filas}</table>
{tab_pie("Usuarios creados y qué permiso he elegido en Odoo 19 para cada uno.")}
<div class="nota"><b>Por qué he elegido estos permisos.</b> En Odoo 19 no pone «Responsable»; lo que más se
parece es el nivel <i>Administrador</i> de cada aplicación. Para «Ventas: Usuario» he puesto <i>Solo mostrar documentos
propios</i>, para que cada comercial vea solo sus presupuestos y oportunidades, mientras que Ana, como responsable, ve los
de todos. CRM no tiene un permiso aparte, va incluido en el de Ventas (I-10). Lo de «Contable» lo explico en la
incidencia I-09.</div>
{fig("11_lista_usuarios.png", "Lista con los 8 usuarios creados.", "92%")}
{par(fig("12_permisos_ana_garcia.png", "Ana García: Ventas = Administrador (Responsable)."), fig("13_permisos_javier_romero.png", "Javier Romero: Inventario = Administrador (Responsable)."))}
{par(fig("14_permisos_marcos_soler.png", "Marcos Soler: Contabilidad = Facturación…"), fig("15_marcos_grupos_modo_desarrollador.png", "…y, en modo desarrollador, el grupo «Mostrar características de contabilidad completas» (Contable)."))}
{fig("16_empleados_departamentos.png", "App Empleados: los 8 empleados repartidos en los 5 departamentos.", "92%")}
""")
    # 9 -------------------------------------------------------------------
    filas = "".join(f"<tr><td>{v[0]}</td><td>{v[1]}</td><td>{v[2]}</td><td>{v[3]}</td></tr>" for v in VERIF)
    s.append(f"""
<h1>9. Verificación de accesos por usuario</h1>
<p>Para comprobar los permisos cerré la sesión del administrador y fui entrando con <b>cada uno de los 8 usuarios</b>.
En cada uno miré qué aplicaciones le salen y qué menús tiene dentro de la aplicación de su departamento. Todos ven
también las apps que son para todo el mundo: <i>Conversaciones, Calendario, Contactos, Tableros, Empleados</i> (solo el
listado) y <i>Aplicaciones</i> (solo para pedir que se instale algo, ver I-11).</p>
<table><tr><th>Usuario</th><th>Apps de negocio visibles</th><th>App revisada</th><th>Menús dentro de la app</th></tr>{filas}</table>
{tab_pie("Resultado: los responsables tienen «Informes» y «Configuración» y los usuarios normales no.")}
<h2>9.1 Ventas: Ana García (Responsable) frente a Pedro López (Usuario)</h2>
{par(fig("u2_ana_garcia_id.png", "Sesión iniciada como Ana García."), fig("u3_pedro_lopez_id.png", "Sesión iniciada como Pedro López."))}
{par(fig("u2_ana_garcia_menu.png", "Apps de Ana: CRM y Ventas, pero no Inventario, Compra ni Facturación."), fig("u3_pedro_lopez_menu.png", "Apps de Pedro: las mismas que Ana."))}
{par(fig("u2_ana_garcia_app.png", "Ventas (Ana): con Informes y Configuración."), fig("u3_pedro_lopez_app.png", "Ventas (Pedro): sin Informes ni Configuración."))}
<h2>9.2 Inventario: Javier Romero (Responsable) frente a Lucía Herrero (Usuario)</h2>
{par(fig("u5_javier_romero_id.png", "Sesión iniciada como Javier Romero."), fig("u6_lucia_herrero_id.png", "Sesión iniciada como Lucía Herrero."))}
{par(fig("u5_javier_romero_menu.png", "Apps de Javier: solo Inventario como app de negocio."), fig("u6_lucia_herrero_menu.png", "Apps de Lucía: solo Inventario como app de negocio."))}
{par(fig("u5_javier_romero_app.png", "Inventario (Javier): con Informes y Configuración."), fig("u6_lucia_herrero_app.png", "Inventario (Lucía): sin Informes ni Configuración."))}
<h2>9.3 Compras (Elena Vidal) y Facturación (Marcos Soler)</h2>
{par(fig("u7_elena_vidal_menu.png", "Apps de Elena Vidal: solo Compra."), fig("u8_marcos_soler_menu.png", "Apps de Marcos Soler: solo Facturación."))}
{par(fig("u7_elena_vidal_app.png", "Compra (Elena, Responsable): con Configuración."), fig("u8_marcos_soler_app.png", "Facturación (Marcos, Contable): Contabilidad y Revisión, sin Configuración."))}
<h2>9.4 Sofía Torres y Carlos Méndez</h2>
{par(fig("u4_sofia_torres_menu.png", "Apps de Sofía Torres (Ventas/CRM Usuario)."), fig("u1_carlos_menu.png", "Apps de Carlos Méndez (Administrador): todas + Ajustes."))}
<h2>9.5 Comprobación en el servidor (matriz de accesos)</h2>
<p>Además, con un pequeño script, entré con cada usuario y pregunté a Odoo si puede leer (L) o crear (C) datos de las
partes principales. Algunos usuarios tienen acceso a cosas de otros departamentos, pero Odoo funciona así: cuando un
comercial confirma un pedido se crea un albarán de almacén y una factura, así que necesita esos permisos aunque no vea
esos menús. Solo Carlos puede crear usuarios y gestionar empleados.</p>
{fig("T10_terminal_matriz_accesos.png", "Qué puede leer (L) y crear (C) cada usuario, comprobado entrando con su cuenta.")}
""")
    # 10 ------------------------------------------------------------------
    s.append(f"""
<h1>10. Copia de seguridad y restauración</h1>
<p>Siguiendo la sección 2.8.2 hice la copia de las dos partes: la base de datos (un fichero .sql sacado con
<code>pg_dump</code>) y el <b>filestore</b>, que es donde Odoo guarda los archivos adjuntos, las imágenes y el logo
(<code>/var/lib/odoo/filestore/techparts</code>). Si solo copias la base de datos, al restaurar pierdes las imágenes y
los adjuntos.</p>
<h2>10.1 Desde la terminal (script backup.sh)</h2>
{cmd('''# Base de datos
docker exec techparts_db pg_dump -U odoo -d techparts --no-owner --no-privileges > backup/techparts_AAAAMMDD_HHMM.sql
# Filestore
docker exec techparts_odoo tar -czf - -C /var/lib/odoo/filestore techparts > backup/filestore_techparts_AAAAMMDD_HHMM.tar.gz''')}
{code(backup_sh)}
<h2>10.2 Desde la web</h2>
<p>También hice la copia desde <b>/web/database/manager → Backup</b>, poniendo la contraseña maestra y el formato
<i>zip (includes filestore)</i>. Te descarga un ZIP con <code>dump.sql</code>, <code>manifest.json</code> y la carpeta
<code>filestore/</code>. Lo mismo se puede hacer con este comando:</p>
{curl_web}
{fig("T08_terminal_backup.png", "Ejecución de backup.sh, copia en ZIP desde la web y las sumas SHA-256 para comprobar los ficheros.")}
<h2>10.3 Prueba de restauración</h2>
<p>Para asegurarme de que la copia funciona de verdad, la restauré en una base de datos nueva
(<code>techparts_restore</code>) con <code>restore.sh</code>. Comprobé que estaban los 8 usuarios y los datos de la
empresa, que no faltaba ningún archivo del filestore y que se podía iniciar sesión. Después borré esa base de datos de
prueba.</p>
{code(restore_sh)}
{fig("T09_terminal_restauracion.png", "La restauración funciona: están los 8 usuarios y la empresa, no falta ningún archivo y el login va bien.")}
<div class="ok">Ficheros que entrego en <code>backup/</code>: <code>techparts_20260925_1003.sql</code> (≈ 24 MB),
<code>filestore_techparts_20260925_1003.tar.gz</code> (≈ 3,4 MB), <code>techparts_web_20260925_1003.zip</code>
(≈ 6,2 MB) y <code>SHA256SUMS_20260925_1003.txt</code>.</div>
""")
    # 11 ------------------------------------------------------------------
    filas = "".join(f"<tr><td><b>{i[0]}</b></td><td>{i[1]}</td><td>{i[2]}</td><td>{i[3]}</td><td>{i[4]}</td></tr>"
                    for i in INCIDENCIAS)
    s.append(f"""
<h1>11. Incidencias encontradas y resolución</h1>
<p>Estos son los problemas que me fueron saliendo durante la práctica. En cada uno pongo el mensaje que me salió,
por qué pasaba y cómo lo solucioné.</p>
<table class="inc"><colgroup><col style="width:7%"><col style="width:10%"><col style="width:26%"><col style="width:27%"><col style="width:30%"></colgroup><tr><th>ID</th><th>Fase</th><th>Qué pasó</th><th>Por qué</th><th>Solución</th></tr>{filas}</table>
{tab_pie("Registro de incidencias.")}
{fig("T03b_terminal_error_429.png", "Incidencia I-02: Docker Hub no me dejaba descargar más veces (429 Too Many Requests).")}
{fig("inc_websocket_desconectado.png", "Incidencia I-07: aviso de «Se perdió la conexión en tiempo real» abajo a la derecha.", "85%")}
<h2>11.1 Cómo he ido resolviendo los problemas</h2>
<p>Casi siempre he hecho lo mismo: primero mirar el log (<code>docker compose logs odoo</code> o
<code>logs/odoo.log</code>), luego buscar qué parte fallaba (por ejemplo, con <code>docker exec techparts_odoo id</code>
vi con qué usuario se ejecuta Odoo, y con el modo desarrollador vi los grupos de permisos), después cambiar solo lo
necesario y, por último, reiniciar y comprobar que el error ya no sale.</p>
""")
    # 12 ------------------------------------------------------------------
    s.append("""
<h1>12. Conclusiones</h1>
<p>He conseguido tener Odoo 19 funcionando con Docker Compose. Una ventaja es que, copiando la carpeta
<code>proyecto/</code> y ejecutando <code>docker compose up -d</code>, se puede montar igual en otro ordenador. La
empresa TechParts S.L. tiene todos sus datos, el logo y la contabilidad española, y están instalados los 6 módulos.
He comprobado los permisos de los 8 usuarios <b>entrando con cada uno</b>: cada uno ve solo lo de su departamento y los
responsables tienen Informes y Configuración, que los demás no tienen.</p>
<p>La copia de seguridad (base de datos + filestore) la he restaurado en otra base de datos y funciona bien. Lo que más
he aprendido: hay que mirar siempre el log después de arrancar; dentro del contenedor Odoo no es root, así que hay que
dar permisos a las carpetas; con <i>workers</i> hace falta nginx para que funcione el chat en tiempo real; y en Odoo 19
algunos permisos solo se ven con el modo desarrollador.</p>
<h2>Qué mejoraría si fuera para una empresa de verdad</h2>
<ul><li>Proxy inverso nginx con HTTPS, <code>proxy_mode = True</code> y <code>workers ≥ 2</code>.</li>
<li><code>list_db = False</code> tras la puesta en marcha, para ocultar el gestor de bases de datos.</li>
<li>Contraseñas en un fichero <code>.env</code> fuera del control de versiones.</li>
<li>Copias automáticas con <code>cron</code> (<code>backup.sh</code> diario) guardadas fuera del servidor.</li>
<li>Contraseñas más seguras y verificación en dos pasos para el administrador.</li></ul>
""")
    # Anexos --------------------------------------------------------------
    s.append("""
<h1>Anexo A. Contenido del ZIP entregado</h1>
<pre class='code'>AEV2_1_VidalMarinCarlos.zip
├── proyecto/
│   ├── docker-compose.yml
│   ├── config/odoo.conf
│   ├── addons/                 (vacía, para módulos propios)
│   ├── logs/                   (odoo.log)
│   ├── backup.sh  ·  restore.sh
│   └── logo_techparts.png
├── backup/
│   ├── techparts_20260925_1003.sql
│   ├── filestore_techparts_20260925_1003.tar.gz
│   ├── techparts_web_20260925_1003.zip
│   └── SHA256SUMS_20260925_1003.txt
└── Manual_Instalacion_TechParts.pdf</pre>
<h2>Restaurar el entorno en otro equipo</h2>
<pre class='cmd'>cd proyecto
sudo chown 100:101 logs
docker compose up -d
./restore.sh ../backup/techparts_20260925_1003.sql ../backup/filestore_techparts_20260925_1003.tar.gz techparts
# o bien: /web/database/manager → Restore → techparts_web_20260925_1003.zip
# Acceso: http://localhost:8069  ·  carlos@techparts.es / Carlos2025!</pre>
<h1 style="page-break-before:auto;margin-top:24px">Anexo B. Scripts que he usado</h1>
<p>Para no tener que repetir todo a mano cada vez que probaba algo, hice unos scripts en Python que se conectan a
Odoo por <b>XML-RPC</b>: uno para los datos de la empresa (<code>paso3_empresa.py</code>), otro para instalar los
módulos (<code>paso4_modulos.py</code>), otro para crear los usuarios, departamentos y empleados
(<code>paso6_usuarios.py</code>) y otro para comprobar los permisos (<code>paso9_matriz_accesos.py</code>). Las
capturas del navegador las saqué con Playwright, entrando con cada usuario (<code>paso7_verificar_usuarios.py</code>).
Las capturas de terminal son la salida de los comandos, que guardé en la carpeta <code>evidencias/</code>.</p>
""")
    return "\n".join(s)


def main():
    doc = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>Manual de instalación Odoo 19 — TechParts S.L.</title><style>{CSS}</style></head>
<body>{portada()}{indice()}{cuerpo()}</body></html>"""
    out_html = AQUI / "Manual_Instalacion_TechParts.html"
    out_html.write_text(doc, encoding="utf-8")
    out_pdf = RAIZ / "Manual_Instalacion_TechParts.pdf"
    pie = (f'<div style="font-size:7.5pt;color:#777;width:100%;padding:0 16mm;display:flex;justify-content:space-between;'
           f'font-family:DejaVu Sans,sans-serif"><span>AEV2.1 · Odoo 19 · TechParts S.L. — {ALUMNO}</span>'
           f'<span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(out_html.as_uri())
        pg.wait_for_load_state("load")
        pg.pdf(path=str(out_pdf), format="A4", print_background=True, display_header_footer=True,
               header_template="<span></span>", footer_template=pie,
               margin={"top": "16mm", "bottom": "18mm", "left": "16mm", "right": "16mm"})
        b.close()
    print("PDF:", out_pdf, "figuras:", _n["fig"], "tablas:", _n["tab"])


if __name__ == "__main__":
    main()
