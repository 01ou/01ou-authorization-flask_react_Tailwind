# api/auth.py

import jwt
from flask import Blueprint, jsonify, request, current_app
from backend.models.schema import add_user, verify_user, get_user_by_id
from backend.utils.util import generate_token, token_required

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json  # JSON データを取得
    
    # フォームデータから username と password を安全に取得する
    username = data.get('username')
    password = data.get('password')
    checkPassword = data.get('checkPassword')

    if password != checkPassword:
        return jsonify({'error': 'Passwords do not match.'}), 400

    # ユーザーの追加処理
    response, status_code, user = add_user(username, password)

    if status_code == 200:
        # ログイン成功時に認証トークンを生成
        token = generate_token(user)
        return jsonify({'token': token}), 200
    else:
        return jsonify(response), status_code


@bp.route('/login', methods=['POST'])
def login():
    data = request.json  # JSON データを取得
    
    # フォームデータから username と password を安全に取得する
    username = data.get('username')
    password = data.get('password')

    # ログインの確認
    response, status_code, user = verify_user(username, password)

    if status_code == 200:
        # ログイン成功時に認証トークンを生成
        token = generate_token(user)
        return jsonify({'token': token}), 200
    else:
        # ログイン失敗
        return jsonify(response), status_code


@bp.route('/logout', methods=['GET'])
def logout():
    return jsonify({'message': 'Successfully logged out'}), 200


@bp.route('/check_logging', methods=['GET'])
@token_required
def check_logging(payload):
    print(f'payload{payload}')
    return jsonify({'message': 'Access granted for user ' + str(payload['user_id'])}), 200


@bp.route('/get_user_info', methods=['GET'])
@token_required
def get_user_info(payload):
    user_id = payload['user_id']
    user, status_code = get_user_by_id(user_id)
    return jsonify({'user': user}), status_code

