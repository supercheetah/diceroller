#!/usr/bin/env python
"""
This is the main module for the RollIt! GUI to diceroller.
"""
import cli_args
import kivy
kivy.require('1.4.1')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.scrollview import ScrollView
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.spinner import Spinner
from kivy.interactive import InteractiveLauncher
from kivy.logger import Logger
from kivy.config import Config
Config.set('kivy', 'window_icon', 'icon.png')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
import re
import rollparse
from dicehelp import dice_help
import pickle
import traceback
import sys

MOBILE = kivy.utils.platform() in ('android', 'ios')
IS_ANDROID = ('android' == kivy.utils.platform())

DICE_HISTORY_FILE = "dice_history.txt"
VARDB_FILE = "vardb.pickle"

if IS_ANDROID:
    import android
else:
    import os
    import errno
    ROLLIT_DIR = os.path.expanduser("~{0}rollit{0}".format(os.sep))
    DICE_HISTORY_FILE = (ROLLIT_DIR + "{0}").format(DICE_HISTORY_FILE)
    VARDB_FILE = (ROLLIT_DIR + "{0}").format(VARDB_FILE)

class DiceEqnInput(TextInput):
    """This is where the equation will be entered.
    """
    history_stack_pos = -1
    true_parent = ObjectProperty(None)
    start_text = "Enter roll dice equation here."
    empty_space = re.compile('^\s*$')
    had_focus = False

    def clear_start_text(self):
        """When we need the start start text to be cleared. Will do
        nothing if it's already been cleared.
        
        Arguments:
        """
        if self.text == self.start_text:
            self.text = ""

    def is_empty(self):
        """Clears the start text, and returns whether or not it's empty.
        
        Arguments:
        - `self`:
        """
        self.clear_start_text()
        return None != self.empty_space.match(self.text)

    def cursor_forward(self):
        """Moves the cursor up one.
        
        Arguments:
        - `self`:
        """
        if len(self.text) > self.cursor_col:
            self.cursor = ( self.cursor_col + 1, 0 )

    def cursor_back(self):
        """Moves the cursor back one.
        
        Arguments:
        - `self`:
        """
        if 0 < self.cursor_col:
            self.cursor = ( self.cursor_col - 1, 0 )

    def add_at_cursor(self, spinner, is_open):
        """This is called when ever the num_spinner is opened or closed.
        
        Arguments:
        - `self`:
        - `spinner`:
        - `is_open`:
        """
        if not is_open:
            self.clear_start_text()
            Logger.debug("DiceEqnInput: num_spinner opened, text=" + str(spinner.text))
            _col = self.cursor_col
            pre_cur_txt = self.text[0:_col]
            post_cur_txt = self.text[_col:len(self.text)]
            self.text = pre_cur_txt + spinner.text + post_cur_txt
            self.cursor = ( _col + len(spinner.text), 0 )
            if self.had_focus:
                Logger.debug("DiceEqnInput: had focus, refocusing")
                if self.true_parent.mobile:
                    self.focus = True

    def _keyboard_on_key_up(self, window, keycode):
        """Handle up and down keys.
        
        Arguments:
        - `keycode`: the key that was just pressed
        """
        Logger.debug("DiceEqnInput: {0}".format(str(keycode)))
        key, keycode_str = keycode
        if (keycode_str == 'down') and (self.history_stack_pos > 0):
            if (self.history_stack_pos != 0):
                self.history_stack_pos -= 1
            #this shouldn't be necessary, but just to be on the safe
            #side
            if (self.history_stack_pos >= 0) and \
                    (self.history_stack_pos < \
                         len(self.true_parent.history_stack)):
                self.true_parent.history_stack[self.history_stack_pos]()
        elif (keycode_str == 'up') and \
                (self.history_stack_pos < \
                     len(self.true_parent.history_stack)):
            if (self.history_stack_pos < \
                    len(self.true_parent.history_stack)-1):
                self.history_stack_pos += 1
            #this shouldn't be necessary, but just to be on the safe
            #side
            if (self.history_stack_pos >= 0) and \
                    (self.history_stack_pos < \
                         len(self.true_parent.history_stack)):
                self.true_parent.history_stack[self.history_stack_pos]()
        return super(DiceEqnInput, self)._keyboard_on_key_up(window, keycode)
        
