#!/usr/bin/env python
# coding: utf-8

import cx_Oracle

from myorm.dbobject import DbObject
from myorm.fields import ForeignKey


class IsNull:
    """ Used as identifier for NULL values in query_args """

    def __init__(self):
        pass


class OracleAdaptor(object):

    def __init__(self, database_settings):
        self.database_settings = database_settings

    def get_connection_and_cursor(self):
        username = self.database_settings['username']
        password = self.database_settings['password']
        host = self.database_settings['host']
        sid = self.database_settings['sid']
        connection = cx_Oracle.connect(f"{username}/{password}@{host}/{sid}")
        cursor = connection.cursor()
        return connection, cursor

    def execute_query(self, query, query_args):
        connection, cursor = self.get_connection_and_cursor()
        if not query_args:
            cursor.execute(query)
        else:
            query_args = [q for q in query_args if not isinstance(q, IsNull)]
            cursor.execute(query, query_args)

        result = []
        if query.startswith("SELECT"):
            result = cursor.fetchall()

        last_id = 1
        if not query.startswith("INSERT"):
            last_id = None

        cursor.close()
        connection.close()
        return (result, last_id)

    def get_filter_query(self, filter_partial):
        key, value = list(filter_partial.items())[0]
        if key.endswith('__in'):
            query = ('%s IN (%s)' % (key.replace('__in', ''), ', '.join(["%s" for i in value])))
        elif key.endswith('__lt'):
            query = '%s < %s' % (key.replace('__lt', ''), '%s')
        elif key.endswith('__lte'):
            query = '%s <= %s' % (key.replace('__lte', ''), '%s')
        elif key.endswith('__gt'):
            query = '%s > %s' % (key.replace('__gt', ''), '%s')
        elif key.endswith('__gte'):
            query = '%s >= %s' % (key.replace('__gte', ''), '%s')
        else:
            if value is not None:
                query = '%s=%%s' % key
            else:
                query = '%s IS NULL' % key
                value = IsNull()
        return query, value

    def get_exclude_query(self, exclude_partial):
        key, value = list(exclude_partial.items())[0]
        if key.endswith('__in'):
            query = ('%s NOT IN (%s)' % (key.replace('__in', ''), ', '.join(["%s" for i in value])))
        elif key.endswith('__lt'):
            query = '%s >= %s' % (key.replace('__lt', ''), '%s')
        elif key.endswith('__lte'):
            query = '%s > %s' % (key.replace('__lte', ''), '%s')
        elif key.endswith('__gt'):
            query = '%s <= %s' % (key.replace('__gt', ''), '%s')
        elif key.endswith('__gte'):
            query = '%s < %s' % (key.replace('__gte', ''), '%s')
        else:
            if value is not None:
                query = '%s <> %%s' % key
            else:
                value = IsNull()
                query = '%s IS NOT NULL' % key
        return query, value

    def get_limit_query(self, limit):
        return f" LIMIT  {limit}"

    def get_select_query(self, base, *args, **kwargs):
        query = "SELECT %s FROM %s" % (', '.join(base.fieldnames), base.tablename)
        return query

    def get_insert_query(self, base, create_partial):
        values = []
        for field in base.fields:
            value = create_partial.get(field.fieldname)
            if isinstance(value, DbObject):
                value = value.id
            if value is None:
                try:
                    value = field.default
                except AttributeError:
                    pass
            values.append(value)
        query = "INSERT INTO %s (%s) VALUES (%s)" % (base.tablename,
                                                     ', '.join(base.fieldnames),
                                                     ', '.join([f":{idx}" for idx, item in enumerate(base.fields, start=1)]))
        return (query, tuple(values))

    def get_delete_query(self, base):
        query = "DELETE FROM %s " % base.tablename
        return query

    def get_update_query(self, base, update_partial):
        values = []
        affected_fields = []
        settings = ''
        for field in base.fields:
            value = update_partial.get(field.fieldname)
            if not value:
                pass
            else:
                values.append(value)
                affected_fields.append(field.fieldname)

        settings = ', '.join(['%s=%%s' % item for item in affected_fields])
        query = "UPDATE %s SET %s " % (base.tablename, settings)
        return (query, tuple(values))

    def bulk_create(self, objects, base):
        max_params = 2000
        max_inserts_per_query = int(max_params / len(base.fieldnames))
        iterations = (len(base.fieldnames) * len(objects)) / max_params

        lower = 0
        for i in range(0, int(iterations) + 1):
            lower = int(i * max_inserts_per_query)
            upper = int(lower + max_inserts_per_query)
            query, query_args = self.get_bulk_insert_query(objects[lower:upper], base)
            self.execute_query(query, query_args)

    def get_bulk_insert_query(self, objects, base):
        values = [tuple(getattr(item, fieldname) for fieldname in item.fieldnames) for item in objects]
        placeholders = ', '.join(['(%s)' % (', '.join(["%s" for i in item])) for item in values])
        query = '''INSERT INTO %s (%s) VALUES %s''' % (base.tablename, ', '.join(base.fieldnames), placeholders)
        return (query, tuple(v for tupl in values for v in tupl))

    def get_create_table_query(self, base, tablename):
        if not tablename:
            tablename = base.tablename
        query = "CREATE TABLE %s (%%s)" % tablename
        fk_fields = []
        fields = []
        fieldnames = []
        for field in base.fields:
            if isinstance(field, ForeignKey):
                fk_fields.append(field)
            fields.append(field)
            fieldnames.append(field.fieldname)

        field_queries = [field.partial_create_table_query for field in fields]

        for field in fk_fields:
            fieldnames.append(field.fieldname)
        field_queries.extend([field.partial_create_table_query_extension for field in fk_fields])

        query = query % ', '.join(field_queries)
        query = query % tuple(fieldnames)
        return (query, None)

    def get_drop_table_query(self, base, tablename):
        if not tablename:
            tablename = base.tablename
        query = "DROP TABLE %s;" % tablename
        return (query, None)

    def get_pkfield_create_query(self):
        return '%s NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY'

    def get_integer_field_create_query(self, field):
        query = '%s NUMBER'
        if field.default is not None:
            query += ' DEFAULT %s' % field.default
        return query

    def get_char_field_create_query(self, field):
        query = '%%s VARCHAR(%s)' % field.max_length
        if field.default is not None:
            query += ' DEFAULT %s' % field.default
        return query

    def get_charfield_create_column_query(self, field):
        query = 'ALTER TABLE %%s ADD COLUMN %s VARCHAR(%s)' % (field.fieldname, field.max_length)
        if field.default is not None:
            query += ' DEFAULT %s' % field.default
        return query

    def get_text_field_create_query(self):
        return '%s TEXT'

    def get_datetime_field_create_query(self, default):
        if default is None:
            return '%s TIMESTAMP NULL DEFAULT NULL'
        elif default == 'now':
            return '%s TIMESTAMP DEFAULT CURRENT_TIMESTAMP'

    def get_boolean_field_create_query(self, default):
        return '(%%s NUMBER(1) NOT NULL CHECK (%%s in (0,1) DEFAULT %s' % default

    def get_foreignkey_field_create_query_base(self):
        return '%s NUMBER'

    def get_foreignkey_field_create_query_extension(self, reference):
        if type(DbObject) == type(reference):
            reference = reference.tablename
        return 'FOREIGN KEY(%%s) REFERENCES %s(id)' % (reference)

    def create_migration_table(self):
        query = """CREATE TABLE IF NOT EXISTS myorm_migrations
                    (name VARCHAR(250), id INTEGER PRIMARY KEY AUTO_INCREMENT)"""
        self.execute_query(query, None)

    def get_done_migrations(self):
        query = "SELECT id, name FROM myorm_migrations"
        return self.execute_query(query, None)

    def insert_migration(self, name):
        query = "INSERT INTO myorm_migrations (name) VALUES (%s)"
        return self.execute_query(query, (name,))
