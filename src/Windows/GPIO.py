#!/usr/bin/env python3
import tkinter, subprocess, os

#ディレクトリ情報
dire = os.getcwd().replace(os.path.sep, '/')

# GPIO設定
def set_GPIO():
    try:
            import board
            # print(dir(board)) # GPIO確認
            import digitalio
        
            global GPIO_C0, GPIO_C1, GPIO_C2, GPIO_C3, GPIO_C4, GPIO_C5, GPIO_C6, GPIO_C7, GPIO_D4, GPIO_D5, GPIO_D6, GPIO_D7
            GPIO_C0 = digitalio.DigitalInOut(board.C0)
            GPIO_C0.direction = digitalio.Direction.OUTPUT

            GPIO_C1 = digitalio.DigitalInOut(board.C1)
            GPIO_C1.direction = digitalio.Direction.OUTPUT

            GPIO_C2 = digitalio.DigitalInOut(board.C2)
            GPIO_C2.direction = digitalio.Direction.OUTPUT

            GPIO_C3 = digitalio.DigitalInOut(board.C3)
            GPIO_C3.direction = digitalio.Direction.OUTPUT

            GPIO_C4 = digitalio.DigitalInOut(board.C4)
            GPIO_C4.direction = digitalio.Direction.OUTPUT

            GPIO_C5 = digitalio.DigitalInOut(board.C5)
            GPIO_C5.direction = digitalio.Direction.OUTPUT

            GPIO_C6 = digitalio.DigitalInOut(board.C6)
            GPIO_C6.direction = digitalio.Direction.OUTPUT

            GPIO_C7 = digitalio.DigitalInOut(board.C7)
            GPIO_C7.direction = digitalio.Direction.OUTPUT

            GPIO_D4 = digitalio.DigitalInOut(board.D4)
            GPIO_D4.direction = digitalio.Direction.INPUT

            GPIO_D5 = digitalio.DigitalInOut(board.D5)
            GPIO_D5.direction = digitalio.Direction.INPUT

            GPIO_D6 = digitalio.DigitalInOut(board.D6)
            GPIO_D6.direction = digitalio.Direction.INPUT

            GPIO_D7 = digitalio.DigitalInOut(board.D7)
            GPIO_D7.direction = digitalio.Direction.INPUT

            return 0

    except:
        return 1

def reboot(body):
    body.destroy()
    cmd = "python " + dire + "/GPIO.py"
    subprocess.run(cmd , shell=True)

def outChange(GPIO, button):
    if GPIO.value == False:
        button["text"] = "ON"
        button["bg"] = "#FF0000"
        GPIO.value = True
    else:
        button["text"] = "OFF"
        button["bg"] = "#00FF33"
        GPIO.value = False


