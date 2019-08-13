from django.shortcuts import render
from django.urls import reverse_lazy #classed based
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Hall
# Create your views here.
def home(request):
    return render(request, 'halls/home.html')

class SignUp(generic.CreateView):
    '''
    Creates a form and passes it
    to the template with name 'form'
    '''
    #this is what you need to create a user
    form_class = UserCreationForm
    #will send us bacj to home
    success_url = reverse_lazy('home')
    #Driects to the signup page, we use 'form.as_p' for paragraph form to look cleaner
    template_name = 'registration/signup.html'

class CreateHall(generic.CreateView):
    '''
    This is where we are imporing
    create view code to make a new
    class
    '''
    model=Hall
    fields=['title']
    template_name= 'halls/create_hall.html'
    success_url = reverse_lazy('home')
