# -*- coding: utf-8 -*-
# @Time    : 2019/10/29 11:52
# @Author  : floatsliang
# @File    : cql.py
from typing import Union, List, Tuple

from .parser import parse_terms, parse_labels, parse_properties, parse_order_by

ROOT_CQL = {'Node', 'Relation', 'Match', 'Merge', 'Create'}


class _CQL(object):
    _params_set = {'pre_cql', 'post_cql'}

    def __init__(self, **kwargs):
        self._params = {}
        self._cql_tmpl = ''
        self.pre_cql = kwargs.pop('pre_cql') if 'pre_cql' in kwargs else ''
        if self.pre_cql and not isinstance(self.pre_cql, _CQL):
            raise Exception(u'ERROR: PRE CQL must be instance of CQL class and its subclasses')
        self.post_cql = kwargs.pop('post_cql') if 'post_cql' in kwargs else ''
        if not self.pre_cql and self.__class__.__name__ not in ROOT_CQL:
            raise Exception(u'ERROR: {} statement cannot be used as root CQL'.format(self.__class__.__name__))

    def __setattr__(self, key, value):
        if key in self._params_set:
            self._params[key] = value
        else:
            super(_CQL, self).__setattr__(key, value)

    def __getattr__(self, item):
        if item in self._params:
            return self._params[item]
        else:
            return super(_CQL, self).__getattribute__(item)

    def __add__(self, other):
        if isinstance(other, _CQL):
            root_cql = other
            while other.pre_cql:
                root_cql = other.pre_cql
            if getattr(self, root_cql.__class__.__name__, None):
                root_cql.pre_cql = self
            else:
                raise Exception(u'ERROR: {} statement cannot followed'
                                u' by {} statement'.format(self.__class__.__name__, root_cql.__class__.__name__))
            return other
        else:
            raise Exception(u'ERROR: non-CQL object {} cannot join with CQL object'.format(other.__class__))

    @property
    def cql(self):
        parsed_params = {}
        for k, v in self._params.items():
            parser = getattr(self, 'parse_' + k, None)
            if parser:
                parsed_params[k] = parser()
            else:
                parsed_params[k] = v
        return self._cql_tmpl.format(**parsed_params).strip()

    def parse_labels(self):
        if isinstance(self, Relation):
            return parse_labels(self._params.get('labels', []), '|')
        return parse_labels(self._params.get('labels', []))

    def parse_pre_cql(self):
        pre_cql = self._params.get('pre_cql', '')
        if pre_cql:
            pre_cql = pre_cql.cql
        return pre_cql


class Relation(_CQL):
    _params_set = {'pre_cql', 'rel_name', 'labels', 'depth', 'properties', 'post_cql'}

    def __init__(self, rel_name: str = '', labels: Union[List, str] = None, depth=None, **kwargs):
        super(Relation, self).__init__(**kwargs)
        self._cql_tmpl = u'{pre_cql} [{rel_name}{labels} {depth}{properties}] {post_cql}'
        self.rel_name = rel_name if rel_name else ''
        if labels:
            self.labels = labels if isinstance(labels, (list, tuple)) else [labels]
        else:
            self.labels = ''
        self.depth = depth if depth else ''
        self.properties = kwargs

    def parse_properties(self):
        parsed_properties = parse_properties(self._params.get('properties', {})) or ''
        if parsed_properties:
            parsed_properties = '{' + parsed_properties + '}'
        return parsed_properties

    def parse_depth(self):
        depth = self._params.get('depth', '')
        if isinstance(depth, (list, tuple)):
            min_depth, max_depth = depth
            depth = '*'
            if min_depth < 0 and max_depth < 0:
                return depth
            elif min_depth < 0:
                return depth + '..' + str(max_depth)
            elif max_depth < 0:
                return depth + str(min_depth) + '..'
            else:
                return depth + str(min_depth) + '..' + str(max_depth)
        else:
            return depth


class Node(_CQL):
    _params_set = {'pre_cql', 'node_name', 'labels', 'properties', 'post_cql'}

    def __init__(self, node_name: str = '', labels: Union[List, str] = None, **kwargs):
        super(Node, self).__init__(**kwargs)
        self._cql_tmpl = u'{pre_cql} ({node_name}{labels} {properties}) {post_cql}'
        self.node_name = node_name if node_name else ''
        if labels:
            self.labels = labels if isinstance(labels, list) else [labels]
        else:
            self.labels = ''
        self.properties = kwargs

    def parse_properties(self):
        parsed_properties = parse_properties(self._params.get('properties', {})) or ''
        if parsed_properties:
            parsed_properties = '{' + parsed_properties + '}'
        return parsed_properties

    def relationship(self, relationship: Relation, target_node):
        self.post_cql = '-' + relationship.cql + '- ' + target_node.cql
        return self

    def relationship_to(self, relationship: Relation, target_node):
        self.post_cql = '-' + relationship.cql + '-> ' + target_node.cql
        return self

    def relationship_from(self, relationship: Relation, target_node):
        self.post_cql = '<-' + relationship.cql + '- ' + target_node.cql
        return self


