import django_filters
from .models import CUSTOMER_TYPES, GENDERS, Customer

# Define predefined age ranges
AGE_RANGES = [
    ('', 'Select Age Range'),  # Empty option for "Select"
    ('0-18', '0-18'),
    ('19-30', '19-30'),
    ('31-40', '31-40'),
    ('41-50', '41-50'),
    ('51+', '51+'),
]


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Name")
    location = django_filters.CharFilter(
        lookup_expr='icontains', label="Location")
    phone_number = django_filters.CharFilter(
        lookup_expr='icontains', label="Phone Number")
    gender = django_filters.ChoiceFilter(choices=GENDERS, label="Gender")
    type = django_filters.ChoiceFilter(
        choices=CUSTOMER_TYPES, label="Customer Type")

    # Using ChoiceFilter for age ranges
    age_range = django_filters.ChoiceFilter(
        choices=AGE_RANGES, label="Age Groups", method='filter_age_range')

    class Meta:
        model = Customer
        fields = ['name', 'location', 'phone_number', 'gender', 'type']

    def filter_age_range(self, queryset, name, value):
        # Check if a valid age range is selected
        if value:
            if value == '0-18':
                queryset = queryset.filter(age__lte=18)
            elif value == '19-30':
                queryset = queryset.filter(age__gte=19, age__lte=30)
            elif value == '31-40':
                queryset = queryset.filter(age__gte=31, age__lte=40)
            elif value == '41-50':
                queryset = queryset.filter(age__gte=41, age__lte=50)
            elif value == '51+':
                queryset = queryset.filter(age__gte=51)
        return queryset
