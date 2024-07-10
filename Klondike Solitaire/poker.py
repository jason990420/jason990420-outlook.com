import PySimpleGUI as sg
import random
from time import sleep
import ctypes

cards       = 52                # Total 52 cards
rows        = 2                 # Two rows
columns     = 7                 # 7 colums
cells       = rows * columns    # Cells - total positions for cards
all         = cells + cards     # Total cards and blan cards
card_width  = 153               # Width of card in pixels
card_height = 200               # height of card in pixels
pad_x       = 36                # Gap between cells on horizontal
pad_y       = 36                # Gap between celss on vertical
card_pad    = 25                # The distance between cards in stack
font        = 'simsun 16 bold'  # font used in buttons
path        = 'PNG 153x200\\'   # Sub-directory for card PNG files
width       = (card_width + pad_x) * columns + pad_x            # Graphic width
height      = (card_height + pad_y) * rows + pad_y + 9*card_pad # Graphic Height
# Coordinates for each cell
ref_x       = [(pad_x + card_width) * int(i%7) + pad_x for i in range(cells)]
ref_y       = [height - card_height * int(i/7) - pad_y * int(i/7 + 1)
                for i in range(cells)]
# Rack position for each cards
stack       = [i for i in range(cells)] + [0 for i in range(24)]+[
               6+i for i in range(8) for j in range(i)]
show_card   = [38, 40, 43, 47, 52, 58, 65]  # Cards shown when beginning
start_x     = int((width-card_width)/2)     # Position for flash card show
start_y     = card_height+pad_y
# Image filenames of cards with top-side and bottom-side
file        = [['']+[path+'0.png' for i in range(52)],
               [path+'n.png']+[path+str(i+1)+'.png' for i in range(52)]]
# Area of rack in cells, 0 ~ 13 for all cells
top         = [3, 4, 5, 6]
bottom      = [7, 8, 9, 10, 11, 12, 13]

button_down = False     # Flag for mouse left button down
drag        = False     # Flag for mouse in drag mode
start       = True      # Flag for initial position of mouse
New_Start   = True      # Flag for new game

ctypes.windll.user32.SetProcessDPIAware()   # Set unit of GUI to pixels

