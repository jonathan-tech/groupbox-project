from django.shortcuts import render, redirect
from django.urls import reverse_lazy #classed based
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall, Video
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse #from the ajax portion addvideo html
import urllib #we use this library to grab youtube id
from django.forms.utils import ErrorList #error if we cant find youtube id
import requests #for the url
from django.contrib.auth.decorators import login_required #apply this to functions that should require a login.
from django.contrib.auth.mixins import LoginRequiredMixin

YOUTUBE_API_KEY = 'AIzaSyC4WM5tcYNraIjlHFxBizRLLD6hQjRWask'
# Create your views here.
def home(request):
    recent_halls = Hall.objects.all().order_by('-id')[:3]
    popular_halls = Hall.objects.get(pk=1),Hall.objects.get(pk=2),Hall.objects.get(pk=3)
    return render(request, 'halls/home.html', {'recent_halls':recent_halls, 'popular_halls':popular_halls})

@login_required
def dashboard(request):
    #find all the hall objects for a particular user
    halls = Hall.objects.filter(user=request.user)
    return render(request, 'halls/dashboard.html', {'halls':halls})

@login_required
def add_video(request, pk):
    '''
    This function will add a video to our
    hall
    '''
    form = VideoForm()
    search_form = SearchForm()
    hall = Hall.objects.get(pk=pk)
    #if the all user and request user are different we dont want them to add a video
    if not hall.user == request.user:
        raise Http404 #error this is imported

    if request.method == 'POST':
        #create somthing
        #going to take all the post data and fill it in to the form
        form = VideoForm(request.POST)
        #will check if we have everything filled in
        if form.is_valid():
            video = Video()
            video.hall = hall
            #to get to its primed information
            #this is what the user submitted
            video.url = form.cleaned_data['url']
            #this is what we want to look at
            parsed_url = urllib.parse.urlparse(video.url)
            #this line of code is getting the v parameter in the url
            video_id =  urllib.parse.parse_qs(parsed_url.query).get('v')
            #To varify that we got the proper id
            if video_id:
                #returns a list
                video.youtube_id = video_id[0]
                # this is the url we got form the youtube api
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={ YOUTUBE_API_KEY }')
                #we want to turn it to a json object
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('detail_hall',pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a youtube url')


    return render(request, 'halls/add_video.html', {'form':form, 'search_form':search_form, 'hall':hall})

@login_required
def video_search(request):
    '''
    the user types in information
    passes over to this function
    we return the infor and display.

    what the user types goes from javascript
    over to server
    then sent back to the user interface

    '''
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={encoded_search_term}&key={YOUTUBE_API_KEY}')
        return JsonResponse(response.json())
    return JsonResponse({'error':'Not working'})

class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    '''
    The user is allowed delete a video
    '''
    model=Video #on the delete.html, it will pass the lowercase version of the model in this case 'hall'
    template_name= 'halls/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.hall.user == self.request.user:
            raise Http404
        return video


class SignUp(generic.CreateView):
    '''
    Creates a form and passes it
    to the template with name 'form'
    '''
    #this is what you need to create a user
    form_class = UserCreationForm
    #will send us bacj to home
    success_url = reverse_lazy('dashboard')
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


class CreateHall(LoginRequiredMixin, generic.CreateView):
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
        return redirect('dashboard')

class DetailHall(generic.DetailView):
    '''
    This way you only view the hall
    you cannot edit,update ect so
    there is no success_url
    '''
    model=Hall #on the detail.html, it will pass the lowercase version of the model in this case 'hall'
    template_name= 'halls/detail_hall.html'
    #no success b

class UpdateHall(LoginRequiredMixin, generic.UpdateView):
    '''
    The user is allowed to make changes
    the hall
    '''
    model=Hall #on the update.html, it will pass the lowercase version of the model in this case 'hall'
    template_name= 'halls/update_hall.html'
    fields=['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        hall = super(UpdateHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall

class DeleteHall(LoginRequiredMixin, generic.DeleteView):
    '''
    The user is allowed delete a hall
    '''
    model=Hall #on the delete.html, it will pass the lowercase version of the model in this case 'hall'
    template_name= 'halls/delete_hall.html'
    fields=['title']
    success_url = reverse_lazy('dashboard')
