from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

# Create your views here.
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from haytunes.forms import SignUpForm, ProfileForm, UserForm
from haytunes.models import Category, Product


def index(request):
    products_audio = Product.objects.filter(type='a')[:6]
    products_video = Product.objects.filter(type='v')[:6]
    products_image = Product.objects.filter(type='i')[:6]
    context = {'products_audio': products_audio, 'products_video': products_video, 'products_image': products_image}

    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    return render(request, 'haytunes/profile.html')


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        #profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            #profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        #profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'haytunes/update_profile.html', {
        'user_form': user_form,
        #'profile_form': profile_form
    })


class CategoryListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'haytunes.can_admin_content'
    model = Category


class CategoryDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'haytunes.can_admin_content'
    model = Category


class CategoryCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'haytunes.can_admin_content'
    model = Category
    fields = '__all__'


class CategoryUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'haytunes.can_admin_content'
    model = Category
    fields = '__all__'


class CategoryDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'haytunes.can_admin_content'
    model = Category
    success_url = reverse_lazy('categories')


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10


class ProductDetailView(generic.DetailView):
    model = Product


class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'haytunes.can_admin_content'
    model = Product
    fields = ['title', 'price', 'author', 'type', 'category', 'owner', 'content']


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'haytunes.can_admin_content'
    model = Product
    fields = ['title', 'price', 'author', 'type', 'category', 'owner', 'content']


class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'haytunes.can_admin_content'
    model = Product
    success_url = reverse_lazy('products')
