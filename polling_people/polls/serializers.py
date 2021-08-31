from rest_framework import serializers

from .models import AnswerForChoice, Poll, Question, UserChoiceAnswer


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class AnswerForChoiceSerializer(serializers.ModelSerializer):
    question_id = serializers.ReadOnlyField(source='question.id')
    text = serializers.CharField(max_length=200)

    class Meta:
        model = AnswerForChoice
        fields = ('id', 'question_id', 'text', )
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerForChoiceSerializer(read_only=True, many=True)
    type_question = ChoiceField(choices=Question.TUPE_OF_QUESTION)

    class Meta:
        model = Question
        fields = ('id', 'poll', 'text_question', 'type_question', 'answers',)
        read_only_fields = ('id', 'poll',)


class QuestionListSerializer(QuestionSerializer):

    class Meta(QuestionSerializer.Meta):
        fields = ('id', 'poll', 'text_question', 'type_question', )


class PollSerializer(serializers.ModelSerializer):
    still_going = serializers.BooleanField(read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'
        read_only_fields = ('id', 'start_date',)


class PollDetailPageSerializer(PollSerializer):
    question = QuestionSerializer(read_only=True, many=True)


class UserChoiceAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserChoiceAnswer
        fields = ('userid', 'question', 'answer_id',)
        read_only_fields = ('userid', 'question', )


class PrintUserAnswerSerializer(serializers.Serializer):
    userid = serializers.IntegerField(read_only=True)
    question = serializers.CharField()
    answer = serializers.CharField()


# class UserIdSerializer(serializers.ModelSerializer):
#     answers = AnswerTextSerializer(read_only=True)

#     class Meta:
#         model = UserID
#         fields = '__all__'
#         read_only_fields = ('id', 'userid', 'poll', 'question',)


# class UserIdTextAnswerSerializer(serializers.ModelSerializer):
#     answers = serializers.CharField(read_only=True)

#     class Meta:
#         model = UserIDTextAnswer
#         fields = '__all__'
#         read_only_fields = ('id', 'userid', 'poll', 'question',)


# class UserHeaderIdSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserHeaderId
#         fields = ('id', 'userheaderid', )
