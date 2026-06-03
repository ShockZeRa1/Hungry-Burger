from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Custom login view that provides specific error messages to determine whether username or password was incorrectly entered
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next", "menu"))
            else:
                error = "Incorrect password, please try again."
            
        except User.DoesNotExist:
            error = f"The username '{username}' was not found in our records. Sign up if you haven't."

        return render(request, "account/login.html", {
            "username": username,
            "error": error
        })

    return render(request, "account/login.html")