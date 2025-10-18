from django.contrib.auth.hashers import make_password
from django.core.files import File
from django.conf import settings
import os
from usuario.models import Usuario, Pais, Departamento, Provincia, Distrito, CodigoPais, ImagenPerfilUsuario


# ===============================
# 👤 USUARIOS DE EJEMPLO
# ===============================
def cargar_usuarios_basicos():
    try:
        peru = Pais.objects.get(nomb_pais="Perú")
        codigo_peru = CodigoPais.objects.get(pais=peru)
        departamento_lima = Departamento.objects.get(nomb_departamento="Lima")
        provincia_lima = Provincia.objects.get(nomb_provincia="Lima")
        distrito_miraflores = Distrito.objects.get(nomb_distrito="Miraflores")
    except Exception as e:
        print(f"❌ Error obteniendo ubicaciones base: {e}")
        print("Asegúrate de ejecutar primero el script de carga de países y regiones.")
        return

    usuarios = [
        {
            "nombres": "Juan",
            "apellidos": "Pérez",
            "email": "juan.perez@example.com",
            "contrasena": "123456",
            "telefono": "+51987654321",
            "direccion": "Av. Los Olivos 123",
            "sexo": "M",
            "dni_ce": 74589632,
        },
        {
            "nombres": "María",
            "apellidos": "Lopez",
            "email": "maria.lopez@example.com",
            "contrasena": "maria2025",
            "telefono": "+51912345678",
            "direccion": "Calle Primavera 456",
            "sexo": "F",
            "dni_ce": 87654321,
        },
        {
            "nombres": "Carlos",
            "apellidos": "Gómez",
            "email": "carlos.gomez@example.com",
            "contrasena": "carlospass",
            "telefono": "+51911223344",
            "direccion": "Av. San Martín 890",
            "sexo": "M",
            "dni_ce": 76543210,
        },
    ]

    for data in usuarios:
        usuario, creado = Usuario.objects.get_or_create(
            email=data["email"],
            defaults={
                "nombres": data["nombres"],
                "apellidos": data["apellidos"],
                # Pasamos la contraseña en texto para que el modelo la encripte en save()
                "contrasena": data["contrasena"],
                "telefono": data["telefono"],
                "direccion": data["direccion"],
                "sexo": data["sexo"],
                "dni_ce": data["dni_ce"],
                "pais": peru,
                "codigo_pais": codigo_peru,
                "departamento": departamento_lima,
                "provincia": provincia_lima,
                "distrito": distrito_miraflores,
            },
        )

        if creado:
            print(f"✅ Usuario creado: {usuario}")
        else:
            # Normalizar la contraseña actualizando a la versión en texto para que save() la encripte
            usuario.contrasena = data["contrasena"]
            usuario.nombres = data["nombres"]
            usuario.apellidos = data["apellidos"]
            usuario.telefono = data["telefono"]
            usuario.direccion = data["direccion"]
            usuario.sexo = data["sexo"]
            usuario.dni_ce = data["dni_ce"]
            usuario.pais = peru
            usuario.codigo_pais = codigo_peru
            usuario.departamento = departamento_lima
            usuario.provincia = provincia_lima
            usuario.distrito = distrito_miraflores
            usuario.save()
            print(f"⚠️ Usuario actualizado: {usuario.email} (contraseña normalizada)")


# ===============================
# 🖼️ ASIGNAR IMÁGENES DE PERFIL
# ===============================
def asignar_imagenes_usuarios():
    # Ruta de ejemplo en /media/usuario/
    ruta_base = os.path.join(settings.MEDIA_ROOT, "usuario")

    if not os.path.exists(ruta_base):
        print(f"⚠️ La carpeta {ruta_base} no existe. Crea la estructura /media/usuario/")
        return

    imagenes_disponibles = [
        "perfil_juan.jpg",
        "perfil_maria.jpg",
        "perfil_carlos.jpg",
    ]

    usuarios = Usuario.objects.filter(email__in=[
        "juan.perez@example.com",
        "maria.lopez@example.com",
        "carlos.gomez@example.com",
    ])

    for usuario, nombre_img in zip(usuarios, imagenes_disponibles):
        ruta_img = os.path.join(ruta_base, nombre_img)

        if not os.path.exists(ruta_img):
            print(f"⚠️ Imagen no encontrada para {usuario.email}: {ruta_img}")
            continue

        # Crear registro de imagen si no existe
        imagen_obj, _ = ImagenPerfilUsuario.objects.get_or_create(
            imagen=f"usuario/{nombre_img}",
            defaults={"es_principal": True}
        )

        usuario.imagenes.add(imagen_obj)
        print(f"🖼️ Imagen asignada a {usuario.email}")


# ===============================
# 🚀 FUNCIÓN GENERAL
# ===============================
def ejecutar_carga_usuarios():
    print("=== 👥 CARGANDO USUARIOS DE EJEMPLO ===")
    cargar_usuarios_basicos()
    asignar_imagenes_usuarios()
    print("=== ✅ USUARIOS INSERTADOS CORRECTAMENTE ===")
