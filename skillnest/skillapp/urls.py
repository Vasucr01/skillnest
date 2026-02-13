from django.contrib import admin
from django.urls import path,include
from skillapp import views
urlpatterns = [
      
    path('',views.index,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_user,name='logout'),
    path('students/',views.students,name='students'),
    path('profile/',views.profile,name='profile'),
    path('init-admin/', views.init_admin, name='init_admin'),
    
    

]



