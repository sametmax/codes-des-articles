#!/usr/bin/env python
# -*- coding: utf-8 -*-

t = (1, 2)
print t
## (1, 2)
print type(t)
## <type 'tuple'>



t = 1, 2
print t
## (1, 2)


a, b = (1, 2)
print a
## 1
print b
## 2



def foo():
    return 1, 2

print foo()
## (1, 2)
print type(foo())
## <type 'tuple'>
a, b = foo()
print a
## 1
print b
## 2



t = "a" in ("b", "a")
print t
## True
t = "a" in "b", "a"
print t
## (False, 'a')



try:
    s = "Ceci est un %s %s" % "test", "idiot"
    print s
except TypeError as e:
    print e
## not enough arguments for format string


s = "Ceci est un %s" % "test", "idiot"
print s
## ('Ceci est un test', 'idiot')

s = "Ceci est un %s %s" % ("test", "idiot")
print s
## Ceci est un test idiot


