"""
Demo program
a "meter" user defined element. In this demo it will be a Graph Element.
"""

import math
import random
import PySimpleGUI as sg


def mapping(func, sequence, *argc):
    """
    Map function with extra argument, not for tuple.
    : Parameters
      func - function to call.
      sequence - list for iteration.
      argc - more arguments for func.
    : Return
      list of func(element of sequence, *argc)
    """
    if isinstance(sequence, list):
        return list(map(lambda i:func(i, *argc), sequence))
    else:
        return func(sequence, *argc)


def add(number1, number2):
    """
    Add two number
    : Parameter
      number1 - number to add.
      numeer2 - number to add.
    : Return
      Addition result for number1 and number2.
    """
    return number1 + number1


def limit(number):
    """
    Limit angle in range 0 ~ 360
    : Parameter
      number: angle degree.
    : Return
      angel degree in 0 ~ 360, return 0 if number < 0, 360 if number > 360.
    """
    return max(min(360, number), 0)

class Clock():
    """
    Draw background circle or arc.
    All angles defined as clockwise from negative x-axis.
    """
    def __init__(self, center_x=0, center_y=0, radius=100, start_angle=0,
        stop_angle=360, fill_color='white', line_color='black', line_width=2,
        style='arc'):
        """
        : Paramters
          center_x, center_y - coordinate of center in pixels.
          radius - radius of center in pixels.
          start_angle - start angle of arc in degree.
          stop_angle - stop angle of arc in degree.
          fill_color - color to fill in arc/pie/circle.
          line_color - color for outline of arc/pie/cirlce.
          line_width - line width for outline of arc/pie/circle.
          style - valid value 'pieslice', 'chord', 'arc', 'first', 'last',
              'butt', 'projecting', 'round', 'bevel', 'miter'.
        : Return
          Instance of clock.
        """
        instance = mapping(isinstance, [center_x, center_y, radius, start_angle,
            stop_angle, line_width], (int, float)) + mapping(isinstance,
            [fill_color, line_color, style], str)
        if False in instance:
            raise ValueError
        start_angle, stop_angle = limit(start_angle), limit(stop_angle)
        self.all = [
            center_x, center_y, radius, start_angle, stop_angle, fill_color,
            line_color, line_width, style]
        self.figure = []
        self.new()

    def new(self):
        """
        Draw Arc or circle, not called by user.
        """
        x, y, r, start, stop, fill, line, width, style = self.all
        start, stop = (
            (180-start, 180-stop) if stop<start else
            (180-stop, 180-start))
        if start == stop%360:
            self.figure.append(
                draw.draw_cricle(
                    (x, y), r, fill_color=fill, line_color=line,
                    line_width=width))
        else:
            self.figure.append(
                draw.draw_arc(
                    (x-r, y+r), (x+r, y-r), stop-start, start, style=style,
                    arc_color=fill, line_width=width))

    def move(self, delta_x, delta_y):
        """
        Move circle or arc in clock by delta x, delta y.
        : Parameters
          delta_x, delta_y - relative movement on x- and y-direction in pixels.
        : Return
          None.
        """
        if False in mapping(isinstance, [delta_x, delta_y], (int, float)):
            raise ValueError
        self.all[0] +=  delta_x
        self.all[1] +=  delta_y
        for figure in self.figure:
            draw.move_figure(figure, delta_x, delta_y)


