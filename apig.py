import json

class SessionExpiredException(Exception):
    pass

def ApigResponse(code,body,event,env,session_key = None,max_age = 60*60*2):
    print("return " + str(code))
    res = {
        'statusCode': code,
        'headers': {
            'Access-Control-Allow-Origin': event['headers']['origin'],
            'Access-Control-Allow-Credentials': True,
            'Cache-Control': 'no-store'
        }
    }
    if session_key != None:
        res['headers']['Set-Cookie'] = 'session='+session_key +'; HttpOnly; Secure; Max-Age=' + str(max_age) +'; Path=/' + env
        
    if isinstance(body, dict):
        res['body'] = json.dumps(body)
    else:
        res['body'] = body
    
    return res

class ApigException(Exception):
    def __init__(self, code, messages):
        print("return " + str(code))
        self.code = code
        self.messages = messages
        print("return:" + str(code))

    def __str__(self):
        exobj = {
            'error': {
                'code': self.code,
                'messages': self.messages
            }
        }
        return json.dumps(exobj)

def ApigSuccess(body,session_key,event):
    print("return 200")
    return {
        'statusCode': "200",
        'headers': {
            'Access-Control-Allow-Origin': event['headers']['origin'],
            'Access-Control-Allow-Credentials': True,
            'Cache-Control': "no-store",
            'Set-Cookie': 'session='+session_key +'; HttpOnly; Secure; Max-Age=' + str(60*60*2)
        },
        'body': body
    }

def get_env(context = None):
    try:
        if context == None:
            print("dev")
            return "dev"
        arns = context.invoked_function_arn.split(':')
        env = "dev"
        if arns[-1] == "prod":
            env = "prod"
        print(env)
        return env
    except Exception as e:
        raise Exception

def extract_session(event):
    try:
        cookie = event['headers']['cookie']
        cookie = cookie.replace(" ","")
        cookie_list = cookie.split(";")
        cookie_dict = {}
        for cookie in cookie_list:
            keyValue = cookie.split("=")
            cookie_dict[keyValue[0]] = keyValue[1]
        session = cookie_dict["session"]
        print(session)
        return session
    except Exception as e:
        raise SessionExpiredException("セッションが見つかりません")

if __name__ == '__main__':
    event = {
        "headers": {
            "origin": "ok"
        }
    }
    body = {"status": "aaaa"}
    print(ApigResponse("200",body,event))