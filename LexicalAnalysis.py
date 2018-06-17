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
		s=''
		i=0;
		lex=self.nextToken()
		while lex.getType().value>0:
			s=s+lex.getType().name+' '
			if i%8==0 and i>0:
				s=s+'\n'
			lex=self.nextToken()
			i=i+1
		print s
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