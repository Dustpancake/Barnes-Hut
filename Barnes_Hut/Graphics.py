from gui.DisplayArea import Universe
from Tkinter import Frame
from Logic import LogicHandler
from Support import Config

class Graphics(Frame):
    """
    Inherits from Tkinter.Frame
    Graphics Class - Handles all display and graphics classes for the simulation
    """
    def __init__(self, master=None):
        """
        Constructor:
        Creates a display area class instance of Universe
        Starts a logic process

        :param master:
        Parent Frame
        """
        Frame.__init__(self, master)
        self.grid()
        self.uni = Universe(self)
        self.uni.grid()
        self.start_logic()
        self.get_key_values()
        self.update_frame()

    def start_logic(self):
        """
        Creates instance of LogicHandler process
        Gets instance data queues
            -star queue
            -tree queue
        Stars LogicHandler instance process
        """
        self.logic = LogicHandler()
        self.star_queue = self.logic.get_queue('star')
        self.tree_queue = self.logic.get_queue('tree')
        self.logic.start()

    def get_key_values(self):
        """
        Get Key Values from config file
        Creates instance of Config class from Support
        """
        cp = Config()
        self.show_tree = int(cp.get("DisplayConfig", "show tree"))
        self.show_stars = int(cp.get("DisplayConfig", "show stars"))
        self.show_com = int(cp.get("DisplayConfig", "show centre of mass"))
        self.save_frames = int(cp.get("DisplayConfig", "save frames"))

    def add_stars(self):
        """
        Adds stars to the Universe instance display
        Gets Star type from the star queue
            first value from queue is star stream size i.e. how many objects are in the queue currently
        Calls Universe.add_star with Star type argument
        """
        make = self.uni.add_star
        queue = self.star_queue
        get = lambda q=queue: self.get_value(q)
        imax = get()
        assert type(imax) == int
        for i in xrange(imax):
            star = get()
            make(star)

    def add_tree(self):
        """
        Adds tree to the Universe instance display
        Gets Node type from the tree queue
        Calls Universe.add_box with Node type argument
        """
        make = self.uni.add_box
        queue = self.tree_queue
        get = lambda q=queue: self.get_value(q)
        imax = get()
        assert type(imax) == int
        for i in xrange(imax):
            node = get()
            make(node)

    def get_value(self, queue):
        """
        Get next item from queue

        :param queue:
        Queue instance from where to get item

        :return:
        Next item from queue
        """
        while True:
            try:
                value = queue.get(block=False)
            except:
                pass
            else:
                return value


    def update_frame(self):
        """
        Update Universe instance frame

        Deletes all current widgets in the canvas
        Adds stars if show_stars == 1
        Adds trees if show_tree == 1
        Calls Universe.save_image if save_frames == 1
        """
        self.uni.canv.delete("all")
        if self.show_stars == 1: self.add_stars()
        if self.show_tree == 1: self.add_tree()
        if self.save_frames == 1: self.uni.save_image()
        self.after(10, self.update_frame)

    def close(self):
        """
        Shutdown function
        Terminates Logic Thread
        """
        while True:
            try:
                self.logic.close()
            except: raise
            else:
                self.logic.terminate()

