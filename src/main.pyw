import sys
import os
from PyQt4 import QtGui, QtCore
from xml.dom import minidom


curx = 0
cury = 0
deflevel = 9
defimagedir = 'images/'

maxlevels = 9
xmax = 0
ymax = 0


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Settings():
    menuHeight = 0
    windowWidth = 256*3
    windowHeight = 256*3+menuHeight


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        
        super(MainWindow, self).__init__(parent)
        
        
        self.setObjectName('MainWindow')
        self.resize(Settings().windowWidth,Settings().windowHeight)
        self.setWindowTitle('Corista Pyramid Viewer')
        self.setWindowIcon(QtGui.QIcon(resource_path('icon.png')))
        
        self.stylesheet = "QMainWindow { background-color: %s } QStatusBar { background-color: %s }" % (QtGui.QColor(0,0,0).name(), QtGui.QColor(255,255,255).name() )
        self.setStyleSheet(self.stylesheet)
        
        self.gui = GUI(self)
        self.setCentralWidget(self.gui)
        
        self.menubar = Menu(self)
        self.setMenuBar(self.menubar)
        
        self.statusbar = StatusBar(self)
        self.setStatusBar(self.statusbar)
        
        print "Application Started"
        
    def setPath(self, path, (x,y), levels):
        (self.xmax, self.ymax) = (x,y)
        self.gui.grid.imagedir = path+'/'
        self.gui.grid.xpos = 0
        self.gui.grid.ypos = 0
        self.gui.grid.level = levels
        self.gui.grid.maxlevels = levels
        self.setWindowTitle('Corista Pyramid Viewer -- %s' % path+'.ser')
        self.statusbar.status.setText("Level: %s -- Center: (%s, %s)" % (self.gui.grid.level, self.gui.grid.xpos, self.gui.grid.ypos))
        self.gui.grid.draw_grid()
        
    def keyPressEvent(self, e):
        self.gui.keyPressEvent(e)
        #if( self.gui.grid.level == 0 ):
        #    self.statusbar.status.setText("Level: %s -- Center: (%s/%s, %s/%s)" % (self.gui.grid.level, self.gui.grid.xpos, self.xmax, self.gui.grid.ypos, self.ymax))
        #else:
        self.statusbar.status.setText("Level: %s -- Center: (%s, %s)" % (self.gui.grid.level, self.gui.grid.xpos, self.gui.grid.ypos))
        
        
        
class Tile(QtGui.QPixmap): # Should this be of type pixmap? Probably?

    def __init__(self, x, y, level=4, imagedir="images/"):
        self.xpos = x
        self.ypos = y
        self.subx = int(x/32)
        self.suby = int(y/32)
        self.loc = "%s%s_%s_%s/%s_%s_%s.jpg" % (imagedir, level, self.subx, self.suby, level, self.xpos, self.ypos) # Calculate the directory the file is in
        #print self.loc
        if( not os.path.isfile(self.loc) ):
            # print "Image at %s,%s was blank" % (self.xpos, self.ypos)
            super(Tile, self).__init__(256,256)
            self.fill(color=QtGui.QColor('white'))
        else:
            super(Tile, self).__init__(self.loc)
        
        self.scaled(256,256);
        
        
class Grid(QtGui.QGridLayout): # Is this just a type of Qt Grid? Maybe?
    
    xpos = curx
    ypos = cury
    level = deflevel
    maxlevels = deflevel
    imagedir = defimagedir
    tiles = [ [1, 2, 3], [1, 2, 3], [1, 2, 3] ]
    
    def __init__(self, parent):
        super(Grid, self).__init__(parent)
        self.parent = parent
        self.setSpacing(2)
        self.init_grid()
        self.draw_grid()
    
    def init_grid(self):
        # Initiate grid
                
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[0])):
                labeltitle = "image"
                self.tiles[x][y] = QtGui.QLabel(labeltitle,self.parent)
                self.tiles[x][y].move(x*256, y*256)
