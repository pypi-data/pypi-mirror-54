import os
import tkinter as tk
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk
from scp import SCPClient


class CanvasFrame(tk.Frame):

    def __init__(self, parent, ssh_client, main):
        super().__init__(parent)
        self.parent = parent
        self.ssh = ssh_client
        self.main = main

        self.configure({
            'width': 600,
            'height': 650,
            'bg': 'gray'
        })

        self.canvas = tk.Canvas(self)
        self.canvas.configure({
            'width': 600,
            'bg': 'white'
        })
        self.canvas.grid(row=0, column=0, columnspan=3, sticky=tk.W)

        self.pc_image = ImageTk.PhotoImage(Image.open(fp=os.path.join('data', 'pc-3.png')))
        self.enve_image = ImageTk.PhotoImage(Image.open(fp=os.path.join('data', 'enve.png')))

        self.canvas.create_image((50, 50), image=self.pc_image)
        self.canvas.create_image((550, 50), image=self.pc_image)

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=1, column=5, rowspan=1, sticky=tk.N + tk.S)

        self.console_output = tk.Text(self)
        self.console_output.configure({
            'width': 85,
            'bg': 'white',
            'yscrollcommand': self.scrollbar.set
        })
        self.console_output.grid(row=1, column=0, columnspan=3, sticky=tk.W)

        self.console_input = tk.Entry(self)
        self.console_input.configure({
            'width': 50,
            'bg': 'white',
        })
        self.console_input.bind('<Return>', self.send_command)
        self.console_input.grid(row=2, column=0, sticky=tk.W)

        self.command_send_button = tk.Button(self, text='Send', command=self.send_command)
        self.command_send_button.grid(row=2, column=1, sticky=tk.E)

        self.command_send_button = tk.Button(self, text='Send File', command=self.send_file)
        self.command_send_button.grid(row=2, column=2, sticky=tk.E)
        self.enve = self.canvas.create_image((50, 50), image=self.enve_image, state='hidden')
        self.connection_line_width = 3
        self.connection_line_start = 75
        self.connection_line = self.canvas.create_line(
            (self.connection_line_start, 75, self.connection_line_start + self.connection_line_width, 75), width=3
        )

        self.enve_anim = self.parent.after(300, self.animate_message)
        self.backward = False
        # self.init_animate_connection()

    def send_command(self, e=None):
        if not self.main.connection_is_active:
            self.console_input.delete(0, tk.END)
            self.console_input.insert(0, 'Connection closed')
            return

        self.init_message_animation()
        command = self.console_input.get()
        self.console_output.insert(tk.END, '> ' + command + '\n')

        stdin, stdout, stderr = self.ssh.exec_command(command)

        for line in stdout:
            self.console_output.insert(tk.END, str('< ' + line))
        self.console_input.delete(0, tk.END)

    def send_file(self):
        filename = askopenfilename()
        dest_filename = self.main.last_path + filename.split('/')[-1]

        scp = SCPClient(self.ssh.get_transport())
        scp.put(filename, dest_filename)
        scp.close()

        self.console_output.insert(tk.END, '> ' + 'File has been sent' + '\n')

    def animate_message(self):
        x = 10 if not self.backward else -10

        coords = self.canvas.coords(self.enve)

        if coords[0] > 500:
            self.backward = True

        elif coords[0] == 40:
            self.backward = False
            self.canvas.itemconfigure(self.enve, state='hidden')
            return

        self.canvas.move(self.enve, x, 0)
        self.parent.after(40, self.animate_message)

    def init_message_animation(self):
        self.canvas.move(self.enve, 10, 0)
        self.canvas.itemconfigure(self.enve, state='normal')
        self.after(10, self.animate_message)

    def init_animate_connection_open(self):
        self.parent.after(10, self.animate_connection_open)

    def animate_connection_open(self):
        self.connection_line_width += 10

        if self.connection_line_width >= 450:
            self.canvas.itemconfigure(self.connection_line, fill='green')
            return
        self.move_line()
        self.after(10, self.animate_connection_open)

    def init_animate_connection_close(self):
        self.canvas.itemconfigure(self.connection_line, fill='red')
        self.parent.after(10, self.animate_connection_close)

    def animate_connection_close(self):
        self.connection_line_width -= 10

        if self.connection_line_width <= 3:
            self.move_line()
            return

        self.move_line()
        self.after(10, self.animate_connection_close)

    def move_line(self):
        self.canvas.coords(
            self.connection_line,
            (self.connection_line_start, 75, self.connection_line_start + self.connection_line_width, 75)
        )
