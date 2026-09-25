"""Tabla de usuarios de TechParts S.L. (datos del enunciado)."""

BASE = ["base.group_user"]  # Usuario interno
ADMIN_TOTAL = ["base.group_system", "base.group_erp_manager", "sales_team.group_sale_manager",
               "purchase.group_purchase_manager", "stock.group_stock_manager",
               "account.group_account_manager", "account.group_account_user", "hr.group_hr_manager"]

USUARIOS = [
    # nombre, login, contraseña, grupos, departamento, puesto
    ("Carlos Méndez", "carlos@techparts.es", "Carlos2025!", ADMIN_TOTAL, "Dirección", "Director general / Administrador del sistema"),
    ("Ana García", "ana.garcia@techparts.es", "Ana2025!", ["sales_team.group_sale_manager"], "Ventas", "Responsable comercial"),
    ("Pedro López", "pedro.lopez@techparts.es", "Pedro2025!", ["sales_team.group_sale_salesman"], "Ventas", "Comercial"),
    ("Sofía Torres", "sofia.torres@techparts.es", "Sofia2025!", ["sales_team.group_sale_salesman"], "Ventas", "Comercial"),
    ("Javier Romero", "javier.romero@techparts.es", "Javier2025!", ["stock.group_stock_manager"], "Almacén", "Responsable de almacén"),
    ("Lucía Herrero", "lucia.herrero@techparts.es", "Lucia2025!", ["stock.group_stock_user"], "Almacén", "Operaria de almacén"),
    ("Elena Vidal", "elena.vidal@techparts.es", "Elena2025!", ["purchase.group_purchase_manager"], "Compras", "Responsable de compras"),
    ("Marcos Soler", "marcos.soler@techparts.es", "Marcos2025!", ["account.group_account_invoice", "account.group_account_user"], "Administración", "Contable"),
]

