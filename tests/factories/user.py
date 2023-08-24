import factory
import random

from factory.mongoengine import MongoEngineFactory

from app.model.user import User


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    user_id = factory.Faker("email")
    user_password = factory.Faker("password")
    is_admin = factory.LazyAttribute(lambda _: random.choice([True, False]))
