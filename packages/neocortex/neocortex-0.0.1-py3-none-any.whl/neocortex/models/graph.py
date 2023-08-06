#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tyler

==== Node Types ====
* User

* NeurotransmitterFamily
* Neurotransmitter


==== Edge Types ====



"""

from py2neo.ogm import GraphObject, Related, RelatedFrom, RelatedTo, Property, Label

class User(GraphObject):
    __primarykey__ = name

    name = Property()

class NeurotransmitterFamily(GraphObject):
    __primarykey__ = "name"

    name = Property()

    neurotransmitters = RelatedFrom("Neurotransmitter", "PARENT")

    owner = RelatedTo("User", "CREATEDBY")

class Neurotransmitter(GraphObject):
    __primarykey__ = "name"

    name = Property()

    family = RelatedTo("NeurotransmitterFamily", "PARENT")

    owner = RelatedTo("User", "CREATEDBY")

class NeuronalReceptor(GraphObject):
    __primarykey__ = "name"

    name = Property()

    family 