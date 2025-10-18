from django.contrib.auth.hashers import make_password, check_password

h = make_password('123456')
print('HASH', h)
print('OK', check_password('123456', h))
