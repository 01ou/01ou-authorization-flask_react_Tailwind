"""
Gather commonly used functions for your project in this folder. 
You can reuse these functions whenever you need to implement similar functionality. 
This practice reduces repetition in your code and enhances its maintainability.
このフォルダには、プロジェクト全体でよく使われる関数をまとめます。
同じ機能を再度実装する必要がある場合に、これらの関数を再利用できます。
これにより、コードの重複が減り、保守性が向上します。
"""

from flask import jsonify, request, current_app
import re, jwt, datetime, time
from functools import wraps

def validate_password(password):
    # 1. パスワードの長さが8文字以上であることを検証
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long.', 400

    # 2. 使用できる文字の範囲を定義（英数字と一部の特殊文字）
    pattern = re.compile(r'^[A-Za-z0-9@#$%^&+=\-*]+$')
    
    # パスワードが指定されたパターンに一致するかどうかを検証
    if not pattern.match(password):
        return False, 'Please use only alphanumeric characters and @ # $ % ^ & + = - *', 400

    # 3. 英語大文字、英語小文字、数字、記号がすべて入っているかを検証
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(char in '@#$%^&+=-*' for char in password)

    if not (has_upper and has_lower and has_digit and has_symbol):
        return False, 'Passwords must contain uppercase and lowercase letters, numbers, and symbols.', 400

    return True, None, 200

def generate_token(user):
    secret_key = current_app.config['SECRET_KEY']
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token
    

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # AuthorizationヘッダーからJWTを取得
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'JWTが必要です'}), 401

        try:
            # JWTの署名を検証
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

            # 有効期限を確認
            exp = payload['exp']
            if exp < time.time():
                return jsonify({'message': 'JWTが期限切れです'}), 401

            # その他の検証処理...

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'JWTが期限切れです'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '無効なJWTです'}), 401

        return f(*args, **kwargs)

    return decorated_function


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(f'token: {token}')
        if not token:
            return jsonify({'message': 'Token not found.'}), 401
        
        try:
            token_parts = token.split()
            payload = jwt.decode(token_parts[1], current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        # 認証が成功した場合の処理を行う
        return func(payload, *args, **kwargs)
    
    return wrapper

