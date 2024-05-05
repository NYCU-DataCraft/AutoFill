import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import ttk

import sv_ttk

from autofill import main
import base64


def nxt_line():
    i = 0
    while True:
        yield i*30
        i += 1

class AutoFill(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("陽明交大教學問卷自動填答系統")
        self.geometry("480x350")

        # Create a container to hold all pages
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Define and add all pages to the application
        for F in (MainPage, Instruction, About, Settings):
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
class MainPage(ttk.Frame):
    def __init__(self, parent, controller):

        self.dark_mode = True
        self.mimic = False
        nxt = nxt_line()

        s = ttk.Style()
        s.configure('my.TButton', font=('微軟正黑體', 12))

        def run_script():
            account = account_input.get()
            password = password_input.get()
            if account == "" or password == "":
                messagebox.showinfo("Warning", "請輸入帳號密碼")
                return

            vbgcalv = controller.frames[Settings].setting
            end_m = main(account, password, self.mimic, vbgcalv)
            #root.destroy()
            messagebox.showinfo("Result", end_m)
        
        def toggle_dark_mode():
            if self.dark_mode:
                dm_button.config(text="夜間模式：OFF")
                sv_ttk.set_theme("light")
                self.dark_mode = False
            else:
                dm_button.config(text="夜間模式：ON")
                sv_ttk.set_theme("dark")
                self.dark_mode = True
        
        def toggle_mimic():
            if self.mimic:
                mimic_button.config(text="仿人模式：OFF")
                self.mimic = False
            else:
                mimic_button.config(text="仿人模式：ON")
                self.mimic = True

        # Create the main application window
        ttk.Frame.__init__(self, parent)

        # Create input fields
        r = next(nxt)
        account_label = ttk.Label(self, text="陽明單一入口帳號：", font=('微軟正黑體', 11))
        account_label.place(x=20, y=r+10)
        account_input = ttk.Entry(self)
        account_input.place(x=160, y=r+5)

        r = next(nxt)+20
        password_label = ttk.Label(self, text="陽明單一入口密碼：", font=('微軟正黑體', 11))
        password_label.place(x=20, y=r+10)
        password_input = ttk.Entry(self, show="*")
        password_input.place(x=160, y=r+5)

        # Create a button to run the script
        br=next(nxt)
        br=next(nxt)
        r = next(nxt)-15
        run_button = ttk.Button(self, text="執行自動填答", command=run_script, style='my.TButton')
        run_button.place(x=125, y=r)
        setting_button = ttk.Button(self, text="自訂填答選項", command=lambda: controller.show_frame(Settings), style='my.TButton')
        setting_button.place(x=235, y=r)

        # Setting buttons
        dm_button = ttk.Button(self, text="夜間模式：ON", command=toggle_dark_mode, style='my.TButton')
        dm_button.place(x=350, y=5)
        mimic_button = ttk.Button(self, text="仿人模式：OFF", command=toggle_mimic, style='my.TButton')
        mimic_button.place(x=350, y=55)

        # Footers
        footer_label0 = ttk.Label(self, text="注意事項", foreground="red", font=('微軟正黑體', 11, "underline"))
        footer_label0.place(x=10, y=next(nxt))
        footer_label1 = ttk.Label(self, text="1. 登入後若出現二階段驗證，程式會暫停30秒，請在30秒內填答完畢", font=('微軟正黑體', 11))
        footer_label1.place(x=10, y=next(nxt))
        footer_label2 = ttk.Label(self, text="2. 開始後除了二階段驗證，不要進行其他任何操作，如上下滾動頁面", font=('微軟正黑體', 11))
        footer_label2.place(x=10, y=next(nxt))
        footer_label3 = ttk.Label(self, text="4. 程式隨機暫停為正常現象（模仿人為操作），請耐心等候", font=('微軟正黑體', 11))
        footer_label3.place(x=10, y=next(nxt))
        footer_label4 = ttk.Label(self, text="3. 此程式不會儲存任何個人資料，請放心使用", font=('微軟正黑體', 11))
        footer_label4.place(x=10, y=next(nxt))

        # Buttons to navigate
        r = next(nxt)
        button = ttk.Button(self, text="使用步驟", command=lambda: controller.show_frame(Instruction), style='my.TButton')
        button.place(x=10, y=r)
        button = ttk.Button(self, text="關於我們", command=lambda: controller.show_frame(About), style='my.TButton')
        button.place(x=100, y=r)

class Settings(ttk.Frame):
    def __init__(self, parent, controller):
        r = 10
        ttk.Frame.__init__(self, parent)

        self.setting = None

        def show():
            a = ""
            ca_buffer = []
            for i in (five_elements, focus_level, attendance, study_span, expectation, difficulty):
                a += f'{i.current()}:{i.get()}\n'
                ca_buffer.append(i.current()+1)
            if any(num <= 0 for num in ca_buffer):
                self.setting = None
                title_label.config(text="自訂填答選項 | 目前：預設(Default)")
                messagebox.showinfo("result", "不合理的設定，請選填每個選項")
            else:
                self.setting = ca_buffer.copy()
                title_label.config(text="自訂填答選項 | 目前：自訂(Custom)")
                messagebox.showinfo("result", a)    # 顯示索引值與內容
            print(self.setting)

        label = ttk.Label(self, text="預設：非常滿意、認真、從不缺課\n3-5小時、前1/3、適中", font=('微軟正黑體', 9), foreground="red")
        label.place(x=290, y=10)

        title_label = ttk.Label(self, text="自訂填答選項 | 目前：預設(Default)", font=('微軟正黑體', 13, "underline"))
        title_label.place(x=10, y=r)
        r+=30
        label = ttk.Label(self, text="教學反應問項", font=('微軟正黑體', 11))
        label.place(x=200, y=r+8)
        five_elements = ttk.Combobox(self,
                    width=15,
                    values=['非常不同意','不同意','普通','同意','非常同意'],
                    state="readonly")
        five_elements.place(x=10, y=r)
        r+=45
        label = ttk.Label(self, text="我對這門課的態度", font=('微軟正黑體', 11))
        label.place(x=200, y=r+8)
        focus_level = ttk.Combobox(self,
                    width=15,
                    values=['認真','一般','不認真'],
                    state="readonly")
        focus_level.place(x=10, y=r)
        r+=45
        label = ttk.Label(self, text="我的缺席狀況", font=('微軟正黑體', 11))
        label.place(x=200, y=r+8)
        attendance = ttk.Combobox(self,
                    width=15,
                    values=['從不缺課','極少(三次以下)','偶而','常常缺課(超過1/3)'],
                    state="readonly")
        attendance.place(x=10, y=r)
        r+=45
        label = ttk.Label(self, text="我每週平均自習本實驗課程的時數約為", font=('微軟正黑體', 11))
        label.place(x=200, y=r+8)
        study_span = ttk.Combobox(self,
                    width=15,
                    values=['0~2小時','3~5小時','6小時以上'],
                    state="readonly")
        study_span.place(x=10, y=r)
        r+=45
        label = ttk.Label(self, text="預期學期結束時，我在本課程的成績", font=('微軟正黑體', 11))
        label.place(x=200, y=r+8)
        expectation = ttk.Combobox(self,
                    width=15,
                    values=['前1/3','中1/3','後1/3'],
                    state="readonly")
        expectation.place(x=10, y=r)
        r+=45
        label = ttk.Label(self, text="本實驗課程之難易度如何", font=('微軟正黑體', 11))
        label.place(x=200, y=r+8)
        difficulty = ttk.Combobox(self,
                    width=15,
                    values=['艱深','適中','過淺','無法判斷'],
                    state="readonly")
        difficulty.place(x=10, y=r)
        r+=45
        # Button to navigate back to StartPage
        button = ttk.Button(self, text="回到主頁", command=lambda: controller.show_frame(MainPage))
        button.place(x=200, y=r)
        # Button to navigate back to StartPage
        button = ttk.Button(self, text="儲存並顯示目前設定", command=show)
        button.place(x=10, y=r)

class Instruction(ttk.Frame):
    def __init__(self, parent, controller):
        r = 10
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="使用步驟", font=('微軟正黑體', 13, "underline"))
        label.place(x=10, y=r)
        r+=30
        label = ttk.Label(self, text="1. 在主頁輸入陽明單一入口的帳號密碼，點擊\"執行自動填答\"，等待\n瀏覽器開啟", font=('微軟正黑體', 11))
        label.place(x=10, y=r)
        r+=50
        label = ttk.Label(self, text="2. 若出現二階段驗證，程式會暫停30秒，請在時間內填寫完畢後\n耐心等待", font=('微軟正黑體', 11))
        label.place(x=10, y=r)
        r+=50
        label = ttk.Label(self, text="3. 若帳號密碼有誤，或程式突然停止運行，請放心等候，出現逾時錯\n誤後重新嘗試即可（暫停超過30秒可關閉瀏覽器重新執行）", font=('微軟正黑體', 11))
        label.place(x=10, y=r)
        r+=50
        label = ttk.Label(self, text="4. 瀏覽器會全程開啟，可以看到程式進行的操作，若有疑慮，請直接\n關閉瀏覽器", font=('微軟正黑體', 11))
        label.place(x=10, y=r)
        r+=50
        label = ttk.Label(self, text="本軟體不會以任何形式儲存或使用你的資料，請放心使用", foreground="red", font=('微軟正黑體', 11))
        label.place(x=10, y=r)
        r+=30

        # Button to navigate back to StartPage
        button = ttk.Button(self, text="回到主頁", command=lambda: controller.show_frame(MainPage))
        button.place(x=10, y=r)

