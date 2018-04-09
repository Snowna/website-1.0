from django.shortcuts import render,get_object_or_404
from .models import Package
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, PackageForm

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    # connect to the database
    all_packages = Package.objects.all()
    return render(request, 'package/index.html', {'all_packages': all_packages})


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
            user = authenticate(username=username,password=password)

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
    return render(request, 'package/login.html', context)


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


def create_package(request):
    if not request.user.is_authenticated():
        return render(request, 'package/login.html')
    else:
        form = PackageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            package = form.save(commit=False)
            package.user = request.user
            package.album_logo = request.FILES['company_logo']
            file_type = package.company_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'package': package,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'package/create_package.html', context)
            package.save()
            return render(request, 'package/detail.html', {'package': package})
        context = {
            "form": form,
        }
        return render(request, 'package/create_package.html', context)