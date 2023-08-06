```python

from pyseri import serializer

class A():
	name = 'class a'

class B():
	name = 'class b'
	a = [A(), A(), A()]

serializer.dump(B(), mapper={'A': {'name'}, 'B':{'name', 'a'}})

#output
"""
{
	'name': 'class b',
	'a': [
		{'name': 'class a'}, 
		{'name': 'class a'},
		 {'name': 'class a'}
	 ]
}
"""
```

```python

from pyseri import serializer

class A():
	getters = ['name']
	#this key is important
	name = 'class a'

class B():
	getters = ['name', 'a']
	#this key is important
	name = 'class b'
	a = [A(), A(), A()]

serializer.dump(B())

#output
"""
{
	'a': [
		{'name': 'class a'}, 
		{'name': 'class a'}, 
		{'name': 'class a'}
	],
	'name': 'class b'}
"""