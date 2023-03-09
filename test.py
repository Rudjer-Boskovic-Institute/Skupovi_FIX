import re

cityr = re.compile('alen', re.IGNORECASE)
result = cityr.search('vaLen')


print(result)


real_comp = re.compile(r'([0-9]+)')
print(real_comp.search('+123i').group())
