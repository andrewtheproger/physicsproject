from models import Task, User
import time
import jwt


def to_models_list(users, secret):
    return [to_model(u, secret) for u in users]


def check_is_token_expired(user, secret):
    try:
        payload = user.decode_auth_token(user.auth_token, secret)
        now = int(time.time())  # sec
        return payload['exp'] < now
    except jwt.ExpiredSignatureError:
        return True
    except jwt.InvalidTokenError:
        return True


def to_model(user, secret):
    is_token_expired = check_is_token_expired(user, secret)

    return {
        'id': user.id,
        'created_date': user.created_date,
        'updated_date': user.updated_date,
        'login': user.login,
        'role': user.role.value if user.role else None,
        'is_token_expired': is_token_expired
    }


def from_register_model(model):
    get_or_none = lambda item, key: item[key] if key in item.keys() else None

    id = get_or_none(model, 'id')
    created_date = get_or_none(model, 'created_date')
    updated_date = get_or_none(model, 'updated_date')
    login = get_or_none(model, 'login')
    password = get_or_none(model, 'password')
    role = get_or_none(model, 'role')

    return User(id=id,
                created_date=created_date,
                updated_date=updated_date,
                login=login,
                role=role),\
        password


def does_login_exists(session, login):
    q = session.query(User).filter_by(login=login)
    res = session.query(q.exists()).scalar()

    return res
