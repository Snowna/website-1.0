from django.shortcuts import render, get_object_or_404,redirect
from .models import Package
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, PackageForm
from django.db.models import Q
from django.http import JsonResponse


def index_v(request):
    # connect to the database
    if not request.user.is_authenticated:
        return render(request, 'package/index_v.html')
    else:
        packages = Package.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            packages = packages.filter(
                Q(package_type__contains__icontains=query) |
                Q(package_company__icontains=query)
            ).distinct()

            return render(request, 'package/index_v.html', {
                'packages': packages,
            })
        else:
            return render(request, 'package/index_v.html', {'packages': packages})


def index(request):
    # connect to the database
    if not request.user.is_authenticated:
        return render(request, 'package/login.html')
    else:
        packages = Package.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            packages = packages.filter(
                Q(package_type__contains__icontains=query) |
                Q(package_company__icontains=query)
            ).distinct()

            return render(request, 'package/index.html', {
                'packages': packages,
            })
        else:
            return render(request, 'package/index.html', {'packages': packages})


def detail(request, package_id):
    #        package = Package.objects.get(pk=package_id)
    package = get_object_or_404(Package, pk=package_id)
    return render(request, 'package/detail.html', {'package': package})


# this class is no value for this project
class UserFormView(View):
    form_class = UserForm
    template_name = 'package/register.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('package:index')
        return render(request, self.template_name, {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                packages = Package.objects.filter(user=request.user)
                return render(request, 'package/index.html', {'packages': packages})
            else:
                return render(request, 'package/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'package/login.html', {'error_message': 'Invalid login'})
    return render(request, 'package/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'package/index_v.html', context)


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                packages = Package.objects.filter(user=request.user)
                return render(request, 'package/index.html', {'packages': packages})
    context = {
        "form": form,
    }
    return render(request, 'package/register.html', context)


def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'package/login.html')
    else:
        packages = Package.objects.filter(user=request.user)
        return render(request, 'package/profile.html', {'packages': packages})


def create_package(request):
    if not request.user.is_authenticated:
        return render(request, 'package/login.html')
    else:
        form = PackageForm(request.POST or None)
        if form.is_valid():
            package = form.save(commit=False)
            package.user = request.user
            package.save()
            return render(request, 'package/detail.html', {'package': package})
        context = {
            "form": form,
        }
        return render(request, 'package/create_package.html', context)


def delete_package(request, package_id):
    package = Package.objects.get(pk=package_id)
    package.delete()
    packages = Package.objects.filter(user=request.user)
    return render(request, 'package/index.html', {'packages': packages})