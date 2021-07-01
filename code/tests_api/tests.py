import pytest

from tests_api.base import ApiBase


class Tests(ApiBase):
    def test_get_users(self):
        response = self.client.get_users()
        assert len(response['data']) > 0

    def test_get_user(self, userid):
        response = self.client.get_user_id(userid)
        user_data = response['data']
        assert user_data['id'] is not None and user_data['first_name'] is not None and user_data['second_name'] is not None

    def test_create_user(self, user):
        """ В документации описан неправильный параметр. Вместо last_name необходим second_name"""
        response = self.client.post_users(*user)
        user_data = response['data']
        assert user_data['id'] is not None and user_data['first_name'] is not None and user_data['second_name'] is not None

    @pytest.mark.parametrize('is_json', [True, False])
    def test_delete_user(self, userid_del, is_json):
        response = self.client.delete_users(userid_del, is_json)
        assert response['message'] in 'Record deleted successfully.'


class TestsNotFound(ApiBase):
    code = 404

    def test_get_user(self):
        self.client.get_user_id(5000, self.code)

    def test_delete_user(self):
        self.client.delete_users(5000, extended_code=self.code)


class TestIncorrectData(ApiBase):
    code = 400

    def test_get_user(self):
        self.client.get_user_id('dad', self.code)

    def test_delete_user(self):
        self.client.delete_users('sef', extended_code=self.code)

    @pytest.mark.parametrize('first, last, age', [
        [None, 'Name%', 50],
        ['%fdf', None, 50],
        ['Name', None, 'sdsd'],
        ['Name', 'Name', None]
    ])
    def test_create_user(self, first, last, age):
        self.client.post_users(first, last, age, self.code)
