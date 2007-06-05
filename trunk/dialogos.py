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
from time import localtime
import os

class DlgVariables(GladeConnect):
    def __init__(self,padre=None):
        GladeConnect.__init__(self, 'glade/pySimplex.glade','dlgVariables')
        self.dlgVariables.set_transient_for(padre)

    def on_okbutton_clicked(self,*args):
        self.variables = self.spnVariables.get_text()
        self.restricciones = self.spnRestricciones.get_text()
        self.dlgVariables.hide()
    
    def on_cancelbutton_clicked(self,*args):
        self.dlgVariables.hide()
        
class Guardar(GladeConnect): 
    def __init__ (self, padre = None):
        GladeConnect.__init__(self, "glade/pySimplex.glade", "dlgGuardar")
        self.dlgGuardar.set_transient_for(padre)

    def on_btnDlg_clicked(self, btn=None):
        if btn.get_name() == 'btnDlga':
            if self.dlgGuardar.get_filename() <> None:
                self.dlgGuardar.hide()
        else:
            self.dlgGuardar.hide()
            
class Abrir(GladeConnect): 
    def __init__ (self, padre = None):
        GladeConnect.__init__(self, "glade/pySimplex.glade", "dlgAbrir")
        self.dlgAbrir.set_transient_for(padre)

    def on_btnDlg_clicked(self, btn=None):
        self.dlgAbrir.hide()
    
class DialogoAcercaDe(gtk.AboutDialog):
	def __init__(self,padre=None,
		     nombre="Nombre",
		     version="1.0",
		     comentario=None,
		     paginaweb=None,
		     logo=None,
		     nombrelogo=None,
		     copyright="\302\251 Copyright %s Juan Carrasco G." % str(localtime()[0]),
		     autor=["Juan Carrasco G. <juacarrag@gmail.com>"]):
		gtk.AboutDialog.__init__(self)
		self.set_modal(True)
		self.set_transient_for(padre)
		self.set_name(nombre)
		self.set_copyright(copyright)
		self.set_version(version)
		self.set_comments(comentario)
		self.set_website(paginaweb)
		self.set_website_label(paginaweb)
		self.set_authors(autor)
                licencia ="""%s es software libre; puede redistribuirlo y/o modificarlo
bajo los términos de la Licencia Pública General de GNU tal como
la publica la Free Software Foundation; tanto en la versión 2 de la
Licencia como (a su elección) cualquier versión posterior.\n
%s se distribuye con la esperanza de que será útil,
pero SIN NINGUNA GARANTÍA; sin incluso la garantía implicada
de MERCANTIBILIDAD o ADECUACIÓN PARA UN PROPÓSITO PARTICULAR.
Vea la Licencia Pública General de GNU para más detalles.\n
Debería haber recibido una copia de la Licencia pública General
de GNU junto con %s; si no, escriba a la Free Software
Foundation, Inc,59 Temple Place, Suite 330, Boston, MA 02111-1307,
Estados Unidos de América""" % (nombre,nombre,nombre)
		self.set_license(licencia)
		#self.set_documenters(doc)
		#self.set_translator_credits(t)
		#self.set_artists(ar)
                path = os.path.join(os.path.join(os.path.dirname(__file__), 'glade'),logo)
		if logo <> None:
			self.set_logo(gtk.gdk.pixbuf_new_from_file(path))
		#self.set_logo_icon_name(path)


		self.connect ("response", self.on_quit)
		self.show()
		
	def on_quit(self,*args):
		if __name__ == "__main__":
			gtk.main_quit()
		else:
			self.destroy()

def aviso(GtkWindow, mensaje,botones = gtk.BUTTONS_OK, tipo=gtk.MESSAGE_INFO):
    '''parametros.....
            GtkWindow: 		
                objeto GtkWindow, ventana desde la cual se realiza
                la solicitud del mensaje
            mensaje:
                mensaje a ser presentado'''
    
    m = mensaje
    m = unicode(m,'latin-1')
    dialog = gtk.MessageDialog(GtkWindow,
                               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               tipo, botones, m.encode('utf-8'))
    dialog.set_title('pySimplex')
    dialog.show_all()
    response = dialog.run()
    dialog.destroy()
    return response