class Match(_CQL):
    _params_set = {'pre_cql', 'nodes', 'filters', 'post_cql'}

    def __init__(self, *nodes, **kwargs):
        super(Match, self).__init__(**kwargs)
        self._cql_tmpl = u'{pre_cql} MATCH {nodes} {filters} {post_cql}'
        if not nodes:
            raise Exception(u'ERROR: nodes of MATCH statement cannot be empty')
        self.nodes = nodes
        self.filters = kwargs

    def parse_nodes(self):
        nodes = self._params.get('nodes', [])
        parsed_nodes = []
        for node in nodes:
            parsed_nodes.append(node.cql)
        return ', '.join(parsed_nodes)

    def parse_filters(self):
        filters = self._params.get('filters', {})
        if filters:
            return 'WHERE ' + parse_terms(filters)
        else:
            return ''

    def Match(self, *nodes):
        return Match(pre_cql=self, *nodes)

    def Return(self, fields: Union[List[str], str], distinct: bool = False, order_by: List = None, skip: int = None, limit: int = None):
        return Return(fields=fields, distinct=distinct, order_by=order_by, skip=skip, limit=limit, pre_cql=self)

    def Create(self, *nodes: List[Node]):
        return Create(*nodes, pre_cql=self)

    def Delete(self, fields: Union[List, str], detach=False):
        return Delete(fields, pre_cql=self, detach=detach)

    def Set(self, **new_properties):
        if self.post_cql:
            raise Exception('ERROR: cannot SET MATCH statement twice')
        self.post_cql = 'SET ' + parse_properties(new_properties, '=')
        return self

    def Where(self, **terms):
        self.filters.update(terms)
        return self


class Return(_CQL):
    _params_set = {'pre_cql', 'distinct', 'fields', 'order_by', 'skip', 'limit', 'post_cql'}

    def __init__(self, fields: Union[List[str], str], distinct: bool = False, order_by: List = None, skip: int = None, limit: int = None,
                 **kwargs):
        super(Return, self).__init__(**kwargs)
        self._cql_tmpl = u'{pre_cql} RETURN {distinct} {fields} {order_by} {skip} {limit} {post_cql}'
        if not kwargs:
            raise Exception(u'ERROR: fields of RETURN statement cannot be empty')
        self.distinct = 'DISTINCT' if distinct else ''
        if not isinstance(fields, (List, Tuple)):
            fields = [fields]
        self.fields = fields
        self.order_by = order_by or ''
        self.skip = skip or ''
        self.limit = limit or ''

    def parse_fields(self):
        fields = self._params.get('fields', [])
        return ', '.join(fields)

    def parse_order_by(self):
        order_by = self._params.get('order_by', [])
        return parse_order_by(order_by) or ''


class Merge(_CQL):
    _params_set = {'pre_cql', 'node', 'post_cql'}

    def __init__(self, node: Node, **kwargs):
        super(Merge, self).__init__(**kwargs)
        self._cql_tmpl = u'{pre_cql} MERGE {node} {post_cql}'
        if not node:
            raise Exception(u'ERROR: properties of MERGE statement cannot be empty')
        self.node = node.cql

    def Set(self, **new_properties):
        if self.post_cql:
            raise Exception('ERROR: cannot SET MERGE statement twice')
        self.post_cql = 'SET ' + parse_properties(new_properties, '=')
        return self

    def Merge(self, node: Node):
        return Merge(node, pre_cql=self)

    def Create(self, *nodes: List[Node]):
        return Create(*nodes, pre_cql=self)

    def Return(self, fields: Union[List[str], str], distinct: bool = False, order_by: List = None, skip: int = None, limit: int = None):
        return Return(fields=fields, distinct=distinct, order_by=order_by, skip=skip, limit=limit, pre_cql=self)


class Create(_CQL):
    _params_set = {'pre_cql', 'nodes', 'post_cql'}

    def __init__(self, *nodes: List[Node], **kwargs):
        super(Create, self).__init__(**kwargs)
        self._cql_tmpl = u'{pre_cql} CREATE {nodes} {post_cql}'
        if not nodes:
            raise Exception(u'ERROR: properties of CREATE statement cannot be empty')
        self.nodes = nodes

    def parse_nodes(self):
        nodes = self._params.get('nodes', [])
        parsed_nodes = []
        for node in nodes:
            parsed_nodes.append(node.cql)
        return ', '.join(parsed_nodes)

    def Set(self, **new_properties):
        if self.post_cql:
            raise Exception('ERROR: cannot SET MERGE statement twice')
        self.post_cql = 'SET ' + parse_properties(new_properties, '=')
        return self

    def Merge(self, node: Node):
        return Merge(node, pre_cql=self)

    def Create(self, *nodes: List[Node]):
        return Create(*nodes, pre_cql=self)

    def Return(self, fields: Union[List[str], str], distinct: bool = False, order_by: List = None, skip: int = None, limit: int = None):
        return Return(fields=fields, distinct=distinct, order_by=order_by, skip=skip, limit=limit, pre_cql=self)


class Delete(_CQL):
    _params_set = {'pre_cql', 'detach', 'results', 'post_cql'}

    def __init__(self, fields: Union[List, str], detach=False, **kwargs):
        super(Delete, self).__init__(**kwargs)
        self._cql_tmpl = u'{pre_cql} {detach} DELETE {results} {post_cql}'
        if not fields:
            raise Exception(u'ERROR: results of DELETE statement cannot be empty')
        self.detach = 'DETACH' if detach else ''
        self.results = fields if isinstance(fields, (list, tuple)) else [fields]

    def parse_results(self):
        results = self._params.get('results', [])
        return ', '.join(results)

    def Merge(self, node: Node):
        return Merge(node, pre_cql=self)
