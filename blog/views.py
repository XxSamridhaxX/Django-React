from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Person
from .forms import PersonForm
# Create your views here.

def hellofunc(request):
    context= {
        'name': 'John',
        'age': 30,
    }
    return render(request,'blog/hello.html',context)

def people_list(request):
    peoples= Person.objects.all()
    return render(request,'blog/people.html',{'peoples':peoples})


def add_person(request):
    if request.method=="POST":
        form= PersonForm(request.POST)
        # form is a python object and requset.POST contains all the data that came through POST method and PersonForm creates raw data into objects
        if form.is_valid():
            # form is valid like fields are filled
            # is the datatype right
            # are there any validation rules broken
            form.save()
            # save data into database
            return redirect('people_list')
    else:
            form=PersonForm()
    return render(request, 'blog/add_person.html', {'form': form})


def edit_person(request,pk):
    person= get_object_or_404(Person,pk=pk)
    if request.method=='POST':
           # 🔹 If the form was submitted (POST), create a form object
        # 🔸 We pass both the submitted data and the existing object (to update it instead of creating a new one)
        form = PersonForm(request.POST,instance=person)
        if form.is_valid():
            form.save()
            return redirect('people_list')
        
    else: 
        form = PersonForm(instance=person)
        # PersonForm creates a FormObject
        # 🔸 instance=person — pre-fills the form with existing data.

    return render(request,'blog/edit_person.html',{'form':form})

def delete_person(reqest,pk):
    person=get_object_or_404(Person,pk=pk)
    person.delete()
    return redirect('people_list')