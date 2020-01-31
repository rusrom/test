import redis
from resources.user import UserModel


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

r = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)


def authenticate(username, password):
    user = UserModel.find_by_username(username)

    attempts = r.get(username)

    # 5 min block trigger
    if attempts and int(attempts) == 5:
        return None

    if user and user.password == password:
        return user

    # Attempts counter
    if attempts:
        # Blocking
        if r.incr(username) == 5:
            r.setex(username, 300, 5)
    else:
        r.setex(username, 60, 1)


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
