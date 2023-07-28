from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_ques_management.models import UserProfile, Question, FavoriteQuestion, ReadQuestion
from user_ques_management.serializers import UserProfileSerializer, QuestionSerializer, FavoriteQuestionSerializer, ReadQuestionSerializer

# View to Retrieve Count of Total Favorite and Read Questions per User, Paginated to 100 Users per Page
@api_view(['GET'])
def user_question_count_view(request):
    page_number = int(request.GET.get('page', 1))

    users = UserProfile.objects.order_by('id').prefetch_related('favoritequestion_set', 'readquestion_set').all()

    paginator = Paginator(users, 100)

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        return Response({'error': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)

    user_question_counts = []
    for user in page:
        favorite_count = user.favoritequestion_set.count()
        read_count = user.readquestion_set.count()
        user_question_counts.append({
            'user_id': user.id,
            'display_name': user.display_name,
            'favorite_count': favorite_count,
            'read_count': read_count,
        })

    return Response({'users': user_question_counts})

# View to Filter Questions by Read, Unread, Favorite, and Unfavorite Status
@api_view(['GET'])
def filtered_question_view(request):
    status = request.GET.get('status', None)

    if status not in ['read', 'unread', 'favorite', 'unfavorite']:
        return Response({'error': 'Invalid status parameter'}, status=status.HTTP_400_BAD_REQUEST)

    filtered_questions = Question.objects.all()

    if status == 'read':
        filtered_questions = filtered_questions.exclude(readquestion__isnull=False)
    elif status == 'unread':
        filtered_questions = filtered_questions.exclude(readquestion__isnull=True)
    elif status == 'favorite':
        filtered_questions = filtered_questions.filter(favoritequestion__isnull=False)
    elif status == 'unfavorite':
        filtered_questions = filtered_questions.filter(favoritequestion__isnull=True)

    serializer = QuestionSerializer(filtered_questions, many=True)
    return Response({'questions': serializer.data})

# View to Insert Favorite Question for a User
@api_view(['POST'])
def add_favorite_question(request):
    serializer = FavoriteQuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Favorite question added successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to Insert Read Question for a User
@api_view(['POST'])
def add_read_question(request):
    serializer = ReadQuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Read question added successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to Retrieve Favorite and Read Questions for a User
@api_view(['GET'])
def get_favorite_and_read_questions(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        favorite_questions = FavoriteQuestion.objects.filter(user_id=user).values('question_id')
        read_questions = ReadQuestion.objects.filter(user_id=user).values('question_id')

        favorite_question_ids = [item['question_id'] for item in favorite_questions]
        read_question_ids = [item['question_id'] for item in read_questions]

        response_data = {
            'user_id': user.id,
            'display_name': user.display_name,
            'favorite_questions': favorite_question_ids,
            'read_questions': read_question_ids,
        }

        return Response(response_data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
