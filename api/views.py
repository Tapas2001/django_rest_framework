from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from django.http import Http404
from rest_framework import mixins, generics, viewsets
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from .paginations import CustomePagination
from employees.filters import EmployeeFilter
from rest_framework.filters import SearchFilter, OrderingFilter


# Create your views here.

 # a. Using Static Data

'''def studentsView(request):
   
   
    students = {
        'id': 1,
        'name': 'Rohit',
        'age': 23,
        'class': 'Computer Science'
    } 
    return JsonResponse(students)'''
   
# b. Using Dynamic Data(From database)(required sealizers)
# Serializing in tow way
# 1. Mannually Serializing

'''def studentsView(request):
    # students = Student.objects.all() # query set
    # print(students)
    # students_list = list(students.values()) # manually serializing
    return JsonResponse(students_list, safe=False)'''


 # 2. Using tool(Serializer(  ))

@api_view(['GET', 'POST'])
def studentsView(request):
    if request.method == 'GET':
        # Get  all the data from Student Table
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True) #many=True for many object other wise raise error
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data) # store data into serializer
        # print(request.data)
        if serializer.is_valid():
            serializer.save() #all the serializer data store in database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        # if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def studentDetailView(request, pk): # write any name inplace request and inpace pk
    try:
       student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, request.data) # here student is current object
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
'''# i. Using Normal Way (APIView)
# APIView is base class have lots of funtionality so here no need to use decorators for allowing methods
# Class-Based View Get All Employees
class Employees(APIView):
    def get(self, request):  #instance method #member methods
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True) # for many employees(if employees object have many employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404
        
    def get(self, request, pk): 
        employee = self.get_object(pk) # self is current class # for employee data call get_object() method
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data = request.data) # this is put method so take current object(employee) also, but in the case of post method don't need current object
        if serializer.is_valid(): # before save check serializer is valid or not
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


'''
# Mixins 
# Create Class base api view using mixins
class Employees(mixins.ListModelMixin ,mixins.CreateModelMixin, generics.GenericAPIView): # for both get and post 
# here mixins.ListModelMixin is used for get all the data(objects data) 
# here mixins.CreateModelMixin is user for post a data(a object data)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    def get(self, request):
        return self.list(request) # list() is a function which coming form ListModelMixin and this list take request and user for get data.
    
    def post(self, request): 
        return self.create(request)  # create() is a function which coming form CreateModelMixin and this list take request and user for creata  data.
        # Here we don't have to do any stuff like checking if the serializer is valid and if it is not valid -
        # - then saving the serializer and returning the response and returning the errors nothing we don't have to do -
        # anything else generic API view will take care of it automatically and mixin will be able to handling or proforming these tasks.
        # So mixins save lots of work.

        # generics.GenericAPIView give resopne automatically(like HTTP 201 Created on the webpage)

# Mixins
# Primary key based operations such as getting a single object updating existing object and deleting the object
class EmployeeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # Get A Single Object Primary Key-Based Operation
    def get(self, request, pk):   #it's a primary key based operation so the funciton take pk parameter
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)
    
    # Note - Mixin & Generic
    ### Mixins is used for CURD operation and request handling and response taken care by generic.GenericAPIView'
    '''


#Generics
# It's more eaiser than mixin and very short(reduce line of code)

# class Employees(generics.ListAPIView, generics.CreateAPIView):
#     # This class take just two attributes
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

# or direct
'''
class Employees(generics.ListCreateAPIView):
    # This class take just two attributes
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
'''

#Generics
'''
# for only retrive(get)
class EmployeeDetail(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk' #lookup_field is used for pk based operation(put pk) '''


# for  retrive(get), update, delete
# 1st way
'''class EmployeeDetail(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk' #lookup_field is used for pk based operation(put pk) '''

'''
# 2nd way(direct)
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk' # lookup_field used for pirmay based operation(if the url take any value)'''



# viewset 

# 1. viewsets.ViewSet
# Here is the problem is we create all fuctionality in one function

# class EmployeeViewSet(viewsets.ViewSet):
#     # for get all the data 
#     def list(self, request):
#         queryset = Employee.objects.all()
#         serializer = EmployeeSerializer(queryset, many = True)
#         return Response(serializer.data)  
   
#     # for create a post
#     def create(self, request):
#         serializer = EmployeeSerializer(data = request.data) # data=request.data insted request.data than couse errror
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # For retriving single object
#     # In viewsets.ViewSet we don't need tow differnt urls( two funtions), it done in one funtion(single url)
#     def retrieve(self, request, pk=None):
#         employee = get_object_or_404(Employee, pk=pk) # this method actually check if wheather we have the data, it'll actually bring the data, otherwise it shows 404
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

#     #we can create update under this same class
#     def update(self, request, pk=None):
#         employee = get_object_or_404(Employee, pk=pk) # return single object if that pk match other wise return error
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    

#     def delete(self, request, pk=None):
#         employee = get_object_or_404(Employee, pk=pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        


# or # best
# 2. viewset.ModelViewSet

class EmployeeViewSet(viewsets.ModelViewSet):
    # This class only take two attribute, you are done with everything, done with non-primary key based operations as well as primary based key operations
    # Don't need write anything like viewset.ViewSet
    # In just tow line of code, you do everything like retrive all the object, create object, retrive single object update object, and delete object 
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # for pagination(custome pagination)
    pagination_class = CustomePagination

    # for filter(global filter)
    # filterset_fields = ['designation'] 

    # for filter(custome filter)
    filterset_class = EmployeeFilter # put EmployeeFilter class



# Blogs View

# this is the non primary based key operations
class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

     # for search filter (searching for data)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['blog_title', 'blog_body'] # we can put any no. of text or char field here  # if you need only then u can put here(like only 'blog_title' or 'blog_body')
    ordering_fields = ['id', 'blog_title']
    # if i put '^' before 'body_title' then if i a india that gives all the blog those title have first word is india other wise empytlist([])(null)
    # search_fields = ['^blog_title']



    # for filtering for data
    #filter_backends = [DjangoFilterBackend]


    # for searching and filtering for data
    # filter_backends = [SearchFilter, DjangoFilterBackend]



# this is the non primary based key operations
class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

   
#for single object
class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'


  