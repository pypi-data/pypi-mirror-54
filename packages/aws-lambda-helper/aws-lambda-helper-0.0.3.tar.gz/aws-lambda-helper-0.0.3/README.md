# Install
pip install aws-lambda-helpers

# How to use

### HTTP

#### http.helper
Easily create response body. You can:
* return status code and body 


```
from lambdahelper import http

@http.helper
def login_handler(event, context):
    http.add_cookie('token', usertoken)
    return 302, '/login_success'
```
