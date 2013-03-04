#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from uuid import uuid4

uid = uuid4()

print type(uid)

uid  # ne marche que dans un shell

str(uid)

print uid.bytes

print uid.get_version()

print uid.int # pratique pour stocker comme un nombre



print uuid4() == uuid4()

uid = uuid4()

print uid == uid

print uid

print str(uid) == "837806a7-6c37-4630-9f6c-9aa7ad0129ed"


from uuid import UUID


UUID(int=160073875847165073709894672235460141549, version=4)