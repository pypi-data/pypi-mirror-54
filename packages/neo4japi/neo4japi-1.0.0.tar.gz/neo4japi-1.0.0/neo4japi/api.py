# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 17:04
# @Author  : floatsliang
# @File    : api.py
from neo4j import GraphDatabase, basic_auth, Transaction
from logging import getLogger
from typing import List, Dict, Union

from .cql import Node, Relation, Match, Merge, Create

DEFAULT_CONF = {
    "uri": "bolt://localhost",
    "auth": basic_auth("neo4j", "neo4j")
}

__all__ = ['Neo4jApi', 'Node', 'Relation']


class Neo4jApi(object):
    logger = getLogger("Neo4jApi")

    def __init__(self, config=None):
        if not config:
            config = DEFAULT_CONF
        self.driver = GraphDatabase.driver(**config)
        self._cli = self.driver.session()
        self._cql_stack = None

    def __enter__(self):
        self._cli.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cli.__exit__(exc_type, exc_val, exc_tb)

    def start_transaction(self):
        return self._cli.begin_transaction()

    def create_index(self, table=None, on=None, t=None):
        pass

    def unique(self, table=None, on=None, t=None):
        pass

    def exists(self, table=None, on=None, t=None):
        pass

    def select(self, fields: Union[List, str] = None, tables: Union[List, str] = None, distinct: bool = False,
               order_by: List = None, limit: int = None,
               offset: int = None, t: Transaction = None, result_name: str = 'nodes', **terms):
        """
        select node with condition
        :param result_name:
        :param distinct:
        :param fields:
        :param tables:
        :param order_by:
        :param limit:
        :param offset:
        :param t:
        :param terms:
        :return:
        """
        if not tables:
            raise Exception(u'ERROR: select node must have Labels/RelType')
        if not fields:
            fields = result_name
        if not isinstance(fields, (list, tuple)):
            fields = [fields]
        for idx, field in enumerate(fields):
            fields[idx] = u'{}.{}'.format(result_name, field)
        new_terms = {}
        for k, v in terms.items():
            new_terms[u'{}.{}'.format(result_name, k)] = v
        _cql = Match(Node(result_name, labels=tables)).Where(**new_terms).Return(fields=fields, distinct=distinct,
                                                                             order_by=order_by, limit=limit,
                                                                             skip=offset)
        self._cql_stack = self._cql_stack + _cql if self._cql_stack else _cql
        return self.execute(t)

    def get_one(self, fields=None, tables=None, order_by=None, offset=None, t=None, compile=False, return_name='result',
                **terms):
        return self.select(fields=fields, tables=tables, order_by=order_by, limit=1, offset=offset, t=t,
                           compile=compile, return_name=return_name, **terms)

    def save(self, tables: str = None, t: Transaction = None, compile: bool = False, **properties):
        """
        insert one node into neo4j (even already exists)
        :param compile:
        :param tables:
        :param t:
        :param properties:
        :return:
        """
        if not tables:
            raise Exception(u'ERROR: save node must have Labels/RelType')
        if properties:
            return self.insert([Node(labels=tables, **properties)], t=t, compile=compile)

    def insert(self, nodes: Union[List[Node], Node], t: Transaction = None, compile: bool = False):
        """
        insert many node into neo4j
        :param compile:
        :param nodes:
        :param t:
        :return:
        """
        if not nodes:
            return self
        if not isinstance(nodes, (list, tuple)):
            nodes = [nodes]
        _cql = Create(*nodes)
        self._cql_stack = self._cql_stack + _cql if self._cql_stack else _cql
        if compile:
            return self
        else:
            return self.execute(t)

    def select_by_nodes(self, nodes: Union[List[Node], Node], t: Transaction = None, compile: bool = False, result_name='nodes', **terms):
        if not nodes:
            raise Exception(u'ERROR: select node must have Labels/RelType')
        if not isinstance(nodes, (list, tuple)):
            nodes = [nodes]
        _cql = Match(*nodes)
        if terms:
            _cql.Where(**terms)
        self._cql_stack = self._cql_stack + _cql if self._cql_stack else _cql
        if compile:
            return self
        else:
            self._cql_stack.Return(fields=result_name)
            return self.execute(t)

    def select_or_insert(self, node: Node, t: Transaction = None, compile: bool = False, result_name=None):
        """
        insert or update node
        :param result_name:
        :param node:
        :param compile:
        :param t:
        :return:
        """
        if not node:
            raise Exception(u'ERROR: select or insert node must have Labels/RelType')
        _cql = Merge(node)
        self._cql_stack = self._cql_stack + _cql if self._cql_stack else _cql
        if compile:
            return self
        else:
            if result_name:
                self._cql_stack.Return(fields=result_name)
            return self.execute(t)

    def update(self,  node_name: str, new_properties: Dict = None, t: Transaction = None, compile: bool = False, result_name: str = None):
        _cql = self._cql_stack
        if not _cql:
            raise Exception(u'ERROR: update node/relationship must have Labels/RelType')
        if not new_properties:
            self.logger.warning('update node/relationship without giving values')
            return self
        properties = {}
        for k, v in new_properties.items():
            properties[u'{}.{}'.format(node_name, k)] = v
        _cql.Set(**properties)
        if compile:
            return self
        else:
            if result_name:
                self._cql_stack.Return(fields=result_name)
            return self.execute(t)

    def delete(self, detach=False, t=None, compile=False, fields: Union[List, str] = None, result_name: str = None):
        _cql = self._cql_stack
        if not _cql:
            raise Exception(u'ERROR: delete node must have Labels/RelType')
        if not isinstance(fields, (list, tuple)):
            fields = [fields]
        self._cql_stack = _cql.Delete(detach=detach, fields=fields)
        if compile:
            return self
        else:
            if result_name:
                self._cql_stack.Return(fields=result_name)
            return self.execute(t)

    def related(self, origin: Node, relation: Relation, target: Node, unique=True, t=None, compile=False, result_name=None):
        if not relation or not origin or not target:
            raise Exception(u'ERROR: create relationship must have relation and origin/target node')
        if unique:
            _cql = Merge(origin.relationship_to(relation, target))
        else:
            _cql = Create(origin.relationship_to(relation, target))
        self._cql_stack = self._cql_stack + _cql if self._cql_stack else _cql
        if compile:
            return self
        else:
            if result_name:
                self._cql_stack.Return(fields=result_name)
            return self.execute(t)

    def has_relation(self, origin: Node, relation: Relation, target: Node, direction=True, t=None, result_name='relation'):
        if not relation or not origin or not target:
            raise Exception(u'ERROR: search relationship must have relation type')
        if direction:
            _cql = Match(origin.relationship_to(relation, target))
        else:
            _cql = Match(origin.relationship(relation, target))
        _cql.Return(fields=result_name)
        return self.execute(t)

    def traverse(self):
        pass

    def look_around(self, origin_table, origin_properties, relation: Union[List, str] = None, relation_properties=None,
                    depth: int = 5, target_table=None, target_properties=None, return_name='target', t=None):
        if not origin_table or not origin_properties:
            raise Exception(u'ERROR: origin node must be accurately located when looking around it')
        if depth:
            depth = (1, depth)
        else:
            depth = (1, 5)
        _cql = Match(Node('origin', labels=origin_table, **origin_properties).relationship(
            Relation(labels=relation, depth=depth, **relation_properties),
            Node(return_name, labels=target_table, **target_properties)))
        _cql.Return(fields=return_name)
        return self.execute(t)

    def family(self):
        pass

    def results(self, fields: List[str], distinct: bool = False, order_by: List = None, skip: int = None, limit: int = None, compile=False, t=None):
        _cql = self._cql_stack
        if not _cql:
            raise Exception(u'ERROR: Return results statement cannot be used as root statement')
        self._cql_stack = _cql.Return(fields=fields, distinct=distinct, order_by=order_by, skip=skip, limit=limit)
        if compile:
            return self
        else:
            return self.execute(t)

    def execute(self, t=None):
        _conn = t if t else self._cli
        _cql = self._cql_stack.cql
        self._cql_stack = None
        return _conn.run(_cql)

    @property
    def query(self):
        return self._cql_stack.cql


