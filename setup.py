try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages
setup(
    name = "django-native-datatables",
    version = "0.8.0",
    packages = find_packages(),
    author = "Christopher Keele",
    author_email = "email@chriskeele.com",
    description = "Add high-performance data-driven tables to your models, with full control template-side",
    url = "",
    include_package_data = True,
    zip_safe = False
)