import tkinter as tk
import json
import time
import winsound

#保存先ファイル
save_json = 'Timer_data.json'
save_file = 'Result.txt'

#Microsoft Teams Webhook
url = "Your Microsoft Teams Webhook"
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
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        #タイムアウトセーブの有無
        self.save_var = tk.IntVar()
        self.save_var.set(self.Timer_data["config"]["timeout_save"])
        self.menu_save = tk.Menu(self.master)
        self.menu.add_cascade(label="Timeout Save", menu=self.menu_save)
        self.menu_save.add_command(label="Save", command=self.save_trigger_on, activebackground="blue")
        self.menu_save.add_command(label="No Save", command=self.save_trigger_off, activebackground="red")
        self.save_on_off_Label = tk.Label(text="Timeout Save:", font=("Meiryo", "12"), fg="purple")
        self.save_on_off_Label.place(x=30, y=610)
        self.save_on_off = tk.Label(textvariable=self.save_var, font=("Meiryo", "12"),  fg="purple")
        self.save_on_off.place(x=150, y=610)

        #スタートカウントの有無
        self.start_count_var = tk.IntVar()
        self.start_count_var.set(self.Timer_data["config"]["start_count"])
        self.menu_start_count = tk.Menu(self.master)
        self.menu.add_cascade(label="Start Count", menu=self.menu_start_count)
        self.menu_start_count.add_command(label="Count", command=self.start_count_trigger_on, activebackground="blue")
        self.menu_start_count.add_command(label="No Count", command=self.start_count_trigger_off, activebackground="red")
        self.start_count_Label = tk.Label(text="Start Count:", font=("Meiryo", "12"), fg="purple")
        self.start_count_Label.place(x=30, y=630)
        self.start_count = tk.Label(textvariable=self.start_count_var, font=("Meiryo", "12"), fg="purple")
        self.start_count.place(x=150, y=630)

        #ロボコン
        self.color_change_var = tk.IntVar()
        self.color_change_var.set(self.Timer_data["config"]["02:30_color"])
        self.menu_0230_color = tk.Menu(self.master)
        self.menu.add_cascade(label="Robocon 2019", menu=self.menu_0230_color)
        self.menu_0230_color.add_command(label="ON", command=self.color_0230_on, activebackground="blue")
        self.menu_0230_color.add_command(label="OFF", command=self.color_0230_off, activebackground="red")
        self._0230_color_Label = tk.Label(text="Robocon:", font=("Meiryo", "12"), fg="purple")
        self._0230_color_Label.place(x=30, y=650)
        self._0230_color = tk.Label(textvariable=self.color_change_var, font=("Meiryo", "12"), fg="purple")
        self._0230_color.place(x=150, y=650)

        # ミュート
        self.mute_var = tk.IntVar()
        self.mute_var.set(self.Timer_data["config"]["mute"])
        self.menu_mute = tk.Menu(self.master)
        self.menu.add_cascade(label="Mute", menu=self.menu_mute)
        self.menu_mute.add_command(label="Mute", command=self.mute_on, activebackground="blue")
        self.menu_mute.add_command(label="No Mute", command=self.mute_off, activebackground="red")
        self.mute_Label = tk.Label(text="Mute Mode:", font=("Meiryo", "12"), fg="purple")
        self.mute_Label.place(x=170, y=610)
        self.mute_on_off = tk.Label(textvariable=self.mute_var, font=("Meiryo", "12"), fg="purple")
        self.mute_on_off.place(x=290, y=610)

        #ノーマルカラー
        self.normal_color_var = tk.StringVar()
        self.normal_color_var.set(self.Timer_data["config"]["normal_color"])
        self.fg_color = tk.StringVar()
        self.fg_color.set(self.normal_color_var.get())
        self.menu_normal_color = tk.Menu(self.master)
        self.menu.add_cascade(label="Normal Color", menu=self.menu_normal_color)
        self.menu_normal_color.add_command(label="Red", command=self.normal_color_red, activebackground="red")
        self.menu_normal_color.add_command(label="Yellow", command=self.normal_color_yellow, activebackground="yellow")
        self.menu_normal_color.add_command(label="Orange", command=self.normal_color_orange, activebackground="orange")
        self.menu_normal_color.add_command(label="Pink", command=self.normal_color_pink, activebackground="pink")
        self.menu_normal_color.add_command(label="Light Green", command=self.normal_color_light_green, activebackground="light green")
        self.menu_normal_color.add_command(label="Green", command=self.normal_color_green, activebackground="green")
        self.menu_normal_color.add_command(label="Light Blue", command=self.normal_color_light_blue, activebackground="light blue")
        self.menu_normal_color.add_command(label="Blue", command=self.normal_color_blue, activebackground="blue")
        self.menu_normal_color.add_command(label="Purple", command=self.normal_color_purple, activebackground="purple")
        self.menu_normal_color.add_command(label="Black", command=self.normal_color_black, activebackground="black")
        self.normal_color_Label = tk.Label(text="Normal Color:", font=("Meiryo", "12"), fg="purple")
        self.normal_color_Label.place(x=170, y=630)
        self.normal_color = tk.Label(textvariable=self.normal_color_var, font=("Meiryo", "12"), fg=self.fg_color.get())
        self.normal_color.place(x=170, y=650)

        #トリガー
        self.started = False
        self.stop_watch_started = False
        self.lapped = False
        self.poop = False
        self.stop_watch_mode = False
        self.timer_mode = True
        self.a_attention_Label = None

        #決まり文句(？)無くても動く
        fi = tk.Frame(self, relief=tk.RIDGE, bd=4)
        fi.pack(fill=tk.BOTH, expand=1)

        #バージョン
        self.version = 3.5
        ######################
        self.version_Label = tk.Label(text="ver" + str(self.version), font=('Meiryo', '15'))
        self.version_Label.place(x=1190, y=660)

        #タイマー単体実行
        self.minute = self.Timer_data["config"]["save_minute"]
        self.second = self.Timer_data["config"]["save_second"]

        #カラー設定
        self.time = self.minute * 60 + self.second
        self.echo = tk.StringVar()
        self.echo.set("%02d:%02d" % (self.minute, self.second))
        self.display = tk.Label(textvariable=self.echo, font=('Meiryo', '150'), fg=self.fg_color.get())
        self.display.place(x=30, y=10)
        self.Label = tk.Label(text='Click or Enter to start', font=('Meiryo', '20'), bg="green", )
        self.Label.place(x=35, y=560)
        self.timer_Label = tk.Label(text="Timer", font=('Meiryo', '15'))
        self.timer_Label.place(x=295, y=10)
        self.Label.bind('<1>', self.start_stop)

        # タイマー単体リセット
        self.Label.bind('<3>', self.reset)

        #ストップウォッチ単体実行
        self.wait_time = 0
        self.watch_time = tk.StringVar()
        self.watch_time.set("%02d:%02d" % (self.wait_time / 60, self.wait_time % 60))
        self.stop_watch_aLabel = tk.Label(text="Click or Enter to Start", font=("Meiryo", "20"), bg="green")
        self.stop_watch_aLabel.place(x=947.5, y=560)
        self.stop_watch_aLabel.bind('<1>', self.start_stop_watch)
        self.stop_watch = tk.Label(textvariable=self.watch_time, font=("Meiryo", "150"),
                                         fg=self.fg_color.get())
        self.stop_watch.place(x=680, y=10)
        self.stop_watch_Label = tk.Label(text="Stop Watch", font=('Meiryo', '15'))
        self.stop_watch_Label.place(x=915, y=10)

        self.color_check()

        # ストップウォッチ単体リセット
        self.stop_watch_aLabel.bind('<3>', self.watch_reset)

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
        self.get_long = tk.Button(text="Set")
        self.get_long.place(x=250, y=327.5)
        self.get_long.bind('<1>', self.set_time)
        self.bind_all('<T>', self.set_time)

        #ラップタイム
        self.lap_list = []
        self.lap_box = tk.Text(width=40)
        self.lap_box.place(x=650, y=317.5)
        self.lap_button = tk.Button(text="Lap Time")
        self.lap_button.place(x=125, y=370)
        self.lap_button.bind('<1>', self.lap_time)
        self.bind_all('<+>', self.lap_time)

        #データセーブ
        self.Result = None
        self.save_button = tk.Button(text="Save")
        self.save_button.place(x=200, y=370)
        self.save_button.bind('<1>', self.data_save)
        self.bind_all('<S>', self.data_save)

        #データボックス読み込みセーブ
        self.load_save_button = tk.Button(text="Load Save")
        self.load_save_button.place(x=250, y=370)
        self.load_save_button.bind('<1>', self.load_save)
        self.bind_all('<L>', self.load_save)

        #ディスプレイ
        self.data_box = tk.Text(width=40)
        self.data_box.place(x=350, y=317.5)
        self.redisplay_button = tk.Button(text="Redisplay")
        self.redisplay_button.place(x=965, y=425)
        self.redisplay_button.bind('<1>', self.redisplay)
        self.bind_all('<Alt-R>', self.redisplay)

        #リトライ実行
        self.attention_time = 15
        self.attention_number = tk.StringVar()
        self.attention_number.set(15)
        self.attention_Label = tk.Label(textvariable=self.attention_number, font=("Meiryo", "29"), bg="black",

                                        fg="red", width=5)
        self.your_free_Label = tk.Label(text="YOU ARE FREE NOW", font=("Meiryo", "29"), bg="light green", fg="blue")
        self.retry_button = tk.Button(text="Retry")
        self.retry_button.place(x=1040, y=425)
        self.retry_button.bind('<1>', self.retry)
        self.bind_all('<Shift-space>', self.retry)

        #データ消去
        self.del_box = tk.Entry(width=5)
        self.del_box.place(x=150, y=415)
        self.data_del_button = tk.Button(text="Data Delete")
        self.data_del_button.place(x=250, y=412.5)
        self.data_del_button.bind('<1>', self.data_delete)
        self.bind_all('<D>', self.data_delete)

        # ポイント定義
        self.max_point = 25
        self.point = tk.IntVar()
        self.point_Label = tk.Label(textvariable=self.point, font=('Meiryo', '25'))
        self.point_Label.place(x=155, y=460)
        self.pt_Label = tk.Label(text="pt", font=("Meiryo", "20"))
        self.pt_Label.place(x=200, y=465)

        #シャツ
        self.shirt_button = tk.Button(text="Tシャツ")
        self.shirt_button.place(x=145, y=510)
        self.shirt_button.bind('<1>', self.shirt)
        self.bind_all('<Q>', self.shirt)

        #バスタオル
        self.bath_towel_button = tk.Button(text="バスタオル")
        self.bath_towel_button.place(x=190, y=510)
        self.bath_towel_button.bind('<1>', self.bath)
        self.bind_all('<W>', self.bath)

        #シーツ
        self.sheet_button = tk.Button(text="シーツ")
        self.sheet_button.place(x=248.5, y=510)
        self.sheet_button.bind('<1>', self.sheet)
        self.bind_all('<E>', self.sheet)

        #ポイント減点
        self.down_pt_button = tk.Button(text="-1pt")
        self.down_pt_button.place(x=287.5, y=510)
        self.down_pt_button.bind('<1>', self.down_pt)
        self.bind_all('<A>', self.down_pt)

        #データ送信
        self.send_title_Label = tk.Label(text="Title", font=("Meiryo", "12"))
        self.send_title_Label.place(x=965, y=365)
        self.send_title = tk.Entry(width=30)
        self.send_title.place(x=965, y=390)
        self.send_data_button = tk.Button(text="Send Data")
        self.send_data_button.place(x=1160, y=387)
        self.send_data_button.bind('<Shift-1>', self.send_result)

        #操作ログ
        self.letter_color = "black"
        self.log_Label = tk.Label(text="Log", font=("Meiryo", "12"))
        self.log_Label.place(x=965, y=310)
        self.log_box = tk.Entry(width=30, font=("Meiryo", "10"), fg=self.letter_color)
        self.log_box.place(x=965, y=340)
        self.log_box.delete(0, tk.END)
        self.log_box.insert(tk.END, "Log")

        #終了
        self.end_button = tk.Button(text="END")
        self.end_button.place(x=1067.5, y=637.5)
        self.end_button.bind('<1>', self.end)

        # 起動時データ読み込み
        with open(save_file, 'r', encoding='UTF-8') as f:
            d = f.read()
            self.data_box.insert('1.0', d)

    #初期色
    def color_check(self):
        if self.minute == 2 and self.second == 30 and self.time > 120 and self.color_change_var.get() == 1:
            self.fg_color.set("blue")

        else:
            if self.minute == 2 and self.second == 30 and self.color_change_var.get() == 1:
                pass

            else:
                self.fg_color.set(self.normal_color_var.get())

        self.display.config(fg=self.fg_color.get())
        self.stop_watch.config(fg=self.fg_color.get())
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
            self.minute_long.delete(0, tk.END)
            self.second_long.delete(0, tk.END)
            self.put_log("red", "Error")

        else:
            self.started = False
            self.stop_watch_started = False
            self.double_reset(event)
            self.color_0230_off()
            self.put_log("blue", "Set")
            self.color_check()

    #タイマー開始終了処理
    def start_stop(self, event):
        if not self.started:
            self.Label.configure(text='Click or Enter to Stop')
            self.put_log("green", "Started")
            self.started = True
            if self.start_count_var.get() == 1 and self.time == self.minute * 60 + self.second and self.mute_var.get() == 0:
                winsound.PlaySound(self.start_sound_file, winsound.SND_FILENAME)
                self.after(0, self.counting)
            else:
                self.after(1000, self.counting)

        else:
            self.Label.configure(text='Enter to Start or Reset')
            self.put_log("green", "Stopped")
            self.started = False
            time.sleep(0.2)

    #ストップウォッチ開始終了処理
    def start_stop_watch(self, event):
        if not self.stop_watch_started:
            self.stop_watch_started = True
            self.stop_watch_aLabel.configure(text='Click or Enter to Stop')
            self.put_log("green", "Started")
            if self.start_count_var.get() == 1 and self.time == self.minute * 60 + self.second and self.mute_var.get() == 0:
                self.after(0, self.watch_counting)
            else:
                self.after(1000, self.watch_counting)

        else:
            self.stop_watch_aLabel.configure(text='Enter to Start or Reset')
            self.put_log("green", "Stopped")
            self.stop_watch_started = False
            time.sleep(0.2)

    #タイマー処理
    def counting(self):
        if self.started:
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
                self.after(1000, self.counting)

            if self.time == 0:
                self.put_log("orange", "Ended")
                self.echo.set("00:00")
                self.Label.configure(text='Enter to Start or Reset')

            if self.time == 1:
                self.after(1100, self.sound_and_reset)

    #ストップウォッチ処理
    def watch_counting(self):
        if self.stop_watch_started:
            self.wait_time += 1
            self.after(1000, self.watch_counting)
            self.watch_time.set("%02d:%02d" % (self.wait_time / 60, self.wait_time % 60))

    #タイマーリセット
    def reset(self, event):
        if not self.started:
            self.lapped = False
            self.lap_list.clear()
            self.lap_box.delete("1.0", tk.END)
            self.put_log("orange", "Reset")
            self.time = self.minute * 60 + self.second
            self.echo.set("%02d:%02d" % (self.minute, self.second))
            self.color_check()
            self.point.set(0)

    #ストップウォッチリセット
    def watch_reset(self, event):
        if not self.stop_watch_started:
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
        self.lapped = True
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
        self.started = False
        self.stop_watch_started = False
        self.Result = None
        number = str(len(self.Timer_data["data_list"]) + 1)
        Local_Result = None
        if not self.lapped:
            if self.point.get() == self.max_point:
                self.Result = str("%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                         str((self.minute * 60 + self.second) - self.time) + "秒経過 満点  "

            else:
                self.Result = str("%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                        str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(self.point.get()) + "pt  "

            Local_Result = number + ". " + self.Result + "\n"

        else:
            d = map(str, self.lap_list)
            self.Result = "\n".join(d)
            if self.point.get() == self.max_point:
                self.Result += "\nFinally." + str("%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                         str((self.minute * 60 + self.second) - self.time) + "秒経過 満点  "

            else:
                self.Result += str("\nFinally." + "%02d:%02d" % (self.time / 60, self.time % 60)) + " " + \
                        str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(self.point.get()) + "pt  "

            Local_Result = number + ". " + self.Result + "\n"

        self.lapped = False
        self.Timer_data["data_list"].append(str(self.Result))
        self.lap_box.delete('1.0', tk.END)
        self.data_box.insert(tk.END, Local_Result)
        self.point.set(0)
        self.double_reset(event)
        self.color_check()
        self.put_log("blue", "Saved")

    #データ読み込みセーブ
    def load_save(self, event):
        with open(save_file, 'w', encoding='UTF-8') as f:
            f.write(self.data_box.get('1.0', 'end'))
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
                with open(save_json, 'w', encoding='UTF-8') as f:
                    json.dump(self.Timer_data, f, indent=3)
                self.put_log("red", "Error")

            self.del_box.delete(0, tk.END)


    #リディスプレイ処理
    def redisplay(self, event):
        self.data_box.delete('1.0', tk.END)
        self.del_box.delete(0, tk.END)
        self.lap_box.delete('1.0', tk.END)
        with open(save_file, 'w', encoding='UTF-8') as f:
            a = 1
            for i in self.Timer_data["data_list"]:
                f.write("{0}.{1}\n".format(a, i))
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
        if not self.poop:
            self.put_log("red", "Retried")
            self.poop = True
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
        if self.attention_time > 0 and self.started:
            self.after(1000, self.retry_count)
            self.attention_number.set(self.attention_time)
            self.put_log("red", "Retried")

        else:
            self.poop = False
            self.a_attention_Label.place_forget()
            self.attention_Label.place_forget()
            self.your_free_Label.place(x=440, y=636)
            self.attention_time = 15
            self.after(1250, forget)
            if self.started:
                self.put_log("green", "Started")
            else:
                self.put_log("green", "Stopped")

    #サウンド
    def sound_and_reset(self):
        self.started = False
        self.stop_watch_started = False
        if self.mute_var.get() == 0:
            winsound.PlaySound(self.end_sound_file, winsound.SND_FILENAME)
        self.Label.configure(text='Enter to Start or Reset')
        if self.save_var.get() == 1:
            number = str(len(self.Timer_data["data_list"]) + 1)
            Local_Result = None
            if not self.lapped:
                if self.point.get() == self.max_point:
                    self.Result = "TIME UP " + \
                                  str((self.minute * 60 + self.second) - self.time) + "秒経過 満点 Time UP  "

                else:
                    self.Result = "TIME UP " + \
                                  str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(
                        self.point.get()) + "pt Time Up  "

                Local_Result = number + ". " + self.Result + "\n"

            else:
                d = map(str, self.lap_list)
                self.Result = "\n".join(d)
                if self.point.get() == self.max_point:
                    self.Result += "\nFinally." + "TIME UP " + \
                                   str((self.minute * 60 + self.second) - self.time) + "秒経過 満点 Time Up  "

                else:
                    self.Result += str("\nFinally." + "TIME UP " + \
                                   str((self.minute * 60 + self.second) - self.time) + "秒経過 " + str(
                        self.point.get()) + "pt  ")

                Local_Result = number + ". " + self.Result + "\n"
            self.lapped = False
            self.Timer_data["data_list"].append(str(self.Result))
            self.lap_box.delete('1.0', tk.END)
            self.data_box.insert(tk.END, Local_Result)
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
            with open(save_json, 'w', encoding='UTF-8') as f:
                json.dump(self.Timer_data, f, indent=3)
            with open(save_file, 'w', encoding='UTF-8') as f:
                f.write("")
            self.send_title.delete(0, tk.END)
            self.put_log("purple", "Sent")

        except:
            self.put_log("red", "Error")

    #セーブ
    def save_trigger_off(self):
        self.save_var.set(0)
        self.put_log("purple", "Save OFF")

    def save_trigger_on(self):
        self.save_var.set(1)
        self.put_log("purple", "Save ON")

    #カウント
    def start_count_trigger_off(self):
        self.start_count_var.set(0)
        self.put_log("purple", "Start Count OFF")

    def start_count_trigger_on(self):
        self.start_count_var.set(1)
        self.put_log("purple", "Start Count ON")

    #ロボコン特別仕様
    def color_0230_off(self):
        self.color_change_var.set(0)
        self.color_check()
        self.put_log("purple", "Robocon OFF")

    def color_0230_on(self):
        self.minute = 2
        self.second = 30
        self.time = self.minute * 60 + self.second
        self.echo.set("%02d:%02d" % (self.time / 60, self.time % 60))
        self.color_change_var.set(1)
        self.color_check()
        self.put_log("purple", "Robocon ON")

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

    #終了
    def end(self, event):
        self.Timer_data["config"]["timeout_save"] = self.save_var.get()
        self.Timer_data["config"]["start_count"] = self.start_count_var.get()
        self.Timer_data["config"]["02:30_color"] = self.color_change_var.get()
        self.Timer_data["config"]["normal_color"] = self.normal_color_var.get()
        self.Timer_data["config"]["mute"] = self.mute_var.get()
        self.Timer_data["config"]["save_minute"] = self.minute
        self.Timer_data["config"]["save_second"] = self.second
        with open(save_json, 'w') as a:
            json.dump(self.Timer_data, a, indent=3)
        self.master.destroy()

if __name__ == '__main__':
    f = Timer(None)
    f.pack()
    f.mainloop()