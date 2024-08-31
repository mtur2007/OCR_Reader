from pynput import keyboard

def on_press(key):
    try:
        print(f"キー '{key.char}' が押されました")
    except AttributeError:
        print(f"特殊キー '{key}' が押されました")

def on_release(key):
    print(f"キー '{key}' が離されました")
    if key == keyboard.Key.esc:
        # ESC キーが押された場合に終了
        return False

# キーボードのリスナーを開始
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
