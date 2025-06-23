from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import DemoModel

@csrf_exempt  
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if name and email and address and phone:
            DemoModel.objects.create(name=name, email=email, address=address, phone=phone)
        return redirect('index') 

    data = DemoModel.objects.all()
    return render(request, 'index.html', {'data': data})



def delete_record(request, record_id):
    instance = get_object_or_404(DemoModel, id=record_id)
    instance.delete()
    return redirect('index')