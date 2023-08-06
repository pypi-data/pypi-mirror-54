# K9

What is K9?  It is a helper library to simplify the automation 
of Kubernetes.

Tested with: 

kubernetes v10.0.1 

## Getting Started

Installing the library:

```shell
pip install -i https://test.pypi.org/simple/ k9==0.0.6
```

Here is a quick test, **test.py**

```python
import pprint

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(helper.list_namespaces())
```

Run it by: 
```shell
python3 test.py
```

## API Definition



### Utility Functions

#### def last_word(value: str)

This function returns the last word separated by a forward slash.  This is helpful when parsing out object names in strings delimited by forward slashes.  For example: 
```python

pod = last_word("pods/my-pod")
# The value of pod is: my-pod
```


