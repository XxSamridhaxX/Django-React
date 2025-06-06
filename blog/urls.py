from django.urls import path
from . import views

urlpatterns = [
    path('hello/',views.hellofunc,name='hello'),
    path('people/',views.people_list,name='people_list'),
    path('addPerson/',views.add_person,name='add_person'),
    path('editPerson/<int:pk>',views.edit_person,name="edit_person"),
    path('deletePerson/<int:pk>',views.delete_person,name="delete_person"),
    path('register/',views.register_user,name="register_user"),
    path('dashboard/',views.dashboard_view,name="dashboard"),
]