from django.core.cache import cache


def get_attempt_key(request, username):
    ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
    return f"login_attempt_{ip}_{username}"


def is_login_blocked(request, username):
    key = get_attempt_key(request, username)
    attempts = cache.get(key, 0)
    return attempts >= 5


def record_failed_login(request, username):
    key = get_attempt_key(request, username)
    attempts = cache.get(key, 0)
    cache.set(key, attempts + 1, timeout=300)


def clear_login_attempts(request, username):
    key = get_attempt_key(request, username)
    cache.delete(key)
