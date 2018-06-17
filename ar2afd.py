#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from enum import Enum

LAMBDA=''
class TokenType(Enum):
	INVALID=-2
	EOF=0
	STAR=1#*
	CROSS=2#+
	SYMBOL=3#symbol from alphabet
	OPENTHEPAR=4#(
	CLOSETHEPAR=5#)

class State(Enum):
	BEGIN=1
	KOWNTYPE=2
	UNKOWNTYPE=3

class Lexeme(object):
	def __init__(self, token='',ttype=TokenType.INVALID):
		self.token=token
		self.ttype=ttype

	def getToken(self):
		return self.token

	def getType(self):
		return self.ttype

	def setToken(self,token):
		self.token=token

	def setType(self,ttype):
		self.ttype=ttype

class LexicalAnalysis(object):
	def __init__(self,re='(aa)*(b + aba)(aa)*'):
		self.dictionary=[]
		self.re=re
		self.it_pointer=0

	def getDictionary(self):
		return self.dictionary

	def getRE(self):
		return self.re

	def reset(self):
		self.it_pointer=0;

	def printTokens(self):
		lex=self.nextToken()
		# while lex.getType().value>0:
		for i in range(17):
			print(lex.getType().name)
			lex=self.nextToken()
		self.reset()

	def createDictionary(self):
		self.dictionary=[]
		for i in range(len(self.re)):
			if(self.re[i]!='(' and self.re[i]!=')' and self.re[i]!='*' and self.re[i]!='+' and self.re[i]!=' '):
				if(self.re[i] not in self.dictionary):
					self.dictionary.append(self.re[i])

	def nextToken(self):
		lex=Lexeme()
		state=State.BEGIN
		while(state!=State.KOWNTYPE and state!=State.UNKOWNTYPE):
			if(self.it_pointer<len(self.re)):
				c=self.re[self.it_pointer]
				self.it_pointer=self.it_pointer+1
			else:
				c=-1
				state=State.KOWNTYPE
				lex.setType(TokenType.EOF)
			if state==State.BEGIN:
				if c==' ':
					state=State.BEGIN
				elif c=='(':
					lex.setToken(c)
					lex.setType(TokenType.OPENTHEPAR)
					state=State.KOWNTYPE
				elif c==')':
					lex.setToken(c)
					lex.setType(TokenType.CLOSETHEPAR)
					state=State.KOWNTYPE
				elif c=='*':
					lex.setToken(c)
					lex.setType(TokenType.STAR)
					state=State.KOWNTYPE
				elif c=='+':
					lex.setToken(c)
					lex.setType(TokenType.CROSS)
					state=State.KOWNTYPE
				elif c==-1: 
					lex.setToken(c)
					lex.setType(TokenType.EOF)
					state=State.KOWNTYPE
				elif c in self.dictionary: 
					lex.setToken(c)
					lex.setType(TokenType.SYMBOL)
					state=State.KOWNTYPE
				else:
					state=State.UNKOWNTYPE
		if state==State.UNKOWNTYPE:
			lex.setType(TokenType.INVALID)
		return lex

