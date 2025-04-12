import os
import pandas as pd
from faker import Faker
from sqlalchemy.orm.session import Session
from database import engine
from models import *

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(base_dir, 'object_data.csv')

def generate_users(num_users):
    fake = Faker()
    users = []
    for _ in range(num_users):
        user = Users(
            username=fake.user_name(),
            email=fake.email(),
            hashed_password=fake.password(),
            is_admin=UserStatus.USER
        )
        users.append(user)
    return users

def generate_comments(users, objects, num_comments):
    fake = Faker()
    comments = []
    for _ in range(num_comments):
        user = fake.random_element(users)
        object = fake.random_element(objects)
        comment = Comments(
            user_id=user.id,
            object_id=object.id,
            text=fake.text(),
            rating=fake.pyfloat(left_digits=1, right_digits=1, positive=True)
        )
        comments.append(comment)
    return comments


def add_data():
    session = Session(bind=engine)

    df, objects = pd.read_csv(path, sep=','), []
    for index, row in df.iterrows():
        obj = Objects(
            address=row['address'],
            category=row['category'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            ramp=row['ramp'],
            lowered_curb = row['lowered_curb'],
            tactile_marking = row['tactile_marking'],
            accessible_restroom = row['accessible_restroom'],
            entrance = row['entrance'],
            level_sidewalk = row['level_sidewalk'],
            elevator = row['elevator'],
            hoist = row['hoist'],
            accessible_parking = row['accessible_parking'],
        )
        objects.append(obj)

    num_users = 5
    users = generate_users(num_users)

    session.add_all(users)
    session.add_all(objects)
    session.commit()

    num_comments = 5
    comments = generate_comments(users, objects, num_comments)

    session.add_all(comments)
    session.commit()

if __name__ == '__main__':
    add_data()