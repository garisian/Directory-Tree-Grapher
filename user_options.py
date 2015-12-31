from Tkinter import *
import tkMessageBox

class UserPrompt(Tk):

    def __init__(self):
        ''''''
        Tk.__init__(self)
        self.width = 0
        self.height = 0
        self.has_legend = False
        self.can_zoom = False
        self.start()

    def get_val(self, ent1, ent2):
        '''(Entry) ->'''
        try:
            self.width = int(ent1.get())
            self.height = int(ent2.get())
            self.withdraw()
            self.req_legend()
            self.req_zoom()
            self.quit()
        except:
            cont_quit = tkMessageBox.showerror("Size error", \
            "You entered an invalid size. Press OK to enter a " + \
            "valid size. Press Esc to quit.")
            self.start()

    def start(self):
        width_request = Label(self, \
                                text="Enter the width of screen: (has to be greater than 600) ").grid(row=0)
        height_request = Label(self, \
                                text="Enter the height of screen: (has to be greater than 600) ").grid(row=1)
        w = Entry(self)
        h = Entry(self)
        w.grid(row=0, column=1)
        h.grid(row=1, column=1)
        close = Button(self, text="OK", command = lambda : self.get_val(w, h))
        close.grid(row=2, column=1)

    def req_legend(self):
        self.has_legend = tkMessageBox.askyesno("Legend", \
                             "Would you like to display a legend " + \
                             "beside the treemap? ")

    def req_zoom(self):
        self.can_zoom = tkMessageBox.askyesno("Zoom-in Function", \
                             "Would you like to be able to zoom " + \
                             "in on the treemap? ")


class Rename(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.new_name = ''
        self.req_name()

    def req_name(self):

        new_name_request = Label(self, \
                    text="Enter the new complete path name for this file: ").\
                                                                    grid(row=0)
        new_name = Entry(self)
        new_name.grid(row=0, column=1)
        close = Button(self, text="OK", command = lambda : \
                                                 self.get_val(new_name))
        close.grid(row=1, column=1)

    def get_val(self, entry):

        self.new_name = entry.get()
        self.withdraw()
        self.quit()

