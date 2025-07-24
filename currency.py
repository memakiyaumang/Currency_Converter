import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Fetch latest exchange rates
def get_rates():
    url = "https://api.apilayer.com/exchangerates_data/latest?base=USD"
    headers = {
        "apikey": "LbGrH6ewsNwV51ahffOUGp4LbOAukecx"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        print("Status Code:", response.status_code)
        print("Response:", response.text)  # Debug output
        data = response.json()

        if 'rates' not in data:
            raise ValueError("Invalid response from API")
        return data['rates']
    except Exception as e:
        messagebox.showerror("API Error", f"Failed to fetch exchange rates.\n{e}")
        return {}

# Perform conversion
def convert():
    try:
        amount = float(amount_entry.get())
        from_currency = from_combobox.get()
        to_currency = to_combobox.get()
        result = amount * rates[to_currency] / rates[from_currency]
        result_label.config(text=f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

# Initialize GUI
root = tk.Tk()
root.title("💱 Real-Time Currency Converter")
root.geometry("450x350")
root.configure(bg="#f4f6f7")  # Light background
root.resizable(False, False)

# Load exchange rates
rates = get_rates()
if not rates:
    root.destroy()
    exit()

currencies = sorted(rates.keys())

# Styling
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 10), background="#f4f6f7")
style.configure("TButton", font=("Segoe UI", 10, "bold"), foreground="white", background="#3498db", padding=6)
style.map("TButton", background=[('active', '#2980b9')])
style.configure("TCombobox", padding=4)

# Title
ttk.Label(root, text="Currency Converter", font=("Segoe UI", 18, "bold"), foreground="#2c3e50", background="#f4f6f7").pack(pady=15)

# Frame for inputs
frame = ttk.Frame(root, padding=10, style="TFrame")
frame.pack(pady=10)

# Amount
ttk.Label(frame, text="Amount:").grid(row=0, column=0, padx=5, pady=8, sticky='e')
amount_entry = ttk.Entry(frame, width=20)
amount_entry.grid(row=0, column=1, padx=5)

# From Currency
ttk.Label(frame, text="From:").grid(row=1, column=0, padx=5, pady=8, sticky='e')
from_combobox = ttk.Combobox(frame, values=currencies, state="readonly", width=18)
from_combobox.grid(row=1, column=1)
from_combobox.set("USD")

# To Currency
ttk.Label(frame, text="To:").grid(row=2, column=0, padx=5, pady=8, sticky='e')
to_combobox = ttk.Combobox(frame, values=currencies, state="readonly", width=18)
to_combobox.grid(row=2, column=1)
to_combobox.set("INR")

# Convert Button
convert_button = ttk.Button(root, text="Convert", command=convert)
convert_button.pack(pady=15)

# Result Label
result_label = ttk.Label(root, text="", font=("Segoe UI", 12, "bold"), foreground="#34495e")
result_label.pack(pady=10)

root.mainloop()
