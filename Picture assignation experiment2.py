from psychopy import visual,core #import visual and core module
from psychopy.hardware import keyboard #import keyboard from hardware module
import random
import math

win = visual.Window( [1000, 600],color='black') #defining the window
kb = keyboard.Keyboard() #defining the keyboard

#create a fixation cross
welcome_text=visual.TextStim (win, text="""Welcome to the experiment\n
Press i for information and space to directly start the experiment.""") 
#display the welcome_text
welcome_text.draw()
win.flip()
#define input to keyboard as keys and take the first key input only
#bc wait keys automatically made a list
#while loop assigning wished input: not in prüft, ob Taste eine der Optionen ist
while (key := kb.waitKeys()[0].name) not in ["i", "space"]:
    pass

if key == "i" : 
    infotext="""In the experiment you will have to assign pictures with temporal implications to the future or the past to 
    two buttons "future" and "past". The buttons will be located in the upper right or left corner of the screen. 
    To assign the picture to the button on the left press "a". If you want to assign the picture to the button on the right,
    please press "l".\nPress any key (e.g. space) to start."""
    visual.TextStim(win, text=infotext).draw()
    win.flip()
    kb.waitKeys()

image_count=4

#paths
past_images=[(f"past/past{i+1}.jpeg","past") for i in range(image_count)]
future_images=[(f"future/future{i+1}.jpeg","future") for i in range (image_count)]
#define how many trials occur
trials=6

results = [] # list of tuple (past/future, buttons_flipped, guess, rt)

#create a CountdownTimer with integrated numbers
countdown_circle=visual.Pie(win, fillColor="#ffe0b8", start = 0, end = 0)
countdown_timer=visual.TextStim(win, text = "3", color="#176e25",height=0.75)
n_frames = 250.
for i in range(round(n_frames)):
    percent = i / n_frames
    countdown_circle.end = percent * 365
    countdown_timer.text = str(math.ceil((1- percent) * 3))
    countdown_circle.draw()
    countdown_timer.draw()
    win.flip()


#create the assignation boxes
past_button=visual.TextStim (win, text='Past',color='black')
future_button=visual.TextStim (win, text='Future',color='black')
left_box=visual.Rect(win,lineWidth=2,fillColor='#ffe0b8',lineColor='#ffe0b8',color='#ffe0b8')
right_box=visual.Rect(win,lineWidth=2,fillColor='#ffe0b8',lineColor='#ffe0b8',color='#ffe0b8')


stimuli=random.sample(past_images+future_images,trials)
for stimulus_path, time_period in stimuli:
    #shuffle the buttons and assign them as left or right button
    buttons = [past_button, future_button]
    random.shuffle(buttons)
    left_button, right_button = buttons
    #load image
    picture_stimulus = visual.ImageStim(win, image=stimulus_path)
    picture_stimulus.size = (0.55, 1.2)
    #position the visual components
    left_box.pos = left_button.pos = (-0.8, 0.667)
    right_box.pos = right_button.pos = (0.8, 0.667)
    picture_stimulus.pos = (0,-0.15)

    #define the size of the buttons
    w, h = past_button.size
    
    right_box.size = left_box.size = (w * 0.67, h * 1.5)
    
    
    #draw components
    left_box.draw()
    right_box.draw()
    left_button.draw()
    right_button.draw()
    picture_stimulus.draw()
    win.flip()
    kb.clock.reset()
    #get the key input
    key = kb.waitKeys()[0]
    #wait for new input if it is not a or l
    while key.name not in ["a", "l"]:
        key = kb.waitKeys()[0]
    #check if the participant guessed past or future
    guess = "past" if (key.name == "a") == (left_button == past_button) else "future"
    results.append((time_period, right_button==past_button, guess, key.rt))
    
#open file for results
with open("results.csv", "w") as file:
    file.write("time period; condition; guess; reaction time\n")
    for tp,c,g,rt in results:
        print(f"{tp}, {c}, {g}, {rt}")
        file.write(f"{tp}; {c}; {g}; {rt}\n")
        

#end screen
end_text=visual.TextStim (win, text="""Thank you for participating. 
You have reached the end of the experiment.""")
#display the end text
end_text.draw()
win.flip()
core.wait(4)


