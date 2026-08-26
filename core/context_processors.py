from django.core.cache import cache
from core.menu import get_menus_for_user
from core.models import Brand, School


def core_context(request):
    brand = cache.get("core_brand")
    if brand is None:
        brand = Brand.get_solo()
        cache.set("core_brand", brand, 300)

    school = cache.get("core_school")
    if school is None:
        school = School.get_solo()
        cache.set("core_school", school, 300)

    return {
        "menus": get_menus_for_user(request.user),
        "brand": brand,
        "school": school,
    }
