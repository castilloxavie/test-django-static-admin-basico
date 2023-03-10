from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic 
from django.utils  import timezone


from .models import Question, Choice

# Create your views here.

# def index(request):
#     lastest_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "lastest_question_list":lastest_question_list
#     })
# 
# 
# def detail(request, question_id):
#     question= get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {
#         "question": question
#     })
# 
# 
# def result(request, question_id):
#     question= get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/result.html", {
#         "question": question
#     })

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name = "lastest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by ("-pub_date")[:5]


class DetailView(generic.DetailView):
    model= Question
    template_name="polls/detail.html"

    def get_queryset(self):
        """
        exclude any questions that aren't published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model= Question
    template_name="polls/result.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question":question,
            "error_message": "No elegiste una respuesta"
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:resultado", args=(question.id,)))
