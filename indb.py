from product import Product

def generate_product():
    list_products=[]

    for x in range(10):
        p = Product(name=f"Product {x+1}",price=4.9 * x)
        list_products.append(p)

    return list_products