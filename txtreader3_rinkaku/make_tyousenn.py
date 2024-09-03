from PIL import Image

def overlay_flag_on_map(map_image_path, flag_image_path, output_image_path):
    # 画像を読み込む
    map_image = Image.open(map_image_path)
    flag_image = Image.open(flag_image_path)
    
    # フラグのサイズを調整する
    flag_width, flag_height = flag_image.size
    map_width, map_height = map_image.size

    # フラグを背景として繰り返すサイズに調整
    flag_resized = flag_image.resize((map_width, map_height))
    
    # フラグ画像を背景として使用
    # フラグを背景として設定するために、地図画像にフラグ画像を貼り付ける
    flag_overlay = Image.new('RGBA', (map_width, map_height), (255, 255, 255, 0))
    flag_overlay.paste(flag_resized, (0, 0), flag_resized)
    
    # フラグの上に地図を合成
    map_image = map_image.convert('RGBA')
    combined_image = Image.alpha_composite(flag_overlay, map_image)
    
    # 結果を保存
    combined_image.save(output_image_path)

# 使用例
overlay_flag_on_map('korean_peninsula_map.png', 'north_korea_flag.png', 'output_image.png')
