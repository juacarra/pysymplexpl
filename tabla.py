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
    def __init__ (self,padre=None,variables=0,restricciones=0,variablesBasicas=[],lista=[],variablesA=[],todas=[],max=True):
        GladeConnect.__init__(self, "glade/pySimplex.glade", "dlgTabla")
        self.dlgTabla.set_transient_for(padre)
        #self.dlgTabla.maximize()
        self.lvwTabla.set_rules_hint(True)
        self.variables = variables
        self.restricciones = restricciones
        self.vb = variablesBasicas
        self.lista = lista
        self.variablesA = variablesA
        self.numColum = 0
        self.columnas = []
        self.todas=todas
        self.max = max
        self.creaColumnas()
        self.cargaDatos()
        
    def creaColumnas(self):
        num = 0
        columnas = []
        columnas.append([num,'R','str'])
        self.columnas.append('R')
        num=num+1
        columnas.append([num,'Z','str'])
        self.columnas.append('Z')
        num=num+1
        for n in range(0,self.variables):
            indice = 'X%s' % (n +1) 
            columnas.append([num ,indice,'str'])
            self.columnas.append(indice)
            num=num+1
        for variableBasica in self.vb:
            columnas.append([num,variableBasica,'str'])
            self.columnas.append(variableBasica)
            num=num+1
        for variableA in self.variablesA:
            columnas.append([num,variableA,'str'])
            self.columnas.append(variableA)
            num=num+1
        columnas.append([num,'Ld','str'])
        self.columnas.append('Ld')
        num=num+1
        columnas.append([num,'VB','str'])
        self.columnas.append('VB')
        self.numColum = num
        self.modelo = gtk.ListStore(*((num + 1)*[str]))        
        SimpleTree.GenColsByModel(self.modelo, columnas, self.lvwTabla)
        
    def calculaM(self):
        self.datos=[]
        for linea in range(0,len(self.modelo)):
            iter=self.modelo.get_iter(linea)
            row = self.modelo.get_path(iter)
            fila=[]
            for dato in self.modelo[row]:
                fila.append(dato)
            self.datos.append(fila)
        lis=[]
        for dato in self.datos:
            if dato[-1][0]=='A':
                liss = []
                for i in range(2,len(dato)-1):
                    liss.append('%sM' % dato[i])
                lis.append(liss)
        total=[]
        for j in range(0,len(lis[0])):
            sum=0
            for i in range(0,len(lis)):
                sum=sum+int(lis[i][j][:-1])
            total.append('%sM' % sum)
        dato = self.datos[0]
        fo=[]
        final=[]
        for i in range(2,len(dato)-1):
            fo.append(dato[i])
        for i in range(0,len(total)):
            if fo[i][0] == '-':
                final.append('%s %s' %(total[i],fo[i]))
            else:
                final.append('%s +%s' %(total[i],fo[i]))
        regresa =[]
        for dato in final:
            num=dato.split(' ')
            if num[0][0]=='0':
                if num[1][1]=='0':
                    regresa.append('0')
                else:
                    regresa.append(num[1])
            elif num[1][1]=='0':
                regresa.append(num[0])
            elif num[0][0]<>'-' and num[1][0]=='-' and num[0]==num[1][1:]:
                regresa.append('0')
            elif num[0][0]=='-' and num[1][0]=='+' and num[0][1:]==num[1][1:]:
                regresa.append('0')
            else:
                regresa.append(dato)
        regresa.insert(0,'1')
        regresa.insert(0,'(0)')
        regresa.append('Z')
        iter=self.modelo.get_iter(0)
        row = self.modelo.get_path(iter)
        for i in range(0,len(regresa)):
            self.modelo.set(iter,i,regresa[i])    
        print regresa    
            
    def cargaDatos(self):
        for dato in self.lista:
            #si LD es negativo se multiplica la R por -1
            j=1
            remplazo = []
            if int(dato[-1]) < 0:
                for num in dato:
                    remplazo.append(int(num) * -1)
                self.lista.insert(j,remplazo)
                self.lista.pop(j+1)                
            j=j+1
        n=0
        for dato in self.lista:
            for i in range(len(dato),self.numColum-2):
                dato.insert(-1,'0')
            dato.insert(0,'0')
            dato.insert(0,'(%s)' % n)
            if type(self.todas[n]) == type(self.todas):
                #print self.todas[n][0],self.columnas.index(self.todas[n][0]),self.todas[n][1],self.columnas.index(self.todas[n][1])
                dato.insert(self.columnas.index(self.todas[n][0]),'1')
                dato.pop(self.columnas.index(self.todas[n][0]) + 1)
                dato.insert(self.columnas.index(self.todas[n][1]),'-1')
                dato.pop(self.columnas.index(self.todas[n][1]) + 1)
                dato.append(self.todas[n][0])
            else:
                #print self.todas[n],self.columnas.index(self.todas[n])
                dato.insert(self.columnas.index(self.todas[n]),'1')
                dato.pop(self.columnas.index(self.todas[n])+1)
                dato.append(self.todas[n])
            if n==0:
                j=0
                for cabecera in self.columnas:
                    if cabecera[0]=='A':
                        #####maximizar True#############
                        if self.max:
                            dato.insert(j,'1M')
                        else:
                            dato.insert(j,'-1M')
                        dato.pop(j + 1)
                    j=j+1
            n = n + 1
            self.modelo.append(dato)
        self.lvwTabla.set_model(self.modelo)
        self.calculaM()
        
    def on_cmdSiguiente_clicked(self, btn=None):
        self.hide()
