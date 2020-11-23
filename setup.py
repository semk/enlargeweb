try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='enlargeweb',
    version='0.2-',
    description='EnlargeWeb project is created to bring the power of cloud computing and web scalability to the world of hosting providers and companies.',
    author='Stanislav Yudin',
    author_email='decvar@gmail.com',
    url='http://code.google.com/p/enlargeweb/',
    install_requires=[
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5",
        "simplejson>=2.0.8",
        "repoze.who>=1.0.10",
        "repoze.who.plugins.formcookie>=0.2.3dev",
        "httplib2>=0.5.0"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'enlargeweb': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'enlargeweb': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = enlargeweb.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
