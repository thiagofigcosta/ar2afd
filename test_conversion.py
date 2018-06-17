#!/usr/bin/env python
# -*- coding: utf-8 -*-

import FiniteAutomata as FA

FAFA=FA.FiniteAutomata
lamb=FAFA.LAMBDA
t=FAFA(['1','2','3','4'],\
	['a','b','c'],\
	[FAFA.Edge('1','a','2'),FAFA.Edge('2',lamb,'1'),FAFA.Edge('2','b','3'),FAFA.Edge('3','a','2'),FAFA.Edge('4','c','3'),FAFA.Edge('4',lamb,'3'),FAFA.Edge('1','c','4')],\
	'1',\
	['3'])
print t.toDFA().tojson() 
