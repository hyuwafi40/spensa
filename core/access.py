from core.utils.constants import JobChoices


def is_authenticated(user):
    return getattr(user, "is_authenticated", False)


def is_developer(user):
    return (
        is_authenticated(user)
        and user.is_active
        and user.job == JobChoices.DEVELOPER
        and user.is_staff
        and user.is_superuser
    )


def is_administrator(user):
    return (
        is_authenticated(user)
        and user.is_active
        and user.job == JobChoices.ADMINISTRATOR
        and user.is_staff
        and not user.is_superuser
    )


def is_teacher(user):
    return (
        is_authenticated(user)
        and user.is_active
        and user.job == JobChoices.TEACHER
        and not user.is_staff
        and not user.is_superuser
    )


def is_student(user):
    return (
        is_authenticated(user)
        and user.is_active
        and user.job == JobChoices.STUDENT
        and not user.is_staff
        and not user.is_superuser
    )


def has_role(user, *roles):
    if not is_authenticated(user) or not user.is_active:
        return False
    return user.job in roles
