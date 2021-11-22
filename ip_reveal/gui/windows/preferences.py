import PySimpleGUIQt as psg


class Window(object):
    
    active = False
    
    tab1_layout = [
            [psg.Checkbox('Enable SecureKill', enable_events=True, key='SECURE_KILL_CHECK')],
            [psg.Text('Name of program to kill:', visible=False, key='SECURE_KILL_PROG_LABEL', size=(175,30)),
             psg.InputText(visible=False, key='SECURE_KILL_PROG', size=(175,30))]
            ]
    
    layout = [
            [
                    psg.TabGroup([[psg.Tab('SecureKill', tab1_layout, tooltip='Kill a program if your IP changes.',)]])
                    ],
            [
                    psg.Button('Save and Exit', disabled=True, key='SAVE_BUTTON'),
                    psg.Button('Exit', key='EXIT_BUTTON')
                    ]
            
            ]
    
    win = psg.Window('Preferences', layout=layout, size=(400,200))
    
    running = False
    
    def run(self):
        self.running = True
        vals_last_save = None
        while self.running:
            event, values = self.win.read(100)

            if vals_last_save is None:
                vals_last_save = values

            vals_differ = (vals_last_save != values)

            save_button_color = 'green' if vals_differ else 'red'
            self.win['SAVE_BUTTON'].update(disabled=not vals_differ, button_color=('black', save_button_color))

            cbox_now = values['SECURE_KILL_CHECK']

            self.win['SECURE_KILL_PROG_LABEL'].update(visible=cbox_now)
            self.win['SECURE_KILL_PROG'].update(visible=cbox_now)

            if event is None:
                self.running = False
                self.win.close()
            if event == 'EXIT_BUTTON':
                self.running = False
                self.win.close

win = Window()
win.run()
