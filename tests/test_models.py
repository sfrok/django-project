from baseapp.models import Product


def test_models1():
    tmp = Product.objects.all()
    a = []
    for i in range(10):
        a.append(Product(id = i+1, name='Товар '+str(i+1), price=-1*i**2*1000, amount = 100-i*10))
        a[i].save()
        assert Product.objects.get(id=a[i].id), f"data failure, id={a[i].id}"
    assert Product.objects.get(id=999) != None, f"id failure, result exists"

    # Stashing changes
    Product.objects.clear()
    tmp.save()