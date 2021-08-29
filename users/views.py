from django.shortcuts import render, redirect
from .forms import UserOurRegistration

def register(request):
    if request.method == "POST":
        form = UserOurRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserOurRegistration()
    return render(request, 'users/registration.html', {'form': form})
