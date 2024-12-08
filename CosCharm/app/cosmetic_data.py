import os
import json

# フォルダが存在しない場合に作成
folder_path = os.path.join('app', 'fixtures')
if not os.path.exists(folder_path):
    print(f"Creating folder: {folder_path}")
    os.makedirs(folder_path)

items = [
    {"name": "薬用スキンコンディショナー エッセンシャル", "brand": "アルビオン", "category": "化粧水", "price": 3300},
    {"name": "ハトムギ化粧水", "brand": "ナチュリエ", "category": "化粧水", "price": 715},
    {"name": "資生堂 オイデルミン エッセンスローション", "brand": "資生堂", "category": "乳液", "price": 6600},
    {"name": "乳液・敏感肌用・しっとりタイプ", "brand": "無印良品", "category": "乳液", "price": 490},
    {"name": "RMK バリアトリートメントエッセンス", "brand": "RMK", "category": "美容液", "price": 7150},
    {"name": "RMK Wトリートメントオイル", "brand": "RMK", "category": "美容オイル", "price": 4840},
    {"name": "THE アイパレ 01 本命のブラウン", "brand": "ビーアイドル", "category": "アイシャドウ", "price": 1980},
    {"name": "シピシピ グリッターイルミネーションライナー 101 フローズンホワイト", "brand": "CipiCipi", "category": "アイライナー", "price": 1540},
    {"name": "ロムアンド ハンオールブロウカラーマスカラ 03 ジントーンインディ", "brand": "ロムアンド", "category": "アイブロウ", "price": 880},
    {"name": "エチュセ アイエディション 19", "brand": "エチュセ", "category": "アイシャドウ", "price": 1540},
    {"name": "フジコ プランプモニュイリップ 01 王道", "brand": "Fujiko", "category": "リップ", "price": 1400},
    {"name": "BBIA ラストベルベットリップティント 01", "brand": "BBIA", "category": "リップ", "price": 1100},
    {"name": "ヴォワールコレクチュールn", "brand": "クレ・ド・ポー ボーテ", "category": "下地", "price": 7700},
    {"name": "ドラマティックフルイド プライマー ラベンダーカラー", "brand": "マキアージュ", "category": "下地", "price": 2970},
    {"name": "ナチュラルラディアント ロングウェア クッションファンデーション", "brand": "NARS", "category": "ファンデーション", "price": 7920},
    {"name": "ディオール フォーエヴァー スキン コレクト ファンデーション 00", "brand": "Dior", "category": "ファンデーション", "price": 7480},
    {"name": "Vim Beauty フェイスパウダー", "brand": "Vim Beauty", "category": "フェイスパウダー", "price": 2300},
    {"name": "ウォンジョンヨ ウォーターブルー ウォーターパウダー 01 クリアホワイト", "brand": "Wonjonyo", "category": "フェイスパウダー", "price": 1980}
]

data = [
    {
        "model": "app.cosmetic",
        "pk": index + 1,
        "fields": item
    }
    for index, item in enumerate(items)
]

# ファイルパスを指定して保存
file_path = os.path.join(folder_path, 'cosmetic.json')
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f'cosmetic.json has been created at {file_path}')
