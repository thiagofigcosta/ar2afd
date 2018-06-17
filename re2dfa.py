#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import LexicalAnalysis as la
import SyntaticalAnalysis as sa

printtopdf=False
if len(sys.argv)==2 and isinstance(sys.argv[1], str):
	pass
elif len(sys.argv)==4 and isinstance(sys.argv[1], str) and (sys.argv[2]=='-o' or sys.argv[2]=='-O' or sys.argv[2]=='--output') and isinstance(sys.argv[3], str):
	printtopdf=True
else:
	print ('Usage ./re2dfa.py \"Regular Expression\" [-o \"filename.pdf\"]')
	raise SystemExit()

l=la.LexicalAnalysis()
l.createDictionary()
s=sa.SyntaticalAnalysis(l)
s.start()
print(s.getDFA().tojson())
if(printtopdf):
	s.eNFAToPDF(sys.argv[3])



# string=''
# for i in range(40):
# 	string=string+'-'
# string=string	
# print (string)
# print('RE=',l.getRE())
# print (string)
# print(s.geteNFA().tojson())
# print (string)
# 
# s.eNFAToPDF()

# t=FA(['1','2','3','4'],\
# 	['a','b','c'],\
# 	[Edge('1','a','2'),Edge('2',FA.LAMBDA,'1'),Edge('2','b','3'),Edge('3','a','2'),Edge('4','c','3'),Edge('4',FA.LAMBDA,'3'),Edge('1','c','4')],\
# 	'1',\
# 	['3'])
# print t.toDFA().tojson()