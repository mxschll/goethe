
import os
import webbrowser
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Interpreter import Interpreter


class TextWidget(tk.Text):
    """Custom text widget that listens to text changes."""

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result


class Editor:
    """Editor for the goethe programming language. Helps with debugging and visualizing the program.
    """

    def __init__(self) -> None:
        self.title = 'Goethe Editor'

        self.interpreter = Interpreter()
        self.interpreter.add_event_listener('<out>', self.__console_append)
        self.interpreter.add_event_listener('<end>', self.__reached_end)

        # The <step> listener was replaced by self.__step_forward() because it
        # caused performance problems with large programs.
        # self.interpreter.add_event_listener('<step>', self.__update_widgets)

        # Path and name of the currently opened file
        self.filepath = False
        self.filename = False

        self.root = tk.Tk()
        self.root.minsize(width=1280, height=720)
        self.root.geometry("1280x720")
        self.__set_title()

        # Setup column layout
        self.root.grid_columnconfigure(0, weight=1, uniform="group")
        self.root.grid_columnconfigure(1, weight=1, uniform="group")
        self.root.grid_rowconfigure(0, weight=1)

        col_one = tk.Frame(master=self.root)
        col_two = tk.Frame(master=self.root)
        col_three = tk.Frame(master=self.root)

        col_one.grid(row=0, column=0, sticky='nsew')
        col_two.grid(row=0, column=1, sticky="nsew")
        col_three.grid(row=0, column=2, sticky="nsew")

        """
        Init text editor.
        """
        scrollbar = tk.Scrollbar(col_one)
        scrollbar.pack(side='right', fill='y')
        self.editor = TextWidget(
            col_one,
            bg='seashell2',
            padx=10,
            pady=10,
            font=('Constantia', 16),
            yscrollcommand=scrollbar.set
        )
        self.editor.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.editor.yview)
        self.editor.bind('<<TextModified>>', self.__text_modified)

        """
        Init memory widget.
        """
        console_fonttype = ('Consolas', 12)
        self.memory_widget = tk.Text(
            col_two,
            bg='black',
            fg='white',
            padx=10,
            pady=10,
            font=console_fonttype,
            height=12)
        self.memory_widget.pack(fill='x')
        self.memory_widget.tag_config(
            'active',
            background='turquoise1',
            foreground='red2')

        """
        Init console widget.
        """
        self.console_widget = tk.Text(
            col_two,
            bg='black',
            fg='white',
            padx=10,
            pady=10,
            font=console_fonttype)
        self.console_widget.pack(fill='both', expand=True)
        self.console_widget.tag_config(
            'prompt',
            foreground='green2')
        self.__console_append('goethe$ ', 'prompt')

        """
        Init program widget.
        """
        self.program_widget = tk.Text(
            col_three,
            bg='black',
            fg='white',
            padx=10,
            pady=10,
            font=console_fonttype,
            width=6)
        self.program_widget.tag_config(
            'active',
            background='turquoise1',
            foreground='red2')

        self.program_widget.pack(fill='both', expand=True)
        self.program_widget.insert('end', 'Program')

        self.__update_widgets()

        """
        Setup menu bar.
        """
        menu_bar = tk.Menu(self.root)

        # File menu
        menu_one = tk.Menu(self.root, tearoff=0)
        menu_one.add_command(label="Open",
                             command=self.__open_file,
                             accelerator="Ctrl+O")
        menu_one.add_command(label="Save",
                             command=self.__save_file,
                             accelerator="Ctrl+S")
        menu_one.add_command(label="Save As",
                             command=self.__save_file_as,
                             accelerator="Ctrl+Shift-S")
        menu_one.add_separator()
        menu_one.add_command(label="Exit",
                             command=self.root.quit,
                             accelerator="Ctrl+W")
        menu_bar.add_cascade(label="File", menu=menu_one)

        # Program menu
        menu_two = tk.Menu(menu_bar, tearoff=0)
        menu_two.add_command(label="Run",
                             command=self.__run_program,
                             accelerator="Ctrl+Shift+G")
        menu_two.add_command(label="Step",
                             command=self.__step_forward,
                             accelerator="Ctrl+G")
        menu_two.add_command(label="Reset",
                             command=self.reset,
                             accelerator="Ctrl+R")
        menu_bar.add_cascade(label="Program", menu=menu_two)

        # Help menu
        menu_three = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=menu_three)
        menu_three.add_command(label="About...",
                               command=lambda: webbrowser.open(
                                   'https://github.com/mxschll/goethe-lang'))

        self.root.config(menu=menu_bar)

        # Add global window keybindings
        self.root.bind_all('<Control-o>', self.__open_file)
        self.root.bind_all('<Control-s>', self.__save_file)
        self.root.bind_all('<Control-S>', self.__save_file_as)
        self.root.bind_all('<Control-G>', self.__run_program)
        self.root.bind_all('<Control-g>', self.__step_forward)
        self.root.bind_all('<Control-r>', self.reset)
        self.root.bind_all('<Control-w>', lambda e: self.root.quit())

    def main(self) -> None:
        """Starts the editor window mainloop.
        """
        self.root.mainloop()

    def __set_title(self, file_saved=False) -> None:
        """Sets the window title depending on the file saved state.

        Args:
            file_saved (bool, optional): True if the currently opened file was saved. Defaults to False.
        """

        title = f'{self.filename} - {self.title}' if self.filename else self.title
        title += '' if file_saved == True else '*'

        self.root.title(title)

    def __text_modified(self, event=False) -> None:
        """Passes the current text to the interpreter and updates widgets.

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """

        self.interpreter.set_text(self.__get_text())
        self.__update_widgets()
        self.__set_title()

    def __get_text(self) -> str:
        """Returns the content of the text editor.

        Returns:
            str: Text editor content.
        """

        return self.editor.get(1.0, 'end')

    def __update_widgets(self, event=False) -> None:
        """Updates memory and console widget text.

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """

        program_pointer = self.interpreter.pointer
        program_instruction = self.interpreter._get_current_instruction()
        memory_pointer = self.interpreter.memory.get_pointer()
        memory_value = self.interpreter.memory.get_value()

        # Update program widget
        self.program_widget['state'] = 'normal'
        self.program_widget.delete(1.0, 'end')

        for i, command in enumerate(self.interpreter.program):
            if i == program_pointer:
                self.program_widget.insert('end', command + '\n', 'active')
            else:
                self.program_widget.insert('end', command + '\n')

        # Scroll active command into view
        self.program_widget.see(float(program_pointer + 5))
        self.program_widget['state'] = 'disabled'

        # Update memory widget
        self.memory_widget['state'] = 'normal'
        self.memory_widget.delete(1.0, 'end')

        self.memory_widget.insert(
            'end', f'Program Pointer:   {program_pointer} → {program_instruction}\n')
        self.memory_widget.insert(
            'end', f'Memory Pointer:    {memory_pointer} → {memory_value}\n\n')

        for i, value in enumerate(self.interpreter.memory.to_list()):
            if i == memory_pointer:
                self.memory_widget.insert('end', value, 'active')
            else:
                self.memory_widget.insert('end', value)

            self.memory_widget.insert('end', ' ')

        self.memory_widget['state'] = 'disabled'

    def __run_program(self, event=False) -> None:
        """Runs the program.

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """
        self.interpreter.run()

    def __step_forward(self, event=False) -> None:
        """Runs the next command of the program.

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """

        self.interpreter.step()
        self.__update_widgets()

    def __reached_end(self, event=False) -> None:
        """Updates widgets and creates new line in console widget.

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """
        self.__console_append('\ngoethe$ ', 'prompt')
        self.__update_widgets()

    def reset(self, event=False) -> None:
        """ Resets the program to the initial state .

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """

        self.interpreter.set_text(self.__get_text())
        self.__update_widgets()

    def __console_append(self, text='', style=None) -> None:
        """Appends the given text to the console widget and scrolls to the bottom.

        Args:
            text (str, optional): Text to be appended. Defaults to ''.
        """

        self.console_widget['state'] = 'normal'
        self.console_widget.insert('end', text, style)
        self.console_widget['state'] = 'disabled'
        self.console_widget.see('end')

    def __open_file(self, event=False) -> None:
        """Loads file into the editor.

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """

        filepath = askopenfilename(
            filetypes=[("Goethe Files", "*.goethe"), ("All Files", "*.*")])

        if not filepath:
            # User did not select a file
            return

        with open(filepath, "r") as file:
            self.filepath = filepath
            self.filename = os.path.basename(self.filepath)
            self.editor.delete(1.0, 'end')
            self.editor.insert('end', file.read())
            self.interpreter.set_text(self.__get_text())
            self.__update_widgets()

    def __save_file_as(self, event=False) -> None:
        """Saves the current text after asking for a filename.

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """

        file = asksaveasfilename(
            defaultextension='.goethe',
            filetypes=[('Goethe Files', '*.goethe'), ('All Files', '*.*')])

        if not file:
            # The user did not specify a file name
            return

        with open(file, "w") as file:
            file.write(self.__get_text())
            self.filepath = file.name
            self.filename = os.path.basename(self.filepath)
            self.__set_title(file_saved=True)

    def __save_file(self, event=False) -> None:
        """Saves the current text without asking for a filename.

        Args:
            event (bool, optional): Tkinter event. Defaults to False.
        """

        if self.filename == False:
            # Filename has not been set yet
            return self.__save_file_as()

        with open(self.filepath, 'w') as file:
            file.write(self.__get_text())
            self.interpreter.set_text(self.__get_text())
            self.__set_title(file_saved=True)
            self.__update_widgets()


if __name__ == '__main__':
    editor = Editor()
    editor.main()
