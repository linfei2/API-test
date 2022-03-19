# API-test
> API test with requests and pytest.
> I tested Simple Books API from Valentin Despa Postman tutorial:
> https://www.youtube.com/watch?v=VywxIQ2ZXw4&t=2142s
> API documentation can be found here:
> https://github.com/vdespa/introduction-to-postman-course/blob/main/simple-books-api.md

#### Technologies
```
* Python 3.8.10
```

#### Setup
Installing dependencies:
```
pip install -r requirements.txt
```

#### Run tests
All tests:
```
pytest
```
Single test:
```
pytest test_books_api.py::<test name>
```
More info about running tests with pytest:
https://docs.pytest.org/en/7.0.x/how-to/usage.html