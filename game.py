from tkinter import *
import random,time
from agent import *
# from PIL import ImageTk, Image

GAME_WIDTH_HEIGHT = 400
BACKGROUND_COLOR = "#FFFFFF"

SPEED = 10

UNIT_X = 8
UNIT_Y = 8

SPACE_SIZE = GAME_WIDTH_HEIGHT/UNIT_X

arr_map = []

action_move = [0,1,2,3]

object_game = [[0]*UNIT_X for _ in range(UNIT_Y)]
object_color = [[0]*UNIT_X for _ in range(UNIT_Y)]
player_position = [0,0]

#Set position win
P_W_X = 3
P_W_Y = 5
object_color[P_W_Y-1][P_W_X-1] = 2

object_color[1][1] = 1
object_color[1][2] = 1
object_color[1][4] = 1
object_color[2][1] = 1
object_color[3][1] = 1
object_color[4][1] = 1

POINT = [0]

GAME_WIDTH = GAME_WIDTH_HEIGHT
GAME_HEIGHT = (GAME_WIDTH_HEIGHT/UNIT_X)*UNIT_Y

trap = []

for t,n in zip(object_color,range(UNIT_Y)):
    for t2,n2 in zip(t,range(UNIT_X)):
        if t2 == 1:
            trap.append([(n*SPACE_SIZE),(n2*SPACE_SIZE)])

print(trap)

def get_status(pp):
    _win = 0
    if pp[0] == ((P_W_X-1)*SPACE_SIZE) and pp[1] == ((P_W_Y-1)*SPACE_SIZE):
        _win = 1
    elif [pp[1],pp[0]] in trap:
        _win = -1
    return _win

def get_object_color(object):
    color = ["white","red",'green']
    return color[object]

def build_object_map(object_color):
    _get_new_position_object = [0,0]
    for arr_oc in object_color:
        for oc in arr_oc:
            tag_name = 'Oj_'+str(oc)+"_"+str(_get_new_position_object[0])+"_"+str(_get_new_position_object[1])
            canvas.create_rectangle(_get_new_position_object[0], _get_new_position_object[1], _get_new_position_object[0] + SPACE_SIZE, _get_new_position_object[1] + SPACE_SIZE, fill=get_object_color(oc),tag=tag_name)
            _get_new_position_object[0] += SPACE_SIZE
        _get_new_position_object[1] += SPACE_SIZE
        _get_new_position_object[0] = 0
    

def movement(key):
    if key == 0:
        if player_position[0] >= SPACE_SIZE :
            player_position[0] -= SPACE_SIZE
    elif key == 1:
        if player_position[0] < GAME_WIDTH-SPACE_SIZE :
            player_position[0] += SPACE_SIZE
    elif key == 2:
        if player_position[1] >= SPACE_SIZE :
            player_position[1] -= SPACE_SIZE
    elif key == 3:
        if player_position[1] < GAME_HEIGHT-SPACE_SIZE:
            player_position[1] += SPACE_SIZE


def next_turn(agent):

        state_S = str(player_position[0])+','+str(player_position[1])
        A_S = agent.agent_play_start(state_S)
        movement(A_S)
        state_E = str(player_position[0])+','+str(player_position[1])
        agent.agent_play_end(A_S,state_E,get_status(player_position))

        x = 0
        y = 0
        canvas.delete("player")
        point = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill='blue',tag='player')
        canvas.move(point,player_position[0],player_position[1])
        canvas.pack()
        HOW = get_status(player_position)
        if HOW == 1 or HOW == -1:
            global award,loop_state
            award += HOW
            loop_state += 1
            label.config(text="AWARD:{} STATE_AWARD: {}".format(award,loop_state))
            canvas.delete("player")
            player_position[0] = 0
            player_position[1] = 0
            point = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill='blue',tag='player')


        window.after(SPEED, next_turn,agent)

    

window = Tk()
window.title("AGENT AI TEST")
window.resizable(False,False)
award = 0
label = Label(window, text="AWARD:{}".format(award),font=('consolas',20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
build_object_map(object_color)
window.update()
loop_state = 0
st = '('+str(player_position[0])+','+str(player_position[1])+')'
agent = Agent(action_move,st )
next_turn(agent)
window.mainloop()