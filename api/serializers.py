from rest_framework import serializers 
from students.models import Student
from employees.models import Employee

# Serializer for Student
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__" # all the fields serialized 

# Serializer for Employee
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"