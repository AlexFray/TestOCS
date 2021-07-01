import pytest as pytest


def pytest_addoption(parser):
    parser.addoption('--url', default='http://127.0.0.1:5000/')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    return {'url': url}
