from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message
from decouple import config

url_safe_timed_serializer = URLSafeTimedSerializer(config('URL_SAFE_TIMED_SERIALIZER_SECRET_KEY'))
mail = None


def generate_token(email):
    return url_safe_timed_serializer.dumps(email, salt='salt')


def send_email(email, header, body):
    msg = Message(header, sender='jeweltry-shop@yahoo.com', recipients=[email])
    msg.body = body
    mail.send(msg)


def retrieve_email(token):
    try:
        email = url_safe_timed_serializer.loads(token, salt='salt', max_age=3600)
        return email
    except SignatureExpired:
        return False
