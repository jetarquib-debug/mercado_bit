from django.core.files import File
from django.conf import settings
import os
from usuario.models import Pais, Departamento, Provincia, Distrito, CodigoPais


# ===============================
# 🌎 PAISES DE SUDAMÉRICA
# ===============================
def cargar_paises_sudamerica():
    paises = [
        "Argentina", "Bolivia", "Brasil", "Chile", "Colombia", "Ecuador",
        "Guyana", "Paraguay", "Perú", "Surinam", "Uruguay", "Venezuela",
    ]

    for nombre in paises:
        pais, creado = Pais.objects.get_or_create(nomb_pais=nombre)
        if creado:
            print(f"✅ País creado: {nombre}")
        else:
            print(f"⚠️ País ya existe: {nombre}")


# ===============================
# 🏛️ DEPARTAMENTOS DEL PERÚ
# ===============================
def cargar_departamentos_peru():
    try:
        peru = Pais.objects.get(nomb_pais="Perú")
    except Pais.DoesNotExist:
        print("❌ El país 'Perú' no existe. Inserta primero los países de Sudamérica.")
        return

    departamentos = [
        "Amazonas", "Áncash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca",
        "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad",
        "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco",
        "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali"
    ]

    for nombre in departamentos:
        dep, creado = Departamento.objects.get_or_create(
            nomb_departamento=nombre, pais=peru
        )
        if creado:
            print(f"✅ Departamento creado: {nombre}")
        else:
            print(f"⚠️ Departamento ya existe: {nombre}")


# ===============================
# 🏙️ PROVINCIAS DE LIMA
# ===============================
def cargar_provincias_lima():
    try:
        lima = Departamento.objects.get(nomb_departamento="Lima")
    except Departamento.DoesNotExist:
        print("❌ El departamento 'Lima' no existe. Inserta los departamentos del Perú primero.")
        return

    provincias = [
        "Barranca", "Cajatambo", "Canta", "Cañete", "Huaral", "Huarochirí",
        "Huaura", "Lima", "Callao", "Oyón", "Yauyos",
    ]

    for nombre in provincias:
        prov, creado = Provincia.objects.get_or_create(
            nomb_provincia=nombre, departamento=lima
        )
        if creado:
            print(f"✅ Provincia creada: {nombre}")
        else:
            print(f"⚠️ Provincia ya existe: {nombre}")


def cargar_distritos_lima_callao():
    # ===============================
    # 🏘️ DISTRITOS DE LIMA
    # ===============================
    try:
        provincia_lima = Provincia.objects.get(nomb_provincia="Lima")
    except Provincia.DoesNotExist:
        print("❌ La provincia 'Lima' no existe. Inserta las provincias primero.")
        return

    distritos_lima = [
        "Ancón", "Ate", "Barranco", "Breña", "Carabayllo", "Chaclacayo", "Chorrillos",
        "Cieneguilla", "Comas", "El Agustino", "Independencia", "Jesús María",
        "La Molina", "La Victoria", "Lince", "Los Olivos", "Lurigancho", "Lurín",
        "Magdalena del Mar", "Miraflores", "Pachacámac", "Pucusana", "Pueblo Libre",
        "Puente Piedra", "Punta Hermosa", "Punta Negra", "Rímac", "San Bartolo",
        "San Borja", "San Isidro", "San Juan de Lurigancho", "San Juan de Miraflores",
        "San Luis", "San Martín de Porres", "San Miguel", "Santa Anita",
        "Santa María del Mar", "Santa Rosa", "Santiago de Surco", "Surquillo",
        "Villa El Salvador", "Villa María del Triunfo",
    ]

    for nombre in distritos_lima:
        dist, creado = Distrito.objects.get_or_create(
            nomb_distrito=nombre, provincia=provincia_lima
        )
        if creado:
            print(f"✅ Distrito creado: {nombre}")
        else:
            print(f"⚠️ Distrito ya existe: {nombre}")

    # ===============================
    # ⚓ DISTRITOS DEL CALLAO
    # ===============================
    try:
        provincia_callao = Provincia.objects.get(nomb_provincia="Callao")
    except Provincia.DoesNotExist:
        print("❌ La provincia 'Callao' no existe. Inserta las provincias primero.")
        return

    distritos_callao = [
        "Callao", "Bellavista", "Carmen de la Legua-Reynoso",
        "La Perla", "La Punta", "Ventanilla", "Mi Perú"
    ]

    for nombre in distritos_callao:
        dist, creado = Distrito.objects.get_or_create(
            nomb_distrito=nombre, provincia=provincia_callao
        )
        if creado:
            print(f"✅ Distrito creado: {nombre}")
        else:
            print(f"⚠️ Distrito ya existe: {nombre}")


# ===============================
# ☎️ CÓDIGOS DE PAÍSES
# ===============================
def cargar_codigos_paises():
    codigos = {
        "Argentina": "54",
        "Bolivia": "591",
        "Brasil": "55",
        "Chile": "56",
        "Colombia": "57",
        "Ecuador": "593",
        "Guyana": "592",
        "Paraguay": "595",
        "Perú": "51",
        "Surinam": "597",
        "Uruguay": "598",
        "Venezuela": "58",
    }

    for nombre_pais, codigo in codigos.items():
        try:
            pais = Pais.objects.get(nomb_pais=nombre_pais)

            # ✅ Ruta FÍSICA real
            ruta_imagen = os.path.join(settings.MEDIA_ROOT, 'codigo_pais', f"{nombre_pais.lower()}.png")

            # ✅ Ruta RELATIVA usada por ImageField (sin MEDIA_ROOT)
            ruta_relativa = f"codigo_pais/{nombre_pais.lower()}.png"

            if not os.path.exists(ruta_imagen):
                print(f"⚠️ No se encontró imagen para {nombre_pais} en {ruta_imagen}")
                ruta_relativa = "codigo_pais/default_bandera.png"

            CodigoPais.objects.update_or_create(
                pais=pais,
                defaults={
                    "codigo": codigo,
                    "imagen_pais": ruta_relativa
                }
            )

            print(f"✅ Código de país insertado o actualizado: {nombre_pais} (+{codigo})")

        except Pais.DoesNotExist:
            print(f"❌ No existe el país {nombre_pais}, insértalo primero.")


# ===============================
# 🚀 FUNCIÓN GENERAL
# ===============================
def ejecutar_carga_completa():
    print("=== CARGANDO DATOS INICIALES ===")
    cargar_paises_sudamerica()
    cargar_departamentos_peru()
    cargar_provincias_lima()
    cargar_distritos_lima_callao()
    cargar_codigos_paises()
    print("=== ✅ CARGA COMPLETA ===")
