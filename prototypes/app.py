from tkinter import Tk, Label, Entry, Button
from tkinter import messagebox

#from autofill import main
def main():
    pass

def run_script():
    account = account_input.get()
    password = password_input.get()
    if account == "" or password == "":
        messagebox.showinfo("Warning", "請輸入帳號密碼")
        return

    end_m = main(account, password)
    #root.destroy()
    messagebox.showinfo("Result", end_m)

# Create the main application window
root = Tk()
root.title("自動填寫問卷表單")
root.geometry("320x200")

# Create input fields
account_label = Label(root, text="陽明單一入口帳號：")
account_label.grid(row=0, column=0)
account_input = Entry(root)
account_input.grid(row=0, column=1)

password_label = Label(root, text="陽明單一入口密碼：")
password_label.grid(row=1, column=0)
password_input = Entry(root, show="*")
password_input.grid(row=1, column=1)

# Create a button to run the script
run_button = Button(root, text="執行自動填答", command=run_script)
run_button.grid(row=3, columnspan=2)

# Footers
footer_label1 = Label(root, text="登入後若出現二階段驗證，程式會暫停20秒，請在20秒內填答完畢", foreground="red")
footer_label1.grid(row=4, columnspan=2)
footer_label2 = Label(root, text="開始後除了二階段驗證，請不要進行其他任何操作", foreground="red")
footer_label2.grid(row=5, columnspan=2)
footer_label3 = Label(root, text="此程式不會儲存任何資料，請放心使用", foreground="red")
footer_label3.grid(row=6, columnspan=2)

# Run the GUI application
root.mainloop()