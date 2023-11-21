import keyboard
import motionControl

# Constants
MOVE_FORWARD_SPEED = 0.34
MOVE_BACKWARD_SPEED = -0.34

# Initial state
movement_states = {'FWD': False, 'BWD': False, 'RTWD': False, 'LFWD': False}

def keyBoardCommand():
    global movement_states

    # Stop motion if no keys are pressed
    if not any(keyboard.is_pressed(key) for key in ['w', 's', 'a', 'd']):
        motionControl.moveSTOP()
        # Reset all movement states
        movement_states = {key: False for key in movement_states}

    # Handle key presses
    # Handle key presses
    for key in ['w', 's', 'a', 'd']:
        if keyboard.is_pressed(key) and not movement_states[key]:
            if key == 'w':
                motionControl.moveL(MOVE_FORWARD_SPEED)
            elif key == 's':
                motionControl.moveL(MOVE_BACKWARD_SPEED)
            elif key == 'd':
                motionControl.moveRT(MOVE_FORWARD_SPEED)
            elif key == 'a':
                motionControl.moveRT(MOVE_BACKWARD_SPEED)
    
            movement_states[key] = True
    
        elif not keyboard.is_pressed(key):
            movement_states[key] = False




            
