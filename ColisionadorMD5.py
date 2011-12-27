#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ColisionadorMD5.py
#
#       Copyright 2011 David Litvak <david.litvakb@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Softyware Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import random
import md5
from multiprocessing import Process, Queue
from itertools import product

class Colisionador:
  def __init__(self,md5,result, queue):
    self.md5 = md5
    self.result = result
    self.queue = queue

  def colisiona(self, valor):
    return valor == self.md5

  def generarColision(self):
    x = 0
    while True:
      for y in self.result:
        cadena = self.getCadena(y)

        if self.colisiona(md5.md5(cadena).hexdigest()):
          self.queue.put(('Te encontre...   Cadena: %s    Iteracion: %d' % (cadena,x)))
          self.queue.close()
          self.queue.join_thread()
          exit(1)

        x += 1

        if not self.queue.empty():
          exit(1)

      exit(1)

  def getCadena(self,tupla):
    cadena = ''

    for t in tupla:
      cadena += t

    return cadena

def colisionarSecuencialmente(val, result, queue):
  md5 = val
  colision = Colisionador(md5, result, queue)
  colision.generarColision()

def getReversed(cadena):
  result = ''
  for x in reversed(cadena):
    result += x
  return result

def getProduct(l, busqueda):
  return product(busqueda, repeat=l)

def ingresoDatos():
  while True:
    try:
      md = str(raw_input('Ingrese la cadena MD5 a colisionar: '))
      if len(md) != 32:
        continue

      lInf = int(raw_input('Ingrese el limite inferior de caracteres a buscar: '))
      lSup = int(raw_input('Ingrese el limite superior de caracteres a buscar: '))

      intervalo = (lInf,lSup)

      return md, intervalo
    except ValueError:
      print '\nLos valores ingresados no son correctos...\n'
      continue

def getProcess(md,x,argsColision,q):
  Process(target=colisionarSecuencialmente, args=(md,getProduct(x, argsColision),q)).start()

def main():
  md, intervalo = ingresoDatos()
  letrasMin = ''.join([chr(x) for x in range(97,123)])
  letrasMay = letrasMin.upper()
  numeros = ''.join([str(x) for x in range(10)])
  simbolos = (
              ''.join([chr(x) for x in range(0,48)])
            + ''.join([chr(x) for x in range(58,65)])
            + ''.join([chr(x) for x in range(91,97)])
            + ''.join([chr(x) for x in range(123,127)])
             )
  letras = letrasMin + letrasMay
  letrasNumeros = letras + numeros
  letrasSimbolos = letras + simbolos
  simbolosNumeros = simbolos + numeros
  todo = letras + numeros + simbolos

  print '\nComenzando...\nEste proceso puede tardar...\nPara finalizarlo pulse Ctrl+C...\n'

  busList = [todo,letrasMin,letrasMay,numeros,simbolos,letras,letrasNumeros,letrasSimbolos,simbolosNumeros]

  q = Queue()

  try:
    for x in range(intervalo[0],intervalo[1] + 1):
      for bus in busList:
        getProcess(md,x,bus,q)
        getProcess(md,x,getReversed(bus),q)

    while True:
      if not q.empty():
        val = q.get()
        q.put(val)
        print val
        print '\nPulse Enter para salir'
        raw_input()
        return 0

    return 1
  except:
    print 'Ha ocurrido un error...\nRevise las variables ingresadas y ejecute nuevamente...'
    return 1

if __name__ == '__main__':
  main()
