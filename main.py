from tkinter import *

canvas_width = 1280
canvas_height = 720
brush_size = 3
color = 'black'

root = Tk()
root.title("Paint on Python")


brushActive = False
rectangleActive = False
circleActive = False
textActive = False


class Text:
    def __init__(self, canvas):
        self.canvas = canvas

        # text items with the tag "editable" will inherit these bindings
        self.canvas.tag_bind("editable", "<Double-Button-3>", self.set_focus)
        self.canvas.tag_bind("editable", "<Button-1>", self.set_cursor)
        self.canvas.tag_bind("editable", "<Key>", self.do_key)
        self.canvas.tag_bind("editable", "<Home>", self.do_home)
        self.canvas.tag_bind("editable", "<End>", self.do_end)
        self.canvas.tag_bind("editable", "<Left>", self.do_left)
        self.canvas.tag_bind("editable", "<Right>", self.do_right)
        self.canvas.tag_bind("editable", "<BackSpace>", self.do_backspace)
        self.canvas.tag_bind("editable", "<Return>", self.do_return)

    def do_return(self, event):
        """Handle the return key by turning off editing"""

        self.canvas.focus("")
        self.canvas.delete("highlight")
        self.canvas.select_clear()

    def do_left(self, event):
        """Move text cursor one character to the left"""

        item = self.canvas.focus()
        if item:
            new_index = self.canvas.index(item, "insert") - 1
            self.canvas.icursor(item, new_index)
            self.canvas.select_clear()

    def do_right(self, event):
        """Move text cursor one character to the right"""

        item = self.canvas.focus()
        if item:
            new_index = self.canvas.index(item, "insert") + 1
            self.canvas.icursor(item, new_index)
            self.canvas.select_clear()

    def do_backspace(self, event):
        """Handle the backspace keye"""

        item = self.canvas.focus()
        if item:
            selection = self.canvas.select_item()
            if selection:
                self.canvas.dchars(item, "sel.first", "sel.last")
                self.canvas.select_clear()
            else:
                insert = self.canvas.index(item, "insert")
                if insert > 0:
                    self.canvas.dchars(item, insert - 1, insert)
            self.highlight(item)

    def do_home(self, event):
        """Move text cursor to the start of the text item"""

        item = self.canvas.focus()
        if item:
            self.canvas.icursor(item, 0)
            self.canvas.select_clear()

    def do_end(self, event):
        """Move text cursor to the end of the text item"""

        item = self.canvas.focus()
        if item:
            self.canvas.icursor(item, "end")
            self.canvas.select_clear()

    def do_key(self, event):
        """Handle the insertion of characters"""

        item = self.canvas.focus()
        if item and event.char >= " ":
            selection = self.canvas.select_item()
            if selection:
                self.canvas.dchars(item, "sel.first", "sel.last")
                self.canvas.select_clear()
            self.canvas.insert(item, "insert", event.char)
            self.highlight(item)

    def highlight(self, item):
        """Highlight the given text item to show that it's editable"""

        items = self.canvas.find_withtag("highlight")
        if len(items) == 0:
            # no highlight box; create it
            uid = self.canvas.create_rectangle((0, 0, 0, 0), fill="white", outline="blue", dash=".", tag="highlight")
            self.canvas.lower(uid, item)
        else:
            uid = items[0]

        # resize the highlight
        bbox = self.canvas.bbox(item)
        rect_bbox = (bbox[0] - 4, bbox[1] - 4, bbox[2] + 4, bbox[3] + 4)
        self.canvas.coords(uid, rect_bbox)

    def set_focus(self, event):
        """Give focus to the text element under the cursor"""

        if self.canvas.type("current") == "text":
            self.canvas.focus_set()
            self.canvas.focus("current")
            self.canvas.select_from("current", 0)
            self.canvas.select_to("current", "end")
            self.highlight("current")

    def set_cursor(self, event):
        """Move the insertion point"""

        item = self.canvas.focus()
        if item:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            self.canvas.icursor(item, "@%d,%d" % (x, y))
            self.canvas.select_clear()

    def create_text(self, cord_x, cord_y, text):
        self.canvas.create_text(cord_x, cord_y, anchor="nw", tags=("editable",), text=text)


def paint(event):
    global brush_size
    global color
    x1 = event.x - brush_size
    x2 = event.x + brush_size
    y1 = event.y - brush_size
    y2 = event.y + brush_size
    w.create_oval(x1, y2, x2, y1, fill=color, outline=color)


