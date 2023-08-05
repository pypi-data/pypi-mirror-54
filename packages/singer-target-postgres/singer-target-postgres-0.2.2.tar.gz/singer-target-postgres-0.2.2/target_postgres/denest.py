from copy import deepcopy

from target_postgres import json_schema
from target_postgres.singer_stream import (
    SINGER_LEVEL,
    SINGER_SEQUENCE,
    SINGER_SOURCE_PK_PREFIX,
    SINGER_VALUE
)


def to_table_batches(schema, key_properties, records):
    """
    Given a schema, and records, get all table schemas and records and prep them
    in a `table_batch`.

    :param schema: SingerStreamSchema
    :param key_properties: [string, ...]
    :param records: [{...}, ...]
    :return: [{'streamed_schema': TABLE_SCHEMA(local),
               'records': [{(path_0, path_1, ...):
                            (_json_schema_string_type, value), ...},
                            ...]},
              ...]
    """
    table_schemas = _get_streamed_table_schemas(schema,
                                                key_properties)

    table_records = _get_streamed_table_records(key_properties,
                                                records)
    writeable_batches = []
    for table_json_schema in table_schemas:
        writeable_batches.append({'streamed_schema': table_json_schema,
                                  'records': table_records.get(table_json_schema['path'], [])})

    return writeable_batches


def _get_streamed_table_schemas(schema, key_properties):
    """
    Given a `schema` and `key_properties` return the denested/flattened TABLE_SCHEMA of
    the root table and each sub table.

    :param schema: SingerStreamSchema
    :param key_properties: [string, ...]
    :return: [TABLE_SCHEMA(denested_streamed_schema_0), ...]
    """
    root_table_schema = json_schema.simplify(schema)

    subtables = {}
    key_prop_schemas = {}
    for key in key_properties:
        key_prop_schemas[key] = schema['properties'][key]
    _denest_schema(tuple(), root_table_schema, key_prop_schemas, subtables)

    ret = [_to_table_schema(tuple(), None, key_properties, root_table_schema['properties'])]
    for path, schema in subtables.items():
        ret.append(_to_table_schema(path, schema['level'], schema['key_properties'], schema['properties']))

    return ret


def _to_table_schema(path, level, keys, properties):
    for key in keys:
        if not (key,) in properties:
            raise Exception('Unknown key "{}" found for table "{}". Known fields are: {}'.format(
                key, path, properties
            ))

    return {'type': 'TABLE_SCHEMA',
            'path': path,
            'level': level,
            'key_properties': keys,
            'mappings': [],
            'schema': {'type': 'object',
                       'additionalProperties': False,
                       'properties': properties}}


def _literal_only_schema(schema):
    ret = deepcopy(schema)

    ret_type = json_schema.get_type(ret)

    if json_schema.is_object(ret):
        ret_type.remove(json_schema.OBJECT)
    if json_schema.is_iterable(ret):
        ret_type.remove(json_schema.ARRAY)

    ret['type'] = ret_type

    return ret


def _denest_schema_helper(table_path,
                          prop_path,
                          table_json_schema,
                          nullable,
                          top_level_schema,
                          key_prop_schemas,
                          subtables,
                          level):
    for prop, item_json_schema in table_json_schema['properties'].items():
        if json_schema.is_object(item_json_schema):
            _denest_schema_helper(table_path + (prop,),
                                  prop_path + (prop,),
                                  item_json_schema,
                                  nullable,
                                  top_level_schema,
                                  key_prop_schemas,
                                  subtables,
                                  level)

        if json_schema.is_iterable(item_json_schema):
            _create_subtable(table_path + (prop,),
                             item_json_schema,
                             key_prop_schemas,
                             subtables,
                             level + 1)

        if json_schema.is_literal(item_json_schema):
            if nullable and not json_schema.is_nullable(item_json_schema):
                item_json_schema['type'].append('null')

            top_level_schema[prop_path + (prop,)] = _literal_only_schema(item_json_schema)


def _create_subtable(table_path, table_json_schema, key_prop_schemas, subtables, level):
    if json_schema.is_object(table_json_schema['items']):
        new_properties = table_json_schema['items']['properties']
    else:
        new_properties = {SINGER_VALUE: table_json_schema['items']}

    key_properties = []
    for pk, item_json_schema in key_prop_schemas.items():
        key_properties.append(SINGER_SOURCE_PK_PREFIX + pk)
        new_properties[SINGER_SOURCE_PK_PREFIX + pk] = item_json_schema

    new_properties[SINGER_SEQUENCE] = {
        'type': ['null', 'integer']
    }

    for i in range(0, level + 1):
        new_properties[SINGER_LEVEL.format(i)] = {
            'type': ['integer']
        }

    new_schema = {'type': [json_schema.OBJECT],
                  'properties': new_properties,
                  'level': level,
                  'key_properties': key_properties}

    _denest_schema(table_path, new_schema, key_prop_schemas, subtables, level=level)

    subtables[table_path] = new_schema


