from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

# Declare both screens as separate classes. Currently there is nothing in here, but there will be when we fill out the GUI.


class CustomDropDown(DropDown):
    pass

class MenuScreen(Screen):
    translateInput = ObjectProperty(None)
    translateButton = ObjectProperty(None)
    translateLabel = ObjectProperty(None)
    top_layout = ObjectProperty(None)
    dd_btn = ObjectProperty(None)

    def __init__(self,*args,**kwargs):
        super(MenuScreen, self).__init__(*args, **kwargs)
        self.drop_down = CustomDropDown()
        notes_dropdown = ObjectProperty(None)
        dropdown = DropDown()
        notes = ['Features', 'Suggestions', 'Abbreviations', 'Miscellaneous']
        for note in notes:
            # when adding widgets, we need to specify the height manually (disabling
            # the size_hint_y) so the dropdown can calculate the area it needs.
            btn = Button(text='%r' % note, size_hint_y=None, height=30)
            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            # then add the button inside the dropdown
            dropdown.add_widget(btn)
        # create a big main button
        mainbutton = Button(text='Usage Notes 2', size_hint=(1, 1))
        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        mainbutton.bind(on_release=dropdown.open)
        #dd_btn.bind(on_release=dropdown.open)
        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        #dropdown.bind(on_select=lambda instance, x: setattr(dd_btn, 'text', x))
        self.top_layout.add_widget(mainbutton)

class SettingsScreen(Screen):
    pass



# Create the screen manager and add the two previously defined screens to it.
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()

#MORE COMMENTS ! (what would me future self want to know?)