from .models import User, Snake, Trivia
from .forms import Questionform

import random

def quiz_list(count):
    trivia_id_list = Trivia.objects.values_list('id', flat=True)
    random_trivia_id_list = random.sample(list(trivia_id_list), min(len(trivia_id_list),count))
    trivia = Trivia.objects.filter(id__in=random_trivia_id_list).order_by('choice2')

    return trivia