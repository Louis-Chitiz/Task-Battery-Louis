from psychopy import visual, event
import codecs
import re


def parse_instructions(input_data):
    '''
    parse instruction into pages
    page break is #
    '''

    text = re.findall(r'([^#]+)', input_data) # match any chars except for #

    return text

def load_instruction(PATH):
    '''
    load and then parse instrucition
    return a list
    '''
    import os
    with codecs.open(os.path.join(os.path.join(os.getcwd(),"mathtaskXiuyi"), PATH), 'r', encoding='utf8') as f:
        input_data = f.read()

    text = parse_instructions(input_data)

    return text

class instructions(object):
    '''
    show instruction and wait for trigger
    '''
    
    def __init__(self, window, instruction_txt):
        self.window = window
        self.instruction_txt = load_instruction(instruction_txt)

        self.display = visual.TextStim(
                window, text='default text', font='Arial', height=0.08,
                name='instruction',
                pos=[0,0], wrapWidth=1100,
                color='black',
                ) #object to display instructions

        self.display.size = 0.8
       

    def show(self):
        # get instruction
        for i, cur in enumerate(self.instruction_txt):
            self.display.setText(cur)
            self.display.draw()
            self.window.flip()
            event.waitKeys(keyList=['return'])