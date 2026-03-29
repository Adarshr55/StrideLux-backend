from django.core.management.base import BaseCommand
from products.models import Category, Product, ProductImage, Size


class Command(BaseCommand):
    help = 'Seed products from JSON data'

    def handle(self, *args, **kwargs):

        products_data = [
            {
                "name": "Classic Leather Loafers",
                "brand": "Urban Outfitters",
                "category": "men",
                "description": "A timeless classic, these loafers are crafted from genuine leather and feature a stylish, modern fit. Perfect for any occasion, offering both comfort and durability.",
                "rating": 4.5,
                "price": 189.9,
                "stock": 15,
                "thumbnail": "images/1.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": ["images/img1.2.png", "images/img1.3.png"]
            },
            {
                "name": "Air Zoom Pegasus",
                "brand": "Nike",
                "category": "sports",
                "description": "Engineered for performance, these running shoes provide excellent cushioning and support. The lightweight design and breathable mesh upper make them ideal for long-distance runs.",
                "rating": 4.8,
                "price": 123,
                "stock": 30,
                "thumbnail": "images/2.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": ["images/img2.3.png"]
            },
            {
                "name": "Floral Print Espadrilles",
                "brand": "Zara",
                "category": "women",
                "description": "Embrace the summer with these beautiful floral espadrilles. Made from lightweight canvas, they feature a flattering silhouette and a vibrant print. Perfect for casual outings.",
                "rating": 4.6,
                "price": 69.9,
                "stock": 25,
                "thumbnail": "images/3.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": ["images/img3.1.png", "images/img3.2.png"]
            },
            {
                "name": "Light-Up Graphic Sneakers",
                "brand": "Gap",
                "category": "kids",
                "description": "Let your kids show off their personality with these fun light-up sneakers. Made from durable materials, they're perfect for everyday play. The vibrant graphics are a hit!",
                "rating": 4.2,
                "price": 39.99,
                "stock": 51,
                "thumbnail": "images/4.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": ["images/img4.2.png", "images/img4.1.png"]
            },
            {
                "name": "Cap-Toe Oxford Shoes",
                "brand": "Hugo Boss",
                "category": "men",
                "description": "Make a statement with these impeccably crafted formal Oxfords. Made from premium calfskin leather, they feature a slim profile and classic cap-toe design.",
                "rating": 4.9,
                "price": 398,
                "stock": 10,
                "thumbnail": "images/5.jpg",
                "isActive": False,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": ["images/img1.2.png", "images/img1.3.png"]
            },
            {
                "name": "Blissfeel Training Shoes",
                "brand": "Lululemon",
                "category": "women",
                "description": "Experience ultimate comfort and flexibility with these high-performance training shoes. Designed for running and workouts, they offer a supportive, cushioned feel.",
                "rating": 4.9,
                "price": 148,
                "stock": 40,
                "thumbnail": "images/6.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": ["images/img5.1.png", "images/img5.2.png"]
            },
            {
                "name": "Canvas High-Top Sneakers",
                "brand": "Levi's",
                "category": "kids",
                "description": "A wardrobe essential for every kid, these canvas high-tops are both stylish and durable. They feature a classic design with a sturdy rubber sole. Perfect for school or play.",
                "rating": 4.7,
                "price": 49.5,
                "stock": 35,
                "thumbnail": "images/7.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": ["images/img6.1.png", "images/im6.2.png"]
            },
            {
                "name": "Ultraboost 1.0 Shoes",
                "brand": "Adidas",
                "category": "sports",
                "description": "Stay comfortable and energized with these versatile running shoes. The adidas BOOST midsole provides incredible energy return, perfect for runs or casual wear.",
                "rating": 4.6,
                "price": 180,
                "stock": 20,
                "thumbnail": "images/8.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": ["images/img8.1.png"]
            },
            {
                "name": "Crystal-Embellished Stilettos",
                "brand": "Vera Wang",
                "category": "women",
                "description": "Turn heads with these stunning evening stilettos. The elegant design features intricate crystal beading and a slim, high heel. The perfect choice for any formal occasion.",
                "rating": 5,
                "price": 850,
                "stock": 5,
                "thumbnail": "images/9.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Suede Classic Sneakers",
                "brand": "Puma",
                "category": "kids",
                "description": "These stylish and comfortable suede sneakers are perfect for active kids. The durable construction and cushioned insole provide all-day support. A timeless design.",
                "rating": 4.4,
                "price": 55,
                "stock": 60,
                "thumbnail": "images/10.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Canvas Deck Shoes",
                "brand": "Tommy Hilfiger",
                "category": "men",
                "description": "A versatile addition to any wardrobe, these canvas deck shoes are perfect for a relaxed yet polished look. Features classic boat-shoe lacing and the iconic Tommy logo.",
                "rating": 4.4,
                "price": 79.5,
                "stock": 22,
                "thumbnail": "images/11.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Jet Set Logo Sneakers",
                "brand": "Michael Kors",
                "category": "women",
                "description": "Accessorize in style with these elegant logo-print sneakers. Crafted from high-quality materials, they feature gold-tone hardware and a comfortable, modern silhouette.",
                "rating": 4.8,
                "price": 165,
                "stock": 18,
                "thumbnail": "images/12.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Cozy Critter Slippers",
                "brand": "Carter's",
                "category": "kids",
                "description": "Ensure a comfortable night with these adorable critter slippers. Made from ultra-soft plush, they feature a fun 3D animal face and a non-slip sole.",
                "rating": 4.7,
                "price": 24.99,
                "stock": 45,
                "thumbnail": "images/13.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "HOVR Phantom Running Shoes",
                "brand": "Under Armour",
                "category": "sports",
                "description": "Dominate your run with these high-performance running shoes. The HOVR cushioning provides a zero gravity feel to maintain energy return and help eliminate impact.",
                "rating": 4.7,
                "price": 140,
                "stock": 28,
                "thumbnail": "images/14.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Classic Check Rain Boots",
                "brand": "Burberry",
                "category": "women",
                "description": "A timeless icon of British style, these rain boots are a must-have. Made from waterproof rubber, they feature the classic check pattern and a comfortable fit.",
                "rating": 4.9,
                "price": 420,
                "stock": 8,
                "thumbnail": "images/15.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Killshot 2 Sneakers",
                "brand": "J.Crew",
                "category": "men",
                "description": "The perfect blend of casual and smart, these iconic sneakers are a wardrobe staple. Based on an original 70s design, they feature a mix of leather and suede.",
                "rating": 4.5,
                "price": 98,
                "stock": 32,
                "thumbnail": "images/16.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Original Tall Rain Boots",
                "brand": "Hunter",
                "category": "kids",
                "description": "Keep little feet dry and happy with these iconic rain boots. Handcrafted from natural rubber, they are fully waterproof and feature a comfortable, non-slip sole.",
                "rating": 4.8,
                "price": 65,
                "stock": 40,
                "thumbnail": "images/17.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Classic Suede Moccasins",
                "brand": "UGG",
                "category": "women",
                "description": "Protect your feet in style with these classic suede moccasins. The timeless design features a plush wool lining and a durable sole for indoor/outdoor wear.",
                "rating": 4.7,
                "price": 100,
                "stock": 35,
                "thumbnail": "images/18.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Leather Chukka Boots",
                "brand": "Clarks",
                "category": "men",
                "description": "A perfect blend of classic design and modern functionality, these chukka boots are a stylish accessory. They feature a durable suede upper and a comfortable crepe sole.",
                "rating": 4.6,
                "price": 150,
                "stock": 20,
                "thumbnail": "images/19.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "LEGO x Adidas Sneakers",
                "brand": "Adidas",
                "category": "kids",
                "description": "Spark creativity and imagination with this engaging LEGO-themed sneaker. With colorful, brick-inspired details, the possibilities for fun are endless.",
                "rating": 4.9,
                "price": 65,
                "stock": 55,
                "thumbnail": "images/20.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Salutation Training Shoes",
                "brand": "Athleta",
                "category": "women",
                "description": "Designed for the active woman, these shoes are perfect for yoga, studio, or the gym. The seamless construction and breathable fabric provide ultimate comfort and support.",
                "rating": 4.6,
                "price": 129,
                "stock": 38,
                "thumbnail": "images/21.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Moab Waterproof Hikers",
                "brand": "Merrell",
                "category": "men",
                "description": "Conquer any trail with these durable and comfortable hiking boots. The waterproof leather upper keeps your feet dry, while the rugged outsole provides excellent grip.",
                "rating": 4.8,
                "price": 140,
                "stock": 25,
                "thumbnail": "images/22.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Classic Old Skool Sneakers",
                "brand": "Vans",
                "category": "kids",
                "description": "Get ready for school with this durable and spacious backpack. It features multiple compartments to keep books and supplies organized, padded shoulder straps for comfort.",
                "rating": 4.7,
                "price": 45,
                "stock": 50,
                "thumbnail": "images/23.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Heeled Leather Ankle Boots",
                "brand": "Steve Madden",
                "category": "women",
                "description": "A perfect-fitting pair of ankle boots is a wardrobe essential. These are crafted from premium leather and hug your ankle for a flattering silhouette.",
                "rating": 4.7,
                "price": 139.95,
                "stock": 30,
                "thumbnail": "images/24.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Vaughn Canvas Sneakers",
                "brand": "Ralph Lauren",
                "category": "men",
                "description": "A timeless classic, this canvas sneaker is the epitome of preppy style. Made from soft, breathable canvas, it features the iconic polo player logo.",
                "rating": 4.6,
                "price": 75,
                "stock": 40,
                "thumbnail": "images/25.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Waterproof Play Sandals",
                "brand": "Keen",
                "category": "kids",
                "description": "Protect your child's feet with these stylish and effective water sandals. They offer UPF 50+ sun protection and are made from a lightweight, quick-dry fabric.",
                "rating": 4.9,
                "price": 49.99,
                "stock": 51,
                "thumbnail": "images/26.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Ghost 15 Running Shoes",
                "brand": "Brooks",
                "category": "sports",
                "description": "Enjoy a comfortable and unrestricted run with these lightweight running shoes. The DNA LOFT v2 cushioning and built-in liner provide comfort and support.",
                "rating": 4.8,
                "price": 140,
                "stock": 33,
                "thumbnail": "images/27.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Ohana Leather Flip-Flops",
                "brand": "OluKai",
                "category": "men",
                "description": "Make a splash in these stylish and comfortable flip-flops. Made from water-resistant synthetic leather, they feature a compression-molded EVA midsole.",
                "rating": 4.7,
                "price": 75,
                "stock": 28,
                "thumbnail": "images/28.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Chuck Taylor",
                "brand": "Converse",
                "category": "kids",
                "description": "A classic high-top sneaker that provides hours of fun. This shoe encourages self-expression and friendly competition. Perfect for school, parties, or a rainy day indoors.",
                "rating": 4.6,
                "price": 40,
                "stock": 60,
                "thumbnail": "images/29.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Pointed-Toe Ballet Flats",
                "brand": "Ann Taylor",
                "category": "women",
                "description": "A sophisticated and versatile ballet flat that is perfect for the office. The elegant design features a flattering pointed toe and is made from a luxurious, easy-care material.",
                "rating": 4.5,
                "price": 118,
                "stock": 35,
                "thumbnail": "images/30.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Boots Formal",
                "brand": "Nike",
                "category": "men",
                "description": "wqedca xaswdeFWegthyyfgtdsaAZXSdzsfx",
                "rating": 4.2,
                "price": 12,
                "stock": 10,
                "thumbnail": "images/31.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Classic Clogs",
                "brand": "Crocs",
                "category": "kids",
                "description": "Unleash your child's inner artist with these deluxe, colorful clogs. They feature a comfortable footbed and ventilation ports for breathability.",
                "rating": 4.0,
                "price": 130,
                "stock": 15,
                "thumbnail": "images/32.jpg",
                "isActive": False,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
            {
                "name": "Sport Shoes",
                "brand": "Nike",
                "category": "sports",
                "description": "Keeps you running long time.",
                "rating": 3.5,
                "price": 123,
                "stock": 20,
                "thumbnail": "images/33.jpg",
                "isActive": True,
                "sizes": ["6", "7", "8", "9", "10"],
                "images": []
            },
        ]

        # clear old data
        self.stdout.write("Clearing old data...")
        Size.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING("Old data cleared."))

        for item in products_data:

            # get or create category
            category, _ = Category.objects.get_or_create(
                name=item['category'].lower()
            )

            # create product
            product = Product.objects.create(
                name=item['name'],
                brand=item['brand'],
                category=category,
                description=item['description'],
                price=float(item['price']),
                stock=int(item['stock']),
                rating=float(item['rating']),
                thumbnail=item['thumbnail'],
                is_active=item.get('isActive', True),
            )

            # create sizes
            for size in item.get('sizes', []):
                Size.objects.create(product=product, size=size)

            # create images
            for image_path in item.get('images', []):
                ProductImage.objects.create(
                    product=product,
                    image=image_path
                )

            self.stdout.write(
                self.style.SUCCESS(f'✓ {product.name}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Done! {len(products_data)} products seeded.')
        )
