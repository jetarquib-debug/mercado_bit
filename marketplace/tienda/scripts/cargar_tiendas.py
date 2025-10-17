from django.core.files import File
from django.conf import settings
import os
from django.contrib.auth.hashers import make_password
from usuario.models import Usuario, CodigoPais, Distrito, Provincia, Departamento, Pais
from tienda.models import Tienda, ImagenPerfilTienda


# ===============================
# 🖼️ CREAR IMÁGENES DE TIENDA
# ===============================
def cargar_imagenes_tienda():
    imagenes = [
        {"archivo": "tienda1.jpg", "es_principal": True},
        {"archivo": "tienda2.jpg", "es_principal": False},
        {"archivo": "tienda3.jpg", "es_principal": False},
    ]

    for img_data in imagenes:
        ruta = os.path.join(settings.MEDIA_ROOT, "tienda", img_data["archivo"])
        ruta_relativa = f"tienda/{img_data['archivo']}"

        if not os.path.exists(ruta):
            print(f"⚠️ Imagen no encontrada: {ruta}")
            ruta_relativa = "tienda/default.png"

        imagen, creado = ImagenPerfilTienda.objects.get_or_create(
            imagen=ruta_relativa,
            defaults={"es_principal": img_data["es_principal"]}
        )

        if creado:
            print(f"✅ Imagen creada: {imagen.imagen}")
        else:
            print(f"⚠️ Imagen ya existe: {imagen.imagen}")


# ===============================
# 🧑‍💼 CREAR USUARIOS PARA TIENDAS
# ===============================
def cargar_usuarios_tiendas():
    try:
        peru = Pais.objects.get(nomb_pais="Perú")
        lima = Departamento.objects.get(nomb_departamento="Lima")
        provincia_lima = Provincia.objects.get(nomb_provincia="Lima")
        distrito_miraflores = Distrito.objects.get(nomb_distrito="Miraflores")
    except Exception as e:
        print(f"❌ Error al obtener ubicaciones: {e}")
        return

    usuarios = [
        {
            "nombres": "Carlos",
            "apellidos": "Fernández",
            "email": "carlos@techstore.com",
            "contrasena": make_password("123456"),
            "pais": peru,
            "departamento": lima,
            "provincia": provincia_lima,
            "distrito": distrito_miraflores,
            "telefono": "987654321",
            "direccion": "Av. Arequipa 1234",
        },
        {
            "nombres": "Lucía",
            "apellidos": "Ramírez",
            "email": "lucia@gaminghub.com",
            "contrasena": make_password("123456"),
            "pais": peru,
            "departamento": lima,
            "provincia": provincia_lima,
            "distrito": distrito_miraflores,
            "telefono": "999111222",
            "direccion": "Jr. Los Laureles 567",
        },
    ]

    for data in usuarios:
        usuario, creado = Usuario.objects.get_or_create(email=data["email"], defaults=data)
        if creado:
            print(f"✅ Usuario creado: {usuario.email}")
        else:
            print(f"⚠️ Usuario ya existe: {usuario.email}")


# ===============================
# 🏪 CREAR TIENDAS
# ===============================
def cargar_tiendas():
    try:
        codigo_peru = CodigoPais.objects.get(pais__nomb_pais="Perú")
        distrito = Distrito.objects.get(nomb_distrito="Miraflores")
        provincia = Provincia.objects.get(nomb_provincia="Lima")
        departamento = Departamento.objects.get(nomb_departamento="Lima")
        pais = Pais.objects.get(nomb_pais="Perú")
    except Exception as e:
        print(f"❌ Error al obtener ubicaciones: {e}")
        return

    imagenes = list(ImagenPerfilTienda.objects.all()[:2])
    usuarios = list(Usuario.objects.filter(email__in=["carlos@techstore.com", "lucia@gaminghub.com"]))

    tiendas = [
        {
            "nombre_tienda": "TechStore Perú",
            "descripcion": "Tienda especializada en computadoras y accesorios.",
            "email": "ventas@techstore.com",
            "codigo_pais": codigo_peru,
            "telefono": "987654321",
            "direccion": "Av. Arequipa 1234",
            "pais": pais,
            "departamento": departamento,
            "provincia": provincia,
            "distrito": distrito,
            "ruc": "20123456789",
            "usuario": usuarios[0] if usuarios else None,
        },
        {
            "nombre_tienda": "Gaming Hub",
            "descripcion": "Todo para gamers: PCs, periféricos y más.",
            "email": "contacto@gaminghub.com",
            "codigo_pais": codigo_peru,
            "telefono": "999111222",
            "direccion": "Jr. Los Laureles 567",
            "pais": pais,
            "departamento": departamento,
            "provincia": provincia,
            "distrito": distrito,
            "ruc": "20567891234",
            "usuario": usuarios[1] if len(usuarios) > 1 else None,
        },
    ]

    for data in tiendas:
        tienda, creada = Tienda.objects.get_or_create(email=data["email"], defaults=data)
        if creada:
            tienda.imagenes.add(*imagenes)
            print(f"✅ Tienda creada: {tienda.nombre_tienda}")
        else:
            print(f"⚠️ Tienda ya existe: {tienda.nombre_tienda}")


# ===============================
# 🚀 FUNCIÓN GENERAL
# ===============================
def ejecutar_carga_tiendas():
    print("=== CARGANDO DATOS DE TIENDAS ===")
    cargar_imagenes_tienda()
    cargar_usuarios_tiendas()
    cargar_tiendas()
    print("=== ✅ CARGA DE TIENDAS COMPLETA ===")
