#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

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
	def __init__(self,er='(aa)*(b + aba)(aa)*'):
		self.dictionary=[]
		self.er=er
		self.it_pointer=0

	def getDictionary(self):
		return self.dictionary

	def reset(self):
		self.it_pointer=0;

	def printTokens(self):
		lex=self.nextToken()
		while lex.getType().value>0:
			print(lex.getType().name)
			lex=self.nextToken()
		self.reset()

	def createDictionary(self):
		self.dictionary=[]
		for i in range(len(self.er)):
			if(self.er[i]!='(' and self.er[i]!=')' and self.er[i]!='*' and self.er[i]!='+' and self.er[i]!=' '):
				unique=True
				for j in range(len(self.dictionary)):
					if(self.er[i]==self.dictionary[j]):
						unique=False
				if(unique):
					self.dictionary.append(self.er[i])

	def nextToken(self):
		lex=Lexeme()
		state=State.BEGIN
		while(state!=State.KOWNTYPE and state!=State.UNKOWNTYPE):
			if(self.it_pointer<len(self.er)):
				c=self.er[self.it_pointer]
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

	def popToken(self):
		t=current.getToken()
		self.consumeToken()
		return t
	def getToken(self):
		return current.getToken()
	def testToken(self,ttype):
		return current.getType()==ttype
	def consumeToken(self):
		self.current=lexical.nextToken()
	def matchToken(self,ttype):
		if self.testToken(ttype):
			self.current=lexical.nextToken()
		else:
			print('ERRRORRR expected ',ttype.name,' but got ',self.current.getType().name)
			raise SystemExit()

	def genStateName(self):
		def baseN(num,b,numerals="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
			return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])
		name=baseN(self.basename,26)
		self.basename=self.basename+1
		return name
		

	def procExpr(self):
		a=self.procTerm()
		while testToken(TokenType.CROSS):
			self.consumeToken()
			b=self.procTerm()
			a.merge(b,'+')
		return a

	def procTerm(self):
		a=self.procFactor()
		while testToken(TokenType.SYMBOL) or testToken(TokenType.OPENTHEPAR):
			b=self.procFactor()
			a.merge(b,'.')
		return a

	def procFactor(self):
		a=None
		if testToken(TokenType.SYMBOL):
			a=self.procSymbol()
		elif testToken(TokenType.OPENTHEPAR):
			consumeToken();
			a=self.procExpr();
			matchToken(TokenType.CLOSETHEPAR)
		elif not testToken(TokenType.STAR):
			print('ERRRORRR expected symbol or ( or * but got',self.getToken())
			raise SystemExit()
		if testToken(TokenType.STAR):
			consumeToken()
			a.star()
		return a

	def procSymbol(self):
		states=[self.genStateName(), self.genStateName()]
		dictionary=self.lexical.getDictionary()
		transitions=Edge(states[0],self.popToken(),states[1])
		initial=states[0]
		finals=[states[1]]
		return AF(states,dictionary,transitions,initial,finals)


class Edge(object): 
	def __init__(self, origin=None,token=None,destiny=None):
		self.origin=origin
		self.token=token
		self.destiny=destiny

class AF(object): 
	def __init__(self,states=[],dictionary=[],transitions=[],initial=None,finals=[]):
		self.states=states
		self.dictionary=dictionary
		self.transitions=transitions
		self.initial=initial
		self.finals=finals

	def merge(self,other,opr):
		if opr=='+':
			a='TODO MEEEEEEEEEEEEEEEEEEEEEEE'
		elif opr=='.':
			a='TODO MEEEEEEEEEEEEEEEEEEEEEEE'
		else:
			print('ERRRORRR unexpected operation ',opr,'expeceted + or .')
			raise SystemExit()

	def star(self):
		a='TODO MEEEEEEEEEEEEEEEEEEEEEEE'