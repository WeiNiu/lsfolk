#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import langid
print langid.classify('famous')
b= langid.classify('game')
if b[0]=='zh':
    print 'true'
print langid.classify('presidente Obama le gusta comer plátano')
print socket.gethostbyname(socket.gethostname())
