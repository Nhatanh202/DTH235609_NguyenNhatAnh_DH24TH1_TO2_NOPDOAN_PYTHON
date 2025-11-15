import tkinter as tk
from modules.gui import App, create_login_window

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    create_login_window(root)
    try:
        if root.state() == 'withdrawn':
            root.mainloop()
        else:
            app = App(root)
            root.mainloop()
    except Exception:
        try:
            root.mainloop()
        except Exception:
            pass