#                 print "Title: %s (%s,%s -- %s,%s)"%(labeltitle, x,y, self.tiles[x][y].height(), self.tiles[x][y].width())

        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[0])):
                self.addWidget(self.tiles[x][y], y, x)
                
    def draw_grid(self):
        self.tiles[0][0].setPixmap(Tile(self.xpos-1,self.ypos-1,level=self.level, imagedir=self.imagedir))
        self.tiles[1][0].setPixmap(Tile(self.xpos-0,self.ypos-1,level=self.level, imagedir=self.imagedir))
        self.tiles[2][0].setPixmap(Tile(self.xpos+1,self.ypos-1,level=self.level, imagedir=self.imagedir))
        self.tiles[0][1].setPixmap(Tile(self.xpos-1,self.ypos-0,level=self.level, imagedir=self.imagedir))
        self.tiles[1][1].setPixmap(Tile(self.xpos-0,self.ypos-0,level=self.level, imagedir=self.imagedir))
        self.tiles[2][1].setPixmap(Tile(self.xpos+1,self.ypos-0,level=self.level, imagedir=self.imagedir))
        self.tiles[0][2].setPixmap(Tile(self.xpos-1,self.ypos+1,level=self.level, imagedir=self.imagedir))
        self.tiles[1][2].setPixmap(Tile(self.xpos-0,self.ypos+1,level=self.level, imagedir=self.imagedir))
        self.tiles[2][2].setPixmap(Tile(self.xpos+1,self.ypos+1,level=self.level, imagedir=self.imagedir))
                
    def set(self, (x,y)):
        (self.xpos, self.ypos) = (x,y)
        
    def up(self):
        self.ypos = self.ypos-1
        self.draw_grid()
    
    def down(self):
        self.ypos = self.ypos+1
        self.draw_grid()
        
    def left(self):
        self.xpos = self.xpos-1
        self.draw_grid()
        
    def right(self):
        self.xpos = self.xpos+1
        self.draw_grid()

    def levelup(self):
        self.level = self.level + 1
        if( self.level > self.maxlevels ):
            self.level = self.maxlevels
        self.xpos = int(self.xpos / 2)
        self.ypos = int(self.ypos / 2)        
        self.draw_grid()
    
    def leveldown(self):
        self.level = self.level - 1
        if( self.level < 0 ):
            self.level = 0
        else:
            self.xpos = int(self.xpos * 2)
            self.ypos = int(self.ypos * 2)
        if( self.xpos == 0 and self.ypos == 0 ):
            self.xpos = 1
            self.ypos = 1
        self.draw_grid()
        
    def removetile(self):
        # Remove the tile somehow -- we know where it is...
        self.tiles[1][1].setPixmap(Tile(-1,-1))
        # This is not fully implemented...
        pass
        
        
        
        
        
        
        
        
        
        
        
        
class GUI(QtGui.QWidget):
    
    def __init__(self, parent):
        super(GUI, self).__init__(parent)
        self.parent = parent
        self.initGrid()
        
    def initGrid(self):        
        self.grid = Grid(self)

        self.color = QtGui.QColor(0,0,0)
        self.setStyleSheet("QWidget { background-color: %s }" % self.color.name())
        
    def keyPressEvent(self, e):
        if( e.key() == QtCore.Qt.Key_Up ):
            self.grid.up()
        elif( e.key() == QtCore.Qt.Key_Down ):
            self.grid.down()
        elif( e.key() == QtCore.Qt.Key_Left ):
            self.grid.left()
        elif( e.key() == QtCore.Qt.Key_Right):
            self.grid.right()
        elif( e.key() == QtCore.Qt.Key_PageUp ):
            self.grid.levelup()
        elif( e.key() == QtCore.Qt.Key_PageDown ):
            self.grid.leveldown()
        elif( e.key() == QtCore.Qt.Key_Delete ):
            self.grid.removetile()





class StatusBar(QtGui.QStatusBar):
    def __init__(self, parent):
        super(StatusBar, self).__init__(parent)
        
        self.status = QtGui.QLabel('Status', self)
        self.addPermanentWidget(self.status)
        


