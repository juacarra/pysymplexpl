#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright Juan Carrasco G. <juacarrag@gmail.com>
#          ##########
#          ##########
#          ########## 

#pySimplexPL es software libre; puede redistribuirlo y/o modificarlo
#bajo los términos de la Licencia Pública General de GNU tal como
#la publica la Free Software Foundation; tanto en la versión 2 de la
#Licencia como (a su elección) cualquier versión posterior.

#pySimplexPL se distribuye con la esperanza de que será útil,pero
#SIN NINGUNA GARANTÍA; sin incluso la garantía implicada de
#MERCANTIBILIDAD o ADECUACIÓN PARA UN PROPÓSITO PARTICULAR.
#Vea la Licencia Pública General de GNU para más detalles.

#Debería haber recibido una copia de la Licencia pública General de
#GNU junto con PySimplexPL; si no, escriba a la Free Software Foundation,
#Inc,59 Temple Place, Suite 330, Boston, MA 02111-1307, Estados Unidos de América

from GladeConnect import *
import gtk
import SimpleTree

class Tabla(GladeConnect):
    def __init__ (self,padre=None,variables=0,restricciones=0,variablesBasicas=[],lista=[]):
        GladeConnect.__init__(self, "glade/pySimplex.glade", "dlgTabla")
        self.dlgTabla.set_transient_for(padre)
        #self.dlgTabla.maximize()
        self.lvwTabla.set_rules_hint(True)
        self.variables = variables
        self.restricciones = restricciones
        self.vb = variablesBasicas
        self.lista = lista
        self.creaColumnas()
        self.cargaDatos()
        
    def creaColumnas(self):
        columnas = []
        columnas.append([0,'R','str'])
        columnas.append([1,'Z','str'])
        for n in range(0,self.variables):
            indice = 'X%s' % (n +1) 
            columnas.append([n + 2 ,indice,'str'])
        for variableBasica in self.vb:
            columnas.append([int(variableBasica[1:] ) +1,variableBasica,'str'])
        columnas.append([self.variables + self.restricciones + 2,'Ld','str'])
        #**************************************************************************************************
        #columnas.append([self.variables + self.restricciones + 3,'Cuoc','str'])
        self.modelo = gtk.ListStore(*((self.variables + self.restricciones + 3)*[str]))        
        SimpleTree.GenColsByModel(self.modelo, columnas, self.lvwTabla)
        
    def cargaDatos(self):
        n=0
        k=0
        #print self.lista
        for dato in self.lista:
            #print dato
            vb=[]
            m=0
            for i in range(0,self.restricciones):
                dato.insert(self.variables + m,'0')
                m = m+1
            if n==0:
                dato.insert(0,'1')
            else:
                dato.insert(0,'0')
                if self.vb[n-1][0]=='S':
                    k=k+1
                    dato.insert(self.variables + k,'1')
                    dato.pop(self.variables + k + 1)
                else:
                    k=k+1
                    dato.insert(self.variables + k,'-1')
                    dato.pop(self.variables + k + 1)
            dato.insert(0,'(%s)' % n)
            n = n + 1
            self.modelo.append(dato)
        self.lvwTabla.set_model(self.modelo)
        
    def on_cmdSiguiente_clicked(self, btn=None):
        self.hide()
