from .models import User
import time
import jwt


def to_models_list(users, secret):
    return [to_model(u, secret) for u in users]


def check_is_token_expired(user, secret):
    try:
        payload = user.decode_auth_token(user.auth_token, secret)
        now = int(time.time())  # sec
        # return payload['exp'] < now
        return False # no timeout dislogin due to site has https
    except jwt.ExpiredSignatureError:
        return True
    except jwt.InvalidTokenError:
        return True


def to_model(user, secret):
    is_token_expired = check_is_token_expired(user, secret)
    str_or_none = lambda x: str(x) if x else None

    return {
        'id': user.id,
        'created_date': user.created_date,
        'updated_date': user.updated_date,
        'email': user.email,
        'role': user.role.value if user.role else None,
        'is_token_expired': is_token_expired,

        'ace_theme': str_or_none(user.ace_theme),
        'color_background_primary': str_or_none(user.color_background_primary),
        'color_background_secondary': str_or_none(user.color_background_secondary),
        'color_background_action': str_or_none(user.color_background_action),
        'color_foreground_primary': str_or_none(user.color_foreground_primary),
        'color_foreground_secondary': str_or_none(user.color_foreground_secondary),
        'color_foreground_action': str_or_none(user.color_foreground_action),
        'color_background_success': str_or_none(user.color_background_success),
        'color_background_warning': str_or_none(user.color_background_warning),
        'color_background_error': str_or_none(user.color_background_error),
        'color_foreground_success': str_or_none(user.color_foreground_success),
        'color_foreground_warning': str_or_none(user.color_foreground_warning),
        'color_foreground_error': str_or_none(user.color_foreground_error),
    }


def from_register_model(model):
    get_or_none = lambda item, key: item[key] if key in item.keys() else None

    id = get_or_none(model, 'id')
    created_date = get_or_none(model, 'created_date')
    updated_date = get_or_none(model, 'updated_date')
    email = get_or_none(model, 'email')
    password = get_or_none(model, 'password')
    role = get_or_none(model, 'role')
    ace_theme = get_or_none(model, 'ace_theme')
    color_background_primary = get_or_none(model, 'color_background_primary')
    color_background_secondary = get_or_none(model, 'color_background_secondary')
    color_background_action = get_or_none(model, 'color_background_action')
    color_foreground_primary = get_or_none(model, 'color_foreground_primary')
    color_foreground_secondary = get_or_none(model, 'color_foreground_secondary')
    color_foreground_action = get_or_none(model, 'color_foreground_action')
    color_background_success = get_or_none(model, 'color_background_success')
    color_background_warning = get_or_none(model, 'color_background_warning')
    color_background_error = get_or_none(model, 'color_background_error')
    color_foreground_success = get_or_none(model, 'color_foreground_success')
    color_foreground_warning = get_or_none(model, 'color_foreground_warning')
    color_foreground_error = get_or_none(model, 'color_foreground_error')

    return User(id=id,
                created_date=created_date,
                updated_date=updated_date,
                email=email,
                role=role,
                color_background_primary=color_background_primary,
                color_background_secondary=color_background_secondary,
                color_background_action=color_background_action,
                color_foreground_primary=color_foreground_primary,
                color_foreground_secondary=color_foreground_secondary,
                color_foreground_action=color_foreground_action,
                color_background_success=color_background_success,
                color_background_warning=color_background_warning,
                color_background_error=color_background_error,
                color_foreground_success=color_foreground_success,
                color_foreground_warning=color_foreground_warning,
                color_foreground_error=color_foreground_error,
                ace_theme=ace_theme),\
        password


def does_email_exists(session, email):
    q = session.query(User).filter_by(email=email)
    res = session.query(q.exists()).scalar()

    return res
