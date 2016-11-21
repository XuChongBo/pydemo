#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from py2neo import Graph, Node, Relationship, watch, authenticate
watch('httpstream')

"""
# 方式1：
g = Graph(host="localhost", password='password',bolt=True, bolt_port=7689)
print g.data('match (n) return count(*)')
sys.exit(1)
"""

# 方式2:  *****访问被代理或docker 容器中的 neo4j server的话，只能用这种方式 *********
# set up authentication parameters
http_port = "7476"
authenticate("localhost:"+http_port, "username", "password")
# connect to authenticated graph database
g = Graph("http://localhost:"+http_port+"/db/data/", bolt_port=7689)


g.data('match (n) return count(*)')
g.run('match (n) return count(*)').dump()


# import data in one transaction
tx = g.begin()
a = Node("Person", name="Alice")
b = Node("Person", name="Bob")
tx.create(a)
ab = Relationship(a, "KNOWS", b)
tx.create(ab)
#tx.commit()
print g.exists(ab)

# get nodes in one autocommit transaction
g.run("MATCH (a:Person) RETURN a.name, a.born LIMIT 4").data()

# get 
g.run('match (n) return count(*)').dump()