class Tick():
    """
    Create tick on clock for minor tick, also for major tick.
    All angles defined as clockwise from negative x-axis.
    """
    def __init__(self, center_x=0, center_y=0, start_radius=90,
        stop_radius=100, start_angle=0, stop_angle=360, step=6,
        line_color='black', line_width=2):
        """
        Create Tick
        : Parameters
          center_x, center_y - center of circle in pixels.
          start_radius, stop_radius - define length of tick by cicle radius
            in pixels.
          start_angle, stop_angle - start and stop angle of arc in degree.
          step - degree per tick.
          line_color - color of tick.
          line_width - line width of tick.
        : Return
          Instance of Tick.
        """
        instance = mapping(isinstance, [center_x, center_y, start_radius,
            stop_radius, start_angle, stop_angle, step, line_width], (
            int, float)) + [mapping(isinstance, line_color, (list, str))]
        if False in instance:
            raise ValueError
        start_angle, stop_angle = limit(start_angle), limit(stop_angle)
        self.all = [
            center_x, center_y, start_radius, stop_radius, start_angle,
            stop_angle, step, line_color, line_width]
        self.figure = []
        self.new()

    def new(self):
        """
        Draw ticks on clock, not called by user.
        """
        (x, y, start_radius, stop_radius, start_angle, stop_angle, step,
            line_color, line_width) = self.all
        start_angle, stop_angle = (180-start_angle, 180-stop_angle
            ) if stop_angle<start_angle else (180-stop_angle, 180-start_angle)
        for i in range(start_angle, stop_angle+1, step):
            start_x = x + start_radius*math.cos(i/180*math.pi)
            start_y = y + start_radius*math.sin(i/180*math.pi)
            stop_x  = x +  stop_radius*math.cos(i/180*math.pi)
            stop_y  = y +  stop_radius*math.sin(i/180*math.pi)
            self.figure.append(draw.draw_line((start_x, start_y),
                (stop_x, stop_y), color=line_color, width=line_width))

    def move(self, delta_x, delta_y):
        """
        Move ticks in clock by delta x, delta y.
        : Parameters
          delta_x, delta_y - relative movement on x- and y-direction in pixels.
        : Return
          None.
        """
        if False in mapping(isinstance, [delta_x, delta_y], (int, float)):
            raise ValueError
        self.all[0] += delta_x
        self.all[1] += delta_y
        for figure in self.figure:
            draw.move_figure(figure, delta_x, delta_y)

class Pointer():
    """
    Draw pointer of clock.
    All angles defined as clockwise from negative x-axis.
    """
    def __init__(self, center_x=0, center_y=0, angle=0, inner_radius=20,
        outer_radius=80, outer_color='white', pointer_color='blue',
        origin_color='black', line_width=2):
        """
        Draw pointer.
        : Parameters
          center_x, center_y - center of circle in pixels.
          angle - default position of pointer in angle.
          inner_radius - define circle radius of fixed position in pixels.
          outer_radiu - defince circle radius of end position in pixels.
          outer_color - outline color of pointer.
          pointer_color - pointer color.
          origin_color - color of fixed point.
          line_width - line width of tick.
        : Return
          Instance of Pointer.
        """
        instance = mapping(isinstance, [center_x, center_y, angle, inner_radius,
            outer_radius, line_width], (int, float)) + mapping(isinstance,
            [outer_color, pointer_color, origin_color], str)
        if False in instance:
            raise ValueError

        self.all = [center_x, center_y, angle, inner_radius, outer_radius,
            outer_color, pointer_color, origin_color, line_width]
        self.figure = []
        self.stop_angle = angle
        self.new(degree=angle)

    def new(self, degree=0):
        """
        Draw new pointer by angle, erase old pointer if exist.
        Degree defined as clockwise from negative x-axis.
        Not called by user.
        """
        (center_x, center_y, angle, inner_radius, outer_radius,
            outer_color, pointer_color, origin_color, line_width) = self.all
        if self.figure != []:
            for figure in self.figure:
                draw.delete_figure(figure)
            self.figure = []
        d = degree - 90
        self.all[2] = degree
        dx1 = int(2*inner_radius*math.sin(d/180*math.pi))
        dy1 = int(2*inner_radius*math.cos(d/180*math.pi))
        dx2 = int(outer_radius*math.sin(d/180*math.pi))
        dy2 = int(outer_radius*math.cos(d/180*math.pi))
        self.figure.append(
            draw.draw_line(
                (center_x-dx1, center_y-dy1), (center_x+dx2, center_y+dy2),
                color=pointer_color, width=line_width))
        self.figure.append(
            draw.draw_circle(
                (center_x, center_y), inner_radius, fill_color=origin_color,
                line_color=outer_color, line_width=line_width))

    def move(self, delta_x, delta_y):
        """
        Move pointer with delta x and delta y.
        : Parameters
          delta_x, delta_y - relative movement on x- and y-direction in pixels.
        : Return
          None.
        """
        if False in mapping(isinstance, [delta_x, delta_y], (int, float)):
            raise ValueError
        self.all[:2] = [self.all[0] + delta_x, self.all[1] + delta_y]
        for figure in self.figure:
            draw.movefigure(figure, delta_x, delta_y)

