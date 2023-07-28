from django.db import models

class UserProfile(models.Model):
    idname = models.CharField(max_length=250, unique=True)
    display_name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.display_name

class Question(models.Model):
    question = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    option5 = models.TextField()
    answer = models.TextField()
    explain = models.TextField()

    def __str__(self):
        return self.question

class FavoriteQuestion(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - {self.question_id}"

class ReadQuestion(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - {self.question_id}"
