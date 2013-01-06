#!/usr/bin/env python
import kivy
kivy.require('1.4.1')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.scrollview import ScrollView
from kivy.factory import Factory
from kivy.clock import Clock
#from kivy.core.window import Keyboard
from kivy.interactive import InteractiveLauncher
from kivy.logger import Logger
from kivy.config import Config
Config.set('kivy', 'window_icon', 'icon.png')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
import re
import rollparse
from dicehelp import dice_help

class DiceEqnInput(TextInput):
    """This is where the equation will be entered.
    """
    history_stack_pos = -1
    true_parent = ObjectProperty(None)
    start_text = "Enter roll dice equation here."

    def clear_start_text(self):
        """When we need the start start text to be cleared. Will do
        nothing if it's already been cleared.
        
        Arguments:
        """
        if self.text == self.start_text:
            self.text = ""
    
    def __init__(self, **kwargs):
        """Here just in case I want to use it.
        
        Arguments:
        - `**kwargs`:
        """
        super(DiceEqnInput, self).__init__(**kwargs)

    def _keyboard_on_key_up(self, window, keycode, *args):
        """Handle up and down keys.
        
        Arguments:
        - `keycode`: the key that was just pressed
        """
        key, keycode_str = keycode
        #for Kivy before 1.4.2, invert the logic here since the
        #history stack is visually inverted
        if (keycode_str == 'down') and (self.history_stack_pos > 0):
            if (self.history_stack_pos != 0):
                self.history_stack_pos -= 1
            #this shouldn't be necessary, but just to be on the safe
            #side
            if (self.history_stack_pos >= 0) and (self.history_stack_pos < len(self.true_parent.history_stack)):
                self.true_parent.history_stack[self.history_stack_pos]()
        elif (keycode_str == 'up') and (self.history_stack_pos < len(self.true_parent.history_stack)):
            if (self.history_stack_pos < len(self.true_parent.history_stack)-1):
                self.history_stack_pos += 1
            #this shouldn't be necessary, but just to be on the safe
            #side
            if (self.history_stack_pos >= 0) and (self.history_stack_pos < len(self.true_parent.history_stack)):
                self.true_parent.history_stack[self.history_stack_pos]()
        return super(DiceEqnInput, self)._keyboard_on_key_up(window, keycode, *args)
        
