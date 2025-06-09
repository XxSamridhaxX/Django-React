from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView



from .views import person_api_list,person_details



urlpatterns = [
    path('hello/',views.hellofunc,name='hello'),
    path('people/',views.people_list,name='people_list'),
    path('addPerson/',views.add_person,name='add_person'),
    path('editPerson/<int:pk>',views.edit_person,name="edit_person"),
    path('deletePerson/<int:pk>',views.delete_person,name="delete_person"),
    path('register/',views.register_user,name="register_user"),
    path('dashboard/',views.dashboard_view,name="dashboard"),

    # LoginView is a class that handles login and session.
    # as_view converts the class into callable function
    # the argument passed to as_view is a template that tells django where and how to render the login form
    path("login/",LoginView.as_view(template_name="blog/login.html"),name="login"),
    # template name expects html page
    path("logout/",LogoutView.as_view(next_page="register_user"),name="logout"),
    # while next_page expects a name of path to follow when you press logout


    # Api views
    path('api/people/',person_api_list,name='api_people'),
    path('api/people/<int:pk>/',person_details,name='api_people'),

    # a path for custom login
    path('api/login',views.custom_login,name="custom_login")
    
]