from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy

class MyAdminSite(AdminSite):
    site_title = gettext_lazy('My site admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = gettext_lazy('COSTA ECOMMERCE')

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy('E-COMMERCE')

admin_site = MyAdminSite()