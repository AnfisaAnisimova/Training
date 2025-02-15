import re
from enum import StrEnum


class Method(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"


class BaseRequest:
    def __init__(self, url: str, method: Method, params: dict | None = None, body: dict | None = None):
        self._url = url
        self._method = self.method_validation(method)
        self._params = params
        self._body = self.body_validation(body, method)

    def method_validation(self, method):
        if method not in [Method.GET, Method.POST]:
            raise Exception("Недопустимый метод")
        return method

    def body_validation(self, body, method):
        if method == Method.GET and body:
            raise Exception("Невозможно задать тело запроса для метода GET")
        return body

    @property
    def url(self):
        return self._url

    @property
    def method(self):
        return self._method

    @property
    def params(self):
        return self._params

    @property
    def body(self):
        if self._method != Method.POST:
            raise Exception('Тело запроса доступно только для метода POST')
        return self._body


class Request(BaseRequest):
    def __init__(self, url: str, method: Method, params: dict | None = None, body: dict | None = None):
        super().__init__(url, method, params, body)

        if len(self._params) > 5:
            raise Exception("Максимальное количество параметров: 5")

        if not re.match(
                "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
                self.url):
            raise Exception("Неправильный формат url")

    def method_validation(self, method):
        if method not in Method.__members__.values():
            raise Exception("Недопустимый метод")
        return method

    @property
    def method(self):
        return self._method

    @property
    def body(self):
        if self._method not in [Method.POST, Method.PUT, Method.PATCH]:
            raise Exception('Тело запроса доступно только для методов POST, PUT, PATCH')
        return self._body


# request = BaseRequest('https://url.com', 'GET', {'1': 'ddd'})
# print(request.method)
# print(request.body)

request2 = BaseRequest('https://url.com', 'GET', {'1': 'ddd'}, {"1": "3"})
print(request2.method)
print(request2.body)

# request3 = BaseRequest('https://url.com', 'PUT', {'1': 'ddd'}, {"1": "3"})
# print(request3.method)
# print(request3.body)

# r = Request("http://url.com", "GET", {'1': 'ddd', '2': 'qqq', '3': 'ttt', '4': 'tty', '5': 'nbg'})
# print(r.body)

# r2 = Request("http://url.com", "GET", {'1': 'ddd', '2': 'qqq', '3': 'ttt', '4': 'tty', '5': 'nbg'}, {"1": "3"})
# print(r2.body)

# r3 = Request("http://url.com", "PUT", {'1': 'ddd', '2': 'qqq', '3': 'ttt', '4': 'tty', '5': 'nbg'}, {"body": "body"})
# print(r3.body)
