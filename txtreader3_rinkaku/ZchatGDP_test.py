import cv2
import numpy as np

# 画像を読み込む
image = cv2.imread('input_image.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ノイズ除去
denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

# 適応的閾値処理
binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# モルフォロジー演算
kernel = np.ones((3,3), np.uint8)
morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# 連結成分のラベリング
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(morph, connectivity=8)

# 結果を表示するための画像を作成
result = np.zeros(image.shape, dtype=np.uint8)

# 緑色を定義（BGRフォーマット）
green_color = (0, 255, 0)

# 各連結成分（文字）に緑色をつける
for i in range(1, num_labels):  # 0はバックグラウンドなのでスキップ
    # 小さすぎる成分は無視
    #if stats[i, cv2.CC_STAT_AREA] < 50:
    #    continue
    
    # 文字のマスクを作成
    char_mask = (labels == i).astype(np.uint8) * 255
    
    # 文字の輪郭を検出
    contours, _ = cv2.findContours(char_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 文字の輪郭を緑色で描画
    cv2.drawContours(result, contours, -1, green_color, 2)
    
    # 文字の内部を緑色で塗りつぶす（オプション）
    # cv2.fillPoly(result, contours, green_color)

# 元の画像と結果を合成
output = cv2.addWeighted(image, 0.7, result, 0.3, 0)

# 結果を表示
cv2.imshow('Green Characters', output)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 結果を保存
cv2.imwrite('output_image.png', output)


