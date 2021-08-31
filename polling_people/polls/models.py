from datetime import date

from django.db import models


class Poll(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    start_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата_начала',
    )
    end_date = models.DateField(
        verbose_name='Дата_окончания',
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Опрос'
        ordering = ('-start_date',)

    def __str__(self):
        return self.title

    def still_going(self):
        now = date.today()
        return self.end_date >= now


class Question(models.Model):
    ONE = 'ONE'
    MULT = 'MULT'
    TEXT = 'TEXT'
    TUPE_OF_QUESTION = [
        (ONE, 'ONE'),
        (MULT, 'MULT'),
        (TEXT, 'TEXT'),
    ]
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        verbose_name='Опрос_мастер',
        null=True,
    )
    text_question = models.TextField(
        verbose_name='Текст_вопроса',
    )
    type_question = models.CharField(
        max_length=4,
        choices=TUPE_OF_QUESTION,
        default=ONE,
        verbose_name='Тип_вопроса'
    )

    class Meta:
        verbose_name = 'Вопрос'
        ordering = ('id',)

    def answers(self):
        if not hasattr(self, '_answers'):
            self._answers = self.answerforchoice_set.all()
        return self._answers

    def __str__(self):
        return self.text_question


class AnswerForChoice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='МастерВопрос'
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Текст',
    )

    class Meta:
        verbose_name = 'Ответ_на_выбор'

    def __str__(self):
        return self.text


class UserChoiceAbstractAnswer(models.Model):
    userid = models.IntegerField(
        verbose_name='UserId',
        null=True,
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='МастерВопрос'
    )

    answer = models.ForeignKey(
        AnswerForChoice,
        on_delete=models.CASCADE,
        verbose_name='Ответ',
    )

    def __str__(self):
        return (f'{self.userid} выбрал {self.answer}.')

    class Meta:
        abstract = True


class UserChoiceAnswer(UserChoiceAbstractAnswer):

    class Meta:
        verbose_name = 'Выбранный_вариант'

    def __str__(self):
        return (f'{self.userid} выбрал {self.answer}.')
