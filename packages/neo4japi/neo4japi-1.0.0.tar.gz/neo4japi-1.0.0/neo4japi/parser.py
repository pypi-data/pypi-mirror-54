# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 17:11
# @Author  : floatsliang
# @File    : parser.py
import json
from typing import List, Tuple, Dict
from six import string_types


def _serialize(val):
    if isinstance(val, string_types):
        val = u"'{}'".format(val)
    elif isinstance(val, dict):
        val = u"'{}'".format(json.dumps(val))
    else:
        pass
    return val


def parse_labels(labels: List[str], div=':'):
    parsed_labels = []
    for label in labels:
        parsed_labels.append(label)
    return ':' + div.join(parsed_labels) if parsed_labels else ''


def parse_order_by(order_by: List[List or Tuple]) -> str:
    order_bys = []
    for field, order in order_by:
        order_bys.append(u'{} {}'.format(field, order))
    return ','.join(order_bys)


def parse_terms(terms: Dict) -> (str, str):
    filters = []
    for field, term in terms.items():
        if isinstance(term, (list, tuple)):
            op = term[1]
            if len(term) == 3:
                relation = u' {} '.format(term[2]).upper()
            else:
                relation = ' AND '
            values = term[0]
            if isinstance(values, (list, tuple)):
                values = list(values)
                for idx, val in enumerate(values):
                    values[idx] = _serialize(val)
                filters.append(u'({})'.format(
                    relation.join([u'{} {} {}'.format(field, op, val) for val in values])))
            else:
                values = _serialize(values)
                filters.append(u'{} {} {}'.format(field, op, values))
        else:
            term = _serialize(term)
            filters.append(u'{}={}'.format(field, term))
    filters = ' AND '.join(filters)
    return filters


def parse_properties(properties: Dict, eq=':'):
    property_list = []
    for key, val in properties.items():
        property_list.append(u'{}{}{}'.format(key, eq, _serialize(val)))
    properties = ', '.join(property_list)
    return properties
