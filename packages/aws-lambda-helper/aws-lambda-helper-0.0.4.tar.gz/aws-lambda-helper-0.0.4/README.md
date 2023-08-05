# Install
pip install aws-lambda-helper

# How to use

### HTTP
```
from lambdahelper import http

@http.helper
def login_handler(event, context):
    http.add_cookie('token', usertoken)
    return 302, '/login_success'
```
#### http.helper
Easily create response body. You can:
* Return a plain string.
* Return an object that will be converted to JSON string.
* Return an Exception.
* Return both status code and body.

### http.set_header
Set response header. Will cover the same name header.
### http.add_header
Add response header. You can add multi headers with same name
### http.add_cookie
Append cookie.
