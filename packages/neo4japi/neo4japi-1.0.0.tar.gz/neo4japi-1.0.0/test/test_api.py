# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 12:24
# @Author  : huziliang@corp.netease.com
# @File    : test_api.py
from neo4japi import *

data_source = {
    "id": 1,
    "name": 'haha',
    "deleted": True,
}
with Neo4jApi() as dbi:
    data_source['deleted'] = False
    dbi.select_or_insert(Node('set', labels='DATASET', id=123), compile=True).update({"deleted": False}, compile=True)
    dbi.select_or_insert(Node('src', labels='DATASOURCE', **data_source), compile=True)
    relation_cql = dbi.related(origin=Node('set'), relation=Relation(labels='BELONGS_TO'), target=Node('src'),
                               compile=True).query
with Neo4jApi() as dbi:
    insert_cql = dbi.insert(Node(labels='DATASOURCE', **data_source), compile=True).query
with Neo4jApi() as dbi:
    dbi.select_by_nodes(
        Node('ds', labels='DATASET', datasource_id=1).relationship(Relation('rel'), Node('sj', labels='SUB_DATAJOB')),
        compile=True)
    dbi.delete(detach=True, fields='sj', compile=True)
    delete_cql = dbi.update({"ds.deleted": 'true'}, compile=True).query
with Neo4jApi() as dbi:
    complicate_cql = dbi.select_by_nodes([Node('src_set', labels='DATASET', id=1).relationship(
        Relation(labels=['PROCESSING', 'PROCESSED'], depth=(-1, -1)),
        Node('sub_job', labels='SUB_JOB').relationship(
            Relation(labels=['PROCESSING', 'PROCESSED'], depth=(-1, -1)),
            Node('rel_set', labels='DATASET'))),
        Node('sub_ob').relationship(Relation(labels='BELONGS_TO'), Node('rel_job', labels='DATAJOB')),
        Node('src_set').relationship(Relation(labels='BELONGS_TO'), Node('data_src', labels='DATASOURCE')),
        Node('rel_set').relationship(Relation(labels='BELONGS_TO'), Node('data_src', labels='DATASOURCE'))],
        compile=True
    ).results(distinct=True, fields=['src_set', 'rel_set', 'rel_job', 'sub_job', 'data_src'], compile=True).query

print(relation_cql, '\n', delete_cql, '\n', insert_cql, '\n', complicate_cql)
