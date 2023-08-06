import paramiko
import tkinter as tk

from src.canvas import CanvasFrame
from src.shell import ShellFrame


class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.last_path = '~/'
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connection_is_active = False
        self.canvas_frame = CanvasFrame(self.parent, self.ssh, main=self)
        self.canvas_frame.grid(row=0, column=0)

        self.shell_frame = ShellFrame(self.parent, self.ssh, main=self)
        self.shell_frame.grid(row=0, column=1, pady=0)

    def set_last_path(self, path):
        self.last_path = path


def main():
    root = tk.Tk()
    root.title("SSH Client")
    root.geometry('1000x650+0+0')
    root.resizable(False, False)
    MainWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()
