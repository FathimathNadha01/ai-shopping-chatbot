from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Order, OrderItem
import google.generativeai as genai
import os
import re


# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# In-memory cart (temporary)
cart = {}

@api_view(['POST'])
def chat(request):
    message = request.data.get("message", "").lower()

    # Show products
    if "show" in message or "list" in message:
        products = Product.objects.all()
        reply = "\n".join([f"{p.name} - ₹{p.price}" for p in products])
        return Response({"reply": reply})

    # Price queries
    if "price" in message or "cost" in message:
        for product in Product.objects.all():
            if product.name.lower() in message:
                return Response({
                    "reply": f"{product.name} costs ₹{product.price}"
                })
        #  Budget queries (under price)
    match = re.search(r'under\s*(\d+)', message.replace("?", ""))

    if match:
        budget = int(match.group(1))
        products = Product.objects.filter(price__lte=budget)

        if products.exists():
            reply = "\n".join(
                [f"{p.name} - ₹{p.price}" for p in products]
            )
            return Response({"reply": reply})
        else:
            return Response({"reply": "❌ No products in this budget"})


    #  Add product to cart
    if "add" in message:
        for product in Product.objects.all():
            if product.name.lower() in message:
                cart[product] = cart.get(product, 0) + 1
                return Response({
                    "reply": f"🛒 {product.name} added to cart ,Anything else?"
                })

        return Response({
            "reply": "❌ Please specify a product name (Backpack, Headphones, Smart Watch)"
        })

    #  Checkout → SAVE ORDER TO DATABASE 
    if "checkout" in message:
        if not cart:
            return Response({"reply": "🛑 Cart is empty"})

        total_price = sum(
            product.price * quantity
            for product, quantity in cart.items()
        )

        # Create Order
        order = Order.objects.create(
            total_price=total_price,
            status="confirmed"
        )

        # Create Order Items
        for product, quantity in cart.items():
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        cart.clear()

        return Response({
            "reply": f"✅ Order confirmed!\nOrder ID: {order.id}\nTotal: ₹{total_price}"
        })

    #  Gemini AI fallback
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    ai_reply = model.generate_content(message)

    return Response({"reply": ai_reply.text})
