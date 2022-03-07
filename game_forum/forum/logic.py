from django.db.models import Avg

from forum.models import UserGameRelation

def set_rating(game):
    rating = UserGameRelation.objects.filter(game=game).aggregate(rating=Avg('rate')).get('rating')
    game.rating = rating
    game.save()
