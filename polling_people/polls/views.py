from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from .models import AnswerForChoice, Poll, Question, UserChoiceAnswer
from .permissions import IsAdminOrReadOnly
from .serializers import (AnswerForChoiceSerializer, PollDetailPageSerializer,
                          PollSerializer, PrintUserAnswerSerializer,
                          QuestionSerializer, UserChoiceAnswerSerializer)


class PollViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsAdminOrReadOnly,)


class PollDetailPageViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Poll.objects.all()
    serializer_class = PollDetailPageSerializer
    permission_classes = (IsAdminOrReadOnly,)


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        poll = get_object_or_404(Poll, pk=self.kwargs['poll_id'])
        return Question.objects.filter(poll=poll)

    def perform_create(self, serializer):
        poll = get_object_or_404(Poll, pk=self.kwargs['poll_id'])
        serializer.save(poll=poll)

    def perform_update(self, serializer):
        poll = get_object_or_404(Poll, pk=self.kwargs['poll_id'])
        serializer.save(poll=poll)


class AnswerForChoiceViewSet(ModelViewSet):
    serializer_class = AnswerForChoiceSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        return AnswerForChoice.objects.filter(question=question)

    def perform_create(self, serializer):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        serializer.save(question=question)

    def perform_update(self, serializer):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        serializer.save(question=question)


class UserChoiceAnswerVievSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PrintUserAnswerSerializer

    def get_queryset(self):
        userid = int(self.request.headers['userid'])
        return UserChoiceAnswer.objects.filter(userid=userid)


@api_view(['GET'])
def choice_answer_view(request, *args, **kwargs):
    try:
        userid = request.headers['userid']
    except Exception:
        return Response(
            'Miss UserID',
            status=status.HTTP_400_BAD_REQUEST,
        )
    question = get_object_or_404(Question, pk=kwargs['question_id'])

    if question.type_question == 'ONE':
        try:
            answer_id = request.data['answer_id']
        except Exception:
            return Response(
                'Miss answer_id',
                status=status.HTTP_400_BAD_REQUEST,
            )
        answer = get_object_or_404(AnswerForChoice, pk=answer_id)
        serializer = UserChoiceAnswerSerializer(data=request.data)
        if serializer.is_valid():
            choise = serializer.save(
                answer=answer,
                question=question,
                userid=userid
            )
            serializer = UserChoiceAnswerSerializer(choise)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if question.type_question == 'MULT':
        try:
            answer_id = request.data['answer_id']
        except Exception:
            return Response(
                'Miss answer_id',
                status=status.HTTP_400_BAD_REQUEST,
            )
        answers = list(map(int, answer_id.split()))
        serializer_data = {}
        for item in answers:
            answer = get_object_or_404(AnswerForChoice, pk=int(item))
            serializer = UserChoiceAnswerSerializer(data=request.data)
            if serializer.is_valid():
                choise = serializer.save(
                    answer=answer,
                    question=question,
                    userid=userid
                )
                serializer = UserChoiceAnswerSerializer(choise)
                serializer_data[item] = serializer.data
        return Response(
            serializer_data,
            status=status.HTTP_201_CREATED,
        )

    if question.type_question == 'TEXT':
        try:
            answer_text = request.data['answer_text']
        except Exception:
            return Response(
                'Miss answer_text',
                status=status.HTTP_400_BAD_REQUEST,
            )
        new_answer = AnswerForChoice.objects.create(
            question=question,
            text=answer_text
        )
        new_data = {'answer_id': [str(new_answer.id)]}
        serializer = UserChoiceAnswerSerializer(data=new_data)
        if serializer.is_valid():
            choise = serializer.save(
                answer=new_answer,
                question=question,
                userid=userid
            )
            serializer = UserChoiceAnswerSerializer(choise)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
