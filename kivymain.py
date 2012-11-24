import kivy
kivy.require('1.4.1')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory

class DiceEqnInput(Widget):
    """
    This is where the dice equation will be entered by the user
    """
    eqn_input_box = ObjectProperty(None)

class DiceWidget(Widget):
    dice_eqn_input = ObjectProperty(None)
    dice_output = ObjectProperty(None)
    mouse_postion = StringProperty("")
    input_height = StringProperty("")
    label_col_div = 6.5 # this is only used to position the debug labels

    def on_touch_move(self, touch):
        """
        this is mostly being used for the purpose of laying things out
        Arguments:
        - `self`:
        - `touch`:
        """
        self.mouse_postion = str(touch.pos)
        #self.dice_output.center = touch.pos
        #self.dice_input.center = touch.pos

class DiceApp(App):
    """
    dice rolling app
    """
    def build(self):
        diceapp = DiceWidget()
        return diceapp
    
Factory.register("DiceWidget", DiceWidget)
Factory.register("DiceEqnInput", DiceEqnInput)
if __name__ == '__main__':
    DiceApp().run()