if __name__ == "__main__":
    global body
    body = tkinter.Tk()
    body.title("GPIO設定")
    body.configure(background = 'white')
    body.geometry("1000x800") # ウィンドウサイズ
    body.resizable(0,0) # リサイズ禁止
    # body.iconbitmap(f"{dire}/icon.ico")
    
    #メニューボタン
    menu_bar = tkinter.Menu(body)
    body.config(menu = menu_bar)
    
    menu_file = tkinter.Menu(menu_bar, tearoff=0, font=("HGPｺﾞｼｯｸE", "10"))
    menu_file.add_cascade(label='閉じる', command=body.destroy)
    menu_file.add_cascade(label='再起動', command=lambda:reboot(body))
    menu_bar.add_cascade(label='ファイル', menu = menu_file) 
    
    
    #テキスト表示
    GPIO_Label = tkinter.Label(body, font=("HGP創英角ﾎﾟｯﾌﾟ体", "15"),background='#ffffff')
    GPIO_Label.place(x = 10, y = 10)
    r = set_GPIO()
    if r == 0:
        GPIO_Label["text"] = 'GPIOを検出'
        C0_Label = tkinter.Label(body, text= "C0" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        C0_Label.place(x = 10, y = 90)
        C1_Label = tkinter.Label(body, text= "C1" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        C1_Label.place(x = 10, y = 180)
        C2_Label = tkinter.Label(body, text= "C2" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        C2_Label.place(x = 10, y = 270)
        C3_Label = tkinter.Label(body, text= "C3" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        C3_Label.place(x = 10, y = 360)
        C4_Label = tkinter.Label(body, text= "C4" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        C4_Label.place(x = 10, y = 450)
        C5_Label = tkinter.Label(body, text= "C5" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        C5_Label.place(x = 10, y = 540)
        C6_Label = tkinter.Label(body, text= "C6" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        C6_Label.place(x = 10, y = 630)
        C7_Label = tkinter.Label(body, text= "C7" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        C7_Label.place(x = 10, y = 720)
        D4_Label = tkinter.Label(body, text= "D4" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        D4_Label.place(x = 500, y = 100)
        D5_Label = tkinter.Label(body, text= "D5" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        D5_Label.place(x = 500, y = 200)
        D6_Label = tkinter.Label(body, text= "D6" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        D6_Label.place(x = 500, y = 300)
        D7_Label = tkinter.Label(body, text= "D7" , font=("HGPｺﾞｼｯｸE", "15"),background='#ffffff')
        D7_Label.place(x = 500, y = 400)
        
        # GPIO設定
        GPIO_C0.value = False
        GPIO_C1.value = False
        GPIO_C2.value = False
        GPIO_C3.value = False
        GPIO_C4.value = False
        GPIO_C5.value = False
        GPIO_C6.value = False
        GPIO_C7.value = False

        # ボタンの初期設定
        
        button_C0 = tkinter.Button(body, text = "OFF", command = lambda:outChange(GPIO_C0, button_C0) , font=("HGPｺﾞｼｯｸE", "13"), width=7, fg = '#FFFFFF', background= "#00FF33")
        button_C0.place(x = 70, y = 80)
        
        button_C1 = tkinter.Button(body, text = "OFF", command = lambda:outChange(GPIO_C1, button_C1) , font=("HGPｺﾞｼｯｸE", "13"), width=7, fg = '#FFFFFF', background= "#00FF33")
        button_C1.place(x = 70, y = 170)
        
        button_C2 = tkinter.Button(body, text = "OFF", command = lambda:outChange(GPIO_C2, button_C2) , font=("HGPｺﾞｼｯｸE", "13"), width=7, fg = '#FFFFFF', background= "#00FF33")
        button_C2.place(x = 70, y = 260)
        
        button_C3 = tkinter.Button(body, text = "OFF", command = lambda:outChange(GPIO_C3, button_C3) , font=("HGPｺﾞｼｯｸE", "13"), width=7, fg = '#FFFFFF', background= "#00FF33")
        button_C3.place(x = 70, y = 350)
        
        button_C4 = tkinter.Button(body, text = "OFF", command = lambda:outChange(GPIO_C4, button_C4) , font=("HGPｺﾞｼｯｸE", "13"), width=7, fg = '#FFFFFF', background= "#00FF33")
        button_C4.place(x = 70, y = 440)
        
        button_C5 = tkinter.Button(body, text = "OFF", command = lambda:outChange(GPIO_C5, button_C5) , font=("HGPｺﾞｼｯｸE", "13"), width=7, fg = '#FFFFFF', background= "#00FF33")
        button_C5.place(x = 70, y = 530)
        
        button_C6 = tkinter.Button(body, text = "OFF", command = lambda:outChange(GPIO_C6, button_C6) , font=("HGPｺﾞｼｯｸE", "13"), width=7, fg = '#FFFFFF', background= "#00FF33")
        button_C6.place(x = 70, y = 620)
        
        button_C7 = tkinter.Button(body, text = "OFF", command = lambda:outChange(GPIO_C7, button_C7) , font=("HGPｺﾞｼｯｸE", "13"), width=7, fg = '#FFFFFF', background= "#00FF33")
        button_C7.place(x = 70, y = 710)
        
    else:
        GPIO_Label["text"] = "GPIOを検出出来ませんでした"
        button_r = tkinter.Button(body, text = "再読み込み", command = lambda:reboot(body) , font=("HGPｺﾞｼｯｸE", "13"))
        button_r.pack(padx=10,pady = 10, anchor=tkinter.SE, expand=True, ipadx=30)
    
    body.mainloop() # ずっと表示させる
    