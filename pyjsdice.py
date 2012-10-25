#import rollparse

import pyjd # this is dummy in pyjs
from pyjamas.ui.Button import Button
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.ListBox import ListBox
from pyjamas import Window
#from pyjamas import logging

def diceEqnOnClick(sender):
    sender.setText("")

def rollItOnClick(sender):
    pass

class DiceRollForm:
    diceEquation = None
    rollItButton = None
    resultsBox = None
    previousEqnsList = None

    def __init__(self):
        vpanel = VerticalPanel()
        hpanel = HorizontalPanel()
        hpanel_input = HorizontalPanel()
        diceEquation = TextBox()
        diceEquation.setText("Click here, and write in your dice roll equation.")
        diceEquation.addClickListener(diceEqnOnClick)
        diceEquation.setVisibleLength(60)
        rollItButton = Button("Roll It!", rollItOnClick)
        width = 550
        #logging.info("Width: " + width)
        resultsBox = TextArea()
        resultsBox.setReadonly(True)
        resultsBox.setWidth(650)
        resultsBox.setVisibleLines(50)
        previousEqnsList = ListBox()
        previousEqnsList.setWidth(500)
        previousEqnsList.setMultipleSelect(True)
        previousEqnsList.setVisibleItemCount(46)
        hpanel_input.add(diceEquation)
        hpanel_input.add(rollItButton)
        vpanel.add(hpanel_input)
        vpanel.add(resultsBox)
        hpanel.add(vpanel)
        hpanel.add(previousEqnsList)
        RootPanel().add(HTML("<h1>Diceroller: A better dice rolling program</h1>"))
        RootPanel().add(hpanel)        
        

if __name__ == '__main__':
    #logging.basicConfig(filename='pyjsdice.log',level=logging.DEBUG)
    #pyjd.setup("diceroller.html")
    diceroller = DiceRollForm()
    #pyjd.run()
