from abc import ABC, abstractmethod
from .models import Job

class Filterable(ABC):
    @abstractmethod
    def apply_filter(self, qs, value):
        pass

class TitleFitler(Filterable):
    def apply_filter(self, qs, value):
        qs = qs.filter(title__icontains=value)
        return qs

class LocationFilter(Filterable):
    def apply_filter(self, qs, value):
        qs = qs.filter(location__icontains=value)
        return qs
    
class MinSalaryFilter(Filterable):
    def apply_filter(self, qs, min_salary):
        if min_salary and min_salary.isdigit():
            qs = qs.filter(salary__gte=int(min_salary))
        return qs

class MaxSalaryFilter(Filterable):
    def apply_filter(self, qs, max_salary):
        if max_salary and max_salary.isdigit():
            qs = qs.filter(salary__lte=int(max_salary))
        return qs 

class RemoteFilter(Filterable):
    def apply_filter(self, qs, remote):
        if remote in ['true', 'false']:
            qs = qs.filter(is_remote=(remote == 'true'))
        return qs

class VisaSponsorshipFilter(Filterable):
    def apply_filter(self, qs, visa_sponsorship):
        if visa_sponsorship in ['true', 'false']:
            qs = qs.filter(visa_sponsorship=(visa_sponsorship == 'true'))
        return qs
    
class FilterOrchestrator:
    filter_registry = {
        'search': TitleFitler,
        'title': TitleFitler,
        'location': LocationFilter,
        'min_salary': MinSalaryFilter,
        'max_salary': MaxSalaryFilter,
        'remote': RemoteFilter,
        'visa_sponsorship': VisaSponsorshipFilter,
    }

    def apply_filters(self, qs, filter_params):
        for name, value in filter_params.items():
            if value:
                filter_class = self.filter_registry.get(name)
                if filter_class:
                    qs = filter_class().apply_filter(qs, value)
        return qs
    


