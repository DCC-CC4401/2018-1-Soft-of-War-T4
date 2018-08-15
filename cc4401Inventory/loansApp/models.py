from mainApp.models import Action
from articlesApp.models import Article
from django.db import models


class Article_Loan(Action):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    STATES = (
        ('V', 'Vigente'),
        ('C', 'Caducado'),
        ('P', 'Perdido')
    )

    state = models.CharField('Estado', choices=STATES, max_length=1, default='V')

    def __str__(self):
        return self.article.__str__() + ' - ' + self.user.__str__() + ' - (' + str(self.starting_date_time) + ')'
