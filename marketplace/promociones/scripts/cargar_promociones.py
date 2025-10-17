from django.utils import timezone
from datetime import timedelta
from promociones.models import Promocion
from pago.models import MetodoPago
from producto.models import Producto, Categoria


def insertar_promociones():
    ahora = timezone.now()

    promociones_data = [
        {
            "descripcion": "Descuento de verano en laptops",
            "descuento_porcentaje": 15.00,
            "fecha_inicio": ahora,
            "fecha_fin": ahora + timedelta(days=30),
            "metodo_pago": MetodoPago.objects.filter(nomb_meto="Tarjeta de Crédito").first(),
            "imagen_promocion": "promociones_imagenes/verano_laptops.png",
            "categorias": ["Laptops", "Accesorios"],
        },
        {
            "descripcion": "Ofertas en periféricos gaming",
            "descuento_porcentaje": 10.00,
            "fecha_inicio": ahora - timedelta(days=3),
            "fecha_fin": ahora + timedelta(days=20),
            "metodo_pago": MetodoPago.objects.filter(nomb_meto="Yape").first(),
            "imagen_promocion": "promociones_imagenes/gaming.png",
            "categorias": ["Teclados", "Mouses", "Auriculares"],
        },
        {
            "descripcion": "Semana tecnológica",
            "descuento_porcentaje": 20.00,
            "fecha_inicio": ahora,
            "fecha_fin": ahora + timedelta(days=10),
            "metodo_pago": MetodoPago.objects.filter(nomb_meto="PayPal").first(),
            "imagen_promocion": "promociones_imagenes/tecnologia.png",
            "productos": ["ASUS TUF Gaming F15", "Dell 27 4K USB-C Monitor"],
        },
    ]

    for promo in promociones_data:
        nueva_promocion, creada = Promocion.objects.get_or_create(
            descripcion=promo["descripcion"],
            defaults={
                "descuento_porcentaje": promo["descuento_porcentaje"],
                "fecha_inicio": promo["fecha_inicio"],
                "fecha_fin": promo["fecha_fin"],
                "metodo_pago": promo["metodo_pago"],
                "imagen_promocion": promo["imagen_promocion"],
            },
        )

        # Asociar categorías (si existen)
        if "categorias" in promo:
            categorias = Categoria.objects.filter(nomb_ca__in=promo["categorias"])
            nueva_promocion.categorias.add(*categorias)

        # Asociar productos (si existen)
        if "productos" in promo:
            productos = Producto.objects.filter(nomb_prod__in=promo["productos"])
            nueva_promocion.productos.add(*productos)

        if creada:
            print(f"✅ Promoción creada: {nueva_promocion.descripcion}")
        else:
            print(f"⚠️ Promoción ya existente: {nueva_promocion.descripcion}")

    print("🎉 Inserción de promociones completada correctamente.")

