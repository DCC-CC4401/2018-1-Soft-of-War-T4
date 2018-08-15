from mainApp.models import Action
from articlesApp.models import Article
from spacesApp.models import Space
from django.db import models


class Space_Reservation(Action):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)

    def __str__(self):
        return self.space.__str__() + ' - ' + self.user.__str__() + ' - (' + str(self.starting_date_time) + ')'

class Article_Reservation(Action):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.article.__str__() + ' - ' + self.user.__str__() + ' - (' + str(self.starting_date_time) + ')'