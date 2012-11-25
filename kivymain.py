import kivy
kivy.require('1.4.1')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.scrollview import ScrollView
from kivy.factory import Factory

class DiceEqnInput(TextInput):
    """This is where the equation will be entered.
    """
    
    def __init__(self, **kwargs):
        """
        
        Arguments:
        - `**kwargs`:
        """
        super(DiceEqnInput, self).__init__(**kwargs)
        pass


class DiceWidget(Widget):
    dice_eqn_input = ObjectProperty(None)
    dice_output = ObjectProperty(None)
    dice_history = ObjectProperty(None)
    roll_it_btn = ObjectProperty(None)
    mouse_postion = StringProperty("")
    input_height = StringProperty("")
    label_col_div = 6.5 # this is only used to position the debug labels

    def roll_it(self):
        """This performs the actual roll.
        
        Arguments:
        - `self`: not used
        """
        eqn_text = self.dice_eqn_input.text
        self.add_to_history(eqn_text)
        self.dice_output.text += eqn_text + '\n'
        pass

    def set_eqn(self, eqn_text):
        """inserts the equation into the input box from the history
        
        Arguments:
        - `self`: not used
        - `eqn_text`: the equation from history
        """
        self.dice_eqn_input.text=eqn_text

    def add_to_history(self, eqn_text):
        """Add to equations history
        
        Arguments:
        - `self`:
        """
        new_btn=BubbleButton(text=eqn_text)
        new_btn.bind(on_press=lambda x, *args: self.set_eqn(eqn_text))
        self.dice_history.add_widget(new_btn)
        if not hasattr(self, '__bubble_height'):
            self.__bubble_height=new_btn.height
        else:
            self.dice_history.height+=self.__bubble_height

    def on_touch_move(self, touch):
        """
        this is mostly being used for the purpose of laying things out
        Arguments:
        - `self`: not used
        - `touch`: mouse position
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
