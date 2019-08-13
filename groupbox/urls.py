"""groupbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth #auth will auto add login logout views
from django.contrib.auth import views as auth_views
from django.urls import path
from halls import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name ='home'),
    #AUTH
    path('signup', views.SignUp.as_view(), name='signup'),
    #completely done
    path('login', auth_views.LoginView.as_view(), name='login'),
    #completeley done
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    #Halls
    #as_views() becouse its a class
    path('halloffame/create', views.CreateHall.as_view(), name='create_hall'),


]
#go and grab from our settings.py url and root. if someone does /static it will move to static directory
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)