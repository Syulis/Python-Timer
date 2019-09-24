import tkinter as tk
import json
import time
import winsound

#保存先ファイル
save_json = 'Timer_data.json'
save_file = 'Result.txt'
url_file = 'Microsoft_Teams_Webhook.txt'

#Microsoft Teams Webhook
with open(url_file, 'r') as a:
    d = a.read()
    url = d

class Timer(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        rd = open(save_json, 'r', encoding='UTF-8')
        self.Timer_data = json.load(rd)
        rd.close()

        #サウンドファイル
        self.start_sound_file = 'SE_START.wav'
        self.end_sound_file = 'SE_END.wav'

        #アプリケーションネーム
        self.master.title('Timer and Stop Watch')

        #フルスクリーン
        self.master.attributes("-fullscreen", True)

        #メニュー
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        #タイムアウトセーブの有無
        self.save_var = tk.IntVar()
        self.save_var.set(self.Timer_data["config"]["timeout_save"])
        menu_save = tk.Menu(self.master)
        menu.add_cascade(label="Timeout Save", menu=menu_save)
        menu_save.add_command(label="Save", command=self.save_trigger_on, activebackground="blue")
        menu_save.add_command(label="No Save", command=self.save_trigger_off, activebackground="red")
        save_on_off_Label = tk.Label(text="Timeout Save:", font=("Meiryo", "12"), fg="purple")
        save_on_off_Label.place(x=30, y=610)
        save_on_off = tk.Label(textvariable=self.save_var, font=("Meiryo", "12"),  fg="purple")
        save_on_off.place(x=150, y=610)

        #スタートカウントの有無
        self.start_count_var = tk.IntVar()
        self.start_count_var.set(self.Timer_data["config"]["start_count"])
        menu_start_count = tk.Menu(self.master)
        menu.add_cascade(label="Start Count", menu=menu_start_count)
        menu_start_count.add_command(label="Count", command=self.start_count_trigger_on, activebackground="blue")
        menu_start_count.add_command(label="No Count", command=self.start_count_trigger_off, activebackground="red")
        start_count_Label = tk.Label(text="Start Count:", font=("Meiryo", "12"), fg="purple")
        start_count_Label.place(x=30, y=630)
        start_count = tk.Label(textvariable=self.start_count_var, font=("Meiryo", "12"), fg="purple")
        start_count.place(x=150, y=630)

        #ロボコン
        self.color_change_var = tk.IntVar()
        self.color_change_var.set(self.Timer_data["config"]["02:30_color"])
        menu_0230_color = tk.Menu(self.master)
        menu.add_cascade(label="Robocon 2019", menu=menu_0230_color)
        menu_0230_color.add_command(label="ON", command=self.color_0230_on, activebackground="blue")
        menu_0230_color.add_command(label="OFF", command=self.color_0230_off, activebackground="red")
        _0230_color_Label = tk.Label(text="Robocon:", font=("Meiryo", "12"), fg="purple")
        _0230_color_Label.place(x=30, y=650)
        _0230_color = tk.Label(textvariable=self.color_change_var, font=("Meiryo", "12"), fg="purple")
        _0230_color.place(x=150, y=650)

        # ミュート
        self.mute_var = tk.IntVar()
        self.mute_var.set(self.Timer_data["config"]["mute"])
        menu_mute = tk.Menu(self.master)
        menu.add_cascade(label="Mute", menu=menu_mute)
        menu_mute.add_command(label="Mute", command=self.mute_on, activebackground="blue")
        menu_mute.add_command(label="No Mute", command=self.mute_off, activebackground="red")
        mute_Label = tk.Label(text="Mute Mode:", font=("Meiryo", "12"), fg="purple")
        mute_Label.place(x=170, y=610)
        mute_on_off = tk.Label(textvariable=self.mute_var, font=("Meiryo", "12"), fg="purple")
        mute_on_off.place(x=290, y=610)

        #ノーマルカラー
        self.normal_color_var = tk.StringVar()
        self.normal_color_var.set(self.Timer_data["config"]["normal_color"])
        self.fg_color = tk.StringVar()
        self.fg_color.set(self.normal_color_var.get())
        menu_normal_color = tk.Menu(self.master)
        menu.add_cascade(label="Normal Color", menu=menu_normal_color)
        menu_normal_color.add_command(label="Red", command=self.normal_color_red, activebackground="red")
        menu_normal_color.add_command(label="Yellow", command=self.normal_color_yellow, activebackground="yellow")
        menu_normal_color.add_command(label="Orange", command=self.normal_color_orange, activebackground="orange")
        menu_normal_color.add_command(label="Pink", command=self.normal_color_pink, activebackground="pink")
        menu_normal_color.add_command(label="Light Green", command=self.normal_color_light_green, activebackground="light green")
        menu_normal_color.add_command(label="Green", command=self.normal_color_green, activebackground="green")
        menu_normal_color.add_command(label="Light Blue", command=self.normal_color_light_blue, activebackground="light blue")
        menu_normal_color.add_command(label="Blue", command=self.normal_color_blue, activebackground="blue")
        menu_normal_color.add_command(label="Purple", command=self.normal_color_purple, activebackground="purple")
        menu_normal_color.add_command(label="Black", command=self.normal_color_black, activebackground="black")
        normal_color_Label = tk.Label(text="Normal Color:", font=("Meiryo", "12"), fg="purple")
        normal_color_Label.place(x=170, y=630)
        self.normal_color = tk.Label(textvariable=self.normal_color_var, font=("Meiryo", "12"), fg=self.fg_color.get())
        self.normal_color.place(x=170, y=650)

        #決まり文句(？)無くても動く
        fi = tk.Frame(self, relief=tk.RIDGE, bd=4)
        fi.pack(fill=tk.BOTH, expand=1)

        #バージョン
        version = 3.8
        ######################
        version_Label = tk.Label(text="ver" + str(version), font=('Meiryo', '15'))
        version_Label.place(x=1190, y=660)

        #タイマー単体実行
        self.minute = self.Timer_data["config"]["save_minute"]
        self.second = self.Timer_data["config"]["save_second"]

        #カラー設定
        self.time = self.minute * 60 + self.second
        self.echo = tk.StringVar()
        self.echo.set("%02d:%02d" % (self.minute, self.second))
        self.timer_display = tk.Label(textvariable=self.echo, font=('Meiryo', '150'), fg=self.fg_color.get())
        self.timer_display.place(x=30, y=10)
        self.timer_start_Label = tk.Label(text='Click or Enter to start', font=('Meiryo', '20'), bg="green")
        self.timer_start_Label.place(x=35, y=560)
        timer_Label = tk.Label(text="Timer", font=('Meiryo', '15'))
        timer_Label.place(x=295, y=10)
        self.timer_start_Label.bind('<1>', self.start_stop)

        # タイマー単体リセット
        self.timer_start_Label.bind('<3>', self.reset)

        #ストップウォッチ単体実行
        self.wait_time = 0
        self.watch_time = tk.StringVar()
        self.watch_time.set("%02d:%02d" % (self.wait_time / 60, self.wait_time % 60))
        self.stop_watch_start_Label = tk.Label(text="Click or Enter to Start", font=("Meiryo", "20"), bg="green")
        self.stop_watch_start_Label.place(x=947.5, y=560)
        self.stop_watch_start_Label.bind('<1>', self.start_stop_watch)
        self.stop_watch_display = tk.Label(textvariable=self.watch_time, font=("Meiryo", "150"),
                                         fg=self.fg_color.get())
        self.stop_watch_display.place(x=680, y=10)
        stop_watch_Label = tk.Label(text="Stop Watch", font=('Meiryo', '15'))
        stop_watch_Label.place(x=915, y=10)

        self.color_check()

        # ストップウォッチ単体リセット
        self.stop_watch_start_Label.bind('<3>', self.watch_reset)

        #同時実行
        self.bind_all('<Shift-Return>', self.double_run)

        #同時リセット
        self.bind_all('<R>', self.double_reset)

        #時間設定
        m = tk.Label(text="分", font=("Meiryo", "10"))
        m.place(x=175, y=330)
        s = tk.Label(text="秒", font=("Meiryo", "10"))
        s.place(x=225, y=330)
        self.minute_long = tk.Entry(width=3)
        self.minute_long.place(x=150, y=330)
        self.second_long = tk.Entry(width=3)
        self.second_long.place(x=200, y=330)
        get_long = tk.Button(text="Set")
        get_long.place(x=250, y=327.5)
        get_long.bind('<1>', self.set_time)
        self.bind_all('<T>', self.set_time)

        #ラップタイム
        self.lap_list = []
        self.lap_box = tk.Text(width=40)
        self.lap_box.place(x=650, y=317.5)
        lap_button = tk.Button(text="Lap Time")
        lap_button.place(x=125, y=370)
        lap_button.bind('<1>', self.lap_time)
        self.bind_all('<+>', self.lap_time)

        #データセーブ
        save_button = tk.Button(text="Save")
        save_button.place(x=200, y=370)
        save_button.bind('<1>', self.data_save)
        self.bind_all('<S>', self.data_save)

        #データボックス読み込みセーブ
        load_save_button = tk.Button(text="Load Save")
        load_save_button.place(x=250, y=370)
        load_save_button.bind('<1>', self.load_save)
        self.bind_all('<L>', self.load_save)

        #データ改ざん
        self.data_number_box = tk.Entry(width=3)
        self.data_number_box.place(x=965, y=470)
        self.data_exchange_box = tk.Entry(width=24)
        self.data_exchange_box.place(x=1000, y=470)
        data_exchange_Label = tk.Label(text=".", font=("Meiryo", "12"))
        data_exchange_Label.place(x=987.5, y=467.5)
        data_exchange_button = tk.Button(text="Exchange Data")
        data_exchange_button.place(x=1155, y=466.5)
        data_exchange_button.bind('<1>', self.data_exchange)
        self.bind_all('<X>', self.data_exchange)

        #データ追加
        self.data_add_box = tk.Entry(width=30)
        self.data_add_box.place(x=965, y=507.5)
        data_add_button = tk.Button(text="Add Data")
        data_add_button.place(x=1155, y=507.5)
        data_add_button.bind('<1>', self.data_add)
        self.bind_all('<C>', self.data_add)

        #ディスプレイ
        self.data_box = tk.Text(width=40)
        self.data_box.place(x=350, y=317.5)
        redisplay_button = tk.Button(text="Redisplay")
        redisplay_button.place(x=965, y=425)
        redisplay_button.bind('<1>', self.redisplay)
        self.bind_all('<Alt-R>', self.redisplay)

        #リトライ実行
        self.attention_number = tk.StringVar()
        self.attention_number.set(15)
        self.attention_Label = tk.Label(textvariable=self.attention_number, font=("Meiryo", "29"), bg="black",
                                        fg="red", width=5)
        self.your_free_Label = tk.Label(text="YOU ARE FREE NOW", font=("Meiryo", "29"), bg="light green", fg="blue")
        retry_button = tk.Button(text="Retry")
        retry_button.place(x=1040, y=425)
        retry_button.bind('<1>', self.retry)
        self.bind_all('<Shift-space>', self.retry)

        #データ消去
        self.del_box = tk.Entry(width=5)
        self.del_box.place(x=150, y=415)
        data_del_button = tk.Button(text="Delete Data")
        data_del_button.place(x=250, y=412.5)
        data_del_button.bind('<1>', self.data_delete)
        self.bind_all('<D>', self.data_delete)

        # ポイント定義
        self.max_point = 25
        self.point = tk.IntVar()
        point_Label = tk.Label(textvariable=self.point, font=('Meiryo', '25'))
        point_Label.place(x=155, y=460)
        pt_Label = tk.Label(text="pt", font=("Meiryo", "20"))
        pt_Label.place(x=200, y=465)

        #シャツ
        shirt_button = tk.Button(text="Tシャツ")
        shirt_button.place(x=145, y=510)
        shirt_button.bind('<1>', self.shirt)
        self.bind_all('<Q>', self.shirt)

        #バスタオル
        bath_towel_button = tk.Button(text="バスタオル")
        bath_towel_button.place(x=190, y=510)
        bath_towel_button.bind('<1>', self.bath)
        self.bind_all('<W>', self.bath)

        #シーツ
        sheet_button = tk.Button(text="シーツ")
        sheet_button.place(x=248.5, y=510)
        sheet_button.bind('<1>', self.sheet)
        self.bind_all('<E>', self.sheet)

        #ポイント減点
        down_pt_button = tk.Button(text="-1pt")
        down_pt_button.place(x=287.5, y=510)
        down_pt_button.bind('<1>', self.down_pt)
        self.bind_all('<A>', self.down_pt)

        #データ送信
        self.send_title_Label = tk.Label(text="Title", font=("Meiryo", "12"))
        self.send_title_Label.place(x=965, y=365)
        self.send_title = tk.Entry(width=30)
        self.send_title.place(x=965, y=390)
        send_data_button = tk.Button(text="Send Data")
        send_data_button.place(x=1160, y=387)
        send_data_button.bind('<Shift-1>', self.send_result)

        #操作ログ
        self.letter_color = "black"
        self.log_Label = tk.Label(text="Log", font=("Meiryo", "12"))
        self.log_Label.place(x=965, y=310)
        self.log_box = tk.Entry(width=30, font=("Meiryo", "10"), fg=self.letter_color)
        self.log_box.place(x=965, y=340)
        self.log_box.delete(0, tk.END)
        self.log_box.insert(tk.END, "Log")

        #最小化
        minimize_button = tk.Button(text="Minimize")
        minimize_button.place(x=1020, y=637.5)
        minimize_button.bind('<1>', self.minimize)

        #終了
        end_button = tk.Button(text="END")
        end_button.place(x=1115, y=637.5)
        end_button.bind('<1>', self.end)

        # 起動時データ読み込み
        with open(save_file, 'r', encoding='UTF-8') as f:
            d = f.read()
            self.data_box.insert('1.0', d)

        d = map(str, self.lap_list)
        e = "\n".join(d)
        self.lap_box.insert("1.0", e)

    #初期色
    def color_check(self):
        if self.minute == 2 and self.second == 30 and self.time > 120 and self.color_change_var.get() == 1:
            self.fg_color.set("blue")

        else:
            if self.minute == 2 and self.second == 30 and self.color_change_var.get() == 1:
                pass

            else:
                self.fg_color.set(self.normal_color_var.get())

        self.timer_display.config(fg=self.fg_color.get())
        self.stop_watch_display.config(fg=self.fg_color.get())
        self.normal_color.config(fg=self.fg_color.get())
        if self.color_change_var.get() == 1:
            self.normal_color.config(fg=self.normal_color_var.get())

    #同時実行
    def double_run(self, event):
        self.start_stop(event)
        self.start_stop_watch(event)

    #同時リセット
    def double_reset(self, event):
        self.reset(event)
        self.watch_reset(event)

    #時間設定
    def set_time(self, event):
        try:
            self.minute = int(self.minute_long.get())
            self.second = int(self.second_long.get())
            self.color_check()
            self.minute_long.delete(0, tk.END)
            self.second_long.delete(0, tk.END)
            self.echo.set("%02d:%02d" % (self.minute, self.second))
            self.time = self.minute * 60 + self.second

        except:
            self.put_log("red", "Error")

        else:
            self.Timer_data["stat"]["timer_started"] = 0
            self.Timer_data["stat"]["stop_watch_started"] = 0
            self.double_reset(event)
            self.color_0230_off()
            self.put_log("blue", "Set")
            self.color_check()

    #タイマー開始終了処理
    def start_stop(self, event):
        if not self.Timer_data["stat"]["timer_started"]:
            self.timer_start_Label.configure(text='Click or Enter to Stop')
            self.put_log("green", "Started")
            self.Timer_data["stat"]["timer_started"] = 1
            if self.start_count_var.get() == 1 and self.time == self.minute * 60 + self.second and self.mute_var.get() == 0:
                winsound.PlaySound(self.start_sound_file, winsound.SND_FILENAME)
                self.after(0, self.counting)
            else:
                self.after(1000, self.counting)

        else:
            self.timer_start_Label.configure(text='Enter to Start or Reset')
            self.put_log("green", "Stopped")
            self.Timer_data["stat"]["timer_started"] = 0
            time.sleep(0.2)

    #ストップウォッチ開始終了処理
    def start_stop_watch(self, event):
        if not self.Timer_data["stat"]["stop_watch_started"]:
            self.Timer_data["stat"]["stop_watch_started"] = 1
            self.stop_watch_start_Label.configure(text='Click or Enter to Stop')
            self.put_log("green", "Started")
            if self.start_count_var.get() == 1 and self.time == self.minute * 60 + self.second and self.mute_var.get() == 0:
                self.after(0, self.watch_counting)
            else:
                self.after(1000, self.watch_counting)

        else:
            self.stop_watch_start_Label.configure(text='Enter to Start or Reset')
            self.put_log("green", "Stopped")
            self.Timer_data["stat"]["stop_watch_started"] = 0
            time.sleep(0.2)

    #タイマー処理
    def counting(self):
        if self.Timer_data["stat"]["timer_started"]:
            self.time -= 1
            if self.minute == 2 and self.second == 30 and self.color_change_var.get() == 1:
                if 90 < self.time <= 120:
                    self.fg_color.set("green")

                elif 30 < self.time <= 90:
                    self.fg_color.set("orange")

                elif self.time <= 30:
                    self.fg_color.set("red")

                self.color_check()

            if self.time >= 0:
                self.echo.set("%02d:%02d" % (self.time / 60, self.time % 60))
                self.after(996, self.counting)

            if self.time == 0:
                self.put_log("orange", "Ended")
                self.echo.set("00:00")
                self.timer_start_Label.configure(text='Enter to Start or Reset')

            if self.time == 1:
                self.after(1100, self.sound_and_reset)

    #ストップウォッチ処理
    def watch_counting(self):
        if self.Timer_data["stat"]["stop_watch_started"]:
            self.wait_time += 1
            self.after(996, self.watch_counting)
            self.watch_time.set("%02d:%02d" % (self.wait_time / 60, self.wait_time % 60))

    #タイマーリセット
    def reset(self, event):
        if not self.Timer_data["stat"]["timer_started"]:
            self.Timer_data["stat"]["lapped"] = 0
            self.lap_list.clear()
            self.lap_box.delete("1.0", tk.END)
            self.put_log("orange", "Reset")
            self.time = self.minute * 60 + self.second
            self.echo.set("%02d:%02d" % (self.minute, self.second))
            self.color_check()
            self.point.set(0)

    #ストップウォッチリセット
    def watch_reset(self, event):
        if not self.Timer_data["stat"]["stop_watch_started"]:
            self.put_log("orange", "Reset")
            self.wait_time = 0
            self.watch_time.set("%02d:%02d" % (self.wait_time / 60, self.wait_time % 60))
            self.point.set(0)

    #ログ
    def put_log(self, color, text):
        self.letter_color = color
        self.log_box = tk.Entry(width=30, font=("Meiryo", "10"), fg=self.letter_color)
        self.log_box.place(x=965, y=340)
        self.log_box.insert(tk.END, text)

    #ラップタイム
    def lap_time(self, event):
        self.Timer_data["stat"]["lapped"] = 1
        if self.point.get() == self.max_point:
            self.lap_list.append(
                "Lap" + str(len(self.lap_list) + 1) + str(".%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                str((self.minute * 60 + self.second) - self.time) + "秒経過 満点  ")
        else:
            self.lap_list.append(
                "Lap" + str(len(self.lap_list) + 1) + str(".%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(self.point.get()) + "pt  ")
        d = map(str, self.lap_list)
        e = "\n".join(d)
        self.put_log("blue", "Set")
        self.lap_box.delete("1.0", tk.END)
        self.lap_box.insert("1.0", e)

    #データセーブ
    def data_save(self, event):
        self.Timer_data["stat"]["timer_started"] = 0
        self.Timer_data["stat"]["stop_watch_started"] = 0
        number = str(len(self.Timer_data["data_list"]) + 1)
        if not self.Timer_data["stat"]["lapped"]:
            if self.point.get() == self.max_point:
                Result = str("%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                         str((self.minute * 60 + self.second) - self.time) + "秒経過 満点  "

            else:
                Result = str("%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                        str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(self.point.get()) + "pt  "

            Final_Result = number + ". " + Result + "\n"

        else:
            d = map(str, self.lap_list)
            Result = "\n".join(d)
            if self.point.get() == self.max_point:
                Result += "\nFinally." + str("%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                         str((self.minute * 60 + self.second) - self.time) + "秒経過 満点  "

            else:
                Result += str("\nFinally." + "%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                        str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(self.point.get()) + "pt  "

            Final_Result = number + ". " + Result + "\n"

        self.Timer_data["stat"]["lapped"] = 0
        self.Timer_data["data_list"].append(str(Result))
        self.lap_box.delete('1.0', tk.END)
        self.data_box.insert(tk.END, Final_Result)
        self.point.set(0)
        self.double_reset(event)
        self.color_check()
        with open(save_file, 'w', encoding='UTF-8') as a:
            a.write(self.data_box.get('1.0', 'end'))
        self.put_log("blue", "Saved")

    #読み込みセーブ
    def load_save(self, event):
        with open(save_file, 'w', encoding='UTF-8') as a:
            a.write(self.data_box.get('1.0', 'end'))
        self.put_log("blue", "Saved")

    #データ消去
    def data_delete(self, event):
        if self.del_box.get() == "all":
            self.Timer_data["data_list"].clear()
            with open(save_json, 'w', encoding='UTF-8') as f:
                json.dump(self.Timer_data, f, indent=3)
            self.redisplay(event)
            self.put_log("red", "Deleted")

        else:
            try:
                target = int(self.del_box.get()) - 1
                if target > len(self.Timer_data["data_list"]):
                    self.put_log("red", "Error")
                    return
                del self.Timer_data["data_list"][target]
                with open(save_json, 'w', encoding='UTF-8') as f:
                    json.dump(self.Timer_data, f, indent=3)
                self.redisplay(event)
                self.put_log("red", "Deleted")

            except:
                self.put_log("red", "Error")

    #データ改ざん
    def data_exchange(self, event):
        try:
            data_number = int(self.data_number_box.get()) - 1
            data_content = str(self.data_exchange_box.get()) + "  "
            self.Timer_data["data_list"][data_number] = data_content
            self.data_number_box.delete(0, tk.END)
            self.data_exchange_box.delete(0, tk.END)
            self.redisplay(event)
            self.put_log("blue", "Data Exchanged")
        except:
            self.put_log("red", "Error")

    #データ追加
    def data_add(self, event):
        try:
            add_data_content = str(self.data_add_box.get()) + "  "
            self.Timer_data["data_list"].append(add_data_content)
            self.data_box.delete('1.0', tk.END)
            self.data_add_box.delete(0, tk.END)
            with open(save_file, 'w', encoding='UTF-8') as f:
                a = 1
                for i in self.Timer_data["data_list"]:
                    f.write("{0}. {1}\n".format(a, i))
                    a += 1

            with open(save_file, 'r', encoding='UTF-8') as f:
                d = f.read()
                self.data_box.insert('1.0', d)
                self.put_log("blue", "Data Add")

        except:
            self.put_log("red", "Error")

    #リディスプレイ処理
    def redisplay(self, event):
        self.data_box.delete('1.0', tk.END)
        self.del_box.delete(0, tk.END)
        self.lap_box.delete('1.0', tk.END)
        self.data_exchange_box.delete(0, tk.END)
        with open(save_file, 'w', encoding='UTF-8') as f:
            a = 1
            for i in self.Timer_data["data_list"]:
                f.write("{0}. {1}\n".format(a, i))
                a += 1

        with open(save_file, 'r', encoding='UTF-8') as f:
            d = f.read()
            self.data_box.insert('1.0', d)

        d = map(str, self.lap_list)
        e = "\n".join(d)
        self.lap_box.insert("1.0", e)
        self.put_log("orange", "Redisplayed")

    #シャツpt
    def shirt(self, event):
        if self.point.get() >= self.max_point:
            self.point.set(self.max_point)
        else:
            self.point.set(self.point.get() + 1)
            if self.point.get() >= self.max_point:
                self.point.set(self.max_point)

    #バスタオルpt
    def bath(self, event):
        if self.point.get() >= self.max_point:
            self.point.set(self.max_point)
        else:
            self.point.set(self.point.get() + 2)
            if self.point.get() >= self.max_point:
                self.point.set(self.max_point)

    #シーツpt
    def sheet(self, event):
        if self.point.get() >= self.max_point:
            self.point.set(self.max_point)
        else:
            self.point.set(self.point.get() + 3)
            if self.point.get() >= self.max_point:
                self.point.set(self.max_point)

    #ポイント減点
    def down_pt(self, event):
        if self.point.get() == 0:
            pass
        else:
            self.point.set(self.point.get() - 1)

    #リトライ
    def retry(self, event):
        if not self.Timer_data["stat"]["retried"]:
            self.put_log("red", "Retried")
            self.Timer_data["stat"]["retried"] = 1
            self.your_free_Label.place_forget()
            self.a_attention_Label = tk.Label(text="Don't Move", font=("Meiryo", "29"), bg="black", fg="red")
            self.a_attention_Label.place(x=460, y=636)
            self.attention_number.set(self.attention_time)
            self.attention_Label.place(x=680, y=636)
            self.after(1000, self.retry_count)

    #リトライカウント
    def retry_count(self):
        def forget():
            self.your_free_Label.place_forget()

        self.attention_time -= 1
        if self.attention_time > 0 and self.Timer_data["stat"]["timer_started"]:
            self.after(1000, self.retry_count)
            self.attention_number.set(self.attention_time)
            self.put_log("red", "Retried")

        else:
            self.Timer_data["stat"]["retried"] = 0
            self.a_attention_Label.place_forget()
            self.attention_Label.place_forget()
            self.your_free_Label.place(x=440, y=636)
            self.attention_time = 15
            self.after(1250, forget)
            if self.Timer_data["stat"]["timer_started"]:
                self.put_log("green", "Started")
            else:
                self.put_log("green", "Stopped")

    #サウンド
    def sound_and_reset(self):
        self.Timer_data["stat"]["timer_started"] = 0
        self.Timer_data["stat"]["stop_watch_started"] = 0
        if self.mute_var.get() == 0:
            winsound.PlaySound(self.end_sound_file, winsound.SND_FILENAME)
        self.timer_start_Label.configure(text='Enter to Start or Reset')
        if self.save_var.get() == 1:
            number = str(len(self.Timer_data["data_list"]) + 1)
            if not self.Timer_data["stat"]["lapped"]:
                if self.point.get() == self.max_point:
                    Result = "TIME UP " + \
                                  str((self.minute * 60 + self.second) - self.time) + "秒経過 満点 Time UP  "

                else:
                    Result = "TIME UP " + \
                                  str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(
                        self.point.get()) + "pt Time Up  "

                Final_Result = number + ". " + Result + "\n"

            else:
                d = map(str, self.lap_list)
                Result = "\n".join(d)
                if self.point.get() == self.max_point:
                    Result += "\nFinally." + "TIME UP " + \
                                   str((self.minute * 60 + self.second) - self.time) + "秒経過 満点 Time Up  "

                else:
                    Result += str("\nFinally." + "TIME UP " + \
                                   str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(
                        self.point.get()) + "pt  ")

                Final_Result = number + ". " + Result + "\n"
            self.Timer_data["stat"]["lapped"] = 0
            self.Timer_data["data_list"].append(str(Result))
            self.lap_box.delete('1.0', tk.END)
            self.data_box.insert(tk.END, Final_Result)
        else:
            pass
        self.time = self.minute * 60 + self.second
        self.echo.set("%02d:%02d" % (self.minute, self.second))
        self.wait_time = 0
        self.watch_time.set("%02d:%02d" % (self.wait_time / 60, self.wait_time % 60))
        self.point.set(0)
        self.color_check()
        self.lap_list.clear()
        self.lap_box.delete("1.0", tk.END)
        self.put_log("orange", "Reset")

    #練習結果投稿
    def send_result(self, event):
        import pymsteams
        myTeamsMessage = pymsteams.connectorcard(url)

        try:
            with open(save_file, 'w', encoding='UTF-8') as f:
                f.write(self.data_box.get('1.0', 'end'))
            with open(save_file, 'r', encoding='UTF-8') as f:
                d = f.read()
            myTeamsMessage.title(self.send_title.get())
            myTeamsMessage.text(d)
            myTeamsMessage.send()
            self.data_box.delete('1.0', 'end')
            self.Timer_data["data_list"].clear()
            with open(save_json, 'w', encoding='UTF-8') as a:
                json.dump(self.Timer_data, a, indent=3)
            with open(save_file, 'w', encoding='UTF-8') as a:
                a.write("")
            self.send_title.delete(0, tk.END)
            self.put_log("purple", "Sent")

        except:
            self.put_log("red", "Error")

    #セーブ
    def save_trigger_off(self):
        self.save_var.set(0)
        self.put_log("red", "Save OFF")

    def save_trigger_on(self):
        self.save_var.set(1)
        self.put_log("blue", "Save ON")

    #カウント
    def start_count_trigger_off(self):
        self.start_count_var.set(0)
        self.put_log("red", "Start Count OFF")

    def start_count_trigger_on(self):
        self.start_count_var.set(1)
        self.put_log("blue", "Start Count ON")

    #ロボコン特別仕様
    def color_0230_off(self):
        self.color_change_var.set(0)
        self.color_check()
        self.put_log("red", "Robocon OFF")

    def color_0230_on(self):
        self.minute = 2
        self.second = 30
        self.time = self.minute * 60 + self.second
        self.echo.set("%02d:%02d" % (self.time / 60, self.time % 60))
        self.color_change_var.set(1)
        self.color_check()
        self.put_log("blue", "Robocon ON")

    #通常文字色
    def normal_color_red(self):
        self.normal_color_var.set("Red")
        self.color_check()
        self.put_log("Red", "Changed Color Red")

    def normal_color_yellow(self):
        self.normal_color_var.set("Yellow")
        self.color_check()
        self.put_log("Yellow", "Changed Color Yellow")

    def normal_color_orange(self):
        self.normal_color_var.set("Orange")
        self.color_check()
        self.put_log("Orange", "Changed Color Orange")

    def normal_color_pink(self):
        self.normal_color_var.set("Pink")
        self.color_check()
        self.put_log("Pink", "Changed Color Pink")

    def normal_color_light_green(self):
        self.normal_color_var.set("Light Green")
        self.color_check()
        self.put_log("Light Green", "Changed Color Light Green")

    def normal_color_green(self):
        self.normal_color_var.set("Green")
        self.color_check()
        self.put_log("Green", "Changed Color Green")

    def normal_color_light_blue(self):
        self.normal_color_var.set("Light Blue")
        self.color_check()
        self.put_log("Light Blue", "Changed Color Light Blue")

    def normal_color_blue(self):
        self.normal_color_var.set("Blue")
        self.color_check()
        self.put_log("Blue", "Changed Color Blue")

    def normal_color_purple(self):
        self.normal_color_var.set("Purple")
        self.color_check()
        self.put_log("Purple", "Changed Color Purple")

    def normal_color_black(self):
        self.normal_color_var.set("Black")
        self.color_check()
        self.put_log("Black", "Changed Color Black")

    #ミュート
    def mute_off(self):
        self.mute_var.set(0)
        self.put_log("Red", "Mute OFF")

    def mute_on(self):
        self.mute_var.set(1)
        self.put_log("Blue", "Mute ON")

    #最小化
    def minimize(self, event):
        self.master.iconify()

    #終了
    def end(self, event):
        self.Timer_data["config"]["timeout_save"] = self.save_var.get()
        self.Timer_data["config"]["start_count"] = self.start_count_var.get()
        self.Timer_data["config"]["02:30_color"] = self.color_change_var.get()
        self.Timer_data["config"]["normal_color"] = self.normal_color_var.get()
        self.Timer_data["config"]["mute"] = self.mute_var.get()
        self.Timer_data["config"]["save_minute"] = self.minute
        self.Timer_data["config"]["save_second"] = self.second

        self.Timer_data["stat"]["timer_started"] = 0
        self.Timer_data["stat"]["stop_watch_started"] = 0
        self.Timer_data["stat"]["lapped"] = 0
        self.Timer_data["stat"]["retried"] = 0
        with open(save_json, 'w') as a:
            json.dump(self.Timer_data, a, indent=3)
        self.master.destroy()

if __name__ == '__main__':
    f = Timer(None)
    f.pack()
    f.mainloop()
