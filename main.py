import curses as c
import time
import fact
from random import randint

stdscr = c.initscr()
c.start_color()
c.use_default_colors()
for i in range(0, c.COLORS):
    c.init_pair(i, i, -1);
c.noecho()
c.cbreak()
stdscr.keypad(1)

def exit_program(player):
    c.endwin()
    print("SCORE:",player.score)
    exit()

def end_game(player):
    c.endwin()
    print("SCORE:",player.score)
    print("Congratulations!")
    exit()

def char_pressed():
    x = stdscr.getch()
    if x == -1:
        return ""
    else:
        return chr(x)

def update_offset(offset,offset_count):
    offset_count += 1
    if offset_count > 10:
        offset = not offset
        offset_count = 0
    return offset, offset_count


begin_x = 0
begin_y = 0
height,width = stdscr.getmaxyx() #48,211
win = c.newwin(height, width, begin_y, begin_x)

offset = True
offset_count = 0
buf = "Game"
stdscr.nodelay(1)

percent = 100
level = fact.Land(100,25,[],percent)
player = fact.Player(randint(int(level.width/4),int(level.width*3/4)),randint(int(level.height/4),int(level.height*3/4)))
player.energy = 1000
msg = "[q] to exit"

while True:
    ch = char_pressed()
    if ch != "":
        buf += ch
        ch = buf[-1]
        
        if ch == "q":
            exit_program(player)
    
        # Move Character
        ch = ord(ch)
        if ch == c.KEY_RIGHT:
            player.move(level,1,0)
            offset = True
        if ch == c.KEY_LEFT:
            player.move(level,-1,0)
            offset = True            
        if ch == c.KEY_DOWN:
            player.move(level,0,1)
            offset = True            
        if ch == c.KEY_UP:
            player.move(level,0,-1)
            offset = True            
        if chr(ch) == "m":
            level.mine(player,player.x,player.y)
        if chr(ch) == "b":
            msg = level.build(player,player.x,player.y,msg)
        if chr(ch) == "p":
            msg = level.connector(player,player.x,player.y,msg)
        if chr(ch) == "e":
            msg = level.energizer(player,player.x,player.y,msg)
        if chr(ch) == "d":
            msg = level.digger(player,player.x,player.y,msg)
        if chr(ch) == "g":
            msg = level.gate(player,player.x,player.y,msg)
    
    win.erase()
    topbar = " NRG:"+str(player.energy)+" "+level.td+" IRN:"+str(player.iron)+" CL:"+str(player.coal)+" PIX:"+str(player.pix)#+" C:"+level.CHARDICT[level.gmap[player.x][player.y]]
    scr = "SCORE:"+str(player.score)
    win.addstr(0,0,topbar+(" "*(level.width-len(topbar)-len(scr)))+scr,c.A_REVERSE)
    level.curses_draw(win)
    if True:
        win.addstr(player.y+1,player.x,"@",c.A_REVERSE)
    win.addstr(level.height+1,0,"[M]ine [B]uild [P]ath [E]nergizer [D]igger [G]ate"+"  "+msg,c.A_REVERSE)
    win.addstr(0,0,level.CHARDICT[level.gmap[player.x][player.y]],c.A_REVERSE)
    win.move(0,0)
    win.refresh()
    level.update(player)
    offset, offset_count = update_offset(offset,offset_count)
    if (player.energy <= 0):
        exit_program(player)
        
    # Check win
    if level.gmap[player.x][player.y] == level.GO:
        player.level += 1
        if (player.level == 4):
            end_game()
        msg = "Level Complete"
        level = fact.Land(100,25,[],percent*3/4)
