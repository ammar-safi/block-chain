import json


def send_response (data=None, message=None, status=200) : 
        print(json.dumps({
            "data" : data ,
            "message" : message ,
            "status" : status 
        }))


def send_bad_request (message) :
    send_response(
        message=message,
        status=400
    )

def send_ok (data) :
    send_response (
        data=data
    )

def send_not_found (message="not found") :
    send_response(
        message=message,
        status=404
    )
def send_server_error (message) :
    send_response(
        message=message,
        status=500
    )

