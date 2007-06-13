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
import sys
from dialogos import *
from tabla import *


class WnIngreso(GladeConnect):
    def __init__(self):
        GladeConnect.__init__(self, 'glade/pySimplex.glade','wnIngreso')
        self.wnIngreso.maximize()
        self.wnIngreso.set_title('pySimplexPL:  ')
        self.path = ''
        if len(sys.argv) ==2:
            self.path = sys.argv[1]
            self.leerArchivo()
        
    def inicio(self):
        self.wnIngreso.set_title('pySimplexPL: ' + self.path)
        dlg = DlgVariables(self.wnIngreso)
        response=dlg.dlgVariables.run()
        if response == gtk.RESPONSE_OK:
            self.variables = int(dlg.variables)
            self.restricciones = int(dlg.restricciones)
            self.creaColumnas()
            self.creaEncavesados()
            
    def leerArchivo(self):
        try:
            archivo = open(self.path,'r')
        except:
            msg = """Error no se pudo Abrir el archivo en:\n %s
            \nElija un lugar en el cual tenga permisos'\n
            de lectura o verifique que el archivo exista\n
            e intentelo nuevamente""" % self.path
        
            aviso(self.wnIngreso,msg,tipo=gtk.MESSAGE_ERROR)
            self.path = ''
            return
        i = 0
        lista = []
        try:
            for linea in archivo:
                if i == 0:
                    self.variables = int(linea.split('variables=')[1][:-1])
                elif i == 1:
                    self.restricciones = int(linea.split('restricciones=')[1][:-1])
                elif i == 2:
                    fo = linea.split(',')
                    fo.insert(0,fo[0][3:])
                    fo.remove(fo[1])
                    fo.append(fo[self.variables - 1][:-1])
                    fo.remove(fo[self.variables - 1])
                else:
                    lista.append(linea.split(','))
                    if lista[i - 3][self.variables + 2][-1] == '\n':
                        lista[i - 3].append(lista[i - 3][self.variables + 2][:-1])
                        lista[i - 3].remove(lista[i - 3][self.variables + 2])
                i = i + 1
        except:
            msg = """            Error el archivo en:
            %s
            no se a podido cargar correctamete
            puede que no sea un archivo valido""" % self.path
            aviso(self.wnIngreso,msg,tipo=gtk.MESSAGE_ERROR)
            return
        self.creaColumnas()
        self.modelo.clear()
        self.modeloR.clear()
        self.modelo.append(fo)
        self.lvwFo.set_model(self.modelo)
        try:
            for dato in lista:
                self.modeloR.append(dato)
            self.lvwIngreso.set_model(self.modeloR)
        except:
            msg = """            Error el archivo en:
            %s
            no se a podido cargar correctamete
            puede que no sea un archivo valido""" % self.path
            aviso(self.wnIngreso,msg,tipo=gtk.MESSAGE_ERROR)
        self.wnIngreso.set_title('pySimplexPL:  ' + self.path)

    def creaColumnas(self):
        self.lvwIngreso.set_rules_hint(True)
        columnas = []
        for n in range(0,self.variables):
            indice = 'X%s' % (n +1) 
            columnas.append([n,indice,'str',None,True])
        self.modelo = gtk.ListStore(*((self.variables)*[str]))        
        SimpleTree.GenColsByModel(self.modelo, columnas, self.lvwFo)
        columnas = []
        for n in range(1,self.variables +1):
            indice = 'X%s' % (n) 
            columnas.append([n,indice,'str',None,True])
        self.modeloR = gtk.ListStore(*((self.variables + 3)*[str]))
        columnas.insert(0,[0,'     ',"str"])
        columnas.append([self.variables + 1 ,'Desigualdad','str',None,True])
        columnas.append([self.variables + 2 ,'Valor','str',None,True])
        SimpleTree.GenColsByModel(self.modeloR, columnas, self.lvwIngreso)
        
    def creaEncavesados(self):
        self.modeloR.clear()
        self.modelo.clear()
        for n in range(0,self.restricciones):
            lista = self.variables*[0]
            lista.insert(0,'R%s' %(n+1))
            lista.append("<=")
            lista.append("0")
            self.modeloR.append(lista)
        self.lvwIngreso.set_model(self.modeloR)
        lista= []
        lista = self.variables*[0]
        self.modelo.append(lista)
        self.lvwFo.set_model(self.modelo)
        
    def limpiar(self):
        self.lvwFo.destroy()
        self.lvwFo = gtk.TreeView()
        self.scrolledwindow2.add(self.lvwFo)
        self.lvwFo.show()
        self.lvwIngreso.destroy()
        self.lvwIngreso = gtk.TreeView()
        self.scrolledwindow1.add(self.lvwIngreso)
        self.lvwIngreso.show()
        
    def on_abrir(self,*args):
        self.limpiar()
        dlg = Abrir(self.wnIngreso)
        response=dlg.dlgAbrir.run()
        if response == -1 or response == -5:
            self.path = dlg.dlgAbrir.get_filename()
            self.leerArchivo()

    def on_acerca_de(self,*args):
        from time import localtime
        autores=['Juan Carrasco <juacarrag@gmail.com>',
                 'Plumero <aaaaaaaaaaa>',
                 'Kramer <bbbbbbbbbbbbbbbb>',
                 'Francisco Brunel <franciscobrunel@gmail.com>',
                 'Pollo <aaaaaaaaaaaaa>']
        comentario="""Comentario aqui """
        copyright="\302\251 Copyright %s Juan Carrasco G.\n" % str(localtime()[0])
        copyright=copyright +"\302\251 Copyright %s Plumero.\n" % str(localtime()[0])
        copyright=copyright +"\302\251 Copyright %s Francisco Brunel.\n" % str(localtime()[0])
        copyright=copyright +"\302\251 Copyright %s Pollo.\n" % str(localtime()[0])
        copyright=copyright +"\302\251 Copyright %s Kramer." % str(localtime()[0])
        DialogoAcercaDe(padre=self.wnIngreso,
                        nombre='pySimplexPL',
                        autor=autores,
                        logo="pySimplex.png",
                        comentario=comentario,
                        copyright=copyright)

    def on_guardar(self,*args):
        if self.path == '':
            dlg = Guardar(self.wnIngreso)
            response=dlg.dlgGuardar.run()
            if response == -1 or response == -5:
                self.path = dlg.dlgGuardar.get_filename()
            else:
                return
        variables = 'variables=' + str(self.variables) + '\n'
        restricciones= 'restricciones=' + str(self.restricciones) + '\n'
        
        fo = 'Fo='
        iter=self.modelo.get_iter(0)
        row = self.modelo.get_path(iter)
        for i in range(0,self.variables):
            fo = fo + str(self.modelo[row][i]) + ','
        re = '\n' 
        for colum in range(0,self.restricciones):
            iter=self.modeloR.get_iter(colum)
            row = self.modeloR.get_path(iter)
            for i in range(0,self.variables+3):
                re = re + str(self.modeloR[row][i]) + ','
            re = re[:-1] + '\n'
        try:
            archivo = open(self.path,'w')
            archivo.write(variables + restricciones + fo[:-1] + re[:-1])
            archivo.close()
        except:
            msg = """            Error no se pudo guardar el archivo en:
            %s
            Elija un lugar en el cual tenga permisos
            de escritura e intentelo nuevamente""" % self.path
            aviso(self.wnIngreso,msg,tipo=gtk.MESSAGE_ERROR)
            self.path = ''
            return
        self.wnIngreso.set_title('pySimplexPL:  ' + self.path)

    def on_nuevo(self,*args):
        self.path = ''
        self.limpiar()
        self.inicio()
        
    def on_btnNext_clicked(self,*args):
        self.optMax.get_active()
        iter=self.modelo.get_iter(0)
        row = self.modelo.get_path(iter)
        fo = []
        for i in range(0,self.variables):
            try:
                #######maximisar True#################
                if self.optMax.get_active():
                    fo.append(int(self.modelo[row][i]))
                else:
                    fo.append(int(self.modelo[row][i])*-1)
                #################################
            except:
                msg = """Error de ingreso de datos
en la F.O. : en el dato '''%s''' solo se aceptan numeros"""% (self.modelo[row][i] ) 
                aviso(self.wnIngreso,msg,tipo=gtk.MESSAGE_ERROR)
                return
        fo.append('0')
        variablesBasicas = []
        lista = []
        todas=['Z']
        variablesA=[]
        lista.append(fo)
        n = self.variables
        for colum in range(0,self.restricciones):
            iter=self.modeloR.get_iter(colum)
            row = self.modeloR.get_path(iter)
            n = n +1
            if str(self.modeloR[row][self.variables + 1]) == '<=':
                variablesBasicas.append('S%s' % n)
                todas.append('S%s' % n)
            elif str(self.modeloR[row][self.variables + 1])=='>=':
                variablesBasicas.append('E%s' % n)
                #todas.append('E%s' % n)
                variablesA.append('A%s' % (colum+1))
                todas.append(['A%s' % (colum+1),'E%s' % n])
                #variablesBasicas.append('A%s' % (colum+1))
            else:
                n=n-1
                variablesA.append('A%s' % (colum+1))
                todas.append('A%s' % (colum+1))
                #variablesBasicas.append('A%s' % (colum+1))
            re = []
            for i in range(1,self.variables+1):
                #print i,self.modeloR[row][i]
                try:
                    a=int(self.modeloR[row][i])
                except:
                    msg = """Error de ingreso de datos
en la R(%s) : en el dato '''%s''' solo se aceptan numeros"""% (i,self.modeloR[row][i]) 
                    aviso(self.wnIngreso,msg,tipo=gtk.MESSAGE_ERROR)
                    return
                re.append(self.modeloR[row][i])
            re.append(self.modeloR[row][self.variables+2])
            lista.append(re)
        #print variablesBasicas
        
        dlg = Tabla(self.wnIngreso,
                    self.variables,
                    self.restricciones,
                    variablesBasicas,
                    lista,
                    variablesA,
                    todas,
                    self.optMax.get_active())
        dlg.dlgTabla.run()
        
    def on_salir(self,*args):
        if __name__ == '__main__':
            gtk.main_quit()

if __name__ == '__main__':
    app = WnIngreso()
    gtk.main()
