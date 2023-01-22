from jwt import encode, decode

def create_token(data:dict) -> str:
    token:str = encode(payload=data, key='Puerto_Ordaz', algorithm='HS256')
    return token

def validate_token(token:str) -> str:
    data:dict = decode(token, key='Puerto_Ordaz', algorithms=['HS256'])
    return data
