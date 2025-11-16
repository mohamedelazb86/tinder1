from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required
def dashboard(request):
    return render(request,'dashboard/dashboard.html',{})


def index(request):
    return render(request,'index.html')