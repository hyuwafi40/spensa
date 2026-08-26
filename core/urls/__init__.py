from .index import urlpatterns as index_urls, app_name
from .account import urlpatterns as account_urls

urlpatterns = index_urls + account_urls

__all__ = ["urlpatterns", "app_name"]
