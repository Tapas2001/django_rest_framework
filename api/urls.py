from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter



# part1
router = DefaultRouter()
router.register('employees', views.EmployeeViewSet, basename= 'employee') #employee(url name(basename))   # here employees is  url but no need to put end point and EmployeeViewSet
#in other method we don't put url name bcz automatically generate but viewsets.ViewSet requeired url name(basename)



urlpatterns = [
    path('students/', views.studentsView),
    path('students/<int:pk>/', views.studentDetailView),

    # path('employees/', views.Employees.as_view()),
    # path('employees/<int:pk>/', views.EmployeeDetail.as_view()), #accepting pk as interger

    # part2
    path('', include(router.urls)), # Here router is router object we mention is top

    # Blogs url
    path('blogs/', views.BlogsView.as_view()),
    # Comments url
    path('comments/', views.CommentsView.as_view()),

    # primary key based operation urls
    path('blogs/<int:pk>/', views.BlogDetailView.as_view()), 
    path('comments/<int:pk>/', views.CommentDetailView.as_view()), 

]