class poker():
    '''
    Definition of eack poker card:
        Parameter:
            card    - Sequence number of cards, 0 ~ 65.
            kind    - Kind of cards, 'Blank Card' or 'Card'
        Attributes:
            card    - Sequence number of cards, 0 ~ 65
            ids     - Id of graphic element
            up      - Card value of upper card, None for no upper card
            down    - Card value of lower card, None for no lower card
            x,y     - Variable coordinate of card used when drag mode
            x0, y0  - Coordinate of card whne in cell/rack
            kind    - Suit of cards, spades♠/hearts♥/clubs♣/diamonds♦ (1~4)
            no      - Number of card (1~13)
            rack    - Which card located (0~13, not in 2)
            fix     - Blank card if defined as fixed position
            side    - State of cards, back side of front side (0/1)
    '''
    def __init__(self, card=None, kind='Card'):

        # Initialize values for each card

        self.card       = card
        self.ids        = None

        if kind=='Blank Card':

            self.x0     = self.x = ref_x[card]
            self.y0     = self.y = ref_y[card]
            self.up     = None
            self.down   = None
            self.kind   = 0
            self.no     = 0
            self.rack   = card
            self.fix    = True
            self.side   = 0 if card==2 else 1

        else:
            self.up     = None
            self.kind   = int(card_list[card-cells]/13)+1
            self.no     = card_list[card-cells] % 13 + 1
            self.side   = 0
            self.fix    = False
            self.rack   = stack[card]
            self.new_card(self.rack)

    def cards(self):
        # Return numbers of cards in rack of caller
        return p[self.rack].up_cards()

    def click_rack0(self):
        # Event handler for click on Rack 0 (foundation)
        if self.fix and (p[1].cards()>0):
            while True:
                pp = p[p[1].find_top()]
                if not pp.move_rack(0): return
        # 0 card/Rack 0
        elif not self.fix:
            # If three cards in Rack 0
            if p[1].cards()==3: p[1].move_rack_bottom()
            self.move_rack(1)

    def click_rack1(self):
        # Click on Rack 1 to move card to Rack 3 ~ 6 (top)
        if self.fix or (self.up_cards()>1):
            return
        else:
            self.move_to_any_rack2()

    def click_rack3(self):
        # Click on Rack 7 ~ 13 (Bottom) to move card to Rack 3 ~ 6 (top)
        # If No card or number of cards moret than 1
        if self.fix or (not self.side) or (self.up_cards()>1):
            return
        else:
            self.move_to_any_rack2()

    def find_top(self):
        # Find top card in caller's Rack
        card = self.rack
        while True:
            if p[card].up == None:
                return card
            card = p[card].up

    def flash(self):
        # Show cards from bottom-center to cells when game start
        for i in range(all):
            index = (p[i].kind-1)*13+p[i].no if p[i].kind!=0 else 0
            filename = file[p[i].side][index]
            # Load image file and show on bottom-center
            if filename != '':
                p[i].ids = draw.DrawImage(
                    filename=filename, location=(start_x, start_y))
                # Calculation step and steps to move image
                x, y, x0, y0 = p[i].x0, p[i].y0, start_x, start_y
                dx, dy, step = start_x-x, start_y-y, 5
                if abs(dx) > abs(dy):
                    step_x = step if dx<0 else -step
                    count  = int(abs(dx)/abs(step_x))
                    step_y = -dy/count
                else:
                    step_y = step
                    count  = int(abs(dy)/step_y)
                    step_x = -dx/count
                num = 0
                # Loop to show trace of card
                while True:
                    num += 1
                    x0 += step_x
                    y0 += step_y
                    draw.RelocateFigure(p[i].ids, x0, y0)
                    draw.TKCanvas.update_idletasks()
                    if num == count:
                        break
                # Move image to final position on cells
                draw.RelocateFigure(p[i].ids, x, y)
                draw.TKCanvas.update_idletasks()

    def move_back(self):
        # Move card back to original position after drag
        pp = self
        while True:
            pp.x, pp.y = pp.x0, pp.y0
            draw.RelocateFigure(pp.ids, pp.x, pp.y)
            if pp.up==None:
                break
            pp = p[pp.up]
        draw.TKCanvas.update_idletasks()

    def move_from_rack1_to_rack2(self, rack):
        # Drag card from Rack 1 to Top (Rack 3 ~ 6)
        # If no card or not only one card
        if (self.up_cards()!=1) or self.fix or (not self.side):
            return
        pp = p[p[rack].find_top()]
        # Move card with no 1 to Top when no card in Top
        if pp.fix and (self.no==1):
            self.move_rack(rack)
        # Move card with same suit and one higher no. to Top
        elif not pp.fix:
            if (self.kind == pp.kind) and (self.no==pp.no+1):
                self.move_rack(rack)

    def move_from_rack1_to_rack3(self, rack):
        # Drag card from Rack 1 to Bottom (Rack 7 ~ 13)
        # If not only one card
        if (self.up_cards()!=1) or self.fix or (not self.side):
            return
        pp = p[p[rack].find_top()]
        # Move card 'King' on Rack 1 to blank rank in Bottom
        if pp.fix and (self.no==13):
            self.move_rack(rack)
        # Move card from Rack 1 to Bottom if different suit and less one
        elif ((not pp.fix) and
            (self.kind%2 != pp.kind%2) and (self.no==pp.no-1)):
            self.move_rack(rack)
        else:
            self.move_back()

    def move_from_rack2_to_rack3(self, rack):
        # Move card from Top to Bottom
        # If blank card
        if (self.up_cards()!=1) or self.fix or (not self.side):
            return
        pp = p[p[rack].find_top()]
        # If 'King' card to blank rack
        if pp.fix and (self.no==13):
            self.move_rack(rack)
        # if card with different suit and less one
        elif ((not pp.fix) and
            (self.kind%2 != pp.kind%2) and (self.no==pp.no-1)):
            self.move_rack(rack)
        else:
            self.move_back()

    def move_from_rack3_to_rack2(self, rack):
        # Move card from Bottom to Top
        # If no card
        if self.fix or (not self.side):
            return
        pp = p[p[rack].find_top()]
        # If card 'Ace' moved to blank rack on Top
        if (pp.fix and (self.up_cards()==1) and (self.no==1)):
            self.move_rack(rack)
        # If one front-side card moved to non-blank rack on TOP
        elif ((not pp.fix) and (self.up_cards()==1) and
            (self.kind==p[card2].kind) and (self.no==p[card2].no+1)):
            self.move_rack(rack)
            # If lower card not shown, then turn over
        else:
            self.move_back()

    def move_from_rack3_to_rack3(self, rack):
        # Move cards from Bottom to Bottom
        # If no card
        if self.fix or (not self.side):
            return
        # If bottom card is 'King' and moved to blank rank
        pp = p[p[rack].find_top()]
        if (pp.fix and (self.no==13)):
            self.move_rack(rack)
        # If cards with differet suit and <1, moved to non-blank rack on Bottom
        elif ((not pp.fix) and (self.kind%2!=pp.kind%2) and (self.no==pp.no-1)):
            self.move_rack(rack)
        else:
            self.move_back()

    def move_offset(self, dx, dy):
        # move Image with offset
        if self.fix or (not self.side):
            return
        pp = self
        while True:                                 # Bring cards to front
            draw.BringFigureToFront(pp.ids)
            if pp.up == None: break
            pp = p[pp.up]
        pp = self
        while True:                                 # Move cards
            pp.x, pp.y = pp.x + dx, pp.y + dy
            draw.RelocateFigure(pp.ids, pp.x, pp.y)
            if pp.up == None: break
            pp = p[pp.up]
        draw.TKCanvas.update_idletasks()

    def move_rack(self, rack):
        # move top cards of caller to up side of card2
        if self.fix: return False
        if rack in [0,1]: self.turn_over()
        card_d = self.down                  # keep down card and cut the link
        p[card_d].up = None

        card_now = self.card                # start from caller card
        if card_now == None: return False
        ok = False
        while True:
            if card_now == None: break      # Not card left for moving
            pp = p[card_now]
            top_card = p[rack].find_top()

            pp.rack = rack                  # Update new info for card
            pp.x0, pp.y0 = pp.x, pp.y = p[top_card].offset(rack)

            p[top_card].up = card_now       # build link
            pp.down = top_card
            pp.update(same=True, front=True)

            card_now = pp.up                # next card
            pp.up = None
            ok = True

        if (ok and (p[card_d].rack in bottom) and (not p[card_d].fix) and
            (not p[card_d].side)):
            p[card_d].turn_over()           # down card to turn over

        return True

    def move_rack_bottom(self):
        # Move lowest card of Rack 1 to Bottom of Rack 0 which with 3 cards
        card1 = p[1].up                     # Remove card1 from Rack 0
        if card1 == None: return
        p[card1].turn_over()
        p[1].up = p[card1].up
        if p[1].up!= None: p[p[1].up].down = 1

        card0 = p[0].up                     # Insert card1 to Rack bottom
        p[0].up = card1
        p[card1].up = card0
        p[card1].down = 0
        p[card0].down = card1

        p[card1].x0 = p[card1].x = p[0].x0  # new position, rack on Rack 0
        p[card1].y0 = p[card1].y = p[0].y0
        p[card1].rack = 0
        p[card1].update()
        draw.SendFigureToBack(p[card1].ids)
        draw.SendFigureToBack(p[0].ids)

        card = p[1].up                      # new position for cards on Rack 1
        p[card].x0 = p[card].x = p[1].x0
        card_up = p[card].up
        p[card_up].x0 = p[card_up].x = p[1].x0 + card_pad
        p[card].update()
        p[card_up].update()

    def move_to_any_rack2(self):
        # Move one card to rack on Top
        for rack in top:
            top_card = p[rack].find_top()
            pp = p[top_card]
            if pp.fix and (self.no==1):     # If 'ACE' card to blank rack
                self.move_rack(rack)
                return True
            elif ((self.kind==pp.kind) and (self.no==pp.no+1)):
                self.move_rack(rack)        # If card with same suit and >1
                return True
        return False

    def new_card(self, card):
        # Initialize a new card for (x, y), (x0, y0) and up
        dy = 0 if card ==0 else card_pad
        count = p[card].cards()
        self.x = self.x0 = p[card].x0
        self.y = self.y0 = p[card].y0 - dy*count
        card = p[card].find_top()
        p[card].up = self.card
        self.down = card

    def offset(self, rack):
        # Calculation coordinate for offset on different rack
        # Rack 1: (card_pad, 0), Bottom: (0, card_pad)
        # If blank rack, (0, 0)
        dx = dy = 0
        if rack == 1:
            dx, dy  = card_pad, 0
        elif rack in bottom:
            dx, dy  = 0, card_pad
        pp = p[p[rack].find_top()]
        if pp.fix:
            dx = dy = 0
        return pp.x0 + dx, pp.y0 - dy

    def turn_over(self):
        # Turn over card and update image
        self.side = 1 - self.side
        self.update(same=False)

    def up_cards(self):
        # count cards up and include caller card
        count = 0 if self.fix else 1
        card = self.up
        while True:
            if card == None:
                return count
            count += 1
            card = p[card].up

    def update(self, same=True, front=False):
        # Update image position, or image if not same
        if front:
            draw.BringFigureToFront(self.ids)
        if same:
            draw.RelocateFigure(self.ids, self.x, self.y)
            draw.TKCanvas.update_idletasks()
        else:
            index = (self.kind-1)*13+self.no if self.kind!=0 else 0
            f = file[self.side][index]
            draw.DeleteFigure(self.ids)
            self.ids = draw.DrawImage(filename=f, location=(self.x, self.y))

