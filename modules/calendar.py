import tkinter as tk
from datetime import datetime

class CalendarDatePicker:
    """3 combobox để chọn ngày, tháng, năm."""
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.day_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        
        # Combobox ngày
        self.day_cb = tk.ttk.Combobox(self.frame, textvariable=self.day_var, values=[f'{i:02d}' for i in range(1, 32)], state='readonly', width=3)
        self.day_cb.pack(side=tk.LEFT, padx=1)
        self.day_cb.bind('<<ComboboxSelected>>', self.update_date)
        
        tk.Label(self.frame, text='/').pack(side=tk.LEFT)
        
        # Combobox tháng
        self.month_cb = tk.ttk.Combobox(self.frame, textvariable=self.month_var, values=[f'{i:02d}' for i in range(1, 13)], state='readonly', width=3)
        self.month_cb.pack(side=tk.LEFT, padx=1)
        self.month_cb.bind('<<ComboboxSelected>>', self.update_date)
        
        tk.Label(self.frame, text='/').pack(side=tk.LEFT)
        
        # Combobox năm
        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 10, current_year + 11)]
        self.year_cb = tk.ttk.Combobox(self.frame, textvariable=self.year_var, values=years, state='readonly', width=5)
        self.year_cb.pack(side=tk.LEFT, padx=1)
        self.year_cb.bind('<<ComboboxSelected>>', self.update_date)
        
        # Set default to today
        today = datetime.now()
        self.day_var.set(f'{today.day:02d}')
        self.month_var.set(f'{today.month:02d}')
        self.year_var.set(str(today.year))

    def update_date(self, event=None):
        # Có thể validate ở đây nếu cần, nhưng tạm thời không
        pass

    def get(self):
        day = self.day_var.get()
        month = self.month_var.get()
        year = self.year_var.get()
        if day and month and year:
            return f'{day}/{month}/{year}'
        return ''

    def set(self, value):
        if value and '/' in value:
            parts = value.split('/')
            if len(parts) == 3:
                self.day_var.set(parts[0])
                self.month_var.set(parts[1])
                self.year_var.set(parts[2])

    def insert(self, idx, value):
        self.set(value)

    def delete(self, start, end=None):
        self.day_var.set('')
        self.month_var.set('')
        self.year_var.set('')