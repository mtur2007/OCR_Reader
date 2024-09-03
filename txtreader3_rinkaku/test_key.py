from pynput import keyboard

a = 0
def on_press(key):

    if key == keyboard.Key.esc:
        # ESC キーが押された場合に終了
        return False
    print(a)
    a += 1

# キーボードのリスナーを開始
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()