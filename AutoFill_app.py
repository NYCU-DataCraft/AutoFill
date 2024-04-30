import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

import PIL

from autofill import main

class AutoFill(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #self.geometry("400x300")

        # Create a container to hold all pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Define and add all pages to the application
        for F in (MainPage, Instruction, About):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the start page by default
        self.show_frame(MainPage)

    def show_frame(self, cont):
        # Show the given frame
        frame = self.frames[cont]
        frame.tkraise()

# Define each page as a separate class
class MainPage(tk.Frame):
    def __init__(self, parent, controller):

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
        tk.Frame.__init__(self, parent)

        # Create input fields
        account_label = tk.Label(self, text="陽明單一入口帳號：")
        account_label.grid(row=0, column=0)
        account_input = tk.Entry(self)
        account_input.grid(row=0, column=1)

        password_label = tk.Label(self, text="陽明單一入口密碼：")
        password_label.grid(row=1, column=0)
        password_input = tk.Entry(self, show="*")
        password_input.grid(row=1, column=1)

        # Create a button to run the script
        run_button = tk.Button(self, text="執行自動填答", command=run_script)
        run_button.grid(row=3, columnspan=2)

        # Footers
        footer_label1 = tk.Label(self, text="登入後若出現二階段驗證，程式會暫停30秒，請在30秒內填答完畢", foreground="red")
        footer_label1.grid(row=4, columnspan=2)
        footer_label2 = tk.Label(self, text="開始後除了二階段驗證，不要進行其他任何操作，如上下滾動頁面", foreground="red")
        footer_label2.grid(row=5, columnspan=2)
        footer_label3 = tk.Label(self, text="此程式不會儲存任何個人資料，請放心使用", foreground="red")
        footer_label3.grid(row=6, columnspan=2)

        # Button to navigate to 使用步驟
        button = tk.Button(self, text="使用步驟", command=lambda: controller.show_frame(Instruction))
        button.grid(row=7, column=0)

        # Button to navigate to 關於我們
        button = tk.Button(self, text="關於我們", command=lambda: controller.show_frame(About))
        button.grid(row=7, column=1)

class Instruction(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="使用步驟", foreground="blue")
        label.grid(row=1, column=1)

        label = tk.Label(self, text="1. 在主頁輸入陽明單一入口的帳號密碼，等待瀏覽器開啟")
        label.grid(row=2, column=1)
        label = tk.Label(self, text="2. 若出現二階段驗證，程式會暫停20秒，請在時間內填寫完畢")
        label.grid(row=3, column=1)
        label = tk.Label(self, text="3. 若帳號密碼有誤，或程式突然停止運行，請\n放心等候，出現逾時錯誤後重新嘗試即可")
        label.grid(row=4, column=1)
        label = tk.Label(self, text="4. 瀏覽器會全程開啟，可以看到程式進行的\n操作，若有疑慮，請直接關閉瀏覽器")
        label.grid(row=5, column=1)
        label = tk.Label(self, text="本軟體不會以任何形式儲存或使用你的資料，請放心使用", foreground="red")
        label.grid(row=6, column=1)

        # Button to navigate back to StartPage
        button = tk.Button(self, text="回到主頁", command=lambda: controller.show_frame(MainPage))
        button.grid(row=7, column=1)

class About(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="關於我們", foreground="blue")
        label.grid(row=0, column=0)

        logo_image = PhotoImage(file="resource/Logo.png")
        img_label = tk.Label(self, image = logo_image)
        img_label.place(x=200,y=0)
        img_label.image = logo_image

        label = tk.Label(self, text="本軟體已開源，請至\n")
        label.place(x=0,y=25)
        label = tk.Label(self, text="開發團隊：Datacraft")
        label.place(x=0,y=50)
        label = tk.Label(self, text="信箱：realdatacraft@gmail.com")
        label.place(x=0,y=75)
        label = tk.Label(self, text="IG：real_datacraft")
        label.place(x=0,y=100)

        # Button to navigate back to StartPage
        button = tk.Button(self, text="回到主頁", command=lambda: controller.show_frame(MainPage))
        button.place(x=150,y=125)

if __name__ == "__main__":
    app = AutoFill()
    app.mainloop()