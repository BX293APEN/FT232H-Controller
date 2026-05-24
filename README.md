# Linux上でFT232Hを動かす

FT232H を Debian 系 Linux 上で Python (Adafruit Blinka) から操作するためのセットアップスクリプトとコントローラクラスです。

## 動作環境

- OS : Debian 系 Linux (Ubuntu / Raspberry Pi OS 等)
- Python : 3.x
- 依存ライブラリ : `pyftdi`, `adafruit-blinka` (セットアップスクリプトで自動インストール)

## セットアップ

```bash
git clone https://github.com/BX293APEN/FT232H-Controller.git
cd FT232H-Controller
chmod 777 FT232H_SETUP.sh
./FT232H_SETUP.sh
```

セットアップスクリプトは以下を自動で行います。

- `libusb-1.0` のインストール
- udev ルール (`/etc/udev/rules.d/11-ftdi.rules`) への FT232H デバイスの登録
- `pyftdi` / `adafruit-blinka` のインストール
- `~/.bashrc` への環境変数 `BLINKA_FT232H=1` の追記

セットアップ後は **シェルを再起動**(または `source ~/.bashrc`)して環境変数を反映してください。

---

## ピン配置

FT232H のピン名と `board` モジュール上での名前の対応は以下の通りです。

| 機能 | ピン名 | board 上の名前 |
|------|--------|---------------|
| GPIO | D4 〜 D7 | `D4` 〜 `D7` |
| GPIO | C0 〜 C7 | `C0` 〜 `C7` |
| 特殊ピン (EEPROM) | C8, C9 | ソフトウェアから制御不可 ※後述 |
| I2C SCL | D0 | `SCL` |
| I2C SDA | D1/D2 | `SDA` |
| SPI SCK | D0 | `SCK` |
| SPI MOSI | D1 | `MOSI` |
| SPI MISO | D2 | `MISO` |
| SPI CS | D3 | `CS` |

> I2C と SPI はピンを共有しているため、同時に使用できません。

### C8 / C9 ピンについて

C8 と C9 はソフトウェアから GPIO として制御できません。これらのピンの機能は FT232H チップの EEPROM を書き換えることでのみ設定できます。ステータス LED の駆動や限定的な波形生成、固定レベル出力などを EEPROM で割り当てることができます。

- EEPROM の書き換えには Windows 専用ツール **FT PROG** が必要です。
- Adafruit のブレークアウトボードでは、**C8** に赤色 LED、**C9** に緑色 LED が実装されています(基板上の LED として使用)。
- Python コードからこれらのピンを `Pin()` で操作しようとしても制御できないため、使用しないでください。

---

## API リファレンス

### `FT232H` クラス (`src/FT232H.py`)

FT232H を操作するためのラッパークラスです。  
インスタンス生成時に `BLINKA_FT232H=1` が設定されていない場合は自動で設定します。

---

#### コンストラクタ

```python
ft232h = FT232H()
```

`board` モジュールをインポートし、GPIO ピン (`C0`) が利用可能な場合は `digitalio` / `busio` もインポートします。

---

#### `check_pin(pinName: str) -> bool`

指定したピン名が `board` モジュールに存在するかを確認します。

```python
ft232h.check_pin("C7")   # True / False
```

| 引数 | 型 | 説明 |
|------|----|------|
| `pinName` | `str` | ピン名 (例: `"C7"`, `"D4"`, `"SCL"`) |

**戻り値** : `bool` — ピンが存在すれば `True`

---

#### `Pin(pinName: str, mode=None)`

指定したピンオブジェクトを返します。

```python
# ピンオブジェクトのみ取得
pin = ft232h.Pin("C7")

# GPIO 出力として取得
led = ft232h.Pin("C7", ft232h.OUT)
led.value = True   # HIGH (点灯)
led.value = False  # LOW  (消灯)

# GPIO 入力として取得
btn = ft232h.Pin("C0", ft232h.IN)
print(btn.value)   # True / False
```

| 引数 | 型 | 説明 |
|------|----|------|
| `pinName` | `str` | ピン名 |
| `mode` | `Direction` or `None` | `ft232h.OUT` / `ft232h.IN` / `None` |

**戻り値** :
- `mode=None` のとき : `board` のピンオブジェクト
- `mode` 指定時 : `digitalio.DigitalInOut` オブジェクト (`.value` で読み書き可能)
- ピンが存在しない場合 : `None`

| 定数 | 説明 |
|------|------|
| `ft232h.OUT` | デジタル出力 (`digitalio.Direction.OUTPUT`) |
| `ft232h.IN`  | デジタル入力 (`digitalio.Direction.INPUT`) |

