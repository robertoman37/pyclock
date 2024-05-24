import curses
import os
from definitions import Pos
from importlib import import_module
"""
This class works by providing a main place for all the modules listed in
the modules/ folder. It contains tabs to switch between the different modules,
and will dynamically import them based on which one is wanted.

MODULE SPECIFIC INSTRUCTIONS
Each module should* subclass the ModuleAbstract class and inplement a disp() and
input() method. The module is given a separate window to do whatever they want
in. The only reserved keybind is ESC for exiting the module and going into the
tab system.

*You really only need to subclass it so far if you want to use input, buttons,
etc."""
class Hub:
    def __init__(self, currentModuleName="clock"):
        self.dir = os.getcwd()
        self.loadedModules = [module for module in\
                              os.listdir(self.dir+"/modules")\
                              if module != "__pycache__" and module != "moduleAbstract.py"]
        self.currentModuleName = currentModuleName
        self.previousModuleName = currentModuleName
        self.tabsAt = []
        self.tabStr = self.createTabs()
        self.size = os.get_terminal_size()
    
    def main(self):
        curses.wrapper(self.cursesMain)

    def cursesMain(self, mainWin):
        self.mainWin = mainWin
        self.prepWin(mainWin)
        while True:
            self.checkModule()
            self.resizeWindow()
            self.currentModule.disp()
            self.moduleWin.refresh()
            code = self.currentModule.input()
            self.processCode(code)

    def resizeWindow(self):
        termSize = os.get_terminal_size()
        if termSize != self.size:
            self.size = termSize
            del termSize
            self.mainWin.resize(self.size.lines, self.size.columns)
            self.tabWin.resize(2, self.size.columns)
            self.moduleWin.resize(self.size.lines - 2, self.size.columns)

            
    def prepWin(self, mainWin):
        curses.cbreak()
        curses.curs_set(0)
        mainWin.clear()
        self.moduleWin = mainWin.subwin(self.size[1]-2, self.size[0], 2, 0)
        self.tabWin = mainWin.subwin(2, self.size[0], 0, 0)
        self.moduleWin.border()
        for i in self.tabsAt:
            self.moduleWin.addstr(0, i, "┴")
        
        for lineNum, line in enumerate(self.tabStr.splitlines()):
            self.tabWin.addstr(lineNum, 0, line)
        mainWin.refresh()
        self.moduleWin.refresh()

    def getModule(self, name):
        try:
            module = import_module(f"modules.{name}")
            return module
        except:
            raise Exception(f"Module modules.{name} not found!")
    
    def getClassFromModule(self, module, name, *args):
        try:
            moduleClass = getattr(module, name)
            module = moduleClass(*args)
            # ^ *args can break stuff if not passed in the right amount of arguments
            if module is None:
                raise Exception(f"Class {name} somehow screwed up")
            return module
        except:
            raise Exception(f"Class {name} not found!")
    
    def checkModule(self):
        if self.previousModuleName != self.currentModuleName\
            or not getattr(self, "currentModule", False):
                module = self.getModule(self.currentModuleName)
                if module is None:
                    raise Exception("module is None")
                self.currentModule = self.getClassFromModule(
                    module,
                    self.currentModuleName.title(),
                    self.moduleWin
                )
        if self.currentModule is None:
            raise Exception(f"Current module class is None\n{self.currentModuleName.title()}")
    
    def changeModule(self, name):
        self.previousModuleName = self.currentModuleName
        self.currentModuleName = name

    def processCode(self, code):
        if code:
            match code:
                case 1:
                    self.changeModule("tabs")
                case _:
                    raise Exception("Module not found")
    
    def createTabs(self):
        finStr = ""
        for i in self.loadedModules:
            finStr += " ╭" + "─"*(len(i) - 3) + "╮"
            
        finStr += "\n"
        
        for i in self.loadedModules:
            finStr += " │" + i[:-3] + "│"
        
        for p, i in enumerate(self.loadedModules):
            self.tabsAt.append(1 + p)
            self.tabsAt.append(2 + p + len(i) - 3)

        return finStr

if __name__ == "__main__":
    h = Hub()
    h.main()