class Meter():
    """
    Create Meter
    All angles defined as count clockwise from negative x-axis.
    Should create instance of clock, pointer, minor tick and major tick first.
    """
    def __init__(self, center=(0, 0), clock=None, pointer=None, degree=0,
            minor_tick=None, major_tick=None):
        """
        Create Meter.
        : Parameters
          center - center position x, y of meter in pixels.
          clock - instance of Clock.
          pointer - instance of Pointer.
          degree - default angle of pointer in degree.
          minor_tick - instance of Tick, maybe with shorter and thiner line.
          major_tick - instance of Tick, maybe with longer and thicker line.
        : Return
          Instance of Meter.
        """
        self.center_x, self.center_y = self.center = center
        self.degree = degree
        self.clock = clock
        self.minor_tick = minor_tick
        self.major_tick = major_tick
        self.pointer = pointer
        self.dx = self.dy = 1

    def move(self, delta_x, delta_y):
        """
        Move Meter to move all componenets in meter.
        : Parameters
          delta_x, delta_y - relative movement on x- and y-direction in pixels.
        : Return
          None.
        """
        self.center_x, self.center_y =self.center = (
            self.center_x+delta_x, self.center_y+delta_y)
        if self.clock:
            self.clock.move(delta_x, delta_y)
        if self.minor_tick:
            self.minor_tick.move(delta_x, delta_y)
        if self.major_tick:
            self.major_tick.move(delta_x, delta_y)
        if self.pointer:
            self.pointer.move(delta_x, delta_y)

    def change(self, degree=None, step=1):
        """
        Rotation of pointer.
        Call it with degree and step to set initial options for rotation.
        Call it Without any option to start rotation.
        : Parameters
          degree - the absolute angle to stop in angle.
          step - the step of pointer move to stop angle in degree.
        : Return
          None.
        """
        if self.pointer:
            if degree != None:
                self.pointer.stop_degree = degree
                self.pointer.step = (step if self.pointer.all[2] < degree
                    else -step)
                return True
            now = self.pointer.all[2]
            step = self.pointer.step
            new_degree = now + step
            if ((step > 0 and new_degree < self.pointer.stop_degree) or
                    (step < 0 and new_degree > self.pointer.stop_degree)):
                self.pointer.new(degree=new_degree)
                return False
            else:
                self.pointer.new(degree=self.pointer.stop_degree)
                return True


layout = [
    [sg.Button('Quit', size=(6, 1), font=('Courier New', 16), key='Quit',
        enable_events=True)],
    [sg.Graph((643, 483), (-321, -241), (321, 241), key='-Graph-')]]
window = sg.Window('Meter', layout=layout, finalize=True, no_titlebar=True)
draw = window.find_element('-Graph-')

clock = Clock(start_angle=0, stop_angle=180, fill_color='white',
              line_width=5, style='arc')
minor_tick = Tick(start_angle=30, stop_angle=150, line_width=2)
major_tick = Tick(start_angle=30, stop_angle=150, line_width=5,
                  start_radius=80, step=30)
pointer = Pointer(angle=30, inner_radius=10, outer_radius=75,
                  pointer_color='white', line_width=5)
meter = Meter(clock=clock, minor_tick=minor_tick, major_tick=major_tick,
              pointer=pointer)
new_angle = random.randint(0, 180)
meter.change(degree=new_angle)

while True:

    event, values = window.read(timeout=20)

    if event == 'Quit':
        break

    if meter.change():
        new_angle = random.randint(30, 150)
        meter.change(degree=new_angle)

window.close()
