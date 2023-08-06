Wagtailpress
============

A Blog build with Wagtail. Its name is not a reference to Wordpress,
but the name wagtail_blog is already taken.


Features
--------

- Index page model
- Article page model
- Authors are defined using [Wagtail person](https://framagit.org/SebGen/wagtailperson)
- Tags
- RSS feed for index pages
- Delivred with acceptable templates


Install
-------

Simply install it from pypi.org:
```bash
pip install wagtailpress
```

Add this app and dependencies to django installed app in your
settings.py:
```bash
INSTALLED_APPS = [
    # …
    'wagtail.contrib.routable_page',
    'wagtailperson',
    'wagtailpress',
    # …
    ]
```

Then, finally, apply migration scripts:
```bash
./manage.py migrate wagtailpress
```


Use
---

This application provide 2 pages models:

-   A blog article page: A simple article
-   A blog index page: The index of your blog, it list its children
    articles, their tags and provide a RSS feed

A blog article page got multiple fields:
-   Title
-   Publication date
-   One or some authors
-   An intro 
-   An optional header image
-   The content of the article


Development
-----------

This source code repository provide a full Django project, so you can
easily work with wagtailperson for testing you modifications.

Simply use these two steps in the source code working directory: 
```bash
./manage.py migrate 
./manage.py runserver 
```


Test
----

To run test, simply run this in the root of the source code working directory:
```bash
./manage.py test
```


Licence 
-------

LGPLv3


Author(s)
---------

Sébastien Gendre <seb@k-7.ch>



