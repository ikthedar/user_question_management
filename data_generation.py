from faker import Faker
import csv
import random

fake = Faker()

# Define functions to generate user and question data
def generate_users(num_users):
    users = []
    generated_idnames = set()
    for _ in range(num_users):
        idname = fake.user_name()
        while idname in generated_idnames:
            idname = fake.user_name()

        generated_idnames.add(idname)
        user = {
            'idname': idname,
            'display_name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number()
        }
        users.append(user)
    return users

def generate_questions(num_questions):
    questions = []
    for _ in range(num_questions):
        question = {
            'question': fake.sentence(nb_words=10),
            'option1': fake.sentence(nb_words=5),
            'option2': fake.sentence(nb_words=5),
            'option3': fake.sentence(nb_words=5),
            'option4': fake.sentence(nb_words=5),
            'option5': fake.sentence(nb_words=5),
            'answer': random.choice(['option1', 'option2', 'option3', 'option4', 'option5']),
            'explain': fake.paragraph(nb_sentences=3)
        }
        questions.append(question)
    return questions

# Generate the user and question data and save it to CSV files
num_users = 10000
users_data = generate_users(num_users)

with open('users_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['idname', 'display_name', 'email', 'phone']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for user in users_data:
        writer.writerow(user)

num_questions = 1000
questions_data = generate_questions(num_questions)

with open('questions_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['question', 'option1', 'option2', 'option3', 'option4', 'option5', 'answer', 'explain']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for question in questions_data:
        writer.writerow(question)
