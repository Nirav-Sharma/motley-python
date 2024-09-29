"""
Creates a box where a user can input 3 out of Starting capital, Years invested, Yearly interest rate and Capital after interest 
then the fourth is calculated depending on which type of interest you select from a dropdown box (Simple, Compound or monthly compound)  
"""


import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import math

def calculate_missing():
    try:
        # Get values from entry boxes
        a_value = a_entry.get()
        b_value = b_entry.get()
        c_value = c_entry.get()
        d_value = d_entry.get()
        it = operation_combo.get()  # Get selected interest type
        
        # Convert entered values to float if possible, else None
        pv = float(a_value) if a_value else None #Starting capital
        n = float(b_value) if b_value else None #Years invested
        r = float(c_value) if c_value else None #Interest rate
        fv = float(d_value) if d_value else None #Capital after interest

        # Perform calculation based on the selected interest type (Simple, Compound or monthly compound)
        if it == 'Simple':
            if pv is None and n is not None and r is not None and fv is not None:
                pv = round(fv / (1 + (r / 100) * n), 2)
                a_entry.insert(0, str(pv))
            elif n is None and pv is not None and r is not None and fv is not None:
                n = math.ceil((fv / pv - 1) / (r / 100))
                b_entry.insert(0, str(n))
            elif r is None and pv is not None and n is not None and fv is not None:
                r = round(100 * (fv / pv - 1) / n, 3)
                c_entry.insert(0, str(r))
            elif fv is None and pv is not None and r is not None and n is not None:
                fv = round((1 + (r / 100) * n) * pv, 2)
                d_entry.insert(0, str(fv))
            else:
                messagebox.showerror("Input Error", "Please enter exactly three values into the interest calculator.")

        elif it == 'Compound':
            if pv is None and n is not None and r is not None and fv is not None:
                pv = round(fv / (1 + (r / 100)) ** n, 2)
                a_entry.insert(0, str(pv))
            elif n is None and pv is not None and r is not None and fv is not None:
                n = math.ceil(math.log(fv / pv) / (math.log(1 + r / 100)))
                b_entry.insert(0, str(n))
            elif r is None and pv is not None and n is not None and fv is not None:
                r = round(100 * ((fv / pv) ** (1 / n) - 1), 2)
                c_entry.insert(0, str(r))
            elif fv is None and pv is not None and r is not None and n is not None:
                fv = round(pv * (1 + (r / 100)) ** n, 2)
                d_entry.insert(0, str(fv))
            else:
                messagebox.showerror("Input Error", "Please enter exactly three values into the interest calculator.")

        elif it == 'Monthly Compound':
            if pv is None and n is not None and r is not None and fv is not None:
                pv = round(fv / (1 + (r / 1200))**(12 * n), 2)
                a_entry.insert(0, str(pv))
            elif n is None and pv is not None and r is not None and fv is not None:
                n = math.ceil(math.log(fv / pv) / (12 * math.log(1 + r / 1200)) - 1)
                b_entry.insert(0, str(n))
            elif r is None and pv is not None and n is not None and fv is not None:
                r = round(((fv / pv) ** (1 / (12 * n)) - 1) * 1200, 3)
                c_entry.insert(0, str(r))
            elif fv is None and pv is not None and r is not None and n is not None:
                fv = round(((1 + (r / 1200))**(12 * n)) * pv, 2)
                d_entry.insert(0, str(fv))
            else:
                messagebox.showerror("Input Error", "Please enter exactly three values into the interest calculator.")

        else:
            messagebox.showerror("Operation Error", "Please select a valid operation.")
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Create the main window
root = tk.Tk()
root.title("Interest Calculator")

# Create labels and entry fields
a_label = tk.Label(root, text="Starting capital:")
a_label.grid(row=0, column=0)

a_entry = tk.Entry(root)
a_entry.grid(row=0, column=1)

b_label = tk.Label(root, text="Years invested:")
b_label.grid(row=1, column=0)

b_entry = tk.Entry(root)
b_entry.grid(row=1, column=1)

c_label = tk.Label(root, text="Yearly interest rate:")
c_label.grid(row=2, column=0)

c_entry = tk.Entry(root)
c_entry.grid(row=2, column=1)

d_label = tk.Label(root, text="Capital after interest:")
d_label.grid(row=3, column=0)

d_entry = tk.Entry(root)
d_entry.grid(row=3, column=1)

# Create a dropdown for interest type selection
operation_label = tk.Label(root, text="Type of interest:")
operation_label.grid(row=4, column=0)

operation_combo = ttk.Combobox(root, values=["Simple", "Compound", "Monthly Compound"])
operation_combo.grid(row=4, column=1)
operation_combo.set("Simple")  

calculate_button = tk.Button(root, text="Calculate Missing Value", command=calculate_missing)
calculate_button.grid(row=5, columnspan=2)

root.mainloop()