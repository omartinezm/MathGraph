import pyglet
from pyglet import clock
from pyglet.gl import *
from win32api import GetSystemMetrics

ZOOM_IN_FACTOR = 1.2
ZOOM_OUT_FACTOR = 1/ZOOM_IN_FACTOR

class DrawGraph(pyglet.window.Window):
    
    def __init__(self, neuralNet, width=0, height=0, x_sep=80, y_sep= 80, *args, **kwargs):
        self.nn=neuralNet
        self.separation_x=x_sep
        self.separation_y=y_sep
        conf=Config(samples=4,depth_size=16)
        super().__init__(min([self.separation_x*(nn.nlayers),GetSystemMetrics(0)]),
                         min([self.separation_y*(max(nn.npl)+1),GetSystemMetrics(1)]),
                         config=conf,caption='Graph',resizable=False,
                         style=pyglet.window.Window.WINDOW_STYLE_DIALOG,
                         *args, **kwargs)
        self.set_location(30,30)
        self.main_batch = pyglet.graphics.Batch()

        self.left=0
        self.right=self.width
        self.bottom=0
        self.top=self.height
        self.zoom_level=2
        self.zoomed_width=self.width
        self.zoomed_height=self.height
        self.batch=pyglet.shapes.Batch()
        
        self.background_lines=pyglet.graphics.OrderedGroup(0)
        self.background=pyglet.graphics.OrderedGroup(1)
        self.foreground=pyglet.graphics.OrderedGroup(2)

        self.vertex=[]
        self.circles=[]
        self.lines=[]
    def init_gl(self, width, height):
        glClearColor(0,0,0,255)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, width, height)
        
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # Move camera
        self.left-=dx*self.zoom_level
        self.right-=dx*self.zoom_level
        self.bottom-=dy*self.zoom_level
        self.top-=dy*self.zoom_level

    def on_mouse_scroll(self, x, y, dx, dy):
        f=ZOOM_IN_FACTOR if dy>0 else ZOOM_OUT_FACTOR if dy<0 else 1
        if 0.2<self.zoom_level*f< 5:
            self.zoom_level*=f

            mouse_x=x/self.width
            mouse_y=y/self.height

            mouse_x_in_world=self.left+mouse_x*self.zoomed_width
            mouse_y_in_world=self.bottom+mouse_y*self.zoomed_height

            self.zoomed_width*=f
            self.zoomed_height*=f

            self.left=mouse_x_in_world-mouse_x*self.zoomed_width
            self.right=mouse_x_in_world+(1-mouse_x)*self.zoomed_width
            self.bottom=mouse_y_in_world-mouse_y*self.zoomed_height
            self.top=mouse_y_in_world+(1-mouse_y)*self.zoomed_height

    def __create_batch__(self):
        acum_l=0
        acum_x=0
        x_pos=self.separation_x/2
        y_pos=self.separation_y
        total_n=sum(self.nn.npl)
        c=(0, 0, int(255*(1-acum_l/total_n)),255)
        for l in tqdm(self.nn.npl,desc="Drawing graph"):
            if acum_l!=0: c=(int(255*((acum_x)/self.nn.nlayers)), 0, int(255*(1-(acum_x)/self.nn.nlayers)), 255)
            for n in range(l):
                self.vertex.append(pyglet.text.Label(self.nn.get_vertexes()[acum_l+n].get_name(),
                                                font_name='Arial',font_size=12,bold=True,
                                                x=x_pos+(acum_x)*self.separation_x, y=y_pos+(n)*self.separation_y,
                                                anchor_x='center', anchor_y='center',color=c,
                                                batch=self.batch,group=self.foreground))
                self.circles.append(pyglet.shapes.Circle(x=self.vertex[-1].x,
                                                         y=self.vertex[-1].y,
                                                         radius=25,color=(255, 255, 255),
                                                         batch=self.batch,group=self.background))
                if acum_x!=0:
                    for j in range(self.nn.npl[acum_x-1]):
                        self.lines.append(shapes.Line(self.vertex[acum_l-self.nn.npl[acum_x-1]+j].x,
                                                      self.vertex[acum_l-self.nn.npl[acum_x-1]+j].y,
                                                      self.vertex[-1].x,self.vertex[-1].y,
                                             width=5, color=c[:-1], batch=self.batch,group=self.background_lines))
            acum_l+=l
            acum_x+=1
            
    def on_draw(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glClear(GL_COLOR_BUFFER_BIT)
        glOrtho(self.left, self.right, self.bottom, self.top, 1, -1)
        self.__create_batch__()
        self.batch.draw()
        glPopMatrix()
        
    def run(self):
        pyglet.app.run()