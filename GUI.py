from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty

# Defines the screen manager to allow for multiple screens in the application along with two screens, a menu screen and a settings screen, as a string
Builder.load_string("""
<ScreenManager>:
    id: screen_manager
    MenuScreen:
        id: menu_screen
        name: 'MenuScreen'
        manager: screen_manager
    SettingsScreen:
        name: 'SettingsScreen'
        manager: screen_manager

<MenuScreen>:
    FloatLayout:
        Label:
            text: "Please enter the desired number of chords"
            size_hint: (.5,.125)
            pos_hint: {'x':.25,'y':.7}
        TextInput:
            id: menu_screen
            text: "Enter the desired number of chords"
            size_hint: (.5,.125)
            pos_hint: {'x':.25,'y':.5}
            multiline: False
        Button:
            text: 'Generate Melody'
            on_press: 
            #transfer the user input from the menu screen to the settings screen for later use
                root.manager.get_screen('SettingsScreen').label_text.text = str(menu_screen.text)
            #change to the settings screen after the user input has been accounted for
                root.manager.current = 'SettingsScreen'
            size_hint: (.25,.125)
            pos_hint: {'x':.375,'y':.3}

<SettingsScreen>:
    label_text: label_text
    FloatLayout:
        Label:
            id: label_text
            #The text here does not matter because the label_text text parameter is changed manually when the user clicks the button on the menu screen
            text: '1'
            size_hint: (.125,.0625)
            pos_hint: {'x':0,'y':.9375}
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
            size_hint: (.125,.0625)
            pos_hint: {'x':.875,'y':.9375}
""")

# Declare both screens as separate classes. Currently there is nothing in here, but there will be when we fill out the GUI.
class MenuScreen(Screen):
    pass

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