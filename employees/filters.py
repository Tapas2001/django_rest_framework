import django_filters
from .models import Employee


# for custome filter

class EmployeeFilter(django_filters.FilterSet): # FilterSet have all the functionality
    designation = django_filters.CharFilter(field_name='designation', lookup_expr='iexact') # field_name = 'designation' is Employee field designation, and lookup_expr='iexact' that means if put 'iexact' it take cass insensetive(take lower case as well as upper case)
    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains') # if you only one then put only one filed(means like designation or name or designation and name)
    # id = django_filters.RangeFilter(field_name='id') #
    # rangeFilter only works in int value, not work with any value other wise error t404 bad request

    # for charfield value filteration
    id_min = django_filters.CharFilter(method='filter_by_emp_id_range', label='From EMP ID') # label is used bcz id_min not show in filter form bcz non model field  # u can set any method any (like 'filter_by_id_range')
    id_max = django_filters.CharFilter(method='filter_by_emp_id_range', label='To EMP ID') # label is used bcz id_max not show in filter form bcz not a model field

    class Meta:
        model = Employee
        fields = ['designation', 'emp_name', 'id_min', 'id_max'] # if id required then put 'id' field in fields



    def filter_by_emp_id_range(self, queryset, name, value): # queryset comes from FilterSet(django_filters.FilterSet)
        print(name, value)
        if name == 'id_min':
            return queryset.filter(emp_id__gte=value) # gte menas greaterthanequal
        elif name == 'id_max':
            return queryset.filter(emp_id__lte=value) # lte means lessthanequal
        return queryset