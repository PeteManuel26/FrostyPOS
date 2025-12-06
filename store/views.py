from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem, Category
from .cart import Cart

def product_list(request):
    products = Product.objects.all()
    return render(request, "store/products.html", {"products": products})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get("cart", {})

    current_qty = cart.get(str(product_id), 0)

    if current_qty < product.stock:
        cart[str(product_id)] = current_qty + 1
        request.session["cart"] = cart

    return redirect("cart")

def cart_view(request):
    cart = Cart(request)
    cart_items = list(cart.items())
    total = sum(item['line_total'] for item in cart_items)
    return render(request, "store/cart.html", {"cart_items": cart_items, "total": total})

def checkout(request):
    cart = Cart(request)
    items = list(cart.items())
    if not items:
        return redirect("products")

    order = Order.objects.create(total=0)
    total = 0
    for item in items:
        product = item['product']
        qty = item['qty']
        line_total = product.price * qty
        OrderItem.objects.create(order=order, product=product, qty=qty, line_total=line_total)
        product.stock -= qty
        product.save()
        total += line_total

    order.total = total
    order.save()
    cart.clear()
    return render(request, "store/receipt.html", {"order": order})

def scan_barcode(request):
    barcode = request.GET.get("barcode")
    cart = Cart(request)
    if barcode:
        product = Product.objects.filter(barcode=barcode).first()
        if product:
            cart.add(product.id, 1)
            return redirect("cart")
        else:
            return render(request, "store/not_found.html", {"barcode": barcode})
    return render(request,"store/scan_barcode.html")

def inventory(request):
    products = Product.objects.all()
    return render(request, "store/inventory.html", {"products": products})

def add_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        barcode = request.POST.get("barcode")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)

        Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            barcode=barcode,
            category=category
        )
        return redirect("inventory")

    categories = Category.objects.all()
    return render(request, "store/add_product.html", {"categories": categories})

def remove_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect("inventory")

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart")

def update_cart(request):
    if request.method == "POST":
        cart = request.session.get("cart", {})

        for product_id, qty in request.POST.items():
            if product_id.startswith("qty_"):
                pid = product_id.split("_")[1]
                qty = int(qty)
                if qty > 0:
                    cart[pid] = qty
                else:
                    cart.pop(pid, None)  # Remove if 0

        request.session["cart"] = cart

    return redirect("cart")