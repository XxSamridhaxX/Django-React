from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Person,User
from .forms import PersonForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.




# TODO: Serializers imports
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PersonSerializer
from rest_framework import status


def hellofunc(request):
    context= {
        'name': 'John',
        'age': 30,
    }
    return render(request,'blog/hello.html',context)

@login_required
def people_list(request):
    peoples= Person.objects.filter(user=request.user)
    return render(request,'blog/people.html',{'peoples':peoples})

@login_required
def add_person(request):
    if request.method=="POST":
        form= PersonForm(request.POST)
        # form is a python object and requset.POST contains all the data that came through POST method and PersonForm creates raw data into objects
        if form.is_valid():
            # form is valid like fields are filled
            # is the datatype right
            # are there any validation rules broken
            person=form.save(commit=False)
            # form.save() le model ko instace banaucha
            person.user=request.user
            person.save()
            messages.success(request,"Person added successfully!")
            # save data into database
            return redirect('people_list')
    else:
            form=PersonForm()
    return render(request, 'blog/add_person.html', {'form':form,
                                                  'title':'Add Person',
                                                  'button_name':'ADD PERSON'})

@login_required
def edit_person(request,pk):
    person= get_object_or_404(Person,pk=pk,user=request.user)
    if request.method=='POST':
           # 🔹 If the form was submitted (POST), create a form object
        # 🔸 We pass both the submitted data and the existing object (to update it instead of creating a new one)
        form = PersonForm(request.POST,instance=person)
        if form.is_valid():
            form.save()
            messages.success(request,"Saved Changes Successfully!")
            return redirect('people_list')
        
    else: 
        form = PersonForm(instance=person)
        # PersonForm creates a FormObject
        # 🔸 instance=person — pre-fills the form with existing data.

    return render(request,'blog/add_person.html',{'form':form,
                                                  'title':'Edit Person',
                                                  'button_name':'Save Changes'})

def delete_person(request,pk):
    person=get_object_or_404(Person,pk=pk,user=request.user)
    person.delete()
    return redirect('people_list')



def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # UserCreationForm is a django inbuilt function that helps us create new users.
            # initializes the form with the submitted data
        if form.is_valid():
            user=form.save()
            # saves the user to the database
            login(request,user)
            # after successful registration login
            messages.success(request,"Registration Successful!")
            return redirect('people_list')
        else:
            messages.error(request,"Registration Failed!")
    else:
        form=UserCreationForm()
        # if the request is post we give empty form to fill data
    return render(request,'blog/register.html',{'form':form,'title':"Register"})

@login_required
# This is login decorators only lets logged-in users see dashboard else redirects to login page
def dashboard_view(request):
        return redirect('people_list')







# TODO: Serializers view

@api_view(['GET','POST'])
# get request bhaneko front end ma data chaiyo bhane ya bata serialize garera data pathaucha of a particular user ko information registry.
@permission_classes([IsAuthenticated])
# Person Authenticated cha bhane matra garna dincha
def person_api_list(request):
    if request.method== "GET":
        persons=Person.objects.filter(user=request.user)

        # TODO: only to test get post using postman(
        # persons=Person.objects.all()
        # )

        serializer = PersonSerializer(persons,many=True)
        # many=true means works only when there are more than one data.
        return Response(serializer.data) 
    elif request.method=="POST":
        serializer=PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            # TODO: only to test get post using postman(
            # dummy_user= User.objects.get(username="abcd1234")
            # serializer.save(user=dummy_user)
            # )

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])    
def person_details(request,pk):
    try:
        person= get_object_or_404(Person,user=request.user,pk=pk)
       
    except Person.DoesNotExist:
        return Response({'error':'Person not found'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method=="GET":
        serializer=PersonSerializer(person)
        return Response(serializer.data)
    
    elif request.method== "PUT":
        # Client JSON → DRF View → Serializer Validation → Database Update → JSON Response
        serializer=PersonSerializer(person,data=request.data)
         # The existing Person instance and the new data from the request are passed to the serializer.
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method== "DELETE":
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


   