class SyntaticalAnalysis(object):
	def __init__(self, lexical):
		self.lexical=lexical
		self.current=lexical.nextToken()
		self.basename=0
		self.eNFA=None
		self.NFA=None
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
		# self.NFA=Converter
		# self.DFA=Converter 

	def geteNFA(self):
		return self.eNFA

	def getNFA(self):
		return self.NFA

	def getDFA(self):
		return self.DFA

	def toPDF(self,json):
		json=json.replace('\"', '\\\"')
		subprocess.call('echo \"'+json+'\" > tmp.json', shell=True)
		subprocess.call('./json2dot.sh tmp.json > tmp.dot', shell=True)
		subprocess.call('dot -Tpdf -o tmp.pdf tmp.dot', shell=True)

	def eNFAToPDF(self):
		self.pdf(self.eNFA.tojson())

	def NFAToPDF(self):
		self.pdf(self.NFA.tojson())

	def DFAToPDF(self):
		self.pdf(self.DFA.tojson())

	def procExpr(self):
		a=self.procTerm()
		while self.testToken(TokenType.CROSS):
			self.consumeToken()
			b=self.procTerm()
			a.merge(b,'+',self.genStateName())
		return a

	def procTerm(self):
		a=self.procFactor()
		while self.testToken(TokenType.SYMBOL) or self.testToken(TokenType.OPENTHEPAR):
			b=self.procFactor()
			a.merge(b,'.')
		return a

	def procFactor(self):
		a=None
		if self.testToken(TokenType.SYMBOL):
			a=self.procSymbol()
		elif self.testToken(TokenType.OPENTHEPAR):
			self.consumeToken();
			a=self.procExpr();
			self.matchToken(TokenType.CLOSETHEPAR)
		elif not self.testToken(TokenType.STAR):
			print('ERRRORRR-002 expected symbol or ( or *, but got ',self.getToken())
			raise SystemExit()
		if self.testToken(TokenType.STAR):
			self.consumeToken()
			a.star()
		return a

	def procSymbol(self):
		states=[self.genStateName(), self.genStateName()]
		dictionary=self.lexical.getDictionary()
		transitions=[Edge(states[0],self.popToken(),states[1])]
		initial=states[0]
		finals=[states[1]]
		return FA(states,dictionary,transitions,initial,finals)


class Edge(object): 
	def __init__(self, origin=None,token=None,destiny=None):
		self.origin=origin
		self.token=token
		self.destiny=destiny
	def tolist(self):
		return [self.origin,self.token,self.destiny]


class FA(object): 
	def __init__(self,states=[],dictionary=[],transitions=[],initial=None,finals=[]):
		self.states=states
		self.dictionary=dictionary
		self.transitions=transitions
		self.initial=initial
		self.finals=finals

	def tojson(self):
		def listToJson(lst):
			json='		['
			for i in range(len(lst)):
				json=json+'\"'+lst[i]+'\"'
				if i != len(lst)-1:
					json=json+', '
			json=json+']'
			return json
		def list2DToJson(lst):
			json='		[\n'
			for i in range(len(lst)):
				json=json+'	'+listToJson(lst[i].tolist())
				if i != len(lst)-1:
					json=json+',\n'
			json=json+'\n		]'
			return json
		json='{ "af": [\n'
		json=json+listToJson(self.states)+',\n'
		json=json+listToJson(self.dictionary)+',\n'
		json=json+list2DToJson(self.transitions)+',\n'
		json=json+'		[\"'+self.initial+'\"],\n'
		json=json+listToJson(self.finals)+'\n'
		json=json+'	]\n}'
		return json

	def merge(self,other,opr,newstate='?'):
		if opr=='+':
			self.states=list(set(self.states)|set(other.states))
			self.dictionary=list(set(self.dictionary)|set(other.dictionary))
			self.transitions=list(set(self.transitions)|set(other.transitions))
			self.finals=list(set(self.finals)|set(other.finals))
			self.states.append(newstate)
			self.transitions.append(Edge(self.states[len(self.states)-1],LAMBDA,self.initial))
			self.transitions.append(Edge(self.states[len(self.states)-1],LAMBDA,other.initial))
			self.initial=self.states[len(self.states)-1]
		elif opr=='.':
			self.states=list(set(self.states)|set(other.states))
			self.dictionary=list(set(self.dictionary)|set(other.dictionary))
			self.transitions=list(set(self.transitions)|set(other.transitions))
			for i in range(len(self.finals)):
				self.transitions.append(Edge(self.finals[i],LAMBDA,other.initial))
			self.finals=other.finals
		else:
			print('ERRRORRR-003 unexpected operation ',opr,', expeceted + or .')
			raise SystemExit()

	def star(self):
		for i in range(len(self.finals)):
			self.transitions.append(Edge(self.finals[i],LAMBDA,self.initial))
		self.finals.append(self.initial)

l=LexicalAnalysis()
l.createDictionary()
l.printTokens()
s=SyntaticalAnalysis(l)
s.start()
print('RE=',l.getRE())
print(s.geteNFA().tojson())
s.eNFAToPDF()