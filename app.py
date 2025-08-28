import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("โปรแกรมรายรับ-รายจ่าย + ภาษี")
root.geometry("700x650")
root.config(bg="white")

# ---------------- สร้างหัวตาราง ----------------
headers = ["วันที่", "รายการ", "รายรับ", "รายจ่าย"]

for i, h in enumerate(headers):
    tk.Label(root, text=h, relief="solid", width=15, bg="lightgray").grid(row=0, column=i)

# ---------------- เก็บ entry ไว้ใน list ----------------
rows = []
def add_row():
    row_entries = []
    r = len(rows) + 1
    for c in range(len(headers)):
        e = tk.Entry(root, width=17, justify="center")
        e.grid(row=r, column=c, padx=1, pady=1)
        row_entries.append(e)
    rows.append(row_entries)

def delete_row():
    if rows:
        row_entries = rows.pop()
        for e in row_entries:
            e.destroy()

def calculate_balance():
    """คำนวณยอดคงเหลือ (รายรับ - รายจ่าย)"""
    balance = 0
    for row in rows:
        try:
            income = float(row[2].get()) if row[2].get() else 0
        except ValueError:
            income = 0

        try:
            expense = float(row[3].get()) if row[3].get() else 0
        except ValueError:
            expense = 0

        balance += income - expense

    balance_var.set(f"{balance:,.2f}")

def calculate_tax():
    """คำนวณภาษีเงินได้แบบก้าวหน้า (ไทย)"""
    try:
        salary = float(entry_salary.get())
    except ValueError:
        messagebox.showerror("Error", "กรุณาใส่เงินเดือนเป็นตัวเลข")
        return

    # สมมุติ: เงินเดือน * 12 = รายได้ทั้งปี
    annual_income = salary * 12

    # ขั้นบันไดภาษี (เงินสะสม, อัตรา)
    brackets = [
        (150000, 0.00),
        (300000, 0.05),
        (500000, 0.10),
        (750000, 0.15),
        (1000000, 0.20),
        (2000000, 0.25),
        (5000000, 0.30),
        (float("inf"), 0.35),
    ]

    tax = 0
    prev_limit = 0

    for limit, rate in brackets:
        if annual_income > limit:
            tax += (limit - prev_limit) * rate
            prev_limit = limit
        else:
            tax += (annual_income - prev_limit) * rate
            break

    tax_var.set(f"{tax:,.2f} บาท/ปี")

# ---------------- ปุ่มเพิ่ม/ลบตาราง ----------------
frame_btn = tk.Frame(root, bg="white")
frame_btn.grid(row=20, column=0, columnspan=5, pady=10)

btn_add = tk.Button(frame_btn, text="+ ตาราง", width=12, command=add_row)
btn_add.grid(row=0, column=0, padx=10)

btn_del = tk.Button(frame_btn, text="- ตาราง", width=12, command=delete_row)
btn_del.grid(row=0, column=1, padx=10)

# ---------------- ปุ่มคำนวณยอดคงเหลือ ----------------
frame_balance = tk.Frame(root, bg="white")
frame_balance.grid(row=21, column=0, columnspan=5, pady=10)

btn_calc_balance = tk.Button(frame_balance, text="คำนวณยอดคงเหลือ", command=calculate_balance)
btn_calc_balance.grid(row=0, column=0, padx=5)

balance_var = tk.StringVar()
lbl_balance = tk.Label(frame_balance, textvariable=balance_var, bg="white", fg="blue", font=("Arial", 12, "bold"))
lbl_balance.grid(row=0, column=1, padx=10)

# ---------------- ช่องคำนวณภาษี ----------------
frame_tax = tk.Frame(root, bg="white")
frame_tax.grid(row=22, column=0, columnspan=5, pady=10)

tk.Label(frame_tax, text="เงินเดือน:", bg="white").grid(row=0, column=0, padx=5)
entry_salary = tk.Entry(frame_tax, width=15)
entry_salary.grid(row=0, column=1, padx=5)

btn_calc_tax = tk.Button(frame_tax, text="คำนวณภาษี (ก้าวหน้า)", command=calculate_tax)
btn_calc_tax.grid(row=0, column=2, padx=5)

tax_var = tk.StringVar()
lbl_tax = tk.Label(frame_tax, textvariable=tax_var, bg="white", fg="red", font=("Arial", 12, "bold"))
lbl_tax.grid(row=0, column=3, padx=10)

root.mainloop()
