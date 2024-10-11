from rest_framework import serializers
from .models import Question, Answer
import uuid


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'answer',
            'is_correct',
            'is_active',         # Add if needed
            'created_at',        # Add if needed
            'updated_at'         # Add if needed
        ]


class CreateQuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)
    question_id = serializers.UUIDField(read_only=True)  # Include question_id in the serializer

    class Meta:
        model = Question
        fields = ['question_id', 'title', 'points', 'difficulty', 'answer']

    def create(self, validated_data):
        answers_data = validated_data.pop('answer')  # Remove answers from the main data
        question = Question.objects.create(**validated_data)  # Create the question

        # Create answers linked to the question
        for answer_data in answers_data:
            Answer.objects.create(question=question, **answer_data)

        return question
    
    def update(self, instance, validated_data):
        # Update the question's fields
        instance.title = validated_data.get('title', instance.title)
        instance.points = validated_data.get('points', instance.points)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.save()

        # Handle the answers
        if 'answer' in validated_data:
            # Clear existing answers
            instance.answer.all().delete()  # Remove old answers

            # Create new answers
            answers_data = validated_data.pop('answer')
            for answer_data in answers_data:
                # Create new answer instances
                Answer.objects.create(question=instance, **answer_data)

        return instance


class RandomQuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, required=False)
    question_id = serializers.UUIDField(read_only=True)  # Include question_id in the serializer

    class Meta:
        model = Question
        fields = [
            'question_id', 'title', 'points', 'answer',
        ]

    def update(self, instance, validated_data):
        # Update the question's fields
        instance.title = validated_data.get('title', instance.title)
        instance.points = validated_data.get('points', instance.points)
        instance.save()

        # Handle answers
        answers_data = validated_data.get('answer')
        if answers_data:
            # Clear existing answers
            instance.answer.all().delete()  # Ensure we clear out the old answers before creating new ones

            for answer_data in answers_data:
                # Create new answer instances
                Answer.objects.create(
                    question=instance,
                    answer=answer_data['answer'],
                    is_correct=answer_data.get('is_correct', False),
                )

        return instance