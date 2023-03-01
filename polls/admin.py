from django.contrib import admin
from .models import Question, Choice

# Register your models here.

# This class is used to clococate answers when asking each question
class choiceInline(admin.StackedInline):
    model = Choice
    extra = 3

"""This class is used to customize the view of the model in the administrator 
and you can also generate the responses with the "inlines" attribute."""
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "questions_text"]
    inlines = [choiceInline]
    list_display = ("questions_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["questions_text"]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)