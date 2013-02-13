from setuptools import setup, find_packages
import os

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()



if 'sdist' in sys.argv:
    # clear compiled mo files before building the distribution
    walk = os.walk(os.path.join(os.getcwd(), 'autocomplete_light/locale'))
    for dirpath, dirnames, filenames in walk:
        if not filenames:
            continue

        if 'django.mo' in filenames:
            os.unlink(os.path.join(dirpath, 'django.mo'))
            print 'unlink', os.path.join(dirpath, 'django.mo')
else:
    # if django is there, compile the po files to mo,
    try:
        import django
    except ImportError:
        pass
    else:
        dir = os.getcwd()
        os.chdir(os.path.join(dir, 'autocomplete_light'))
        os.system('django-admin.py compilemessages')
        os.chdir(dir)


setup(
    name='django-session-security',
    version='1.2.0',
    description='Let the user secure his session for usage in public computers',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://github.com/yourlabs/django-session-expiry',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'),
    license = 'MIT',
    keywords = 'django session',
    install_requires=[
        'django',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

