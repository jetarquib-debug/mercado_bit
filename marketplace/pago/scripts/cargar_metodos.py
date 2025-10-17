from pago.models import MetodoPago

def insertar_metodos_pago():
    metodos = [
        ("Tarjeta de Crédito", "metodos_pago_imagenes/tarjeta_credito.png"),
        ("Tarjeta de Débito", "metodos_pago_imagenes/tarjeta_debito.png"),
        ("Yape", "metodos_pago_imagenes/yape.png"),
        ("Plin", "metodos_pago_imagenes/plin.png"),
        ("PayPal", "metodos_pago_imagenes/paypal.png"),
        ("Transferencia Bancaria", "metodos_pago_imagenes/transferencia.png"),
        ("Efectivo", "metodos_pago_imagenes/efectivo.png"),
    ]

    for nombre, imagen in metodos:
        MetodoPago.objects.get_or_create(
            nomb_meto=nombre,
            defaults={"imagen_metodo": imagen}
        )

    print("✅ Métodos de pago insertados correctamente.")
