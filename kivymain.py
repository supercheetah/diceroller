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
import rollparse

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
    output_spool = ""
    mouse_postion = StringProperty("")
    input_height = StringProperty("")
    label_col_div = 6.5 # this is only used to position the debug labels

    def spool_print(self, output_str):
        """This will store the strings to be printed until it's ready to be printed.
        
        Arguments:
        - `self`: not used
        - `output_str`: The string that is eventually to be printed to the output box.
        """
        self.output_spool += output_str + '\n'

    def complete_spool_print(self):
        """Once the spool is ready to be printed, this should be called.
        
        Arguments:
        - `self`: not used
        """
        self.dice_output.text = self.output_spool + self.dice_output.text
        self.dice_output.cursor = (0,0)
        self.output_spool=""
        
    def roll_it(self, *args):
        """This performs the actual roll.
        
        Arguments:
        - `self`: not used
        """
        eqn_text = self.dice_eqn_input.text
        try:
            is_separated, const_strings, (ans_str, answers) = rollparse.solve_roll(eqn_text)
            self.add_to_history(eqn_text)
            self.spool_print(eqn_text)
            if 0 < len(const_strings) and not is_separated:
                self.spool_print("Calculated constants:")
                i = 1
                for c in const_strings:
                    spool_print("  {0}: {1}".format(i, c))
                    i += 1

            if is_separated:
                self.spool_print("Rolls:")
                for i in range(0, len(ans_str)):
                    const_counter = 1
                    for c_str in const_strings[i]:
                        self.spool_print("    [{0}: {1}]".format(const_counter, const_str))
                        const_counter += 1
                    self.spool_print("  {0}: {1} = {2}".format(i+1, ans_str[i], answers[i]))
            else:
                self.spool_print("{0} = {1}".format(ans_str, answers))
        except Exception as e:
            print e
            self.spool_print(str(e))
        self.complete_spool_print()
        self.dice_eqn_input.text=""
        Clock.schedule_once(self.set_eqn_focus)

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
