import pylsl
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, core, sound 

# LSL.openChannel('name', type, UID)

def main():
    win = visual.Window([512, 512])

    # writes text to win on the back buffer
    message = visual.TextStim(win, text='ehllo') 
    message.setAutoDraw(True)
    win.flip() # displays back buffer to front

    core.wait(1.0)

    for i in xrange(0, 10):
      if i % 2:
        message.setText('odd')
      else:
        message.setText('even')

      win.flip()
      core.wait(1.0)

    sound.Sound('stimulus-400.wav').play()
    core.wait(2.0)

if __name__ == '__main__':
    main()
