# esto huncha frontend ra backend kura garda HTTP methods ma JSON exchange use garera kam garcha
#tra django ma ta model ko object huncha data ani front end ma ta JSON huncha data teslai vice versa ma change garna hami lai chaincha serializers
#django rest framework ko euta part ho yo

from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id','name','age','email','phone_number']
        # fields= '__all__'
        # Person model lai serialize garcha all the fields lai 