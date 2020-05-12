import django_tables2 as tables
# from .models import JobPost

class SimpleTable(tables.Table):
    class Meta:
        model = Simple