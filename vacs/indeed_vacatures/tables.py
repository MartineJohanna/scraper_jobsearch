import django_tables2 as tables
from .models import JobPost

class ScraperTable(tables.Table):
    class Meta:
        model = JobPost
        template_name = "django_tables2/bootstrap.html"
        fields = ("titel","bedrijf","plaats" )