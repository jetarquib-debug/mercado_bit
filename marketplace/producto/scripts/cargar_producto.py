
from django.utils import timezone
from tienda.models import Tienda
from producto.models import Marca, Categoria, Producto, ImagenProducto


def insertar_productos():
    # --- Marcas ---
    marcas_data = [
        ("ASUS", "marcas_imagenes/asus.png"),
        ("HP", "marcas_imagenes/hp.png"),
        ("Lenovo", "marcas_imagenes/lenovo.png"),
        ("Acer", "marcas_imagenes/acer.png"),
        ("Apple", "marcas_imagenes/apple.png"),
        ("Samsung", "marcas_imagenes/samsung.png"),
        ("Dell", "marcas_imagenes/dell.png"),
        ("MSI", "marcas_imagenes/msi.png"),
        ("Logitech", "marcas_imagenes/logitech.png"),
        ("Razer", "marcas_imagenes/razer.png"),
    ]

    marcas = {}
    for nombre, img in marcas_data:
        marca, _ = Marca.objects.get_or_create(
            nomb_marca=nombre,
            defaults={"imagen_marca": img}
        )
        marcas[nombre] = marca

    # --- Categorías ---
    categorias_data = [
        ("Laptops", "Portátiles de alto rendimiento para trabajo o gaming."),
        ("Monitores", "Pantallas de distintas resoluciones y tamaños."),
        ("Teclados", "Teclados mecánicos, inalámbricos y más."),
        ("Mouses", "Ratones ópticos y gamer."),
        ("Auriculares", "Headsets y audífonos con micrófono."),
        ("Tablets", "Tablets Android y iPad."),
        ("Componentes", "Tarjetas gráficas, RAM, procesadores."),
        ("Almacenamiento", "Discos duros y SSD."),
        ("Accesorios", "Fundas, cables, cargadores."),
        ("Impresoras", "Impresoras láser y multifuncionales."),
    ]

    categorias = {}
    for nombre, desc in categorias_data:
        cat, _ = Categoria.objects.get_or_create(
            nomb_ca=nombre,
            defaults={"descripcion": desc, "imagen_categoria": f"categorias_imagenes/{nombre.lower()}.png"}
        )
        categorias[nombre] = cat

    # --- Tienda base ---
    tienda = Tienda.objects.first()
    if not tienda:
        print("⚠️ No hay ninguna tienda registrada. Inserta una tienda antes de ejecutar este script.")
        return

    # --- Productos ---
    productos_data = [
        {"nomb_prod": "ASUS TUF Gaming F15", "marca": "ASUS", "categorias": ["Laptops"], "precio": 4599.90, "stock": 12, "estado": "disponible", "imagen": "productos_imagenes/asus_tuf_f15.jpg"},
        {"nomb_prod": "HP Pavilion x360", "marca": "HP", "categorias": ["Laptops"], "precio": 3899.00, "stock": 8, "estado": "disponible", "imagen": "productos_imagenes/hp_x360.jpg"},
        {"nomb_prod": "Lenovo IdeaPad 3", "marca": "Lenovo", "categorias": ["Laptops"], "precio": 2999.90, "stock": 15, "estado": "disponible", "imagen": "productos_imagenes/lenovo_ideapad3.jpg"},
        {"nomb_prod": "Acer Nitro 5", "marca": "Acer", "categorias": ["Laptops"], "precio": 4799.00, "stock": 5, "estado": "disponible", "imagen": "productos_imagenes/acer_nitro5.jpg"},
        {"nomb_prod": "Apple MacBook Air M2", "marca": "Apple", "categorias": ["Laptops"], "precio": 6499.00, "stock": 7, "estado": "disponible", "imagen": "productos_imagenes/macbook_air_m2.jpg"},
        {"nomb_prod": "Samsung Galaxy Book3", "marca": "Samsung", "categorias": ["Laptops"], "precio": 4899.00, "stock": 10, "estado": "disponible", "imagen": "productos_imagenes/samsung_book3.jpg"},
        {"nomb_prod": "Dell Inspiron 14", "marca": "Dell", "categorias": ["Laptops"], "precio": 3799.00, "stock": 9, "estado": "disponible", "imagen": "productos_imagenes/dell_inspiron14.jpg"},
        {"nomb_prod": "MSI Katana GF76", "marca": "MSI", "categorias": ["Laptops"], "precio": 5299.00, "stock": 6, "estado": "disponible", "imagen": "productos_imagenes/msi_gf76.jpg"},
        {"nomb_prod": "Logitech G Pro X", "marca": "Logitech", "categorias": ["Auriculares"], "precio": 599.00, "stock": 20, "estado": "disponible", "imagen": "productos_imagenes/logitech_gpro_x.jpg"},
        {"nomb_prod": "Razer BlackShark V2", "marca": "Razer", "categorias": ["Auriculares"], "precio": 629.00, "stock": 14, "estado": "disponible", "imagen": "productos_imagenes/razer_blacksharkv2.jpg"},
        {"nomb_prod": "ASUS ROG Swift 27\"", "marca": "ASUS", "categorias": ["Monitores"], "precio": 1899.00, "stock": 5, "estado": "disponible"},
        {"nomb_prod": "Samsung Odyssey G5", "marca": "Samsung", "categorias": ["Monitores"], "precio": 1699.00, "stock": 8, "estado": "disponible"},
        {"nomb_prod": "Dell UltraSharp 24\"", "marca": "Dell", "categorias": ["Monitores"], "precio": 999.00, "stock": 9, "estado": "disponible"},
        {"nomb_prod": "Logitech G915 TKL", "marca": "Logitech", "categorias": ["Teclados"], "precio": 749.00, "stock": 13, "estado": "disponible"},
        {"nomb_prod": "Razer Huntsman Mini", "marca": "Razer", "categorias": ["Teclados"], "precio": 599.00, "stock": 10, "estado": "disponible"},
        {"nomb_prod": "Logitech G Pro Wireless", "marca": "Logitech", "categorias": ["Mouses"], "precio": 499.00, "stock": 25, "estado": "disponible"},
        {"nomb_prod": "Razer DeathAdder V2", "marca": "Razer", "categorias": ["Mouses"], "precio": 419.00, "stock": 18, "estado": "disponible"},
        {"nomb_prod": "Crucial P3 1TB SSD", "marca": "Dell", "categorias": ["Almacenamiento"], "precio": 379.00, "stock": 40, "estado": "disponible"},
        {"nomb_prod": "Kingston NV2 500GB", "marca": "HP", "categorias": ["Almacenamiento"], "precio": 249.00, "stock": 35, "estado": "disponible"},
        {"nomb_prod": "Seagate Barracuda 2TB", "marca": "Lenovo", "categorias": ["Almacenamiento"], "precio": 299.00, "stock": 22, "estado": "disponible"},
        {"nomb_prod": "Corsair Vengeance 16GB DDR5", "marca": "ASUS", "categorias": ["Componentes"], "precio": 459.00, "stock": 25, "estado": "disponible"},
        {"nomb_prod": "MSI GeForce RTX 4060 Ti", "marca": "MSI", "categorias": ["Componentes"], "precio": 2499.00, "stock": 6, "estado": "disponible"},
        {"nomb_prod": "Intel Core i7-13700K", "marca": "Dell", "categorias": ["Componentes"], "precio": 2199.00, "stock": 10, "estado": "disponible"},
        {"nomb_prod": "AMD Ryzen 7 7800X3D", "marca": "ASUS", "categorias": ["Componentes"], "precio": 2299.00, "stock": 7, "estado": "disponible"},
        {"nomb_prod": "HP DeskJet 2720e", "marca": "HP", "categorias": ["Impresoras"], "precio": 399.00, "stock": 15, "estado": "disponible"},
        {"nomb_prod": "Canon PIXMA G3110", "marca": "Lenovo", "categorias": ["Impresoras"], "precio": 649.00, "stock": 8, "estado": "disponible"},
        {"nomb_prod": "Epson EcoTank L3250", "marca": "Acer", "categorias": ["Impresoras"], "precio": 779.00, "stock": 10, "estado": "disponible"},
        {"nomb_prod": "Logitech C920 HD Pro", "marca": "Logitech", "categorias": ["Accesorios"], "precio": 349.00, "stock": 22, "estado": "disponible"},
        {"nomb_prod": "Razer Mouse Bungee V3", "marca": "Razer", "categorias": ["Accesorios"], "precio": 199.00, "stock": 30, "estado": "disponible"},
        {"nomb_prod": "Samsung Galaxy Tab S9", "marca": "Samsung", "categorias": ["Tablets"], "precio": 3599.00, "stock": 12, "estado": "disponible"},
        {"nomb_prod": "Apple iPad Air 5", "marca": "Apple", "categorias": ["Tablets"], "precio": 3799.00, "stock": 9, "estado": "disponible"},
        {"nomb_prod": "Lenovo Tab P11 Pro", "marca": "Lenovo", "categorias": ["Tablets"], "precio": 2899.00, "stock": 14, "estado": "disponible"},
        {"nomb_prod": "Acer Iconia One 10", "marca": "Acer", "categorias": ["Tablets"], "precio": 1499.00, "stock": 10, "estado": "disponible"},
        {"nomb_prod": "ASUS Prime B650M-A", "marca": "ASUS", "categorias": ["Componentes"], "precio": 899.00, "stock": 10, "estado": "disponible"},
        {"nomb_prod": "MSI MPG A850G PSU", "marca": "MSI", "categorias": ["Componentes"], "precio": 599.00, "stock": 15, "estado": "disponible"},
        {"nomb_prod": "Razer Goliathus Chroma", "marca": "Razer", "categorias": ["Accesorios"], "precio": 259.00, "stock": 20, "estado": "disponible"},
        {"nomb_prod": "Logitech MX Master 3S", "marca": "Logitech", "categorias": ["Mouses"], "precio": 599.00, "stock": 16, "estado": "disponible"},
        {"nomb_prod": "Samsung Portable SSD T7 1TB", "marca": "Samsung", "categorias": ["Almacenamiento"], "precio": 529.00, "stock": 25, "estado": "disponible"},
        {"nomb_prod": "Apple Magic Keyboard", "marca": "Apple", "categorias": ["Teclados"], "precio": 849.00, "stock": 10, "estado": "disponible"},
        {"nomb_prod": "HP X1000 Wired Mouse", "marca": "HP", "categorias": ["Mouses"], "precio": 59.00, "stock": 50, "estado": "disponible"},
        {"nomb_prod": "Dell Pro Wireless Keyboard", "marca": "Dell", "categorias": ["Teclados"], "precio": 299.00, "stock": 20, "estado": "disponible"},
        {"nomb_prod": "MSI Optix G32C4", "marca": "MSI", "categorias": ["Monitores"], "precio": 1499.00, "stock": 8, "estado": "disponible"},
        {"nomb_prod": "Acer Predator XB283K", "marca": "Acer", "categorias": ["Monitores"], "precio": 2299.00, "stock": 6, "estado": "disponible"},
        {"nomb_prod": "Razer Kraken X Lite", "marca": "Razer", "categorias": ["Auriculares"], "precio": 299.00, "stock": 22, "estado": "disponible"},
        {"nomb_prod": "Logitech G733 Lightspeed", "marca": "Logitech", "categorias": ["Auriculares"], "precio": 699.00, "stock": 12, "estado": "disponible"},
        {"nomb_prod": "ASUS ZenScreen MB16AC", "marca": "ASUS", "categorias": ["Monitores"], "precio": 999.00, "stock": 7, "estado": "disponible"},
        {"nomb_prod": "HP ENVY Inspire 7220e", "marca": "HP", "categorias": ["Impresoras"], "precio": 749.00, "stock": 10, "estado": "disponible"},
        {"nomb_prod": "Apple AirPods Pro 2", "marca": "Apple", "categorias": ["Auriculares"], "precio": 1299.00, "stock": 11, "estado": "disponible"},
        {"nomb_prod": "Dell 27 4K USB-C Monitor", "marca": "Dell", "categorias": ["Monitores"], "precio": 1899.00, "stock": 6, "estado": "disponible"},
        {"nomb_prod": "Samsung 980 PRO NVMe 2TB", "marca": "Samsung", "categorias": ["Almacenamiento"], "precio": 899.00, "stock": 12, "estado": "disponible"},
        {"nomb_prod": "Lenovo Legion M600 Wireless", "marca": "Lenovo", "categorias": ["Mouses"], "precio": 369.00, "stock": 14, "estado": "disponible"},
        {"nomb_prod": "MSI MAG CoreLiquid 240R", "marca": "MSI", "categorias": ["Componentes"], "precio": 699.00, "stock": 10, "estado": "disponible"},
    ]

    for p in productos_data:
        producto, _ = Producto.objects.get_or_create(
            nomb_prod=p["nomb_prod"],
            tienda=tienda,
            defaults={
                "descripcion": f"{p['nomb_prod']} de la marca {p['marca']}.",
                "precio": p["precio"],
                "stock": p["stock"],
                "estado": p["estado"],
                "marca": marcas[p["marca"]],
                "peso": 1.5,
            }
        )
        producto.categoria.set([categorias[c] for c in p["categorias"]])

        # Crear imagen principal si no existe
        ImagenProducto.objects.get_or_create(
            producto=producto,
            es_principal=True,
            defaults={"imagen": p.get("imagen", "productos_imagenes/default_producto.png")}
        )

    print("✅ Se insertaron marcas, categorías y productos con éxito.")