def _denest_schema(table_path, table_json_schema, key_prop_schemas, subtables, level=-1):
    new_properties = {}
    for prop, item_json_schema in table_json_schema['properties'].items():

        if json_schema.is_object(item_json_schema):
            _denest_schema_helper(table_path + (prop,),
                                  (prop,),
                                  item_json_schema,
                                  json_schema.is_nullable(item_json_schema),
                                  new_properties,
                                  key_prop_schemas,
                                  subtables,
                                  level)

        if json_schema.is_iterable(item_json_schema):
            _create_subtable(table_path + (prop,),
                             item_json_schema,
                             key_prop_schemas,
                             subtables,
                             level + 1)

        if json_schema.is_literal(item_json_schema):
            new_properties[(prop,)] = _literal_only_schema(item_json_schema)

    table_json_schema['properties'] = new_properties


def _get_streamed_table_records(key_properties, records):
    """
    Flatten the given `records` into `table_records`.
    Maintains `key_properties`.
    into `table_records`.

    :param key_properties: [string, ...]
    :param records: [{...}, ...]
    :return: {TableName string: [{(path_0, path_1, ...): (_json_schema_string_type, value), ...}, ...],
              ...}
    """

    records_map = {}
    _denest_records(tuple(),
                    records,
                    records_map,
                    key_properties)

    return records_map


def _denest_subrecord(table_path,
                      prop_path,
                      parent_record,
                      record,
                      records_map,
                      key_properties,
                      pk_fks,
                      level):
    """"""
    """
    {...}
    """
    for prop, value in record.items():
        """
        str : {...} | [...] | ???None??? | <literal>
        """

        if isinstance(value, dict):
            """
            {...}
            """
            _denest_subrecord(table_path + (prop,),
                              prop_path + (prop,),
                              parent_record,
                              value,
                              records_map,
                              key_properties,
                              pk_fks,
                              level)

        elif isinstance(value, list):
            """
            [...]
            """
            _denest_records(table_path + (prop,),
                            value,
                            records_map,
                            key_properties,
                            pk_fks=pk_fks,
                            level=level + 1)

        elif value is None:
            """
            None
            """
            continue

        else:
            """
            <literal>
            """
            parent_record[prop_path + (prop,)] = (json_schema.python_type(value), value)


def _denest_record(table_path, record, records_map, key_properties, pk_fks, level):
    """"""
    """
    {...}
    """
    denested_record = {}
    for prop, value in record.items():
        """
        str : {...} | [...] | None | <literal>
        """

        if isinstance(value, dict):
            """
            {...}
            """
            _denest_subrecord(table_path + (prop,),
                              (prop,),
                              denested_record,
                              value,
                              records_map,
                              key_properties,
                              pk_fks,
                              level)

        elif isinstance(value, list):
            """
            [...]
            """
            _denest_records(table_path + (prop,),
                            value,
                            records_map,
                            key_properties,
                            pk_fks=pk_fks,
                            level=level + 1)

        elif value is None:
            """
            None
            """
            continue

        else:
            """
            <literal>
            """
            denested_record[(prop,)] = (json_schema.python_type(value), value)

    if table_path not in records_map:
        records_map[table_path] = []
    records_map[table_path].append(denested_record)


def _denest_records(table_path, records, records_map, key_properties, pk_fks=None, level=-1):
    row_index = 0
    """
    [{...} ...] | [[...] ...] | [literal ...]
    """
    for record in records:
        if pk_fks:
            record_pk_fks = pk_fks.copy()
            record_pk_fks[SINGER_LEVEL.format(level)] = row_index

            if not isinstance(record, dict):
                """
                [...] | literal
                """
                record = {SINGER_VALUE: record}

            for key, value in record_pk_fks.items():
                record[key] = value
            row_index += 1
        else:  ## top level
            record_pk_fks = {}
            for key in key_properties:
                record_pk_fks[SINGER_SOURCE_PK_PREFIX + key] = record[key]
            if SINGER_SEQUENCE in record:
                record_pk_fks[SINGER_SEQUENCE] = record[SINGER_SEQUENCE]

        """
        {...}
        """
        _denest_record(table_path, record, records_map, key_properties, record_pk_fks, level)
