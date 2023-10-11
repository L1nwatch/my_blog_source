Here is the updated function:

```python
@decorator_with_args
def log_wrapper(func, *, str_format="", level="info", logger=None):
    """
    负责进行日志记录的装饰器
    :param func:
    :param str_format:
    :param level:
    :param logger:
    :return:
    """

    @wraps(func)
    def wrapper(request=None, *func_args, **func_kwargs):
        if request is not None:
            # 检查是否要发送邮件
            ip_address = get_ip_from_django_request(request)
            http_header = get_http_header_from_request(request)

            email_check = email_sender.want_to_send_email(ip_address)
            
            # if 'bot' or 'spider' is found in the headers, don't send the email
            if 'bot' in http_header or 'spider' in http_header:
                email_check = False

            # 记录日志并发送邮件
            make_a_log = threading.Thread(target=background_deal, kwargs={"logger": logger,
                                                                          "level": level,
                                                                          "request": request,
                                                                          "func_kwargs": func_kwargs,
                                                                          "str_format": str_format,
                                                                          "ip_address": ip_address,
                                                                          "email_check": email_check})
            make_a_log.start()

        return func(request, *func_args, **func_kwargs)

    return wrapper
```
This new function will check the http headers for the words 'bot' or 'spider' and if it finds either, it will set the email_check variable to False to prevent an email from being sent. This is useful for preventing unnecessary emails from being sent when the request is from a bot or spider.