def id_to_card(ids):
    # find card for image id
    for card in range(all):
        if p[card].ids == ids:
            return card
    return None

def get_card(x, y, down=True):
    # get card by position (x,y), button down for 1st one, button up for 2nd one
    x, y = draw._convert_canvas_xy_to_xy(x, y)
    ids = draw.TKCanvas.find_overlapping(x,y,x,y)
    if down+len(ids)<2: return None
    return id_to_card(ids[down-2])

def condition():
    # Check all the conditions of cards selected when button down and up
    result = set()
    if drag:                                    result.add('D'  )
    if card1!=None:                             result.add('C1' )
    if card2!=None:                             result.add('C2' )
    if card1!=None and p[card1].rack==0:        result.add('R10')
    if card1!=None and p[card1].rack==1:        result.add('R11')
    if card1!=None and p[card1].rack in top:    result.add('R12')
    if card1!=None and p[card1].rack in bottom: result.add('R13')
    if card2!=None and p[card2].rack==0:        result.add('R20')
    if card2!=None and p[card2].rack==1:        result.add('R21')
    if card2!=None and p[card2].rack in top:    result.add('R22')
    if card2!=None and p[card2].rack in bottom: result.add('R23')
    if card1!=None and p[card1].fix==False:     result.add('F1' )
    if card2!=None and p[card2].fix==False:     result.add('F2' )
    if card1!=None and p[card1].side==1:        result.add('S1' )
    if card2!=None and p[card2].side==1:        result.add('S2' )
    return result

