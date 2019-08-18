from django.shortcuts import render, redirect
from django.urls import reverse_lazy #classed based
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm
# Create your views here.
def home(request):
    return render(request, 'halls/home.html')

def dashboard(request):
    return render(request, 'halls/dashboard.html')

def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()

    if request.method == 'POST':
        #create somthing
        #going to take all the post data and fill it in to the form
        filled_form = VideoForm(request.POST)
        #will check if we have everything filled in
        if filled_form.is_valid():
            video = Video()
            #to get to its primed information
            video.url = filled_form.cleaned_data['url']
            video.title = filled_form.cleaned_data['title']
            video.youtube_id = filled_form.cleaned_data['youtube_id']
            video.hall = Hall.objects.get(pk=pk)
            video.save()


    return render(request, 'halls/add_video.html', {'form':form, 'search_form':search_form})


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

    def form_valid(self, form):
        '''
        When the user signups up this code
        will automaticaly sign them in
        '''
        #we validate the signup process
        view = super(SignUp, self).form_valid(form)
        #just before we show the view lets sign the user in
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request,user)
        return view


class CreateHall(generic.CreateView):
    '''
    This is where we are imporing
    create view code to make a new
    class
    '''
    model=Hall
    fields=['title']
    template_name= 'halls/create_hall.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        '''
        Will check if the form is good to go
        '''
        #will go get the user object
        form.instance.user = self.request.user
        #will validate user
        super(CreateHall, self).form_valid(form)
        return redirect('home')

class DetailHall(generic.DetailView):
    '''
    This way you only view the hall
    you cannot edit,update ect so
    there is no success_url
    '''
    model=Hall #on the detail.html, it will pass the lowercase version of the model in this case 'hall'
    template_name= 'halls/detail_hall.html'
    #no success b

class UpdateHall(generic.UpdateView):
    '''
    The user is allowed to make changes
    the hall
    '''
    model=Hall #on the update.html, it will pass the lowercase version of the model in this case 'hall'
    template_name= 'halls/update_hall.html'
    fields=['title']
    success_url = reverse_lazy('dashboard')

class DeleteHall(generic.DeleteView):
    '''
    The user is allowed delete a hall
    '''
    model=Hall #on the delete.html, it will pass the lowercase version of the model in this case 'hall'
    template_name= 'halls/delete_hall.html'
    fields=['title']
    success_url = reverse_lazy('dashboard')
