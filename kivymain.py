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
from kivy.clock import Clock
from kivy.core.window import Keyboard

class DiceEqnInput(TextInput):
    """This is where the equation will be entered.
    """
    history_stack_pos = -1
    true_parent = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        """
        
        Arguments:
        - `**kwargs`:
        """
        super(DiceEqnInput, self).__init__(**kwargs)
        pass

    def _keyboard_on_key_up(self, window, keycode, *args):
        """handle particular key events
        
        Arguments:
        - `self`: not used
        - `keycode`: the key that was just pressed
        """
        key, keycode_str = keycode
        if (keycode_str == 'up') and (self.history_stack_pos > 0):
            print "going up, history_stack_pos: ", self.history_stack_pos
            print "len(self.true_parent.history_stack): ", len(self.true_parent.history_stack)
            if (self.history_stack_pos != 0):
                self.history_stack_pos -= 1
                print "subtract 1 from history_stack_pos: ", self.history_stack_pos
            if (self.history_stack_pos >= 0) and (self.history_stack_pos < len(self.true_parent.history_stack)):
                self.true_parent.history_stack[self.history_stack_pos]()
                print "self.history_stack_pos after cb: ", self.history_stack_pos
        elif (keycode_str == 'down') and (self.history_stack_pos < len(self.true_parent.history_stack)):
            print "going down, history_stack_pos: ", self.history_stack_pos
            print "len(self.true_parent.history_stack): ", len(self.true_parent.history_stack)
            if (self.history_stack_pos < len(self.true_parent.history_stack)-1):
                self.history_stack_pos += 1
                print "added 1 from history_stack_pos: ", self.history_stack_pos
            if (self.history_stack_pos >= 0) and (self.history_stack_pos < len(self.true_parent.history_stack)):
                self.true_parent.history_stack[self.history_stack_pos]()
                print "self.history_stack_pos after cb: ", self.history_stack_pos
        
class DiceWidget(Widget):
    dice_eqn_input = ObjectProperty(None)
    dice_output = ObjectProperty(None)
    dice_history = ObjectProperty(None)
    roll_it_btn = ObjectProperty(None)
    history_stack = []
    mouse_postion = StringProperty("")
    input_height = StringProperty("")
    label_col_div = 6.5 # this is only used to position the debug labels

    def roll_it(self, *args):
        """This performs the actual roll.
        
        Arguments:
        - `self`: not used
        """
        eqn_text = self.dice_eqn_input.text
        self.add_to_history(eqn_text)
        self.dice_output.text+=eqn_text + '\n'
        self.dice_eqn_input.text=""
        self.dice_eqn_input.focus=True

    def set_eqn(self, eqn_text, history_stack_pos):
        """inserts the equation into the input box from the history
        
        Arguments:
        - `self`: not used
        - `eqn_text`: the equation from history
        - `history_stack_pos`: position in the history stack
        """
        self.dice_eqn_input.text=eqn_text
        self.dice_eqn_input.history_stack_pos=history_stack_pos

    def set_eqn_focus(self, dt):
        """set the focus back on the input box
        
        Arguments:
        - `self`:
        - `dt`:
        """
        self.dice_eqn_input.focus=True

    def add_to_history(self, eqn_text):
        """Add to equations history
        
        Arguments:
        - `self`: not used
        """
        new_btn=BubbleButton(text=eqn_text)
        last_pos=len(self.history_stack)
        print "last_pos: ", last_pos
        eqn_fn = lambda *args: self.set_eqn(eqn_text, last_pos)
        self.history_stack.append(eqn_fn)
        new_btn.bind(on_press=eqn_fn)
        self.dice_eqn_input.history_stack_pos = last_pos+1
        self.dice_history.add_widget(new_btn, last_pos+1)
        if not hasattr(self, 'bubble_height'):
            self.bubble_height=self.dice_eqn_input.height
        else:
            self.dice_history.height+=self.bubble_height
        Clock.schedule_once(self.set_eqn_focus)

    def on_touch_move(self, touch):
        """
        this is mostly being used for the purpose of laying things out
        Arguments:
        - `self`: not used
        - `touch`: mouse position
        """
        self.mouse_postion = str(touch.pos)

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
