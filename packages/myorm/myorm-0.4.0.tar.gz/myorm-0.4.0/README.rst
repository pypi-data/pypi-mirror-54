=====
myorm
=====
(Version 0.4.0)

*******
Purpose
*******
Provides an ORM for SQLite.

Usage
=====
To use the power of myorm you need to set up an adaptor and let your classed inherit from myorm.DbObject.

For example:
************
DbObject = myorm.DbObject
DbObject.adaptor = myorm.SQLiteAdaptor(database='database.db')

class User(DbObject):

    name = myorm.CharField(max_length=25)
    password = myorm.CharField(max_length=50)
    describtion = myorm.TextField()
    registered = myorm.DateField()
    logins = myorm.IntegerField()
    active = myorm.BooleanField(default=True)

Users automatically get an additional id which is an instance if myorm.PkField.

Instance methods:
***************************
    - .save()
        - Simply saves the object. If it is new, it will be created, if it already exists, it will be updated.
    - .delete()

Class methods
***********************
    - .create_table()
        - Function to create tables.
          The class which calls this function will get a table in the database.
          It DOES NOT provide migrations (at the moment), it simply creates a table.

The class provides an interface to create objects: The objects manager. It is available as in User.objects.get()

Manager operations:
*****************************
    User.objects

    - .all()
        - Returns all objects, unordered
    - .get(key=value)
        - E.g.: User.objects.get(id=2)
          Returns one object
    - .filter(key=value)
        - E.g.: User.objects.filter(active=True)
          Returns a list of objects (like `get` but returns more than one).
          key__lt, key__lte, key__gte and key__gt can be used to limit the results. lte means 'lower than equal',
          lt means 'lower than', gte means 'greater than equal' and gt means 'greater than'
          E.g. "logins__lt=10". This will return all users with less than 10 logins.
          The filters can be combined: User.objects.filter(logins__gte=10, logins__lte=50).

    - .exclude(key=value)
    - .create()
        - Used to create objects of the calling class. Takes fieldnames as kwargs. E.g. User.objects.create(name='Christian', ..)
          It returns the just created object.
    - .oder_by('name')
    - .count()


DbObject class methods
**********************
    DbObject

    - .raw(query, args)
        - The builtin SQL injection function. It simply executes queries and can be userd with arguments.
          It always returns what it fetches. Use it wisely.
          E.g. DbObject.raw("INSERT INTO user (name, description) VALUES (?, ?)", 'Christian', 'myorm developer.')


License
=======
myorm is available under the terms of the GPLv3.


Disclaimer
==========
This software comes without any warranty. You use it on your own risk. It may contain bugs, viruses or harm your software and hardware in another way. The developer is not responsible for any consequences which may occur caused by using the software.