class About(ttk.Frame):
    def __init__(self, parent, controller):

        # tkinter doesn't work with image path for some reasons
        Logo_image = b'iVBORw0KGgoAAAANSUhEUgAAALQAAAC0CAYAAAA9zQYyAABDIElEQVR4nO2dd2AUxfv/n5nd68ml90ZCCAkk1NB7B1GqgihVQJGPSg29946AKCi9KCJIUXqV3ksSQnpPLrn0y/Xdnfn9kZwGPgbQr+jvY/b15+3s7Mzce599ZuaZGQAREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREREZF/IZRSTCmV/9PlEBH5S5i9eO+I/mM2XJuy+kRnjP7p0vx7wf90AWoKLk7qewKSFN6+l3xs0IQ9S27EZjr/02X6NyLaitcEpZTBCAn02d9kH836cUx8Vu5chUye1rJp8KRF4zvdotXmIvJHEQX9Gjh+6Z7rkTMPNhipLGHjiuHrPBDSV72+YteF+pdvZa83mvXNavmoV+9eMvRzhJDxnyrvvwlR0K+BzMxMxdwdt8Yn5xTNVMtQbJtG4VMZKeVYZOGihnWNAwCglKoGz/thrCZXO99OqbjfJdI/KmpEt4eitf6/IQr6L4LFGHhCAKBiRINlEFmw7ULrG9FJS4utuIGFo0jCYH3jQLdlW6f13YYQ4gEA5u680ubGo8SVVk4IC/ByWbl3zsANCCHLP1qZ/2FEQf8FzP36px5J2YXD64bWXrnwvfbRVa9RSlWDVhyakJxZFFVikTnKEKJ1fOz29m3qvXhs39bJAABPnxbYzzt8a2p6QcFEJzvZ1W7NGk6L6hce98/U5n8bcZTjL0AmkxWVWkjghfsJZ4Z8fnw8pVRqu4YQMhya+c6yAa3q9A7xYK7o5RL0oIgbvuNKwonxX515m2UwhIW5lR+e89b8zhEBbwmC2fPwrbvn39946qPiYuqw9fj1UEop80/W738J0UL/CTBCQOiz3m5iIVXP3HE0Kru47FNnhex6h4haU2cMaPW0apq0khLHmbsuTY7JKp9QyMnUdozZGu4p3f5mZODCsV1b5QMARGdkOM05cHNWXrF1LGaU2TxX6O7r4nJkZLfwhf2ahuX+jdX8n0QU9B/kXk6Ocsvxi4soKJO2jRuwDSEk2K5hAJiy90qXu0np6yxgdQn18py/Y1zvXc+nmf3dlS6X4zNXJxskjZ1YjvuwS702E7s1uWtLwyCAT/ec630tuWilxkjqE0TBz57EtK3tPWfj0K7HeSJ2HatDFPQfhFIqH7Xp4PInJcbRjiq7s70b1Js5sXv9pKppjkWneOw8Hz0rV2f6wF4tPzWoeZ2ZH7WNSKma5lJsmue6i7FTcop0HznY21/sWT9g+vReDROqpjmTnOy+9aenM2KL9eNKeaxwZiyWUC+nrcPaRC4d2MhL+3fU938NUdCvAAKA5yZI0MeHfun5JDVvtYXyjqH+bjN2D+n+LUKI2NIzDIbRu6/0jc7OXgmUt6vn6zlj29Auv6YBAGAxgv/su9TnTqZ2FQdEHeHnMmPHe133/Veavef63c4qXpphgnoEAdR24B70r+0zLqpPx7sg8gyioF/Cwh8vt4orKRlex9v7i1W9Wz2xCAK2Ce5YdIrHptsP5hWXmUd4KRx/HNqs9ewhzV2yqt5/8GGCz65bMQty9IahnmqHQyND688a0qHOc2kyfb6583BBga58qKva/sd3IyNmjWkalFE1zXcxSX67b8fMS8g3jlQgYAc3qNVv/pttj73+FvjfQhT0S1h49HKnCxmarw2UyFWOrrfl1KLvXst7xdROkfEAABIGw5gDFwc80pSsACqwDXxdpu0Y1PUQJ/zqNgOlFI3+4cLgJ7nFKwBjPtzXY9q2/m2PVfWtK9JcHvwoX7scEE8jvX2m73i78w+2se3KNHjsocuDY3ILFyGGCg18PGdsH9DhqEBFn9qGKOjnQACw4/q90EbeLnmNAwNLAQC+fpzoe+zB0/lPddYxxUgG3lIutaWH44Lt/Tp/axPl57Ep/j/fe7qoWGd418VJ/u07DZrM+7ChX3bVvL+MTgj64W7islyzaUAttWzfh2F1Zg+MrKepmubrW/GBh2OeLtOYLANcnZx3jWraaMGweu7PpFl3NTroRFL68lK9oZ+Hi/rLkWF1lg1qElLwelvmfwNR0FWglEo/PPzzlDtFpkmOjCKuc0jQ9Hnt6t1BCFFKKR7/88mht/LMc9I5aR0Z6IVwR9UPXWsFLJveqkFsZRrJyCOXRz4u0i6QgMTQwstz9qTIoCuXkpP9xrZte49WPEM26MjFD1K1+QtYhi1u5OM2d/ubnQ9VHbmglEqG/nBxXGxpyWw5oiXNvD1mbnmz/VGePlNW5QcHT30UXWqYzrCMtpm3Y9RXvTqfIf9drRqFKOgqZGZmKqbdfLj5qo6MKpUoobWMnr8y9I1uFuE3mex5FB+4KzFjaVyZYYhJxkJnFbvr2MA3RlUV0vqbCWE/pyctKzSaumGZMp23WtxDXNRrD/XpsskWhLT2xuOIY2k5iw1Gwxsejo5bRzcOXDwwOPjXkQsMAKvuRYeeeJq6osgq9PRxcvhyQfPQpS18fYtsaRAArLqSWO9oVtKqUs7cMcjefv3aDt1Wh7gi3etvrf8/EQX9HJRSdtTZK+/fKjItZATBrr2384ffdGvz43O+rGzExavv3ckvWUiRIGnt7jZhX7cOB7ln00jfO3tt1H2tblGuIHGXgxkC7aWn3gjymLWwceNHtnwG/XT1o8TSkgWMTJrTwtNtytcdIs8KFddQpdWXDjxz5cM0bfFCBaNIb+7jOnFjx8ir5Nkyywb8fPnj7OLSeVKZ/Gmkt9fkje0b3a6JnnWNFvT6mzFhTwxF/YM9XffNCA/PrHpt5ZPkOmcSEpfnWc193J3U20bXDV48rFatZ3zZjdFpoQdTEldqOWNvX6Vye/+IJgs/DXDLtYkRAGD1neTwo7kpSxKMlr7ljAwCCGiauKpXDKhrv2+Qf3gxAMD8e3FNzmYkry3jScsAO+cv5rZpsLy1o2Ox7TkIABbeiml4Ojt3tY4nLX2clOu/bBaxrrazc1nVNLPvPGl8Pit7rZG3NPJTO67Y0bPdl8+Hrv7bqdGCXnH1Tq+jBZo95RJJaQtnh6g9bdse5ekzvqx00IVLY+N0+kVSrNS2c3WYsrlts5NClTwopbJ3Ll/5+EmRcR4jxQVtHBym7ejY6hj3bD7y9y5dHX+vWD8zl6hc1YwF+rup3vuyfZvvqqRR9Tt7cXK8wTTdnpHGN/d0mL61RYsLzz1L0e/s9U9TSw1z1Aoa18LTefL65s1vPDdGrup77peJKWXGqc4MxPQO8PhoRtOmz0zB/5up0cFJM9o1P9WjVlgHO1aWfL2k8IeOF85+eTAtzdN2HSFk/aFr581vB4R0smOZnCuFBUe6X7y2/lS61qtKGsvhTh0+H+hfu4sDEnIulmkPd7p4cevPz+ZjPtC5/bphIb49w+3M56mCh0QL1/12dplLlTSGn3p0WfyWX0APDJRczC/6ufelm0tTKHUAqPijEEKm4z3arurn79HNihh6XlN2csDFq9OrLr5FCBl+6t5xaQdP97dcZJIcKydRvvaG/P+IGm2hbVBKZQOu3xyfWF46355l8pqoHSd29PWNczCZzD0qO2qUUkW/a7c+Sy0zzrKTSHMi3e0mbm7c+OxzvqzyratXJ6Xoy2fYS2QZrZx8pmyKDHtm5EFDNaox1xMmpJYZZjliRXJbZ5cpa1s0vFA1TQqlDp9duDY7y2T9TC2l9wMcJEcpT3ze8qizdkgd3ywAgHvF1GHB/RvTMizlnzjKZHe7+XpOmhcWFvNcvXDVWceagCjoShAAzItLanI7K2utjpLmZgnWuVLQNPN0nrU8vNFpUplmzqOEFheLcjcKhGsQIrP7fFyDVqvrQRl1dXIq4SkFBACTHj1qe6ewbLWZcI1CVLJ1k8Parop0Rr/6uxgApjyI63BXm7fcClyjWmqHdRtatVjphlC5LY0EIRh390H3R8WFq7QS3LCcAgTz8rjmrnaz1jdtdEygFDAAfHbvSbs7Rdo1CNGAxgr5/E1tW31T00RcFVHQz0FzqHJU6rUJcRYyTStXObqbDeYmSsWX79XyXdHe27sAACC6NMNpzZPc/+QYuOlSqTSdATPykjEnh4dFLG/n6FgCAEAptX/35tVJ+UZTlD2jimvp5Tp5dmjo9arPekoL7Oddi59aaOGnOrE4OtLdbfKsevVuAgBQAIQA6CWdzvWL6LgZiVbLx+WsTOkgCJaGcvz1qCDPZZ08AvMAKqz1ypibUWrM8dvatl9cdQYSIYCLFx86durUuPRva8R/kBot6MfZ2XWVCoWxjsuz8RcAAJ/HxDe7rCtelYFoRwlhwB/I3TYOyrndEHspPDzcigBgXmx828dFBeuyJJJmWCBQl5IrzdxcZk4KC7tBoMISz3z8uP3TIt1anqGhvvbKpZsbN92AEDLZnoMBYP7DmE6PdYVrCeGDa9nZL1kf2WJT1TQMAEx/eK/3Q6NhmQZkDViegh8ijxrZOS4Y2LjeqXCErLY/8rkOonL09P3jEeW9dqwZOaUmzJDXaEHHajTNDYQfZxSEhyF+Adt9nlt5nVGa4bQmWTMp1Uz/UypXOXtYi8uGeLr1GBxU/7btm34zJcXjW23plHjCjTNKpfZOZmtphIzdOtDHbk2kT2ghBoCrGo37zvTUGYWUH+OMpA+aKDymD6ztluZpZzEj5KoDAPg5Ld/z5/zEqAJe+EiNZbdbOSgXfFS/4dWqGvwu7Wmtq3nF05M4GGGSOyj8TXptbwfHge83Cr32fN22nXpc98jJx+sNhcWtg/1dZ3+z4v2vaoIrUqMFDQBwMz+nbZmFW8xxfL6DvXpee3f3xKrXEQB88fRp6wd6w7JyInQIltkvi3IIW+0UiEptaTAALI9/0iWurHy5nsibCQwCd4Y718zBbeaY2v4PEEIUA8DimIedkg2WNcAz3lIJpCsRzWvo5DFnZJ2AJ7Z85kfHdcss160glAbUUjvOmRcRuh0hxNmexSIMCx486p8vWEfLZWjv4PAmP0ZWuc5gBOM3nuwbE5e+HgTG3KyO76drp/W+QGrIooAaL2gAgJsaTa0cs361wWptqkCSpe/UqbOnqogAAIqLix02pmVM1grcBDtGEt3A2e2zoYG+j6qmeaTRuB/PzYtK5YWPTSoHla+xPHpOs8AOTsip1JYmrizb5dt4zYwMgM84uVrqaNVnBavYRVPCGuy2PfNejs71oCZjRolgGesmYU52UnnN7lbXM7XqsyilMgCw2iZwAAAeppU4Lj5wYbY2RzfeXaH4/oOeDRa+2aX+M2Go/3ZEQVdyIzNTkWE1RxWbzFMIxUfDPdymd/LwyKOUShFCVoCKxtqckNAuQ2/4nCWcn7dKuWB8WPj2qtsOYAD4Ki66d6KFLKMCHxKiUo3/KDR0z/PLsDY/iX4j2ULnG1jcnApm6svK9zeQyxf2rVMnGaBiyG1jQkL33HLTYgRI6a/ECz6uF/HjcyGndo/SH7GNAxuXzj1yq+m1x6kbLAZrcKiH46ztU/ruwhgRSgE0Go3Ky8vL8Lc15j9IjRZ0bFqaJyuV8qE+PoW23w4kpL2RYizdYBQ4i7eTx8yiktxuMon02IyGTS/YTGFcerrXiVL9f8opHe/AoEsRTvIZ3f2Cn1mGda2gwPuWpjDKaLV8oJCzR+t7es5+w9X1mXDSm3l5HtcLCqK0HIxD9vYqP6vp80/qh00CqNhKDCEknNFo3O9pC6LsMRI+DQ+fZ3u5jqXkeey49nCtqx1OFspo5pPcwuVKwDF9QkImTRkUGVOZh/SjGUdGC7Q8YMfqETPETuG/nLhMTbgRc2OtgK+18vH51fr9kp3td76gYEUuT9/KM5ntTYJV569QrtjZwmcDQj5GgMq46aSsjiWmkuWAiIuTTLlwZJ06BxBCgi2WAwPAnsT0N3NNhiUSLLBeMvnMISEhP1WGkWKEEMEAsCs+qaeG8AtYjlP7qJVThwTWOUkuXWQXdLxMFqKFhEEIeEIkCCEOA8DcSzEdT6WnrEwtI83tKNW7Wo1WHzu7TVvG91vthZABAGDvL3FeR47cXlGcb+4f4Keas3vV8I3/UDP/rdRoQQMA3M3L6VZi4ZeYCX3q5CCZ187ZJxOgIupu4cPYsXet+gXJVHCnJiv4YsnPvdR+06c1qRVnM3axpaXO17SFUwWOG+2A0akAtfu8dj7OzwQ6XcrP90wtKprFEdJfJVN8G2Hnvraxl722qsG8nqxxf2otmWIEy1tqiWRvIzuX7Q09PQuq+siUUuU7529OuK8pnFZsAEepWQAflo9t5+k+ZfM7Hc7ahgqnbLnY5U5M+kaBNymaBnhO3DR74PEa0ies2YJOo2nyQBRovpyWG1ZAjOuMnMVfyUgXvB0c/Ku1XvM0uun1Av2aRxzfsZjnwIMTstsr1Qu+6dRiZ9VFsT+n5HQrshiWyjAjdWLpom61az+zxAojBAdSM3qWcdaZSiDgybJLuwQFna06PY0Rgn2ZSZ15g7mPt1y2p2utOg9s969ISAg7npK7OqHU3LvMyoGrmSP1VNLdn0W2nNMvzC0XACCWUrtFK49MycoqnOKgUJ56r1v4jF5NfAq3H7lRf8aHfW/9rY37D1GjBR2n1XYQBEEd7hl/Kgs6Sq4lx8/PN3PjMbD7u/h5zw6vDOF8WFLiuDombtZ1feHEDFBIvHRIaK6kq46+1W12VQuaqNO5PSkqiRIE6zv2DPu9u739JjuEcNWJm0fl5e4pBXmTBII6ShnZFUx4RycVu7Odp9+vgqvcKYnY8l4Vk1h7f0bG6SSODxbMCHx5a04bZ+WC3W902WPzqVecuBFx9n76eoOObxzoop733Yy+Xy7aer3l9TvxK5WMNe3YN+NH1AQjXaMF/SS7oEspNU+3AJctk8tWtXXzid+WkNw/21i62QxI46O0m/Rp3bpXKFTM1g27c3PAjaKS1ekmeVBtoz4x7v23ImyCqsovGTndrZx1tsAiBSECsmflu10V0t1hbm7lABVuwenMnB56EMZTCu3khMtxwMKUtgEhZ3+vnJPuJbbck5N+kyM81EP4zBvuXlHzWzeMqfTF2Q92nR3xNFO7VE5RZkv/kP8sH9XsyZDF+yckJBmnmkuQs68z7D+/Z+zQmiDoGh0+SjCXSzAuNgrSQZpSy6nTycmdR9cNPlLP3rEP5lHBk+Kyn6Lu3VtMKVUKALCreasfP/P36tMMrCeNiNbqe/jkIkqp6vl825eXXPaTsZ/KGclRVirTWUF4o8xiGR6bmR9MKWUEOh93u3X9fLCUTnKmsFzJSI8hhH93m69diTG1Y8qy5jmwgrGdXLliR6fw9+e1bhiDAODkg8R6PbYe33tfU7jJ1d7+x4WDuvddPab53X7T93/1MNmyrMREnFUyi9HPS367ppiuGlLN6rmXl9dSaxGWlzHQkbUao94JqrMGoGLiYs79+5NSzabZiEquNXHwmDS1QWB85TX5gBPnP87I182zo7IHXQN9PpvXpfETW55VV6xE5+UFGSkNAwATNaInrWp75j9fhqrpbTAIQdTdh2/G6Ao3lPOU1nW0+3R781anCFR8LT45cbPX7fScTZzVLA338560b1CXwwKhIJMyEDlu1/WsUqa1v7Q8vlWoW9SqKf1PPJ//v5UaL2gAgFsaTWCWwbDKxHENFDLlnLcD/X/tFC6OedjxfpFuQxHPuwerlVE7mrXcjxCiCAA+u3yt1d2kgg18uVArzEs9Zde73fb9FcLRaDSqtenZs5M5/jOW0uPdg/ymfehXsSVCMaUOI0+cn5apKZqoxopLfcNqT5zSOtw2GaN8d/mPUzKyC6Kc7O2OD+nUaMHwnhXXagqioCuhlCoPxSdOyxW4CQhJ9rdwUM23rbD+Ni/F40B81tJsfflIR7lqx3s+tReMCQvIBQC4Wkqdlh46t0BTXDjWUyn7dmhE07nDOjy79vCP8G2Spv6TwrwNWkEfYadSzFnXqOl22yjIovvRTc+kFmwoMZnCQx0kyw736b4ZVY47rzh3L+Ls7aR1pjJro7ru9gt3Tu2/xbapOqVUUTV6799MjRZ0WlqaHKAWBAYis+23HSkpb+WVlX1hJUjrpFZ9OiEk5BZAhVsw7OqNkTHFxasZijUtnV3/81WHFlcoVHRERhy83D8+MfdzhgrlDQO8Jn01ouu5PzL2ixGCrU+fDs7QG5ZbBfw0xMV++pjg4NjKZ7PDr98Z8yi/cBlLIaONu/cnX7ZvfJ1UXMPD9l4ekZievUItCCmtwupMWPJum7uVHUbm4/kHh1o5S+2dK4bPqwkzhTW6U2iRutgVMln9b2qyWth++6B27Z8i1OquHKZZj3TaEzPu3ZlKKZUhhOi+9m12DgwM7iTFpPhqluZk/x9/mUkplZ65Ex20450OP43r0KCdksEJ92KTf3x7yYE5lFLFq5TjXnGxw5bE2OVlFtNSZwm7ZWXzRn2wSac4+/Sp9950rVfXazf33NKVfOFsLz84p03dHl9UivlYvCawx9cnt8fmZH/p4aLaP39gp96LK8V88kqu28Apu7+IS0r/0mzmyqAGiBmghltoAID7ublNS6zcZCsHqQ520k1tvLxsawilcx4/+CRDVz6PIPZaExfnyVPr1UsEACikVD36x/NTkkvLo5wZesaJKGUWo9k8MDLos0/aNskeuOK7CZnZRfOUjPRux0b1J88e1rLa4yXOZaeEaA2W+SYQnKUS6YJRQXVvL3kU/UGMSb/EWaE8mFic36mcl7oFqOymHGrX4jueEGAA4ONz13vfSdNsYPRWpoGny+TtQ3se4UnFsqzpW892uBmTsc5kEjwiajlFfTNn0MGqkzz/Zmq8oAEArmZo6hdwhmUGjvdQYNmiQXUDT9oi4Rc+edLuYX7hV6VUcKplp4ra16rVtzwhgABg/KnbPR5mZK1PNbNhViMPwcAlNPXzmPLN8M4npu451+zOvZSNnJH4hfj5zNi9sP8+Xnh248XLKZomBsb4oRUJSe1UzluSTBLJ5ZKsZUkm6+h0hmGlJgOoqeXnSHevqdPDwhIAKhbQfvrT2WkZheWTnCg+Pzw4aMKHHRqlVeapeHftoUkpWSXT1AxzbUizelFjh7SqMVsYAIiC/jVIKJEWqu8kFi4qspqHS4hkZyt/78WNnSrimA9rNO47Ep4uzTGZh7syql0f1gmdPyjQIw8A4HBcuteXN2MWxRXoR1kMiHHlOXO4s/0Xh6e2WADgSQZM2buwIK90rIu9+sD77zeYN6h9kwJKKX6cVVyvhFojEeKedPT3v3s0NbVFvN60NgtQmwLCA2vQlXqzssWrm0dutoWnLrn/NPLnjKwNxnJdeH2Vw5JvB3bdbNtabMWJexFn7yauMegMzX1cHJYfnvXOugMnzwe9+0bXZABgf28C6N9IjRZ0skbjXkZZPxNv6qIC2N/Y3z9nZ2L0+1kGsl6PaWqA1G7yJ2F1blCoOLZt8C/XRsSUlqylAuR1cgkY90W78GuVHTM04ruz799LK1xRWop9GI4HP3t0sWcd18mLR/V6PHr+8T5xcZkrpcRc0qxhwAfLZg3MfFpQ4Esoza3v7m48nJb2fqbFsjgf44ByjgcJb7geIWFmjanf9ApAZafwys0x0YVlyzDl0ju6eI/f0CnyVuWz2Q/2XhmRkKxZBsDlNa1T66ONQ9veGzT32yn6Ut07tV1cdpjNFsftK4ctqwludM3uFFrBjeO5t3UC+SzRaj1xLDl5yKiQBvsDWaY3EcDyuLTkzNQ795ZQSpU8IfBtu9a7+/u6dpUhoeBiRsLpgYcuz6OUyhFCdM97PfaNiajbp54DnGYogYx8a+cTN9PPTlh1qP/WeW8dH/BWqz4quSrDVGxoAQAWS06ONtzDQ38uJeXDYp4s4hAbYGcy6QOJdcNwH49BNjEfy8wM7nH56vcPSss/d5NKvzvRPbLHuo5NbyMAOBqbWK/XV4f3P87M3OxsLzu2ZUS/7k3c+NJuM/Yef5hpXhGvxU3vJuav5C0WK6ohpquGVPP3oZSiGE1B+3yLeWUBpi3KLVYDS+nWNnaq5Q7e3qaN9x/PTDXpoxBFFzp5+cyJ1eZ3C3FW7/0kNLSo909no1KK9DNdET43sHbtyZPbNUgFqNhIZuqam1PiUsumlRmlqjB3svHE6mETKp8nP3LkjmrAgBZFtpUwP6albcgl/EhsERI9AC14p17dExWzgQgWRD/ueqswf2Mxx6oClPYTj3VqcWTwj5c/8pCydnopjr0Tl/cltVrk9V3tpu0a1uv7cZtPD7iXlr8yT8fUYo0I3KXmtHoh7lH7Zvc9LNSQ+NGaLmiMECIPNZr66Xrj6nyMexUjAFRe+ksnhapPq5AQ3bzY2J73tNpNhQics0xmR3uCn3ZROU3d2qnF6REXrrd/lJ6+mZioupGT+9R9Q3v8wFMKEgbB1G+udLv4OG0lX673j/TzmrplQb89tgkSSimCpCTpFXvnhmXGsikcpSleUunm1v7+OQAAOZQq192/PTWl3DqNQfjUW0FuE8MZO8u06IRVcYXGkQosFKv0eqUzOFzpGlx7wrwuYQljtx5990ZSyZ5io0Rib7FCkIP8cN+WvvM6ertl/RST2mD6x72v1wRJ12iXIzMzM/DgwYNMYy+vJ41Y5/fUnLCGmC2WYgG10zCmAAoAC8PDTw8NCensSthzVoxwMpHUP5Ff9EPv4xfmbO/c+uaGrr3bO0mVZx9ma3d1/uLHDUfSShwFQmHFB+3OzXq3Ti8/B8WRR/GaL3qP373l2LEUj8pHowd2dkGCYA1zYtlNA2rXnmMT86Gs5Dpr7t7fX2Ain9RSKKcf6tBm0OM8S/AH0XEXrluFUQUyijgrkYU6eS/75cPeb8/rUjH6USTwfkUsI3GU0bLIOurpp9YOGfrxoPZxm07f6/EwNm9MTTFdNaSav09KQUEzTBRZgR52eQAVjbErKX5wmsm83iKQpLpqt09H1vaLBqiYdRty7dq42yWm+VlWcHMwmaGuBJ/q6+s+aU77lgnv7jw97Gm2dqXCKs3sGFo3atl7Da8KtMIaf7jw8NC4uIyFKp7Na97Ib/Tiuf0znhYU+BI3t9zwyu1uEQBsTYrvm6HTLbMKWOutcp4xsV7goxE3r0+5U26ekUgYeylnhFCLcKebk/fUNV0jr1Z0VhGM3P3L249SslbLgRa2CQ6csmpomyu2ZV7vTtqzUF9uDjm146PBNcHrqNEWWqAsn8+Xz7uSm9kToGLXoRF1Qr+v5+jcg1KGv1GguTj1cexY24LVA+3abX7bx/ONBix3g8cUHhskvY49Sf82PStLuXdE972D6wd3lWG+7PSDuz8PWHlicqWfTL9Z8PbePh0b9VLIqLaorKglAJgcOC7bJubY/Hy7rxPjZxQbzSscJcqj45o17TepftDtWbdutY82c0uzJIy9O28U2sikW9a3btp7daWYr+Tq3Hp9+dPnjzNzd7rYK8/O6tP8jZWVYj4Xl+3Sb8ruzTm5pZMd7BSPasK0N0ANt9CUUnw3L29QmcU0xQLkipNMtbLKTKFyxsP7s1JNpokyIv+5pbPP9E/qe2cAANzLyXGddzsu6l6JeYLUZBWG1g3suKLyJFhKMxX9116ZlpdlmeqKZOc6tw2ZOvnt5qkAFYfU34uLsxs6oENeVlam3N/f33QhNzVAq+OnlAtckEKi2Dg8JOgshYrNGsfcevjpVatho8xkSW+iYuftatdxL0cIYACYdOF++2tJmRt5k9m1nrPjzAMf9N7LCRUTPlE7Tre+cS9nE9ET/3o+TjO+WTbwv/YZ+bdSowVt41ZaVstMYtxs5HlQMbJpg4KDf92yYO6jez0el1g2lQsCG6iWTNzdvNVxASpXsJy5/NbDdO0aMCG7hi6uU78b2eU7TiDAYgxRX5/ucvNR1jqzldo3DnKe+s3sgT/yQkWulFKUnp4uK8Xy2tnEOMJCoNiNYXZ3qDwhQKOhqtVZd2ckG00TZYAvdHP3nvZhvdqJlfcq3jlydmJigX6WmqKbHUO9JizpWDEbSCmVDVl1+JPMdM08mUR9/83IJpOihkc8/tfv/1WFGi1oSikbX5hTO8zNN+F6ebl7Wm7WilIrNxCIdHNHT+dl4R4eegCAnWmxngczteuzjeUDPLFy05L6YcttoaXb7t8P2Hc3e01BiaGfvx3z9eQuPef1qOdQRAFg/80Uj+++v7G4SFv6joeL6pvPPui0rFPjwFJKKb5fmBvCmWgjQiCzdYDPLdsIyOmctNDzudpVeRa+raNUsnxTs2abEKqIBlxx/37Yz+l5a8p01o615PIVx9/tudp2bdm52yGXbqStLi0xdfV1Uq/+cd6A5ZPXfduS51DjjdOHbBJjOWoACYWFYcVm61Ij4bL8WMmSut7eBbufJnyYbjatslBrdG2F/X+U1Cqxmhjd6MiI5D6Xr46LKylbISU0qZO718cb2ja1HdUmHbLj9NiE7ILlEsBJHYK9J68f1uUXnlCglDKjF/7wbsJTzXwlkWc2b+b30ZKoZtpYDefLKyyaxk4VZyFSSvGOxJS+KeWlK0wCr/VTOs6YEhF63da5G3Xt2rD7BbqVWICiVk4e477q0vTWp0cvfNCztt+5Y/czGz/M0nwu5Yi5iZfPx5s+7vrL8Dnfj3uSql8kAyo0qqVatWX5e6tqghtdszuFPO9IANxNlP0s2sidO52Y8tbwsLpf+0rRW4KAmOslJWePl1n2/FBScv7jG/fePdqh7Zae7t7dEaVwPi373IAfLkytPA5CODi61+Y+EXXeIJjy5x6mnnx32ffzKaVqAMB7l7y7v2+v5m/LWWIuzte2B3A1MaWl2lLHWnpKKZtcXu6+Kz5+SYHJtNIJq35+2yVg4OSI0OsIAG4UFvr0vnBp5+3ism32Mub0qrZNOnVQMVltd//0w4mMgs3LbiTtuZOdu8dJLr366RsNuy3oGnCn97Sd393OMG4stkoddSaDk6Fcz0INmSqsGbWsBkopjsnN75Npta7VqWVBvLbgwvCw8K4AAE8LCuz3ZGTMfmA2Tc5ArITRc1YfmWTzhvrB80NdXUnPQyfnZJUbP3NE7MkPQkKmjmlTsSnivWLqsGTLwbkZecWfOUgkZ95u0XjSJ4OaJgMAxMbG2kWnlKuG9GmlTU+/JAsM7GT+RaMJzNAZpxkoH6iU4vUjg+qcoQDAIgSLo6M7XtbmrS+38l5+KnXU8U7t9w7++fKA29qylTkmPhgsBLx4UtDYlZ3x3fC+uxBCZNG+cxHfXk56UGZVsv7ImBMR4DH9m4UDvretXvm3U6MFbeNqVlbLHN7wud7CBztL1QMHBPn/AlDx+Zrx6P5bD0qMq58goW6pFUMtjtzoosDTNnVuf/39E+d7xWeWb+IsAlPP22nCgcFdjwuUggQDjPr8eL+YhPy1YOEl9YO9Ju+aPeCQLXyUUkDp6VSWy+QFFwn6MVYOlQTZ1f6yqTcqsJ02O+POnUlJevMsIwu3unt6jpsUEqLtdeLcwkellk8KBYnUyWSFIIwu9AwKmLywawPbWDn79uqjE5+kFKx2kytP92vgOmPK6J6P/7GG/QcQBV1JdEqeR5y1ZGmhle+PgV37cYPQtbawzZ1Pn9Y6mJ+57I6JDCnjWPCwlJc2kasXHn+zy6avr6X6HHgau0pbou/vKXfaNDQyaFtCXFLX5WPe/Hr3hUS3Qz9dWpOnFfp6OrpuHT6s/uJBrcOLKaVMdH5+PZ2Fb8KDJaVzQO1rh9KTmiALNJWpFL9cyM1fUWDlOjsCWr2xTfO1U2/db3imrGBDigVaWM0M+Br1+iYq2bo1XVv9elbh7qsp/t9fur2quNjU09dZsf6HuUNWo+c2cK8JiIKuAqWU2Z2YODpDp1vCI3QzQOU8bUxYUELlNcmgGxfG3yrSz8vmZc7ORg5aS5kVPw3qPZNSyg7dfvbDJ7naxQywxcYSU4CPXHWmX+PgSZPfb5783qTvPopPyZ9tj/nUdhHBY+fObaONyTcECCY+s0lgYOnJpNQ+iRbLolIQ5EbORDizYPCWOc+a2iTk3OG4dK9l6Yk3Y0ASIDFR8EXG2K6O9lO/6tzhDAEAFgGM23+x951kzQbgBSHS233ClnE9T9ekobqq1OhO4fMghISRdet+Hexk14sD7HyvtOD8jPt3hrEIAUKIO9Sm64YhXj69Iii9yWEpZBn41pV7avD7x/T4cnCDul0VQHMNgCRJxYY3d11+eG7YkkOD968dtPWN1qG9ZSAR8stLOwA4lUd4+D5xl9ayHk9L+ziX8IsNgIMIx3k7YuZCD7eA3lObhJwDAChUSBzyJchVTThoIeF3zKzfoOfmSjFnZlLnLl8fW30tNeeQnUJ5a1CXxl2/rMFiBhAtdLUkFlL11tTb83PNxg8xyL7vHVJ79nueFZvEnMsuc1lz587MrKKyDz2x5IcxzcJnvdegdj4AwK3EQvXKIxdmJGWUTCoxyOR2xGwNd1F+/cXI7jPulxdIc9OzVR8OeyM7OiPDqRTJemp403tFPBdBeCHfVSZdNTgo6AhCiFBK0fqYmKZnivPXFlj5UD87+9lHW7XZgRAiCAAmn7vT7FpKzhdceXmdYBe3md+P6rmtpow1vwhR0C8AAcDs+/cHPC4rW2fgeVNdO8dPt7Zuft62e9GwYxcGxOYUrCW8xBTp5fvpN++0uEABgGUQfLbpZJ8rT4qWFxVZ6jlwBujWxLPj6tmDfrHl/Tg1tW6RVNq7iOM7ABFSPVnVpnYBFcdOUEqZ6Q/v/CetlJtrxubY1i4eE2dGRDyuvCYddOz8uBRN6XwVgcR2QYH/WdYr8sHvlb8mIgr6FViXEB10Ole7LtfAdfeQKJd/2yh0vUflLOLWe7H+++4kr9eXmnoEKFSrNg96a42fDzJSANhz8pbvwXNJy1Kzy4cGusHGb+Z+PNvLCxkopfhxTk7DMgFaUBaldPD2vmyLtTiZleV7JTdzaSbP95MzinXbWzRbZdskZl1CRtCR2Pi1ReXGngEsu2lZ/fBljRtXTMyIVCAK+hWhlEp6Xr0+KbVEN18lwK0uHt4T1rVpFIsRAinLQL8vjn2SnFeyBDPs/W51Q6cuH9z4oVAxU8iOmvv9yNT47EUKxu5hZKTv+CVTe5fE5OfXkhOlJsRbXVCZP9qTmNglWadbrRcAfJSqaVMiwi5DRRCg8NG1B/2vF2jXY46nDdTO//muV5sTNdlXrg5R0H8ADAAjr1zvcltbso6YLT5N7T2m+gjUodSoM24f2vubz374pfXNuJy1RGeqG+rpuGDX1AFbAUCQsJifvepy8we3Hi/z8VMc+GrtmD33ExLUqdHRJS1btpQKgszhul47Po+zDrNi5kx37+CFj4qy1I8K89dEOPvsOVKQ0z6jTPexI5Uee8vPd/qspjVrv7o/gijoP8GeR8nuO1OT5meXmEbwHLWScs6utkq16cLHb84DAPr20r2LsjTGT5wU6kPvdG88bXS30CIArQSAJ7t/eOo0clDXnJycHKWPj4/xUmGhb25x6Vw9b2kileEVY2qHHV4fHd37WrlxXTYlISxv0ZrMFomLUjb/VLuOX4odvxcjCvpPwiIEQ45dGPwgp2hVlknqLzFxUJsx32zn7z1pw/udb3+08dKbsU/jN1o5wVzH0+fHwuyiNiHBLvM+n93/aloalVvkeV7FiLMrMFomGoAxeymcVnf0dNQujXk8O81AJmUyWGG0mEBFydVIlf3kZU0b3Pun6/y/gCjo/yOfX35S58fEpFVJxeZ+ghGBC88VNXGTL9s3ceCGnUfveh/8JXqlJsc82FDGYGeJobRlA+dBG5aNunxHo2loAKEJsgq5HfX6s6eVTOATPbcxDXD3AkJB0Jdb3Fh2zcjgoFUtXSuOTxZ5OaKg/wIopdL3tp/95FFu2exCPXJ2s+igpa9y+I6oIXsppXjsnMOjnsTlLTLpqHf9UMexB7YM33YvObWWiWF0rf39iwEAtiY83pvN2A8tNnGALWXRPlI8a2aDyBM1IeTzr0ScKfwLQAhZD4zpsa5fPc8+AWpy28DYQ74emkkYDAghsm3p29vf7Nqgl587XFJIKRUECo1q1cq0iZlSKrMSHCCzmokvIdvfcvPoNUMU859CtNB/Mcfjc1y3/3h9QV5u2WhXlf2uj3o2mtunU2ghAMClhw8dMx4XqUaO7JpjS38js9An21y2XGc1t5VJ0MKhIWF7asrxEa8DUdCvAUopGrPu5JAnKdqVCmLUtgzx/WzF5L7PbPRCKUW3NZqwYqNpmVmgvINcNb9LgNeTajMVeSVEQb9G1u65FHzhTsp6XYm1jb+L3eL9G4Z9UTEjSNGTXI1/IUf7E0oKa1H+UGBgoPnlOYq8DFHQrxlKqWx41Lf/SU3XznSQ0Atdm4VNmjSpZ350UZG32Ww22Rbbivw1sP90Af7tIIQsCMG6acsO3Yt7kLoqJSu/J0JoJ6U017bSW0Tkf5LDhx+5f7XzUq1/uhwiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIn+Ov2Xqm8EIeIEwUBGuykslLLVyPMII/aGTEjACwBgDVJ7EbttA/EUgAGAYDKjyLo4XsJRlCCAAKyegivJhSl6hJAwCQAgBwggEgcAfObMEAQCh9Nf2ljCY8q+QActg4PiKckolDAVakRnH/7FJRoQq8kIIASUUOOHl99OK8jISFvMcT/5LKyyDaXXHxSEAYFkMVk7AAIAkLPPr0jHbRqiCQOFV2v2P8NoFnZlJFePXfP15iZ4GIArAYyAMIYgwEuzn6nDq8KpBn79C2wICgHem7vw0R2fuQYhA7DAlLRoGzlzynzdfeJb1pJX7OzxKKp1u5iQUMABFiGEoERAgEICCREKZ+r72W76a9/7RF+Xz5f5op8NXr6+1WIgLIGAd7NgnP2/4cOarrPFDAPD2rB0f5BRYB7FWKwhYgRzUKObE56NnvuioCEqptPcnX3yuM7G1gDKURxgBNgFDJdhdrT59fMP7n7/K+YMIAPpP2/GJttjSEwkCkUgQCa/jOWdj1MDYF90Xte5E5P0naUsthOUxkSKKeEAUgACmgAl2daBxR9d/OO332mD112cCz9xLX1vOEQUDGFEAAVGEKIMACQCYQdjPnT11YPnIDX+lpF97LIfZnCTR6Jhu+UYIZAkBnkEgERBYGYAyQ37nD+bsK9q2aOjel1WKUCpr/8G24RlGWSRQCirEg2uu8QwAvFDQBTqrb65e1ssoSABAAIQAKr4LLAgUgUSKwUXPnH5ZPR5lJkZkl8IoC68EigQos1harNt9YQMA5Lzs3tHzv3vzVmLRpjJeocTAAqESUBhN3QdM3KZnMFrwAlHinDLSqcwqDwVCgAALAuYBURmUGEq6DpnxTem+ZWN2vez5hFJpi9Fbh+fp5c0wIcBKKLgUmy8BwAsFXaC3umeXS7sbEQZEAAgmwBAGBIQBAwYeBLfq7i00U3V2KbxVDlKWpQACEMDAgoAIMBQBg1iQyanmZWX/o7z2FSuC4EQxQmaKABhEwIFawR4EkFMOdLyCvZNq2PDpmiNdXpbPqi3n/A1WqI0ID4gAWAmCglJdS/ySb4xKRjglowMlowM5NgImZgDKgxQZwY7Vgz3SgxxbXnqwe36BvjlPWRCAAKU8WHhwepKmq/+y+6JWnmryOKloi8EqU0oRB3IsgAybwSLwkKQxzxoctXckesFm5BixZkJ5QMgI9lgPjogHOXBgEBgmLr183SeLD3Z+WRmWb7vsb7KQYEoEEIACL1AoLjW2wC/ZBJ1BmCBKgAoEpIgDO2QFO8yDGgiogYA9spjB5v89hwSZiB1rtNozOlAhA0ioFYAKIAEzKBkd2LE6sMec5a9eyfDaLXQZU4Iq3T7wclZeivBzXE8JQzO0ee/Ga+n7RVap09PkrLmU0l9etCl3fEFpQyOHnVhqBRZRMAGGMiPfSMilKuSFDNXdF+HncYVieR8eENFZFPUfJWiWC4jBdQMc1vo5yy9ZTGZJoJ/DwxfVgcEIio20NU8xSLAAlArAgQzn6czNAeBs9fcBxKRkTi/gFT6YoeDjAj9H1HLeml5gap+QiaaUErkkKTd//q6zZ38a0a1bNWGkFCHEgJeD6kpjP/vVAiuF9BztO8laMryIc3CKy9Da2q5a1+dpdkkDk4CdGMQDgwE4wkCZGTW6oiX2bd1QeXX3EcQiCgAKhoMmtd0WOcuFu5QDBoAFSgVkr3TQYPz7EYO1/NzSm5db3jFyVgZRteudRM0aIyc4B3qoDwd6KXYInFkS4GiXdLS6h/9J/pbwUYQAsUBBLbGmfzWnz08AAA9LSq6Nm3o0XKMXGpp5iQpe8LVAAJBfam5jAQx2Uijz93SMjcksbWMwk+AZR88EA0C1m3p/MurNPAD4CQBg4rpL+dE4l1LA4KJibn41Y+CJVyn/dydjnJcfuNmYUAyBrtJHOjNxKjDggJIyo2330d81NAghMBFsb8UATjIubXiPiI/G9GubSyk91eajXeHppagXJ0gUZp1UWt2zaUXzgYLBmZvnvfMzAEBiYuGV95cfDdcYJU0sAmtru98VNAKAolJDC45KQSkxlwV6qO/HZuk7Gyw48MdvTwUDQLUvM6YVPTYWA7ipZdc2z+h77lXaCwBgTL+25QBwEgBg/8/RTg+TNUsYBKBmacL2WW+ffNV8/ih/2yJZSiUg8BKJ7YGRLk6lChZnYmCAx/IXdqwIpZJyvRApgAD2EiYxxN9liwIRyhGJMkeja/KqZeB5o4ylFd8LQqjsVe+7+uhpqMXM+TAYgZs9PaRWsjcwomA18w22fXfL/UX3UpASlgLIAWk+frt9LkDFtr0eCi7RhTWCA6KCVJC/9MtLgTA29yq0rqtOKoFUBgTAlBWgms8+AAChlCnXWZtRSkEhY1JDvGVbWUyIIGB5fm5R41epvwAsmKD6l+5l5JeUyBFQzCMGBIQlfzafV+G1C9oZnAEoQgQLIDDk1+4PQhgEyjOUMiC8xJfbtPeKr97I1aWYglLFRreqH3hFIcHFHGWgoNT4Uj/6VzgADASAIrAI0lce98orMjTjKZZgRKiLg90VlVx5nwUeTBz1up2S+0I/GgECliBgKY+tnMDYfm8c7Li9UR157wYhju+p6qmKq7sfAwBFCHjEPCNbigUGIa56JVeycd9tL4OFD2MQBZVCHtO/ef2rMomkkCMISvSWDvgFjUcqdu4FBARYTP/0wZ1SGaGAgBLEAgH2tS5q+HtWrKAqA7BVf0YMZYAH5iX/yuPM4nADT12lFIGrk/z2O12DsjYdpEnFpdilTC80z8qmSh+flx+/wAEPfOVIJUtfbQAUI4ACPWlpplJwYIX8zk1bPLl0+wGbBqWCCcuZwhJrcwC4WN39AraAgCXAIdkzz5v36aAYAIgBANg0v/rnV57KAgj/Zgy+2Hc16Ouz8Q15gkCgwgtf54cZmvoGgbpLKAEvFXu7a+dwTYthOxIzrYJ7kYk2jY6OsQsPD9f/bt0ppgghIBTAYrHWmfPFsRwDJViOMXJSMtppFe7cS+F5gQIgYEAAIK/3QNvXLuhiKAYARAEooOe68xQB+nWmoBoQAGiLi5vzVIIU2GwO9nC+gxCivSbtuIl0XEuDma+9/cTpQAB46YpphhF+LQF90dBCFeITEtXvLz3bECE5qOU0enBP/+JTp2Mf30nKz9ZbaUCJTt/qRX50hX2lwNI/fghVVlbFKCNQAQwmIbzv5P0TOJZB+y/EDig34CAZSMFBwmngBf5zgbaotRUQVjDU4ufhepsTCNjb45vYyLc1WsyBBy4m1IZq+iAEIQRAwSwA3IrNWXsXqABUShHDMSE+ks0IYOqrWAXWwiDbp4Si/56g+St57S4Hq2MQpQRVGsRf/UCOFzCiwAAAUEIwVKNqQimrM/CtCBFAKqFlVKbwmPPFsfoqO6WeRQKYBcY+Kbvo1fxoBmMglc/BwLwkNQAAbD0WU9dopUFACchV8vx5G87Xi9Fq60gV0nwKFMot1ogj5+84/969CBAgChgqjraqto7VIZHkYUCACAUo0kHD2Kzyz+PTy9ZnlTPtOITAQWVObt3ce051LxOhlCkz8a0EwMBKoRgrkN3MjadDFWq5jkE8WAVWmZ2nb1rd8xnMMxW1IGARGJmBlypNgkxlIPZys4lRvGo9qMBhoFDpvrxezb12C61SqQkgTBCiQCj5dQ5BwjKk5ZidfMWbi3iwfV2fY9/p+256sxAqUCmUmYjboctxRyVEIDyRYo5IAbEEiku4xgjgpZMzVKA8VNoKJLyayczUlkVYqFRGBClk5pkH/5CfNACDgCyCVIKAAaOV+Fy4nRkIAP817EaBAkEgUARAAFF4Qeft9/D09BQAQKjwYjEAokDRb+8kQiynZL2q3fdu9w83PQ1mEkqoBHQG6nHil8QTFCPCA8NyvAwoQ6BAb25kCwt4Hp7DHAAFTAEclDhXKuV0iHCYsHJQ20tTXrUyAsUCIKAVRu31npf4t4xDI/hdF/pXEKreciVrS+w5wtgBcEDAjPWCTIGpHCSEA4wEICAFTpC6YQTwCqEdfxgjYZwIEABsAU6gUqMEpFiQAEs5QJgHQlmp3gIOL83ouRp+dfC8T1Jmqb3CHnNLPuyfXt04MqKAACg42XPxPo7SUwTLka64vG1OuTSyWM+GnbsZs5pS+t7vrSAvsPAOPGHtgXJAgccmQaqyYAEkAgCDzEBABkZB4oQQwO/1KBhMEKUI5AyBVmGen/Xp5H4OoKKjX+wMlu9XvFITAqiqVuj1Hmn7N3QKnQEqQ4MQ/PZppJQCxjZ7XX0dGZZSCogiyoKDnC2UyHEBEEwRZXCxyRokEJBSJP2DYUII4NU8DkCIpYA4wEgg7nbyNEFitWBBgjge25WaTX4EZPCiZkS2uiOBQJWv0KkbiZ+mabnxjlIud5vnrQ4AkF9dHhhjcFIo7p1eP2oyAYBt+88FbTqbfKbQLATreFq7sjK/+4WjgAEhDuxk0kI1I9FaJDywvBSXmrhAK6UyiiQvaLuKNqIYAy8I+jdatvw/7IL694wQ/w2CLgYKBBBhAaHf4uN4gSg6jv3Kg4IcgFY/diSzACCgiMEUwnxdvv5oaKflAABgALupW36+WGiAMIpeJW4NgIdKD4e+euNiUvEqyllU3r9lnYEt24WkAADsOHK794243AOYFwCg+q+olJMApQQ4KnG5fz9VDQBlLAYoNUtqlwoKe4lZ70R0kmoLRAAAEwRYoKzNZxn7frfUNmO3PSqxQjCPLDy8wJVhgQOMZVDL22HL1F7tVwIUgIODv2LMxu/OF5qhAUNfNIomAEU8AJUAJa9oAX4HA6iAIABMKQB9Hd/R3/hbhu0wEIQJgEBY95mbzzcgmEd9onaN0OhQU4IoyPGL/xQEQoVfggXSOdxDTwEgh1ICW3mKgQFMra82BIcFhIEHBnEAzKtthI8ojzClwIJAGWu5vlN4xWFBI+d+Z2YoBQw8MNUImlIALLFwGFgwmHDdaTsvrp66+coX6dnZHeJSSt9CRAqMnHBOLsZq3whcOQhE8G9JEAYAJDBAWZvKftcgSAEAAUEspcASs7VTp4qyU0oFFvEIUQaY3zfslfCAgAcAKQj/B6W4gwFYyoOApUDQi93P/yuvXdAVEysMFkCA9CJjT82VuM6AMJgpozBTGTjLTOa6AS5f4GrjOKRAgAUCEhCq+F9ZSUksIAkmf2CjTgkoAFEpEMT8/jjX78IAAQEoMGBgfvuSIFaKKaqIHqsOgVCoE+iwuTC2oFOxFTtkatFYTfGT93meKCwUkIophwBv+83v9GpXWF0eBDGIQxLg0G/KQwAgIIwISIHAi4fBCEiAggSA4l8trFYLDACLKDBA6Av8PZ4FCgxQYAC/LJLpBVgsZiSAFHgkhcrX8bXxtzg2AhVYBACcoGTKqVxRLrAKwkvBCXM0PMBx9tdz3j1QnSwFhkMUeAkLAAJHqrgsAq2YPgOgRHilzyHPESwgzBBMAIH1lepOQcCAKXBUYAxG46/FtPIVrggFDMIL7MJXM989H+HnMkGJMS8QBegEidJK5EiOZRDortzyw8pRK1+0fS6hPIuRALhigURlmQCAIwwCCpRWbzsJkVBCeQnBBHjhN8tISB7lCcWVXZrq3R0soIrxTQqY/PnxY6uVQZQKUow4wIT7067Lq/DaLbTRyAlu9iROhsyEB7lAEaUIBJASIvFytjt6YMl7G75f+n6196swa/S0I/c5ptzdSemcbfvdX6Xifez4J3LWRF0c1ZmvMu/nas/qPO1IDI+sEme5uuRVyu+khDxvhSFRwkKhSia32H53UNIiHzvTE0oA2ctotRFrAAD7V72/u+/kHf6aYm4EQQJPBcw4q5hHqz7qHfWS/e2IlyONszeVYy+VPNVWRUoBvOxICqZlyY72TDxU467JpWaTp5o8Ult1zk5q50zb756enryHmjyRmwwSV6Uyvbq2c1KhMm+19SlDCO8sVVc7Pf8yXNycrR72WTF2nNHLXWmf8WfzeRX+liVYjzQaVXlBgdQBHMBqtSfgBMDoylCjRrV0L9uwkFKKcgEUuvhCxmBwNUdG/rbCg1KqKCwEVq8HLjAQvXQ7Wkopji8sVLkCQKyrq6nTC8JVq9wjKSwEOe8KxBPAaLOmByllOgAoigsLUairq/FlK1cYjOBeSqqjmhCqwxg1qlXLhBCyvOgeAIBMShWGwkKWKXG1hoT8lj4tjcqLSKrMPSjI6l95MOfv1RcA5FqtFru7u5urhudmUqowJxVJciTl1k7VbOVLKWVuJxWpAuq4CJ4Apj+7uaTtP2QrymF50SodERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERGR/9/5f9VJY75NPUcbAAAAAElFTkSuQmCC'

        ttk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="關於我們", font=('微軟正黑體', 13, "underline"))
        label.place(x=10, y=10)

        image_data_base64_encoded_string = Logo_image
        logo_image = tk.PhotoImage(data=image_data_base64_encoded_string)
        img_label = tk.Label(self, image = logo_image)
        img_label.place(x=270,y=100)
        img_label.image = logo_image

        label = ttk.Label(self, text="本軟體已開源，請至https://github.com/NYCU-DataCraft/AutoFill", font=('微軟正黑體', 11))
        label.place(x=10,y=40)
        label = ttk.Label(self, text="開發團隊：Datacraft", font=('微軟正黑體', 11))
        label.place(x=10,y=70)
        label = ttk.Label(self, text="信箱：realdatacraft@gmail.com", font=('微軟正黑體', 11))
        label.place(x=10,y=160)
        label = ttk.Label(self, text="IG：real_datacraft", font=('微軟正黑體', 11))
        label.place(x=10,y=130)
        label = ttk.Label(self, text="開發人員名單：Tu32、Muennl", font=('微軟正黑體', 11))
        label.place(x=10,y=100)

        # Button to navigate back to StartPage
        button = ttk.Button(self, text="回到主頁", command=lambda: controller.show_frame(MainPage))
        button.place(x=10,y=210)

if __name__ == "__main__":
    app = AutoFill()
    sv_ttk.set_theme("dark")
    app.mainloop()