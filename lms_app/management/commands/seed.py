from django.core.management.base import BaseCommand
from ...models import Course, Question, Answer
import random
from django.utils.crypto import get_random_string

# python manage.py seed --mode=refresh
# Clears all data and creates questions and answers
MODE_REFRESH = 'refresh'

#  Clears all data and does not create any object
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done')

def clear_data():
    # Deletes all the table data
    # logger.info("Delete instances")
    Answer.objects.all().delete()
    Question.objects.all().delete()

def create_course():
    # logger.info("Creating a course")
    topics = ["dogs", "cats", "birds", "coding", "mental health"]
    title = random.choice(topics)
    course = Course(
        title=title,
        description=f"All about "+title,
        video_id = get_random_string(length=6)
    )
    course.save()
    # logger.info("{} course created.".format(course))
    print("*************************************************************")
    print(course.__dict__)
    return course

def create_quiz():
    # logger.info("Creating a quiz")
    questions = [
        "What lorem ipsum dolor sit amet, consectetur adipiscing elit?",
        "Who lorem ipsum dolor sit amet, consectetur adipiscing elit?",
        "Where lorem ipsum dolor sit amet, consectetur adipiscing elit?",
        "How lorem ipsum dolor sit amet, consectetur adipiscing elit?",
        "When lorem ipsum dolor sit amet, consectetur adipiscing elit?"
    ]
    random.shuffle(questions)
    correct_answer_index = random.randint(1,4)
    # temporarily assign a correct_answer_id and then come back to update it
    for question in questions:
        item = Question(
            content = question,
            correct_answer_id = 2,
            course = Course.objects.last()
        )
        item.save()

        a_num = 0
        for num in range(1,5):
            if num == correct_answer_index:
                correct_option = create_correct_answer()
                item.correct_answer_id = correct_option.id
                item.save()
            else:
                create_wrong_answer(a_num)
                a_num +=1
        print("-----------------------------------------------------------------------")
        print(item.__dict__)


def create_correct_answer():
    # Creating a correct answer
    # logger.info("creating a correct answer")
    correct_answers = [
        "Pick me!  I'm the right answer.",
        "Obviously the correct answer",
        "Pick me if you want to be right!",
        "I'm telling you: this is the correct answer.",
        "Hint: this is the correct answer!"
    ]

    correct_answer = Answer(
        content = random.choice(correct_answers),
        question = Question.objects.last()
    )
    correct_answer.save()
    print(correct_answer.__dict__)
    return correct_answer

def create_wrong_answer(idx):
    # Creating a correct answer
    # logger.info("creating a correct answer")
    wrong_answers = [
        "An appealing but incorrect answer.",
        "Obviously NOT the correct answer",
        "Hint: this is an incorrect answer!"
    ]

    answer = Answer(
        content = wrong_answers[idx],
        question = Question.objects.last()
    )
    answer.save()
    print(answer.__dict__)

    return answer

def run_seed(self, mode):
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Create 2 courses with questions and answers
    for i in range(2):
        create_course()
        create_quiz()