class Menu(QtGui.QMenuBar):
    
    def __init__(self, parent):
        
        super(Menu, self).__init__(parent)
        self.parent = parent
        
        self.setGeometry(QtCore.QRect(0, 0, Settings().windowWidth, Settings().menuHeight))
        self.setObjectName('menubar')
    
        exitAction = QtGui.QAction('Exit', parent)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(parent.close)
        
        openAction = QtGui.QAction('Open File', parent)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open .SER File')
        openAction.triggered.connect(self.showDialog)
        
        openActionDir = QtGui.QAction('Open Directory', parent)
        openActionDir.setShortcut('Ctrl+D')
        openActionDir.setStatusTip('Open Directory')
        openActionDir.triggered.connect(self.showDialogDir)
        
        # This does not do anything, btw
        rebuildAction = QtGui.QAction('Rebuild Pyramid', parent)
        rebuildAction.setShortcut('Ctrl+R')
        rebuildAction.setStatusTip('Rebuild Pyramid')
        rebuildAction.triggered.connect(self.Pyramid)
                
        self.menufile = QtGui.QMenu(self)
        self.menufile.setTitle("File")
        self.menufile.setObjectName('menufile')
        
        self.menufile.addAction(exitAction)
        self.menufile.addAction(openAction)
        self.menufile.addAction(openActionDir)
        #self.menufile.addAction(rebuildAction)
        
        
        helpAction = QtGui.QAction('Help', parent)
        helpAction.setShortcut('Ctrl+H')
        helpAction.setStatusTip('Show Help')
        helpAction.triggered.connect(self.helpmenu)
        
        self.menuhelp = QtGui.QMenu(self)
        self.menuhelp.setTitle("Help")
        self.menuhelp.setObjectName('menuhelp')
        
        self.menuhelp.addAction(helpAction)
        
        
        
        
        self.addAction(self.menufile.menuAction())
        self.addAction(self.menuhelp.menuAction())

    def showDialog(self):
        
        fname = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open file', '.', filter='*.ser')

        series = minidom.parse(str(fname))
        path = fname.replace('.ser','')
        
        xtiles = int((series.getElementsByTagName('level-0-tiles-x')[0]).childNodes[0].data)
        ytiles = int((series.getElementsByTagName('level-0-tiles-y')[0]).childNodes[0].data)
        levels = int((series.getElementsByTagName('pyramid-levels')[0]).childNodes[0].data)
        
        self.parent.setPath(path, (xtiles, ytiles), levels-1)
        
    def showDialogDir(self):
        
        dialog = QtGui.QFileDialog()
        
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dialog.exec_()
        
        dir = dialog.directory()
        
        # You should write this in one line, I almost did it but then I gave up
        containsGoodSubDirectories = False
        for x in range(2):
            for y in range(5):
                for z in range(5):
                    if containsGoodSubDirectories == False:
                        containsGoodSubDirectories = QtCore.QDir( dir.absolutePath()+'/'+'_'.join( (str(x),str(y),str(z)) ) ).exists()                    
                    if containsGoodSubDirectories == True:
                        break

        if( dir.exists() and containsGoodSubDirectories ):
            self.parent.setPath(dir.absolutePath(), (0,0), 9)
        else:
            print 'Directory was invalid, report this somewhere!'
            print dir.absolutePath()      
        

    def Pyramid(self):
        print "Rebuilding Pyramid... NOT"
        
    def helpmenu(self):
        
        mes = "\nPg Up:\t\tMove up in pyramid\t\nPg Down:\tMove down in pyramid\t\nArrow Keys:\tMove around image"
        
        box = QtGui.QMessageBox(self.parent)
        box.addButton(box.Close)
        box.setDefaultButton(box.Close)
        box.setWindowTitle("Help")
        
        box.setText("Corista Pyramid Viewer\nWritten in Python using QT")
        
        box.setInformativeText(mes)
        
        #box.setDetailedText("Created by Erik Dahlinghaus")
        
        box.exec_()
        
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    
    mw = MainWindow()
    mw.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
    
