from collections import namedtuple
from core.utils.constants import COMMON_PROFILE_FIELDS, ROLE_PROFILE_FIELDS
from core.utils.collections import PROFILE_FIELD_CONFIG

ProfileFieldItem = namedtuple("ProfileFieldItem", ["label", "value", "icon"])


def get_profile_fields(user, profile):
    fields = [
        ProfileFieldItem("Username", user.username, "fa-user"),
        ProfileFieldItem("Nama Lengkap", user.get_full_name() or "-", "fa-id-badge"),
        ProfileFieldItem("Email", user.email or "-", "fa-envelope"),
        ProfileFieldItem("Role", user.get_job_display(), "fa-user-tag"),
    ]

    if not profile:
        return fields

    allowed_fields = COMMON_PROFILE_FIELDS.copy()
    if user.job:
        allowed_fields += ROLE_PROFILE_FIELDS.get(user.job, [])

    for field_name in allowed_fields:
        if field_name == "photo":
            continue

        config = PROFILE_FIELD_CONFIG.get(field_name)
        if not config:
            continue

        raw_value = getattr(profile, field_name, None)

        if config.type == "choice":
            method_name = config.display_method
            value = getattr(profile, method_name)() if raw_value else "-"
        elif config.type == "date":
            value = raw_value.strftime("%d %b %Y") if raw_value else "-"
        elif config.type == "unit":
            if raw_value is not None:
                value = f"{raw_value} {config.unit}"
            else:
                value = "-"
        else:
            value = raw_value if raw_value else "-"

        fields.append(ProfileFieldItem(config.label, value, config.icon))

    return fields
