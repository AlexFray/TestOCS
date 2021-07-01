import requests
from urllib.parse import urljoin


class ErrorRequests(Exception):
    pass


class Client:
    def __init__(self, addr):
        self.addr = addr
        self.session = requests.Session()

    def get_users(self, extended_code=200):
        r = self._request('GET', f'/users')
        code, response = r.status_code, r.json()
        if code != extended_code:
            raise ErrorRequests(f"Ошибка запроса: код ответа не совпадает с ожидаемым: {code} != {extended_code}\n"
                                f"Ответ: {response}")
        return response

    def get_user_id(self, userid, extended_code=200):
        r = self._request('GET', f'/users/{userid}')
        code, response = r.status_code, r.json()
        if code != extended_code:
            raise ErrorRequests(f"Ошибка запроса: код ответа не совпадает с ожидаемым: {code} != {extended_code}\n"
                                f"Ответ: {response}")
        return response

    def post_users(self, first_name, last_name, age, extended_code=201):
        r = self._request('POST', '/users', {'first_name': first_name, 'second_name': last_name, 'age': age})
        code, response = r.status_code, r.json()
        if code != extended_code:
            raise ErrorRequests(f"Ошибка запроса: код ответа не совпадает с ожидаемым: {code} != {extended_code}\n"
                                f"Ответ: {response}")
        return response

    def delete_users(self, userid, is_json=False, extended_code=200):
        if is_json:
            r = self._request('DELETE', '/users', {'id': userid})
        else:
            r = self._request('DELETE', f'/users/{userid}')
        code, response = r.status_code, r.json()
        if code != extended_code:
            raise ErrorRequests(f"Ошибка запроса: код ответа не совпадает с ожидаемым: {code} != {extended_code}\n"
                                f"Ответ: {response}")
        return response

    def _request(self, method, path, json=None):
        url = urljoin(self.addr, path)
        kwargs = {}
        if json:
            kwargs['json'] = json

        return self.session.request(method, url, **kwargs)
