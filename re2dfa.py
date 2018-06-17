#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import LexicalAnalysis as la
import SyntaticalAnalysis as sa

printout=''
half=False
re='';
ok=False
for i in range(1,len(sys.argv)):
	if(sys.argv[i]=='-o' or sys.argv[i]=='-O' or sys.argv[i]=='--output'):
		if(isinstance(sys.argv[i+1], str)):
			printout=sys.argv[i+1]
			i=i+1
		else:
			ok=False
			break;
	elif(sys.argv[i]=='-h' or sys.argv[i]=='-H' or sys.argv[i]=='--Half-Process'):
		half=True
	elif(isinstance(sys.argv[i], str)):
		re=sys.argv[i]
		ok=True
	


if not ok:
	print ('Usage ./re2dfa.py \"Regular Expression\" [-o \"filename.pdf\"]')
else:
	l=la.LexicalAnalysis(re)
	l.createDictionary()
	s=sa.SyntaticalAnalysis(l)
	s.start()
	if half:
		print(s.geteNFA().tojson())
		if(printout!=''):
			s.eNFAToPDF(printout)
	else:
		print(s.getDFA().tojson())
		if(printout!=''):
			s.DFAToPDF(printout)