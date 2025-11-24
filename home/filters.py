from abc import ABC, abstractmethod
from django.conf import settings


class Filterable(ABC):
    @abstractmethod
    def apply_filter(self, qs, value):
        pass


class TitleFitler(Filterable):
    def apply_filter(self, qs, value):
        print("using the title filter", value, qs)
        qs = qs.filter(title__icontains=value)
        print("filtered query, ", qs)
        return qs


class skillFitler(Filterable):
    def apply_filter(self, qs, skills):
        qs = qs.filter(skills__icontains=skills)
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
        if remote in ["true", "false"]:
            qs = qs.filter(is_remote=(remote == "true"))
        return qs


class VisaSponsorshipFilter(Filterable):
    def apply_filter(self, qs, visa_sponsorship):
        if visa_sponsorship in ["true", "false"]:
            qs = qs.filter(visa_sponsorship=(visa_sponsorship == "true"))
        return qs


from django.conf import settings


class AISearchFilter(Filterable):
    def apply_filter(self, qs, value):
        """
        qs: queryset of all jobs
        value: the search input (title/query)
        request: needed to get the current user
        """
        from groq import Groq

        print("in the AI filter")

        # Build a concise prompt for the AI
        job_texts = ""
        for job in qs:
            job_texts += f"Title: {job.title}\n"
            job_texts += (
                f"Description: {job.skills}\n"  # Or job.description if you have
            )
            job_texts += f"Location: {job.location}\n"
            job_texts += f"Salary: {job.salary}\n"
            job_texts += f"Remote: {'Yes' if job.is_remote else 'No'}\n"
            job_texts += "-" * 30 + "\n"

        prompt = (
            f"You are a helpful assistant for recommending jobs.\n"
            f"User query: {value}\n"
            f"Here are the available jobs:\n{job_texts}\n"
            f"Please provide the top 3 jobs most relevant to the user's query. "
            f"Respond in a conversational way, including descriptions, location, salary (if relevant), "
            f"and remote info (if applicable). If you cannot understand the query, say: "
            f"'Please be more specific. Here are some related jobs. AND BE VERY CONSICSE IN THE ASWERS WITH 3 senteces or less!!!'"
        )

        print("Sending prompt to GROQ...", settings.GROQ_API_KEY)
        client = Groq(api_key=settings.GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
        )

        # Get AI response
        if hasattr(completion.choices[0].message, "content"):
            response_text = completion.choices[0].message.content
        else:
            response_text = str(completion.choices[0])

        print("GROQ response:", response_text)

        # Optionally, parse AI response to extract job titles to filter queryset
        # This part can be adjusted depending on how structured you want the filter
        return response_text


class FilterOrchestrator:
    filter_registry = {
        "search": TitleFitler,
        "title": TitleFitler,
        "skills": skillFitler,
        "location": LocationFilter,
        "min_salary": MinSalaryFilter,
        "max_salary": MaxSalaryFilter,
        "remote": RemoteFilter,
        "visa_sponsorship": VisaSponsorshipFilter,
        "ai": AISearchFilter,
    }

    def apply_filters(self, qs, filter_params):
        for name, value in filter_params.items():
            if value:
                filter_class = self.filter_registry.get(name)
                if filter_class:
                    qs = filter_class().apply_filter(qs, value)
        return qs
