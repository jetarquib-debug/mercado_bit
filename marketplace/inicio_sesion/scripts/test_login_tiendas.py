from usuario.models import Usuario, Pais, Departamento, Provincia, Distrito, CodigoPais
from tienda.models import Tienda
from django.contrib.auth.hashers import check_password


def preparar_usuarios_y_tiendas():
    # Asegurarse de que existan ubicaciones básicas
    pais = Pais.objects.filter(nomb_pais__icontains='Peru').first() or Pais.objects.first()
    departamento = Departamento.objects.first()
    provincia = Provincia.objects.first()
    distrito = Distrito.objects.first()
    codigo = CodigoPais.objects.filter(pais=pais).first() if pais else None

    datos = [
        {'nombres': 'Ana', 'apellidos': 'Sanchez', 'email': 'ana@example.com', 'contrasena': 'ana123'},
        {'nombres': 'Luis', 'apellidos': 'Martinez', 'email': 'luis@example.com', 'contrasena': 'luis123'},
        {'nombres': 'Pablo', 'apellidos': 'Rojas', 'email': 'pablo@example.com', 'contrasena': 'pablo123'},
    ]

    usuarios = []
    for d in datos:
        u, creado = Usuario.objects.get_or_create(email=d['email'], defaults={
            'nombres': d['nombres'], 'apellidos': d['apellidos'], 'contrasena': d['contrasena'],
            'telefono': '', 'direccion': '', 'pais': pais, 'codigo_pais': codigo,
            'departamento': departamento, 'provincia': provincia, 'distrito': distrito,
        })
        if creado:
            print(f'Usuario creado: {u.email}')
        else:
            # normalizar contraseña para el test
            u.contrasena = d['contrasena']
            u.save()
            print(f'Usuario actualizado (contraseña seteada): {u.email}')
        usuarios.append((u, d['contrasena']))

    # Crear tiendas para los dos primeros usuarios
    for u, _ in usuarios[:2]:
        tienda, creada = Tienda.objects.get_or_create(
            usuario=u,
            defaults={
                'nombre_tienda': f"Tienda de {u.nombres}",
                'email': f'ventas+{u.email}',
            }
        )
        if creada:
            print(f'Tienda creada para {u.email}: {tienda.nombre_tienda}')
        else:
            print(f'Tienda ya existe para {u.email}: {tienda.nombre_tienda}')

    return usuarios


def simular_logins(usuarios):
    print('\n--- Simulando intentos de login ---')
    for u, pw in usuarios:
        pw_ok = check_password(pw, u.contrasena)
        tiene_tienda = Tienda.objects.filter(usuario=u).exists()
        permit = pw_ok and (not tiene_tienda)
        print(f'{u.email} | pw_ok={pw_ok} | tiene_tienda={tiene_tienda} -> login_permitido={permit}')


def ejecutar_test():
    usuarios = preparar_usuarios_y_tiendas()
    simular_logins(usuarios)


if __name__ == '__main__':
    ejecutar_test()
