"""Configura los datos de la empresa TechParts S.L."""
import base64
from comun import rpc

uid, call = rpc()
es = call("res.country", "search", [["code", "=", "ES"]])[0]
valencia = call("res.country.state", "search", [["country_id", "=", es], ["name", "ilike", "Valencia"]])
eur = call("res.currency", "search", [["name", "=", "EUR"]])[0]
call("res.currency", "write", [eur], {"active": True})
logo = base64.b64encode(open("../proyecto/logo_techparts.png", "rb").read()).decode()

datos = {
    "name": "TechParts S.L.",
    "vat": "ESB46098765",
    "street": "Polígono Industrial Fuente del Jarro",
    "street2": "C/ de la Innovación, 7, nave 3",
    "city": "Paterna",
    "zip": "46988",
    "state_id": valencia[0],
    "country_id": es,
    "phone": "+34 960 987 654",
    "email": "admin@techparts.es",
    "website": "https://www.techparts.es",
    "currency_id": eur,
    "logo": logo,
}
call("res.company", "write", [1], datos)
# Zona horaria e idioma del administrador
call("res.users", "write", [uid], {"tz": "Europe/Madrid", "lang": "es_ES"})
print(call("res.company", "read", [1], fields=["name", "vat", "street", "street2", "city", "zip",
                                                "state_id", "country_id", "phone", "email",
                                                "website", "currency_id"]))
