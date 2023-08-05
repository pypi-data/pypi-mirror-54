# ipdetector
This is a Simple project to categorize and validate private and public IP/IP ranges.

Category ID

* 0 : Private IP
* 1 : Public IP
* 2 : Private IP range
* 3 : Public IP range

Output : [<categoryID>, <data>]

## Installation

Run the following to install:

```python
pip install ipdetector
```

## Usage

```python
>>from ipdetector import ipCategorizer
>>ipCategorizer('192.168.1.0/24')
[2, '192.168.1.0/24']
>>
```
