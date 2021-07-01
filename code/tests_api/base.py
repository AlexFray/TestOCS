import random
from mimesis import Person
import pytest

from api.client import Client


class ApiBase:
    person = Person()

    @pytest.fixture(autouse=True, scope='function')
    def setup(self, config):
        self.client: Client = Client(config['url'])

    @pytest.fixture(scope='function')
    def userid(self):
        response = self.client.get_users()
        return response['data'][random.randint(0, len(response['data']) - 1)]['id']

    @pytest.fixture(scope='function')
    def user(self):
        first_name = self.person.first_name()
        second_name = self.person.last_name()
        age = random.randint(18, 99)
        yield first_name, second_name, age
        response = self.client.get_users()
        id_user = [user['id'] for user in response['data'] if user['first_name'] in first_name
                   and user['second_name'] in second_name and user['age'] == age][0]
        self.client.delete_users(id_user)

    @pytest.fixture(scope='function')
    def userid_del(self):
        first_name = self.person.first_name()
        second_name = self.person.last_name()
        age = random.randint(18, 99)
        response = self.client.post_users(first_name, second_name, age)
        return response['data']['id']

