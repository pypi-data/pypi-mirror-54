import os
import tkinter as tk


class ShellFrame(tk.Frame):
    def __init__(self, parent, ssh_client, main):
        super().__init__(parent)
        self.parent = parent
        self.main = main
        self.ssh = ssh_client
        self.credentials_list = []

        self.connection_flag = False

        # Connection Label
        self.conn_label = tk.Label(self, text='Connection parameters:')
        self.conn_label.grid(row=0, columnspan=3, sticky=tk.NW)

        # Host and Port
        self.host_label = tk.Label(self, text='Host:')
        self.port_label = tk.Label(self, text='Port:')

        self.host_label.grid(row=1, column=1, sticky=tk.W)
        self.port_label.grid(row=1, column=2, sticky=tk.W)

        self.host_var = tk.StringVar(self)
        self.port_var = tk.StringVar(self)

        self.host_entry = tk.Entry(self, textvariable=self.host_var)
        self.port_entry = tk.Entry(self, textvariable=self.port_var)

        self.host_entry.grid(row=2, column=1, sticky=tk.W)
        self.port_entry.grid(row=2, column=2, sticky=tk.W)

        # Username and Password
        self.username_label = tk.Label(self, text='Username:')
        self.password_label = tk.Label(self, text='Password:')

        self.username_label.grid(row=3, column=1, sticky=tk.W)
        self.password_label.grid(row=3, column=2, sticky=tk.W)

        self.username_var = tk.StringVar(self)
        self.username_entry = tk.Entry(self, textvariable=self.username_var)

        self.password_var = tk.StringVar(self)
        self.password_entry = tk.Entry(self, show='*', textvariable=self.password_var)

        self.username_entry.grid(row=4, column=1, sticky=tk.W)
        self.password_entry.grid(row=4, column=2, sticky=tk.W)

        # Open Connection Button
        self.connection_button_text = tk.StringVar(self, "Open Connection")
        self.connection_button = tk.Button(self, textvar=self.connection_button_text, command=self.toggle)
        self.connection_button.grid(row=5, column=1, sticky=tk.W + tk.E, pady=2)

        # Save connection button
        self.save_connection_button = tk.Button(self, text="Save", command=self.save_connection)
        self.save_connection_button.grid(row=5, column=2, sticky=tk.W + tk.E, pady=2)

        # Scroll Bar and Command Line Output
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=6, column=5, rowspan=1, sticky=tk.N + tk.S)

        self.sessions_list = tk.Listbox(self, yscrollcommand=self.scrollbar.set)
        self.sessions_list.grid(row=6, column=0, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S)
        self.init_sessions_list()
        self.sessions_list.bind('<<ListboxSelect>>', self.load_credentials)

    def read_inputs(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        return host, port, username, password

    def host_is_valid(self, host):
        pass

    def toggle(self):
        if not self.main.connection_is_active:
            self.main.canvas_frame.init_animate_connection_open()
            host, port, username, password = self.read_inputs()
            self.ssh.connect(hostname=host, port=port, username=username, password=password)
            self.connection_button_text.set('Close Connection')
            self.main.canvas_frame.console_output.insert(tk.END, '> ' + 'Connection Established' + '\n')

        else:
            self.main.canvas_frame.init_animate_connection_close()
            self.ssh.close()
            self.connection_button_text.set('Open Connection')
            self.main.canvas_frame.console_output.insert(tk.END, '> ' + 'Connection Closed' + '\n')

        self.main.connection_is_active = not self.main.connection_is_active

    def update_window(self):
        for line in iter(lambda: self.stdout.readline(), ""):
            self.sessions_list.insert(tk.END, str(line))
            self.scrollbar.config(command=self.sessions_list.yview)
        # self.root2.after(1000, self.update_window)

    def save_connection(self):
        host, port, username, password = self.read_inputs()
        file_name = os.path.join('src', 'credentials.txt')

        with open(file_name, 'a') as file:
            credentials = '{0}#{1}#{2}#{3}\n'.format(host, port, username, password)
            file.writelines([credentials])

        self.credentials_list.append((host, port, username, password))
        self.update_session_list()

    def update_session_list(self):
        self.sessions_list.delete(0, tk.END)
        for credential in self.credentials_list:
            if credential and len(credential) == 4:
                line = '{0}@{1}'.format(credential[0], credential[2])
                self.sessions_list.insert(tk.END, line)

    def init_sessions_list(self):
        file_name = os.path.join(self.main.BASE_DIR, 'src', 'credentials.txt')

        with open(file_name, 'r') as file:
            for line in file:
                credentials = line.strip('\n').split('#')
                self.credentials_list.append(tuple(credentials))
        self.update_session_list()

    def load_credentials(self, event):
        try:
            index = self.sessions_list.curselection()[0]
            credentials = self.credentials_list[index]

            host, port, username, password = credentials

            self.host_var.set(host)
            self.port_var.set(port)
            self.username_var.set(username)
            self.password_var.set(password)
        except IndexError:
            pass
