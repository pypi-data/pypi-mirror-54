# access_dict_by_dot
Using this package, we can access the items in a dictionary using dot operator instead of writiting dict_name["key"].

## for example


from access_dict_by_dot import AccessDictByDot

dictionary = {
    'key1':'value1',
    'key2':'value2',
    'key3':{
                'subkey1':'subvalue1',
                'subkey2':'subvalue2'
            }
}


d = AccessDictByDot.load(dictionary)
print(d.key1)
print(d.key3.subkey1)






