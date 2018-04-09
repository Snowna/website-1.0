from django.shortcuts import render,get_object_or_404
from .models import Package
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import  UserForm


def index(request):
    # connect to the database
    all_packages = Package.objects.all()
    return render(request, 'package/index.html', {'all_packages': all_packages})


def detail(request, package_id):
    #        package = Package.objects.get(pk=package_id)
    package = get_object_or_404(Package, pk=package_id)
    return render(request, 'package/detail.html', {'package': package})


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