# Three buttons on top side - 'New Game', 'Game Over' and 'Flush All'
# One Graphic area on bottom side
layout= [[sg.Button('New Game',  pad=(pad_x, (pad_y,0)), font=font),
          sg.Button('Game Over', pad=(pad_x, (pad_y,0)), font=font),
          sg.Button('Flush All', pad=(pad_x, (pad_y,0)), font=font)],
         [sg.Graph(background_color='green', canvas_size=(width, height),
          graph_bottom_left=(0,0), key='Graph', pad=(0,0), enable_events=True,
          graph_top_right=(width, height), drag_submits=True)]]

# Create window
window  = sg.Window('Klondike Solitaire', layout=layout,
                    background_color='green', finalize=True).Finalize()
# Easy name for graphic element
draw    = window['Graph']

# Loop Start for event detect
while True:

    # Initial poker cards, flash only when game start
    if New_Start:
        card_list = random.sample(range(cards), cards)
        p = [0 for i in range(all)]
        for i in range(cells+cards):    # Initial cards
            kind = 'Blank Card' if i < cells else 'Card'
            p[i] = poker(card=i, kind=kind)
        p[0].flash()                    # Flash cards
        for card in show_card: p[card].turn_over()
        New_Start = False

    event, values = window.read(timeout=100)    # read window event

    if event==None or event=='Game Over':   # Window close of Game over clicked
        break

    # No event
    elif event == sg.TIMEOUT_KEY:
        continue

    elif event == 'New Game':           # New Game button event
        for i in range(all):
            if p[i].ids != None: draw.DeleteFigure(p[i].ids)
        New_Start = True

    elif event == 'Flush All':          # Auto move cards to top
        while True:
            result = False
            for i in [1]+bottom:        # Check all cards
                card = p[i].find_top()
                if p[card].fix: continue
                ok = p[card].move_to_any_rack2()
                result = result or ok
            if not result: break

    if event == 'Graph':                # Button down event

        x1, y1 = values['Graph']
        if not start:                   # Keep position
            x0, y0 = old_position
            dx, dy = x1-x0, y1-y0
            old_position = (x1, y1)

        if button_down:                 # Check first mouse button down
            if (x1,y1)!=(x0,y0):
                drag = True
                if (card1 != None) and (p1.side==1):    # Check if movable
                    if (((p1.rack in [1]+top) and p1.up_cards()==1) or
                        (p1.rack in bottom)):
                        p1.move_offset(dx, dy)
        else:
            if start:                   # save initial position
                old_position = values['Graph']
                start = False
            button_down = True          # 1st mouse down event
            card1 = get_card(x1, y1)    # Mouse down generate two time events
            if card1 != None:
                p1 = p[card1]

    elif event == 'Graph+UP':           # Button down event

        x2, y2 = values['Graph']
        card2   = get_card(x2, y2, down=False)
        if card2!= None:
            p2=p[card2]
            rack2=p2.rack
        result = condition()
        '''
        Check condition for what to do
        D for Drag, C for card, S for card shown, F for card not fixed
        R1m for button down/area m, R2n for button up/area
        '''
        if   {'D','C1','R10','S1','F1'}.issubset(result) and 'C2' not in result:
            p1.move_back()
        elif {'D','C1','R11','S1','F1','C2','R22'}.issubset(result):
            p1.move_from_rack1_to_rack2(rack2)
        elif {'D','C1','R11','S1','F1','C2','R23'}.issubset(result):
            p1.move_from_rack1_to_rack3(rack2)
        elif {'D','C1','R12','S1','F1','C2','R23'}.issubset(result):
            p1.move_from_rack2_to_rack3(rack2)
        elif {'D','C1','R13','S1','F1','C2','R22'}.issubset(result):
            p1.move_from_rack3_to_rack2(rack2)
        elif {'D','C1','R13','S1','F1','C2','R23'}.issubset(result):
            p1.move_from_rack3_to_rack3(rack2)
        elif {'D','C1','S1','F1'}.issubset(result) and (
             ('R11' in result) or ('R12' in result) or ('R13' in result)):
            p1.move_back()
        elif {'C1','R10'}.issubset(result):
            p1.click_rack0()
        elif {'C1','R11'}.issubset(result):
            p1.click_rack1()
        elif {'C1','R13'}.issubset(result):
            p1.click_rack3()

        button_down = False
        drag = False
        start = True

window.close()