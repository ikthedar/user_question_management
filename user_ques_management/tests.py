from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user_ques_management.models import UserProfile, Question, ReadQuestion, FavoriteQuestion
from user_ques_management.serializers import ReadQuestionSerializer
from user_ques_management.views import user_question_count_view, filtered_question_view, get_favorite_and_read_questions

class UserQuestionCountAPITest(APITestCase):
    def setUp(self):
        # Create test data
        self.user1 = UserProfile.objects.create(idname="user1", display_name="User 1", email="user1@test.com", phone="1234567890")
        self.user2 = UserProfile.objects.create(idname="user2", display_name="User 2", email="user2@test.com", phone="9876543210")
        self.question1 = Question.objects.create(question="Question 1", option1="Option 1", option2="Option 2", option3="Option 3", option4="Option 4", option5="Option 5", answer="option1", explain="Explanation 1")
        self.question2 = Question.objects.create(question="Question 2", option1="Option 1", option2="Option 2", option3="Option 3", option4="Option 4", option5="Option 5", answer="option1", explain="Explanation 2")
        self.favorite1 = FavoriteQuestion.objects.create(user_id=self.user1, question_id=self.question1)
        self.favorite2 = FavoriteQuestion.objects.create(user_id=self.user1, question_id=self.question2)
        self.read1 = ReadQuestion.objects.create(user_id=self.user2, question_id=self.question1)
        self.read2 = ReadQuestion.objects.create(user_id=self.user2, question_id=self.question2)

    def test_user_question_count_view(self):
        url = reverse('user_question_count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['users']), 2)  # Assuming 2 users in the test data
        self.assertEqual(response.data['users'][0]['user_id'], self.user1.id)
        self.assertEqual(response.data['users'][0]['display_name'], self.user1.display_name)
        self.assertEqual(response.data['users'][0]['favorite_count'], self.user1.favoritequestion_set.count())
        self.assertEqual(response.data['users'][0]['read_count'], self.user1.readquestion_set.count())
        self.assertEqual(response.data['users'][1]['user_id'], self.user2.id)
        self.assertEqual(response.data['users'][1]['display_name'], self.user2.display_name)
        self.assertEqual(response.data['users'][1]['favorite_count'], self.user2.favoritequestion_set.count())
        self.assertEqual(response.data['users'][1]['read_count'], self.user2.readquestion_set.count())

class FilteredQuestionViewAPITest(APITestCase):
    def setUp(self):
        # Create test data
        self.user1 = UserProfile.objects.create(idname="user1", display_name="User 1", email="user1@test.com", phone="1234567890")
        self.user2 = UserProfile.objects.create(idname="user2", display_name="User 2", email="user2@test.com", phone="9876543210")
        self.question1 = Question.objects.create(question="Question 1", option1="Option 1", option2="Option 2", option3="Option 3", option4="Option 4", option5="Option 5", answer="option1", explain="Explanation 1")
        self.question2 = Question.objects.create(question="Question 2", option1="Option 1", option2="Option 2", option3="Option 3", option4="Option 4", option5="Option 5", answer="option1", explain="Explanation 2")
        self.favorite1 = FavoriteQuestion.objects.create(user_id=self.user1, question_id=self.question1)
        self.favorite2 = FavoriteQuestion.objects.create(user_id=self.user2, question_id=self.question2)
        self.read1 = ReadQuestion.objects.create(user_id=self.user1, question_id=self.question1)

    def test_filtered_question_view(self):
        url = reverse('filtered_questions')
        response = self.client.get(url, {'status': 'read'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['questions']), 1)
        self.assertEqual(response.data['questions'][0]['question'], self.question2.question)
        self.assertEqual(response.data['questions'][0]['option1'], self.question2.option1)
        


class AddReadQuestionAPITest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(idname="test_user", display_name="Test User", email="test@test.com", phone="1234567890")
        self.question = Question.objects.create(question="Sample question", option1="Option 1", option2="Option 2", option3="Option 3", option4="Option 4", option5="Option 5", answer="option1", explain="Explanation")
        self.url = reverse('add_read_question')
        self.valid_payload = {
            'user_id': self.user.id,
            'question_id': self.question.id,
        }
        self.invalid_payload = {
            'user_id': 999,  # Invalid user_id to simulate a non-existing user
            'question_id': self.question.id,
        }

    def test_add_read_question_valid_payload(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReadQuestion.objects.count(), 1)

    def test_add_read_question_invalid_payload(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ReadQuestion.objects.count(), 0)

    def test_add_read_question_missing_fields(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ReadQuestion.objects.count(), 0)

class AddFavoriteQuestionAPITest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(idname="test_user", display_name="Test User", email="test@test.com", phone="1234567890")
        self.question = Question.objects.create(question="Sample question", option1="Option 1", option2="Option 2", option3="Option 3", option4="Option 4", option5="Option 5", answer="option1", explain="Explanation")
        self.url = reverse('add_favorite_question')
        self.valid_payload = {
            'user_id': self.user.id,
            'question_id': self.question.id,
        }
        self.invalid_payload = {
            'user_id': 999,  # Invalid user_id to simulate a non-existing user
            'question_id': self.question.id,
        }

    def test_add_favorite_question_valid_payload(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteQuestion.objects.count(), 1)

    def test_add_favorite_question_invalid_payload(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FavoriteQuestion.objects.count(), 0)

    def test_add_favorite_question_missing_fields(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FavoriteQuestion.objects.count(), 0)

class GetFavoriteAndReadQuestionsViewAPITest(APITestCase):
    def setUp(self):
        # Create test data
        self.user1 = UserProfile.objects.create(idname="user1", display_name="User 1", email="user1@test.com", phone="1234567890")
        self.user2 = UserProfile.objects.create(idname="user2", display_name="User 2", email="user2@test.com", phone="9876543210")
        self.question1 = Question.objects.create(question="Question 1", option1="Option 1", option2="Option 2", option3="Option 3", option4="Option 4", option5="Option 5", answer="option1", explain="Explanation 1")
        self.question2 = Question.objects.create(question="Question 2", option1="Option 1", option2="Option 2", option3="Option 3", option4="Option 4", option5="Option 5", answer="option1", explain="Explanation 2")
        self.favorite1 = FavoriteQuestion.objects.create(user_id=self.user1, question_id=self.question1)
        self.favorite2 = FavoriteQuestion.objects.create(user_id=self.user2, question_id=self.question2)
        self.read1 = ReadQuestion.objects.create(user_id=self.user1, question_id=self.question1)

    def test_get_favorite_and_read_questions_view(self):
        url = reverse('favorite_read_questions', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], self.user1.id)
        self.assertEqual(response.data['display_name'], self.user1.display_name)
        self.assertEqual(response.data['favorite_questions'], [self.question1.id])
        self.assertEqual(response.data['read_questions'], [self.question1.id])

    def test_user_not_found(self):
        url = reverse('favorite_read_questions', args=[999])  # Using an invalid user_id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'User not found.'})