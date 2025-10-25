from abc import ABC, abstractmethod
from django.db.models import Q
from profiles.models import Profile


class Filterable(ABC):
    @abstractmethod
    def apply_filter(self, qs, value):
        pass


class SkillsFilter(Filterable):
    def apply_filter(self, qs, value):
        if not value:
            return qs
        # match any profile whose skills text contains the term
        return qs.filter(skills__icontains=value)


class LocationFilter(Filterable):
    def apply_filter(self, qs, value):
        if not value:
            return qs
        # Use the CityPreference selected_city if available on the user
        return qs.filter(user__city_preference__selected_city__icontains=value)


class ProjectsFilter(Filterable):
    def apply_filter(self, qs, value):
        if not value:
            return qs
        # Search in experiences and links for a project keyword
        return qs.filter(
            Q(experiences__title__icontains=value)
            | Q(experiences__description__icontains=value)
            | Q(links__label__icontains=value)
            | Q(links__url__icontains=value)
        ).distinct()


class FilterOrchestrator:
    filter_registry = {
        'skills': SkillsFilter,
        'location': LocationFilter,
        'projects': ProjectsFilter,
    }

    def apply_filters(self, qs, filter_params):
        for name, value in filter_params.items():
            if value:
                filter_class = self.filter_registry.get(name)
                if filter_class:
                    qs = filter_class().apply_filter(qs, value)
        return qs
