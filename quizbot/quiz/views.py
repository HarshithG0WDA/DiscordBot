from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Answer
from .serializers import RandomQuestionSerializer, CreateQuestionSerializer
import uuid

class RandomQuestion(APIView):
    def get(self, request, format=None, **kwargs):
        question = Question.objects.filter().order_by('?')[:1]
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)

class CreateQuestionsView(APIView):
    def post(self, request):
        # Use the serializer to validate the incoming data
        serializer = CreateQuestionSerializer(data=request.data)

        if serializer.is_valid():
            # Create question using the validated data
            question = serializer.save()

            # Handle answer creation
            answers = request.data.get('answer', [])  

            for answer_data in answers:
                # Check if the answer already exists
                if not Answer.objects.filter(question=question, answer=answer_data['answer']).exists():
                    Answer.objects.create(
                        question=question,
                        answer=answer_data['answer'],
                        is_correct=answer_data.get('is_correct', False),  
                        is_active=True
                    )

            return Response({'status': 'success', 'message': 'Question created successfully'}, status=status.HTTP_201_CREATED)

        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):
    def get_object(self, question_id):
        try:
            return Question.objects.get(question_id=question_id)  
        except Question.DoesNotExist:
            return None

    def put(self, request, question_id, *args, **kwargs):
        question = self.get_object(question_id)
        if not question:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = CreateQuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            
            answers_data = request.data.get('answer', [])
            if answers_data:
                
                question.answer.all().delete() 

                
                for answer_data in answers_data:
                    Answer.objects.create(
                        question=question,
                        answer=answer_data['answer'],
                        is_correct=answer_data.get('is_correct', False), 
                    )

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = self.get_object(question_id)
        if question is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionAndAnswerView(APIView):
    def get(self, request, format=None, **kwargs):
        questions = Question.objects.all()  # Fetch all questions
        serializer = RandomQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def put(self, request, question_id, *args, **kwargs):
        question = Question.objects.get(question_id=question_id)
        if not question:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = CreateQuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            
            answers_data = request.data.get('answer', [])
            if answers_data:
                
                question.answer.all().delete() 

                
                for answer_data in answers_data:
                    Answer.objects.create(
                        question=question,
                        answer=answer_data['answer'],
                        is_correct=answer_data.get('is_correct', False),  
                    )

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)