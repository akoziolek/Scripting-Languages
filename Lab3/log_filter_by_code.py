#HTTP codes
#1xx informational response – the request was received, continuing process
#2xx successful – the request was successfully received, understood, and accepted
#3xx redirection – further action needs to be taken in order to complete the request
#4xx client error – the request contains bad syntax or cannot be fulfilled
#5xx server error – the server failed to fulfil an apparently valid request

def get_entries_by_code(log, HTTP_code):
    if not isinstance(HTTP_code, int) and (HTTP_code < 100 or HTTP_code > 599):
        raise ValueError('Invalid HTTP code')
    return [row for row in log if row[6] == HTTP_code]

