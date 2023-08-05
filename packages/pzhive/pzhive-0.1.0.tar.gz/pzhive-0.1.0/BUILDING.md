
### build
Now run this command from the same directory where setup.py is located:

```
python setup.py sdist bdist_wheel
```


### Upload

```
python -m twine upload  dist/*
```

### install

```
pip install pzhive
```

### Use

```
#!/usr/bin/env python
# coding=utf-8


from pzhive import pzhive

cursor = pzhive.connect_by_zk(zk_url="zk_host:2181",
                              zk_name_space="name_space",
                              auth="KERBEROS",
                              configuration={"hive.server2.proxy.user": "hadoop"},
                              kerberos_service_name="hive",
                              kerberos_service_host="xxx",
                              database="default")

cursor.execute("show tables")
print(cursor.fetchall())

```