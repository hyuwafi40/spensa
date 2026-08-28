from .index import urlpatterns as index_urls, app_name
from .account import urlpatterns as account_urls
from .year import urlpatterns as year_urls
from .term import urlpatterns as term_urls
from .subject import urlpatterns as subject_urls
from .classroom import urlpatterns as classroom_urls
from .activeyear import urlpatterns as activeyear_urls
from .activesubject import urlpatterns as activesubject_urls
from .activeclassroom import urlpatterns as activeclassroom_urls
from .brand import urlpatterns as brand_urls
from .school import urlpatterns as school_urls
from .log import urlpatterns as log_urls
from .profile import urlpatterns as profile_urls

urlpatterns = (
    index_urls
    + account_urls
    + year_urls
    + term_urls
    + subject_urls
    + classroom_urls
    + activeyear_urls
    + activesubject_urls
    + activeclassroom_urls
    + brand_urls
    + school_urls
    + log_urls
    + profile_urls
)

__all__ = ["urlpatterns", "app_name"]
