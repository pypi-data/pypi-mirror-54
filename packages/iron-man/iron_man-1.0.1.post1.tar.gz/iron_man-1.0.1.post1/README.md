# Project description

Iron-Man is a bloom filter based Cython & C. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple Instance around Redis.

Irom-Man offers suggestions, but doesn't enforce any dependencies or project layout. It is up to the developer to choose the tools and libraries they want to use.


# Installing

Install and update using pip:
```bash
pip install -U iron-man
```


# A Simple Example
```python
from iron_man import LocalBloomFilter

lbf = LocalBloomFilter(capacity=10000,error=0.0001)

# check item is it in filter
print(lbf.is_contain("content"))

# add item to filter
lbf.add("content")
print(lbf.is_contain("content"))
```

# Links
<ul>
<li>Releases: <a href="https://pypi.org/project/iron-man/">https://pypi.org/project/iron-man/</a></li>
<li>Code: <a href="http://gitlab.nuist.pro:3000/aberstone/IronMan.git">http://gitlab.nuist.pro:3000/aberstone/IronMan.git</a></li>
<li>Issue tracker: <a href="http://gitlab.nuist.pro:3000/aberstone/IronMan/issues">http://gitlab.nuist.pro:3000/aberstone/IronMan/issues</a></li>
</ul>