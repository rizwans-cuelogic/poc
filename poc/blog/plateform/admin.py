from django.contrib import admin

# Register your models here.



def forgotpass(request):
	return render(request,'plateform/forgotpass.html')