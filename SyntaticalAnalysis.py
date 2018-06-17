#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import LexicalAnalysis as LA
import FiniteAutomata as FA

class SyntaticalAnalysis(object):
	def __init__(self, lexical):
		self.lexical=lexical
		self.current=lexical.nextToken()
		self.basename=0
		self.eNFA=None
		self.DFA=None

	def popToken(self):
		t=self.current.getToken()
		self.consumeToken()
		return t
	def getToken(self):
		return self.current.getToken()
	def testToken(self,ttype):
		return self.current.getType()==ttype
	def consumeToken(self):
		self.current=self.lexical.nextToken()
	def matchToken(self,ttype):
		if self.testToken(ttype):
			self.current=self.lexical.nextToken()
		else:
			print('ERRRORRR-001 expected ',ttype.name,', but got ',self.current.getType().name)
			raise SystemExit()

	def genStateName(self):
		def baseN(num,b,numerals="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
			return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])
		name=baseN(self.basename,26)
		self.basename=self.basename+1
		return name
		
	def start(self):
		self.eNFA=self.procExpr()
		self.DFA=self.eNFA.toDFA() 

	def geteNFA(self):
		return self.eNFA

	def getDFA(self):
		return self.DFA

	def toPDF(self,json,out):
		json=json.replace('\"', '\\\"')
		subprocess.call('echo \"'+json+'\" > tmp.json', shell=True)
		subprocess.call('./json2dot.sh tmp.json > tmp.dot', shell=True)
		subprocess.call('dot -Tpdf -o '+out+' tmp.dot', shell=True)
		subprocess.call('rm -f tmp.json tmp.dot', shell=True)

	def eNFAToPDF(self,out):
		self.toPDF(self.eNFA.tojson(),out)

	def DFAToPDF(self,out):
		self.toPDF(self.DFA.tojson(),out)

	def procExpr(self):
		a=self.procTerm()
		while self.testToken(LA.TokenType.CROSS):
			self.consumeToken()
			b=self.procTerm()
			a.merge(b,'+')
		return a

	def procTerm(self):
		a=self.procFactor()
		while self.testToken(LA.TokenType.SYMBOL) or self.testToken(LA.TokenType.OPENTHEPAR):
			b=self.procFactor()
			a.merge(b,'.')
		return a

	def procFactor(self):
		a=None
		if self.testToken(LA.TokenType.SYMBOL):
			a=self.procSymbol()
		elif self.testToken(LA.TokenType.OPENTHEPAR):
			self.consumeToken();
			a=self.procExpr();
			self.matchToken(LA.TokenType.CLOSETHEPAR)
		elif not self.testToken(LA.TokenType.STAR):
			print('ERRRORRR-002 expected symbol or ( or *, but got ',self.getToken())
			raise SystemExit()
		if self.testToken(LA.TokenType.STAR):
			self.consumeToken()
			a.star()
		return a

	def procSymbol(self):
		states=[self.genStateName(), self.genStateName()]
		dictionary=self.lexical.getDictionary()
		transitions=[FA.FiniteAutomata.Edge(states[0],self.popToken(),states[1])]
		initial=states[0]
		finals=[states[1]]
		return FA.FiniteAutomata(states,dictionary,transitions,initial,finals)
