import calendar
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Theme colors
PANEL = '#ffffff'
TEXT = "#000000"

class CalendarDialog(tk.Toplevel):
    def __init__(self, parent, initial_date=None):
        super().__init__(parent)
        self.title("Chọn Ngày")
        self.geometry("300x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.selected_date = initial_date or datetime.now().date()
        self.result = None

        self.year_var = tk.IntVar(value=self.selected_date.year)
        self.month_var = tk.IntVar(value=self.selected_date.month)

        self.create_widgets()
        self.update_calendar()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        nav_frame = ttk.Frame(frame)
        nav_frame.pack(fill=tk.X)

        ttk.Button(nav_frame, text="<", command=self.prev_month).pack(side=tk.LEFT)
        ttk.Label(nav_frame, textvariable=self.month_var, width=3).pack(side=tk.LEFT, padx=5)
        ttk.Label(nav_frame, text="/").pack(side=tk.LEFT)
        ttk.Label(nav_frame, textvariable=self.year_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Button(nav_frame, text=">", command=self.next_month).pack(side=tk.LEFT)

        self.calendar_frame = ttk.Frame(frame)
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="OK", command=self.on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Hủy", command=self.on_cancel).pack(side=tk.RIGHT)

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(self.year_var.get(), self.month_var.get())

        days = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
        for i, day in enumerate(days):
            ttk.Label(self.calendar_frame, text=day, font=('Arial', 10, 'bold')).grid(row=0, column=i, padx=2, pady=2)

        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue
                btn = ttk.Button(self.calendar_frame, text=str(day), width=3,
                                command=lambda d=day: self.select_date(d))
                btn.grid(row=week_num, column=day_num, padx=1, pady=1)
                if day == self.selected_date.day and self.month_var.get() == self.selected_date.month and self.year_var.get() == self.selected_date.year:
                    btn.configure(style='Accent.TButton')

    def prev_month(self):
        if self.month_var.get() == 1:
            self.month_var.set(12)
            self.year_var.set(self.year_var.get() - 1)
        else:
            self.month_var.set(self.month_var.get() - 1)
        self.update_calendar()

    def next_month(self):
        if self.month_var.get() == 12:
            self.month_var.set(1)
            self.year_var.set(self.year_var.get() + 1)
        else:
            self.month_var.set(self.month_var.get() + 1)
        self.update_calendar()

    def select_date(self, day):
        self.selected_date = self.selected_date.replace(day=day, month=self.month_var.get(), year=self.year_var.get())
        self.update_calendar()

    def on_ok(self):
        self.result = self.selected_date
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

class CalendarDatePicker:
    """Entry-like widget that opens CalendarDialog to pick a date."""
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=PANEL)
        self.var = tk.StringVar()
        self.entry = tk.Entry(self.frame, textvariable=self.var, bg='white', fg=TEXT, width=10)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.btn = ttk.Button(self.frame, text='📅', width=3, command=self.open_calendar, style='Primary.TButton')
        self.btn.pack(side=tk.LEFT, padx=(6,0))

    def open_calendar(self):
        init = self.var.get().strip()
        dlg = CalendarDialog(self.frame, init_date=init if init else None)
        res = dlg.show()
        if res:
            self.var.set(res)

    def get(self):
        return self.var.get()

    def insert(self, idx, value):
        try:
            self.var.set(str(value))
        except Exception:
            pass

    def delete(self, start, end=None):
        try:
            self.var.set('')
        except Exception:
            pass