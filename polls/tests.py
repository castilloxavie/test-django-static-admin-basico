from datetime import timedelta
import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

# Create your tests here.


# los test se le hacer a los modelos y a las vistas
class  QuestionModelTest(TestCase):

    def setUp(self):
        self.question = Question(questions_text = " ¿quien es el mejor Couser Director de PLatzi?")

    def test_was_created_recently_future_questions(self):
        time= timezone.now() + timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_created_recently_present_questions(self):
        time= timezone.now() - timedelta(hours=24)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_created_recently_past_questions(self):
        time= timezone.now() - timedelta(days=1, minutes=1)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)


def create_question(questions_text, days):
    """craete question wiith give "questions_text", and published the given 
    number of day oofset to now(negative for questions in the past, positive
    for questions that h   ave yet to be published )"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(questions_text=questions_text, pub_date= time )

class QuestionIndexTest(TestCase):

    def test_no_questions(self):
        """If no question exist, an appropiatee message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["lastest_question_list"], [])


    def test_future_question(self):
        """
        questions with a pub__date in the futer aren't dispay on the index page
        """
        create_question("future Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["lastest_question_list"],[])

    def tes_past_questions(self):
        """
        questions with a pub_date in the past are displayed on the index page
        """
        question = create_question("past Question", days=-5 )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["lastest_question_list"],[question])


    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are dispalyed
        """
        past_questio = create_question(questions_text="past question", days=-30)
        future_questio = create_question(questions_text="future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lastest_question_list"],
            [past_questio]
        )

    def test_two_past_questios(self):
        """
        The question index page may display multiple questions.
        """
        past_questio1 = create_question(questions_text="past question 1", days=-30)
        past_questio2 = create_question(questions_text="past question 2", days=-50)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lastest_question_list"],
            [past_questio1, past_questio2]
        )

    def test_two_future_question(self):
         """
         the questions with the pub_date in the future aren't  not dysplayed on idex page
         """
         future_questio1 = create_question(questions_text="future question 1", days=30)
         future_questio2 = create_question(questions_text="future question 2", days=60)
         response= self.client.get(reverse("polls:index"))
         self.assertQuerysetEqual(
            response.context["lastest_question_list"], []
         )


class QuestionDetailtest(TestCase):


    def test_future_question(self):
        """
        the datail view od a question with a pub_date in the future
        return a 404 error not found
        """
        future_question = create_question(questions_text="future question", days=30)
        url = reverse("polls:detalle", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        the deail view of a question with a pub_date in the past displays 
        the question's text
        """
        past_question = create_question(questions_text="future question", days=-30)
        url = reverse("polls:detalle", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.questions_text)



