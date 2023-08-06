# django_config

<!-- TOC -->

This is a basic django app that creates a table for EAV (Entity-Attribute-Value) configuration settings where each row has the following fields:

- application
- property_name
- property_value

It provides methods for retrieving configuration properties that allow for a default value to be passed in.  It is entirely in the admin and ORM layer, does not include an external-facing web app.  This is purposely not all that complicated or sophisticated.  If you want something more robust, there are other, better options.  This is quick and dirty.

# Installation

- This application, simple though it may be, has been updated to support django 1.7 and later, and with it the new built-in data migrations.

- Install django\_config application:

    - install django_config - Either:
    
        - install using pip:

                pip install django-basic-config
            
        - Clone code into your django site/project.

                git clone https://github.com/jonathanmorgan/django_config

    - add the `django_config.apps.Django_ConfigConfig` application to `INSTALLED_APPS`:
    
            INSTALLED_APPS = (
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'django.contrib.messages',
                'django.contrib.staticfiles',
                # Uncomment the next line to enable the admin:
                # 'django.contrib.admin',
                # Uncomment the next line to enable admin documentation:
                # 'django.contrib.admindocs',
                'django_config.apps.Django_ConfigConfig',
            )
        
    - install database tables
    
            python manage.py migrate django_config

# License

Copyright 2013-present (2019) Jonathan Morgan

This file is part of [https://github.com/jonathanmorgan/django_config](https://github.com/jonathanmorgan/django_config).

django_config is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

django_config is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with [https://github.com/jonathanmorgan/django_config](https://github.com/jonathanmorgan/django_config).  If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).