class DiceWidget(Widget):
    dice_eqn_input = ObjectProperty(None) #text box where the equation
                                          #will be entered by the user
    dice_output = ObjectProperty(None) #text box where the parsed
                                       #equation and its answer will
                                       #be outputted
    dice_history = ObjectProperty(None) #history of equations that
                                        #have been entered
    roll_it_btn = ObjectProperty(None) #the button to submit the rolls
                                       #(although enter is just fine
                                       #too)
    history_stack = [] #all the lambdas for the equations that have
                       #been used before--history of equations, they
                       #set the dice_eqn_input text, return the text
                       #as well
    dice_images = ListProperty([])
    output_collector = "" #used for when we're about to print
                          #something to the dice output box
    mouse_postion = StringProperty("") #just used in debugging
    input_height = StringProperty("") #just used in debugging
    label_col_div = 6.5 # this is only used to position the debug
                        # labels
    help_is_on = False
    var_match = re.compile('\s*\w+\s*=\s*$')
    mult_eqns_end = re.compile('[^;]*;\s*$')
    help_match = re.compile('help', re.I)
    help_done = re.compile('done', re.I)
    var_list_bubble = ObjectProperty(None) #this is the variable list
                                           #that will show on the
                                           #screen
    var_dict = {} #this is the dictionary that will be used for
                  #storing the variables, and their lambdas to pull up
                  #their equations
    var_list_stack = [] #for workaround for Kivy 1.4.1

    def stash_print(self, output_str):
        """This will stash the strings to be printed until it's ready
        to be printed.
        
        Arguments:
        - `output_str`: The string that is eventually to be printed to
                        the output box.
        """
        self.output_collector += output_str + '\n'

    def complete_stash_print(self):
        """Once the collected print statements are ready to be
        printed, this should be called.
        
        Arguments:
        """
        self.dice_output.text = self.output_collector + self.dice_output.text
        self.dice_output.cursor = (0,0)
        self.output_collector=""
        
    def roll_it(self, *args):
        """This performs the actual roll.
        
        Arguments:
        """
        self.dice_eqn_input.clear_start_text()
        eqn_text = self.dice_eqn_input.text
        if eqn_text == '':
            Clock.schedule_once(self.set_eqn_focus)
            return

        if self.help_match.match(eqn_text):
            self.help_is_on = True
            self.dh = dice_help()
            help_str, self.dice_eqn_input.text = self.dh.next()
            self.stash_print(help_str)
            self.complete_stash_print()
            Clock.schedule_once(self.set_eqn_focus)
            return

        if self.help_done.match(eqn_text):
            self.help_is_on = False
            self.stash_print("Just type help again if you need it.")
            self.complete_stash_print()
            del self.dh
            self.dice_eqn_input.text=""
            Clock.schedule_once(self.set_eqn_focus)
            return

        try:
            if self.help_is_on:
                try:
                    help_str, self.dice_eqn_input.text = self.dh.next()
                    self.stash_print(help_str)
                    self.complete_stash_print()
                except StopIteration:
                    self.help_is_on = False
            var_array = [eqn.strip() for eqn in eqn_text.split('=', 2)]
            var_name = None
            if 1 < len(var_array):
                var_name, eqn_text = var_array
                self.add_var(var_name, eqn_text)
            self.add_to_history(eqn_text)
            eqns = [eqn.strip() for eqn in eqn_text.split(';')]
            for eqn_text in eqns:
                is_separated, const_strings, (ans_str, answers) = rollparse.solve_roll(eqn_text)
                self.stash_print(eqn_text)
                if 0 < len(const_strings) and not is_separated:
                    self.stash_print("\tCalculated constants:")
                    i = 1
                    for c in const_strings:
                        self.stash_print("\t  {0}: {1}".format(i, c))
                        i += 1

                if is_separated:
                    self.stash_print("\tRolls:")
                    for i in range(0, len(ans_str)):
                        const_counter = 1
                        for c_str in const_strings[i]:
                            self.stash_print("\t    [{0}: {1}]".format(const_counter, const_str))
                            const_counter += 1
                            self.stash_print("\t  {0}: {1} = {2}".format(i+1, ans_str[i], answers[i]))
                else:
                    self.stash_print("\t{0} = {1}".format(ans_str, answers))
        except Exception as e:
            print e
            self.stash_print(str(e))
        self.complete_stash_print()
        if not self.help_is_on:
            self.dice_eqn_input.text=""
        Clock.schedule_once(self.set_eqn_focus)

    def set_eqn(self, eqn_text, history_stack_pos):
        """Inserts the equation into the input box from the history.
        
        Arguments:
        - `eqn_text`: the equation from history
        - `history_stack_pos`: position in the history stack
        """
        self.dice_eqn_input.text=eqn_text
        self.dice_eqn_input.history_stack_pos=history_stack_pos
        return eqn_text

    def set_eqn_focus(self, dt):
        """Set the focus back on the input box.
        
        Arguments:
        - `dt`: not used
        """
        self.dice_eqn_input.focus=True

    def add_var(self, var_name, eqn_text):
        """Add to the variables bubble list and dictionary.
        
        Arguments:
        - `self`:
        - `var_name`:
        - `eqn_text`:
        """
        #This function was actually created and modeled after
        #self.add_to_history.  Relevant comments can be found there.
        new_btn=BubbleButton(text=var_name)
        last_pos=len(self.var_dict)
        eqn_fn = lambda *args: self.set_eqn(eqn_text, len(self.history_stack)+1)
        self.var_dict[var_name] = eqn_fn
        new_btn.bind(on_press=self.var_dict[var_name])
        try:
            kivy.require('1.4.2')
            self.var_dict[var_name] = eqn_fn
            self.var_list_bubble.content.add_widget(new_btn, last_pos+1)
        except Exception:
            self.var_list_bubble.content.clear_widgets()
            self.var_list_bubble.content.add_widget(new_btn)
            for dice_roll in reversed(self.var_list_stack):
                dice_bubble=BubbleButton(text=dice_roll)
                dice_bubble.bind(on_press=self.var_dict[dice_roll])
                self.var_list_bubble.content.add_widget(dice_bubble)
            self.var_list_stack.append(var_name)
        self.dice_eqn_input.history_stack_pos = len(self.history_stack)
        if not hasattr(self, 'bubble_height_var'):
            self.bubble_height_var=self.dice_eqn_input.height
        else:
            self.var_list_bubble.height+=self.bubble_height_var
            self.var_list_bubble.parent.height+=self.bubble_height_var

    def add_to_history(self, eqn_text):
        """Add to equations history
        
        Arguments:
        """
        #new button to be added to the history list
        new_btn=BubbleButton(text=eqn_text)
        last_pos=len(self.history_stack) #last position in the history
                                         #stack
        eqn_fn = lambda *args: self.set_eqn(eqn_text, last_pos)
        new_btn.bind(on_press=eqn_fn)
        try:
            #kivy 1.4.2 will respect the order bubble buttons are
            #added
            kivy.require('1.4.2') #this will throw an exception if
                                  #it's not 1.4.2
            self.history_stack.append(eqn_fn)
            self.dice_history.content.add_widget(new_btn, last_pos+1)
        except Exception:
            #nasty ugly work around for kivy issue #819
            self.dice_history.content.clear_widgets()
            self.dice_history.content.add_widget(new_btn)
            for dice_roll in reversed(self.history_stack):
                dice_bubble=BubbleButton(text=dice_roll())
                dice_bubble.bind(on_press=dice_roll)
                self.dice_history.content.add_widget(dice_bubble)
            self.history_stack.append(eqn_fn)
        self.dice_eqn_input.history_stack_pos = last_pos+1
        if not hasattr(self, 'bubble_height'):
            self.bubble_height=self.dice_eqn_input.height
        else:
            self.dice_history.height+=self.bubble_height
            #Why change the following? Because the parent is actually
            #an anchor layout.
            self.dice_history.parent.height+=self.bubble_height

    def on_touch_move(self, touch):
        """
        This is mostly being used for the purpose of laying things
        out, and getting a position.
        
        Arguments:
        - `touch`: mouse position
        """
        self.mouse_postion = str(touch.pos)
        return super(DiceWidget, self).on_touch_move(touch)

    def set_bind(self, image, dice_text):
        """This will bind the image's on_touch_up event.
        
        Arguments:
        - `image`: The image widget itself.
        - `dice_text`: The dice text that's to be used.
        """
        Logger.debug('DiceWidget: setting bind for ' + dice_text)
        image.bind(on_touch_up=lambda im, touch: self.add_dice_input(im, touch, dice_text))

    def add_dice_input(self, image, touch, dice_text=None):
        """This will add dice to dice_eqn_input.
        
        Arguments:
        - `dice_text`: This should never be None.
        """
        assert dice_text!=None, ("Something very bad happened."
                                 " Somehow I tried to add"
                                 " blank dice. Please report this.")
        if not image.collide_point(touch.x, touch.y):
            return
        #Logger.debug('DiceWidget: touch.button=' + touch.button)
        if touch.button != 'left':
            return
        #Logger.debug('DiceWidget: touch up for ' + dice_text)
        self.dice_eqn_input.clear_start_text()
        if self.dice_eqn_input.text == '':
            self.dice_eqn_input.text = dice_text
        elif self.var_match.match(self.dice_eqn_input.text) or self.mult_eqns_end.search(self.dice_eqn_input.text):
            self.dice_eqn_input.text += dice_text
        else:
            self.dice_eqn_input.text += ' + ' + dice_text

    def log_mesg(self, mesg='you forgot something...'):
        """For log messages.
        
        Arguments:
        - `mesg`: The debug message.
        """
        Logger.debug('DiceKV: ' + mesg)

class DiceApp(App):
    """
    Dice rolling app.
    """
    icon = "icon.ico"
    title = "Roll it!"
    def build(self):
        diceapp = DiceWidget()
        return diceapp

#Config.set('kivy', 'log_level', 'info')
Factory.register("DiceWidget", DiceWidget)
Factory.register("DiceEqnInput", DiceEqnInput)
if __name__ in ('__android__', '__main__'):
    DiceApp().run()
    #this seems to just crash unfortunately
    #il = InteractiveLauncher(DiceApp()).run()
