from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.filter(product=product)

    # Clear data of session
    # product.is_review_exist = False
    # request.session['reviewed_products'] = []

    reviewed_products = request.session.get('reviewed_products')
    if reviewed_products is not None:
        if product.id in reviewed_products:
            product.is_review_exist = True
        else:
            product.is_review_exist = False
    else:
        product.is_review_exist = False
        request.session['reviewed_products'] = []

    if request.method == 'POST' and not product.is_review_exist:
        form = ReviewForm(request.POST)

        if form.is_valid():
            frm = form.save(commit=False)
            frm.product = product
            frm.user = request.user

            # Add to session
            request.session['reviewed_products'].append(product.id)
            product.is_review_exist = True
            request.session.modified = True

            frm.save()
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
    }

    return render(request, template, context)