def brush_size_change(new_size):
    global brush_size
    brush_size = new_size


def color_change(new_color):
    global color
    change_active("brush")
    color = new_color


def change_active(paint_type):
    global brushActive
    global rectangleActive
    global circleActive
    global textActive
    if paint_type == "brush":
        rectangleActive = False
        circleActive = False
        textActive = False
        brushActive = True
    elif paint_type == "rectangle":
        brushActive = False
        circleActive = False
        textActive = False
        rectangleActive = True
    elif paint_type == "circle":
        brushActive = False
        rectangleActive = False
        textActive = False
        circleActive = True
    elif paint_type == "text":
        brushActive = False
        rectangleActive = False
        circleActive = False
        textActive = True
    else:
        print("Choose tool first.")


w = Canvas(root,
           width=canvas_width,
           height=canvas_height,
           bg='white')


def rectangle(x, y):
    global sx1
    global sy1
    global brush_size
    global color
    w.create_rectangle(sx1, sy1, x, y, outline=color, width=brush_size)


def circle(x, y):
    global cx1
    global cy1
    global color
    global brush_size
    w.create_oval(cx1, cy1, x, y, outline=color, width=brush_size)


def print_sample_text(x, y):
    Text(w).create_text(x, y, "You can edit me :)")


def onclick(event):
    global rectangleActive
    global circleActive
    global textActive
    if rectangleActive:
        global sx1
        global sy1
        sx1 = event.x
        sy1 = event.y
    elif circleActive:
        global cx1
        global cy1
        cx1 = event.x
        cy1 = event.y
    elif textActive:
        print_sample_text(event.x, event.y)


def onrelease(event):
    global rectangleActive
    global circleActive
    x = event.x
    y = event.y
    if rectangleActive:
        rectangle(x, y)
    elif circleActive:
        circle(x, y)


def onmotion(event):
    global brushActive
    if brushActive:
        paint(event)


w.bind('<Button-1>', onclick)
w.bind('<ButtonRelease-1>', onrelease)
w.bind('<B1-Motion>', onmotion)

red_btn = Button(text="Red", width=10, command=lambda: color_change('red'))
black_btn = Button(text="Black", width=10, command=lambda: color_change('black'))
yellow_btn = Button(text="Yellow", width=10, command=lambda: color_change('yellow'))
blue_btn = Button(text="Blue", width=10, command=lambda: color_change('blue'))
green_btn = Button(text="Green", width=10, command=lambda: color_change('green'))
delete_btn = Button(text="Delete All", width=10, command=lambda: w.delete('all'))
eraser_btn = Button(text="Eraser", width=10, command=lambda: color_change('white'))

paint_btn = Button(text="Brush", width=10, command=lambda: change_active("brush"))
rectangle_btn = Button(text="Rectangle", width=10, command=lambda: change_active("rectangle"))
circle_btn = Button(text="Oval", width=10, command=lambda: change_active("circle"))
text_btn = Button(text="Text", width=10, command=lambda: change_active("text"))


tree_btn = Button(text='3', width=10, command=lambda: brush_size_change(3))
five_btn = Button(text='5', width=10, command=lambda: brush_size_change(5))
seven_btn = Button(text='7', width=10, command=lambda: brush_size_change(7))
twelve_btn = Button(text='12', width=10, command=lambda: brush_size_change(12))
fifteen_btn = Button(text='15', width=10, command=lambda: brush_size_change(15))


w.grid(row=2, column=2,
       columnspan=7, padx=5, pady=5, sticky=E+W+S+N)

red_btn.grid(row=0, column=1)
black_btn.grid(row=0, column=2)
yellow_btn.grid(row=0, column=3)
blue_btn.grid(row=0, column=4)
green_btn.grid(row=0, column=5)
eraser_btn.grid(row=0, column=6)

tree_btn.grid(row=1, column=1)
five_btn.grid(row=1, column=2)
seven_btn.grid(row=1, column=3)
twelve_btn.grid(row=1, column=4)
fifteen_btn.grid(row=1, column=5)
delete_btn.grid(row=1, column=6)
paint_btn.grid(row=0, column=7)
rectangle_btn.grid(row=1, column=7)
circle_btn.grid(row=1, column=8)
text_btn.grid(row=0, column=8)

root.mainloop()
