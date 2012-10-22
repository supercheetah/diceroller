import rollparse

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

class DiceEquationInput(TextBox):
    def __init__(self):
        self.setText("Click here, and write in your dice roll equation.")

    def onClick(self, sender):
        self.setText("")

class DiceRollForm:
    def __init__(self):
        vpanel = VerticalPanel()
        hpanel = HorizontalPanel()
        hpanel_input = HorizontalPanel()
        dice_equation = DiceEquationInput()
        roll_it_button = Button()
        results_box = TextBox()
        results_box.setReadonly(True)
        previous_eqns_list = ListBox()
        hpanel_input.add(dice_equation)
        hpanel_input.add(roll_it_button)
        vpanel.add(hpanel_input)
        vpanel.add(results_box)
        hpanel.add(vpanel)
        hpanel.add(previous_eqns_list)
        RootPanel().add(HTML("<h1>Roll it!</h1>"))
        
        

if __name__ == '__main__':
    #pyjd.setup("diceroller.html")
    diceroller = DiceRollForm()
