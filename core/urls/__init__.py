from .index import urlpatterns as index_urls, app_name
from .account import urlpatterns as account_urls
from .year import urlpatterns as year_urls
from .term import urlpatterns as term_urls
from .subject import urlpatterns as subject_urls
from .classroom import urlpatterns as classroom_urls
from .activeyear import urlpatterns as activeyear_urls
from .activesubject import urlpatterns as activesubject_urls
from .activeclassroom import urlpatterns as activeclassroom_urls

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
)

__all__ = ["urlpatterns", "app_name"]
