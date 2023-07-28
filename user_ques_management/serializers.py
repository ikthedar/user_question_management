from rest_framework import serializers
from .models import UserProfile, Question, FavoriteQuestion, ReadQuestion

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class FavoriteQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteQuestion
        fields = '__all__'

class ReadQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadQuestion
        fields = '__all__'