---

#### `I2C() -> busio.I2C | None`

I2C バスオブジェクトを生成して返します。  
`SCL` ピンが利用可能なときのみ動作します。

```python
i2c = ft232h.I2C()
```

**戻り値** : `busio.I2C` オブジェクト。`SCL` が存在しない場合は `None`。

生成した I2C オブジェクトは Adafruit の CircuitPython ライブラリにそのまま渡せます。

```python
import adafruit_bme280
i2c   = ft232h.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
print(bme280.temperature)
```

---

## I2C 使用例

### 追加ライブラリのインストール

```bash
# SSD1306 OLEDドライバ
sudo pip install adafruit-circuitpython-ssd1306 --break-system-packages
# 画像生成 (Pillow)
sudo pip install pillow --break-system-packages
```

---

### SSD1306 OLED ディスプレイへの表示

128×64 ピクセルの SSD1306 OLED ディスプレイ(I2C アドレス `0x3C`)にテキストを描画するサンプルです。

```python
from src.FT232H import FT232H
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

ft232h = FT232H()
i2c = ft232h.I2C()

# ディスプレイの初期化 (幅128, 高さ64, アドレス0x3C)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled_w = display.width   # 128
oled_h = display.height  # 64

# Pillow で描画バッファを作成 ("1" = 1bit モノクロ)
image = Image.new("1", (oled_w, oled_h))
draw  = ImageDraw.Draw(image)

# 背景を黒で塗りつぶす (fill=0)
draw.rectangle((0, 0, oled_w - 1, oled_h - 1), outline=0, fill=0)

# フォントを読み込んでテキストを描画
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
draw.text((3, 0), "Hello, FT232H!", font=font, fill=1)  # fill=1 で白文字

# OLEDに転送して表示
display.image(image)
display.show()
```

#### 1文字ずつアニメーション表示

```python
text = "Hello, FT232H!"
for i in range(1, len(text) + 1):
    draw.rectangle((0, 0, oled_w - 1, oled_h - 1), outline=0, fill=0)  # 毎フレーム背景クリア
    draw.text((3, 0), text[:i], font=font, fill=1)
    display.image(image)
    display.show()
```

> **Pillow の "1" モード(1bit モノクロ)について**
> `fill=0` が黒(消灯)、`fill=1` が白(点灯)です。  
> 背景と文字の色を反転させたい場合は `fill` の値を入れ替えてください。

---

### I2C デバイスへの直接読み書き

Adafruit Blinka の `busio.I2C` オブジェクトは `writeto` / `readfrom_into` で任意のデバイスと通信できます。  
以下は RX8900 リアルタイムクロックから温度レジスタ (`0x17`) を読み取るサンプルです。

```python
from src.FT232H import FT232H

ft232h = FT232H()
i2c = ft232h.I2C()

DEVICE_ADDR = 0x32  # デバイスの I2C アドレス

# レジスタ 0x17 へ書き込み(読み出し先の指定)
i2c.writeto(DEVICE_ADDR, bytes([0x17]))

# 1バイト読み取り
result = bytearray(1)
i2c.readfrom_into(DEVICE_ADDR, result)

# RX8900 の温度変換式
raw = result[0]
temp = (raw * 2 - 187.19) / 3.218
print(f"{round(temp, 3)} ℃")
```

#### I2C 通信の主なメソッド

| メソッド | 説明 |
|----------|------|
| `i2c.writeto(addr, buf)` | `addr` に `bytes` / `bytearray` を送信 |
| `i2c.readfrom_into(addr, buf)` | `addr` から `buf` の長さ分だけ受信 |
| `i2c.writeto_then_readfrom(addr, out, in_buf)` | 書き込み → 読み取りをアトミックに実行 |
| `i2c.scan()` | バス上のデバイスアドレス一覧を返す |

デバイスのアドレスが不明な場合は `i2c.scan()` でスキャンできます。

```python
print([hex(addr) for addr in i2c.scan()])
# 例: ['0x3c', '0x32']
```

---

## サンプル実行 (Lチカ)

`src/FT232H.py` を直接実行すると、**C7 ピン**に接続した LED を 1 秒間隔で点滅させるサンプルが動作します。

```bash
python3 src/FT232H.py
```

終了するには `Ctrl+C` を押してください。

**回路** : C7 と GND の間に LED と電流制限抵抗 (330Ω 程度) を直列に接続してください。

---

## 参考文献

- [Adafruit — CircuitPython Libraries on any Computer with FT232H (Linux)](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/linux)
