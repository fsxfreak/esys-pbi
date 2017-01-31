import pylsl
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, core, sound 

def main():
    win = visual.Window([512, 512])

    # writes text to win on the back buffer
    message = visual.TextStim(win, text='ehllo') 
    message.setAutoDraw(True)
    win.flip() # displays back buffer to front

    core.wait(1.0)

    message.setText('world')
    win.flip()
    core.wait(1.0)

    print sound.Sound
    s = sound.Sound('stimulus-400.wav')
    s.play()
    #sound.Sound('A',secs=2)
    core.wait(2.0)

if __name__ == '__main__':
    main()