class DiceWidget(FloatLayout):
    dice_eqn_input = ObjectProperty(None) #text box where the equation
                                          #will be entered by the user
    dice_output = ObjectProperty(None) #text box where the parsed
                                       #equation and its answer will
                                       #be outputted
    dice_history = ObjectProperty(None) #BubbleButton history of
                                        #equations that have been
                                        #entered
    roll_it_btn = ObjectProperty(None) #the button to submit the rolls
                                       #(although enter is just fine
                                       #too)
    num_spinner = ObjectProperty(None)
    cur_fwd_btn = ObjectProperty(None)
    cur_bk_btn = ObjectProperty(None)
    history_stack = [] #all the lambdas for the equations that have
                       #been used before--history of equations, they
                       #set the dice_eqn_input text, return the text
                       #as well
    dice_images = ListProperty([])
    output_collector = "" #used for when we're about to print
                          #something to the dice output box
    help_is_on = False
    var_match = re.compile('\s*\w+\s*:\s*$')
    mult_eqns_end = re.compile('[^;]*;\s*$')
    end_is_blank = re.compile('\s*\w+\s*:\s*$|[^;]*;\s*$|^\s*$')
    has_op = re.compile('[-+*/]\s*$')
    help_match = re.compile('help', re.I)
    help_done = re.compile('done', re.I)
    var_list_bubble = ObjectProperty(None) #this is the variable list
                                           #that will show on the
                                           #screen
    var_dict = {} #this is the dictionary that will be used for
                  #storing the variables, and their lambdas to pull up
                  #their equations
    var_list_stack = [] #for workaround for Kivy 1.4.1
    mobile = MOBILE
    is_android = IS_ANDROID

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
        self.dice_output.cursor = (0, 0)
        self.output_collector = ""
        
    def roll_it(self, *args):
        """This performs the actual roll.
        
        Arguments:
        """
        self.dice_eqn_input.clear_start_text()
        eqn_text = self.dice_eqn_input.text
        if eqn_text == '':
            if not MOBILE:
                Clock.schedule_once(self.set_eqn_focus)
            return

        if self.help_match.match(eqn_text):
            self.help_is_on = True
            self.dh = dice_help()
            help_str, self.dice_eqn_input.text = self.dh.next()
            self.stash_print(help_str)
            self.complete_stash_print()
            if not MOBILE:
                Clock.schedule_once(self.set_eqn_focus)
            return

        if self.help_done.search(eqn_text):
            self.help_is_on = False
            self.stash_print("Just type help again if you need it.")
            self.complete_stash_print()
            del self.dh
            self.dice_eqn_input.text = ""
            if not MOBILE:
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
            var_array = [eqn.strip() for eqn in eqn_text.split(':', 2)]
            var_name = None
            is_var = False
            if 1 < len(var_array):
                var_name, eqn_text = var_array
                is_var = True
            eqn_text_save = eqn_text
            eqns = [eqn.strip() for eqn in eqn_text.split(';')]
            for eqn_text in reversed(eqns):
                is_separated, const_strings, (ans_str, answers) = \
                    rollparse.solve_roll(eqn_text)
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
                            self.stash_print("\t    [{0}: {1}]".format( \
                                    const_counter, c_str))
                            const_counter += 1
                        self.stash_print("\t  {0}: {1} = {2}".format( \
                                i+1, ans_str[i], answers[i]))
                else:
                    self.stash_print("\t{0} = {1}".format(ans_str, answers))
            self.add_to_history(eqn_text_save)
            if is_var:
                self.add_var(var_name, eqn_text_save)
        except Exception as e:
            print e
            self.stash_print(str(e))
        self.complete_stash_print()
        if not self.help_is_on:
            self.dice_eqn_input.text = ""
        if not MOBILE:
            Clock.schedule_once(self.set_eqn_focus)
        if MOBILE:
            self.dice_eqn_input.focus = False
        self.hide_vkbd()

    def set_eqn(self, eqn_text, history_stack_pos):
        """Inserts the equation into the input box from the history.
        
        Arguments:
        - `eqn_text`: the equation from history
        - `history_stack_pos`: position in the history stack
        """
        self.dice_eqn_input.text = eqn_text
        self.dice_eqn_input.history_stack_pos = history_stack_pos
        return eqn_text

    def set_eqn_focus(self, dt):
        """Set the focus back on the input box.
        
        Arguments:
        - `dt`: not used
        """
        self.dice_eqn_input.focus = True

    def add_var(self, var_name, eqn_text, do_save=True):
        """Add to the variables bubble list and dictionary.
        
        Arguments:
        - `self`:
        - `var_name`:
        - `eqn_text`:
        """
        #This function was actually created and modeled after
        #self.add_to_history.  Relevant comments can be found there.
        var_exists = var_name in self.var_dict
        self.var_dict[var_name] = eqn_text
        if do_save:
            with open(VARDB_FILE, 'wb') as var_file:
                pickle.dump( self.var_dict, var_file )
        if not var_exists:
            new_btn = BubbleButton(text = var_name)
            last_pos = len(self.var_dict)
            new_btn.bind(on_press = lambda *args: self.set_eqn( \
                    self.var_dict[var_name], len(self.history_stack)+1))
            try:
                kivy.require('1.4.2')
                self.var_list_bubble.content.add_widget(new_btn, last_pos+1)
            except Exception:
                self.var_list_bubble.content.clear_widgets()
                self.var_list_bubble.content.add_widget(new_btn)
                for dice_roll in reversed(self.var_list_stack):
                    dice_bubble = BubbleButton(text = dice_roll)
                    dice_bubble.bind(on_press = self.var_dict[dice_roll])
                    self.var_list_bubble.content.add_widget(dice_bubble)
                self.var_list_stack.append(var_name)
            if not hasattr(self, 'bubble_height_var'):
                self.bubble_height_var = self.dice_eqn_input.height
            else:
                self.var_list_bubble.height += self.bubble_height_var
                self.var_list_bubble.parent.height += self.bubble_height_var

    def add_to_history(self, eqn_text, do_save=True):
        """Add to equations history
        
        Arguments:
        """
        #new button to be added to the history list
        new_btn = BubbleButton(text = eqn_text)
        last_pos = len(self.history_stack) 
        eqn_fn = lambda *args: self.set_eqn(eqn_text, last_pos)
        if do_save:
            append_overwrite = 'a' if last_pos < 40 else 'w'
            with open(DICE_HISTORY_FILE, append_overwrite) as dh_file:
                # We only care about the last 40
                if last_pos >= 40:
                    for eqn in self.history_stack[last_pos-40:last_pos]:
                        dh_file.write(eqn + '\n')
                dh_file.write(eqn_text + '\n')
        new_btn.bind(on_press = eqn_fn)
        try:
            #kivy 1.4.2 will respect the order bubble buttons are
            #added
            kivy.require('1.4.2') #this will throw an exception if
                                  #it's not 1.4.2 or later
            self.history_stack.append(eqn_fn)
            self.dice_history.content.add_widget(new_btn, last_pos+1)
        except Exception:
            #nasty ugly work around for kivy issue #819
            self.dice_history.content.clear_widgets()
            self.dice_history.content.add_widget(new_btn)
            for dice_roll in reversed(self.history_stack):
                dice_bubble = BubbleButton(text = dice_roll())
                dice_bubble.bind(on_press = dice_roll)
                self.dice_history.content.add_widget(dice_bubble)
            self.history_stack.append(eqn_fn)
        self.dice_eqn_input.history_stack_pos = last_pos+1
        if not hasattr(self, 'bubble_height'):
            self.bubble_height = self.dice_eqn_input.height
        else:
            self.dice_history.height += self.bubble_height
            #Why change the following? Because the parent is actually
            #an anchor layout.
            self.dice_history.parent.height += self.bubble_height

    def set_bind(self, image, dice_text):
        """This will bind the image's on_touch_up event.
        
        Arguments:
        - `image`: The image widget itself.
        - `dice_text`: The dice text that's to be used.
        """
        Logger.debug('DiceWidget: setting bind for ' + dice_text)
        image.bind(on_touch_up = lambda im, touch: \
                       self.add_dice_input(im, touch, dice_text))

    def add_dice_input(self, image, touch, dice_text = None):
        """This will add dice to dice_eqn_input.
        
        Arguments:
        - `dice_text`: This should never be None.
        """
        assert dice_text != None, ("Something very bad happened."
                                   " Somehow I tried to add"
                                   " blank dice. Please report this.")
        if not image.collide_point(touch.x, touch.y):
            return
        if hasattr(touch, 'button'):
            if touch.button != 'left':
                return
        self.dice_eqn_input.clear_start_text()
        if self.dice_eqn_input.text == '':
            self.dice_eqn_input.text = dice_text
        elif self.var_match.match(self.dice_eqn_input.text) or \
                self.mult_eqns_end.search(self.dice_eqn_input.text) or \
                self.has_op.search(self.dice_eqn_input.text):
            self.dice_eqn_input.text += dice_text
        else:
            self.dice_eqn_input.text += ' + ' + dice_text

    def sep_rolls_add(self):
        """Adds a separated roll into the dice input box.
        
        Arguments:
        - `self`:
        """
        self.dice_eqn_input.clear_start_text()
        if not self.end_is_blank.match(self.dice_eqn_input.text):
            return
        self.dice_eqn_input.text += '{xd}'
        self.dice_eqn_input.cursor = (self.dice_eqn_input.cursor[0] - 3, 0)
        Clock.schedule_once(self.set_eqn_focus)

    def named_roll_add(self):
        """Adds a named roll into the dice input box.
        
        Arguments:
        - `self`:
        """
        self.dice_eqn_input.clear_start_text()
        if self.dice_eqn_input.is_empty():
            self.dice_eqn_input.text = 'Named roll: '
            self.dice_eqn_input.select_text(0, 10)
            self.dice_eqn_input.cursor = (self.dice_eqn_input.cursor[0] - 2, 0)
            Clock.schedule_once(self.set_eqn_focus)

    def hide_vkbd(self, *args):
        """Hide the virtual keyboard.
        
        Arguments:
        - `self`:
        """
        Logger.debug("DiceWidget: hiding keyboard")
        if IS_ANDROID:
            android.hide_keyboard()

    def on_touch_up(self, touch):
        """Receives touch events. Hides the keyboard on mobile devices
        if the touch is anywhere except on dice_eqn_input.
        
        Arguments:
        - `self`:
        - `touch`:
        """
        dei = self.dice_eqn_input
        Logger.debug("DiceWidget: touch.pos: " + str(touch.pos))
        Logger.debug("DiceWidget: \tdice_eqn_input collision: "
                     + str(self.dice_eqn_input.collide_point(*touch.pos)
                           ))
        rel_layout = self.num_spinner.parent
        if not self.dice_eqn_input.collide_point(*touch.pos) and \
                not self.cur_bk_btn.collide_point(*touch.pos) and \
                not self.cur_fwd_btn.collide_point(*touch.pos):
            self.hide_vkbd()
            self.dice_eqn_input.had_focus = False
            if MOBILE:
                self.dice_eqn_input.focus = False

        if self.num_spinner.collide_point(*rel_layout.to_widget(*touch.pos)) \
                and self.dice_eqn_input.focus:
            self.dice_eqn_input.had_focus = True
            self.hide_vkbd()
            Logger.debug("DiceWidget: dice_eqn_input had focus, hiding kbd")
            if MOBILE:
                self.dice_eqn_input.focus = False

        return super(DiceWidget, self).on_touch_up(touch)

    def log_mesg(self, mesg = 'you forgot something...'):
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
        Logger.debug('DiceApp: 01062012 App start')
        self.diceapp = DiceWidget()
        return self.diceapp

    def on_pause(self):
        """We just want to pause on the mobile app, not completely
        shut down.
        
        Arguments:
        - `self`:
        """
        return True

    def on_resume(self):
        """Things we need to do on resuming the app on a mobile
        device.
        
        Arguments:
        - `self`:
        """
        pass

    def on_start(self):
        """Things to do when first starting up.
        
        Arguments:
        - `self`:
        """
        try:
            with open(DICE_HISTORY_FILE, 'r') as dh_file:
                for line in dh_file:
                    self.diceapp.add_to_history(line.strip(), False)
        except IOError as e:
            Logger.debug("DiceApp: Can't read history file")

        try:
            vardb = None
            with open(VARDB_FILE, 'rb') as var_file:
                vardb = pickle.load(var_file)
            for var_name, eqn_text in vardb.iteritems():
                self.diceapp.add_var(var_name, eqn_text, False)
        except Exception as e:
            Logger.debug("DiceApp: Can't read variables file")
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname, lineno, fn, text = frame
                Logger.debug("Error in %s on line %d" % (fname, lineno))

    
    def on_stop(self):
        """Things to do when the app is shutting down.
        
        Arguments:
        - `self`:
        """
        pass

Factory.register("DiceWidget", DiceWidget)
Factory.register("DiceEqnInput", DiceEqnInput)
if __name__ == '__main__':
    if not cli_args.dice_args.debug:
        Config.set('kivy', 'log_level', 'info')
    if not MOBILE:
        try:
            Logger.debug("main: making dir " + ROLLIT_DIR)
            os.makedirs(ROLLIT_DIR)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                Logger.debug("main: cannot make {} due to error: {}".format(ROLLIT_DIR, exception))
                raise
    DiceApp().run()
    #this seems to just crash unfortunately
    #il = InteractiveLauncher(DiceApp()).run()
