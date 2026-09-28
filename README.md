# setlog-formats

[setlog-remix](https://github.com/horiyu/setlog-remix) 用のフォーマット集。iPhone のショートカットで撮った動画を、
ここにあるフォーマット（エフェクトと編集の型）で仕上げてから [setlog](https://setlog.kr/) に送る。

ショートカットにこのリポジトリ（`horiyu/setlog-formats`）を書いておくと、撮ったあとにフォーマットの一覧が出る。
自分のフォーマットを作るなら、このリポジトリを fork するか、同じ形のリポジトリを作ってショートカットの
リポジトリ名を書き換えるだけでいい。

*Formats for setlog-remix: point the iOS Shortcut at a repository like this one and pick a format after
shooting. A format is a JSON file — no code runs — so anyone can publish one.*

| id | 名前 | 中身 |
|---|---|---|
| `plain` | そのまま | 最初の3秒を枠いっぱいに |
| `vhs` | VHS | 色あせ・にじみ・走査線・ノイズ、`▶ PLAY` と日付時刻 |
| `film` | シネマ | ティール＆オレンジの LUT、シネスコの黒帯、一言を字幕に |
| `mono` | モノクロ | 硬めの白黒と粒子、日付と曜日 |
| `timelapse` | タイムラプス | 撮ったぶん全部を 2.5 秒に早回し、倍率を表示 |
| `boomerang` | ブーメラン | 最初の 1.3 秒を行って戻る |
| `pixel` | ドット | 粗いドットに潰して、一言を下に |

## フォーマットの作り方

`formats/<id>/format.json` を1つ置くと1つのフォーマットになる。`<id>` は英数字とハイフン。

```json
{
  "spec": 1,
  "name": "VHS",
  "description": "90年代のホームビデオ。日付入り",
  "order": 10,
  "clip": { "mode": "head", "duration": 3 },
  "frame": { "mode": "fill" },
  "effects": [
    { "type": "grade", "contrast": 1.12, "saturation": 0.78, "temperature": 0.35 },
    { "type": "scanlines", "spacing": 3, "opacity": 0.22 },
    { "type": "text", "text": "{date:%b. %d %Y}", "uppercase": true, "position": "bottom-right" }
  ]
}
```

出来上がりは **1710×962・30fps・音なし**（setlog が撮る横長の枠）。setlog の Log に残るのは頭から **2 秒ちょっと**
なので、見せたいものは最初の 2 秒に置く。数値は範囲外だとエラーになる。知らないキーもエラー（打ち間違いに気づけるように）。

### いちばん上

| キー | 既定 | |
|---|---|---|
| `spec` | 1 | 書式の版。今は 1 |
| `name` | id | 一覧に出る名前（40字まで） |
| `description` | "" | 一覧で名前の横に出る説明（120字まで） |
| `order` | 100 | 一覧の並び順（小さいほど上） |
| `author` | "" | 作者 |
| `clip` | | どこを使うか（下） |
| `frame` | | 枠への収め方（下） |
| `effects` | [] | 上から順にかかるエフェクト（24個まで） |

### clip

| キー | 既定 | 範囲 | |
|---|---|---|---|
| `mode` | `head` | `head` / `middle` / `tail` / `fit` | 頭から / 真ん中 / お尻 / 全部を `duration` に早回し |
| `start` | 0 | 0–3600 | `head` は頭から何秒飛ばすか、`tail` はお尻から何秒手前で終えるか |
| `duration` | 3 | 0.5–15 | 出来上がりの秒数 |
| `speed` | 1 | 0.25–8 | 再生速度（`fit` では自動） |
| `loop` | `none` | `none` / `reverse` / `boomerang` | 逆再生 / 行って戻る（前半 `duration/2` を往復） |

### frame

| キー | 既定 | |
|---|---|---|
| `mode` | `fill` | `fill` は切り取って枠いっぱい、`fit` は全体を収めて余白をぼかしで埋める |
| `turn` | `none` | 縦の動画を `ccw`（左回り）/ `cw`（右回り）に倒してから収める |
| `background` | `#0E0E10` | 予備の背景色 |

### effects

各エフェクトは `{"type": "<種類>", ...}`。色は `#RRGGBB`・`#RRGGBBAA`・`white` `black` `red` `yellow` `green` `blue` `orange` `gray`。

| type | パラメータ（既定） |
|---|---|
| `grade` | `brightness` 0（-1–1）、`contrast` 1（0–3）、`saturation` 1（0–3）、`gamma` 1（0.1–5）、`hue` 0（-180–180 度）、`temperature` 0（-1 寒色 – 1 暖色） |
| `mono` | なし。白黒 |
| `sepia` | `amount` 1（0–1） |
| `invert` | なし。ネガ |
| `mirror` | なし。左右反転 |
| `grain` | `amount` 20（0–100）。ノイズ |
| `vignette` | `strength` 0.5（0–1）。周辺減光 |
| `blur` | `radius` 4（0–60） |
| `sharpen` | `amount` 1（0–3） |
| `pixelate` | `size` 16（2–200）。1 ドットのピクセル数 |
| `rgbshift` | `amount` 6（0–60）。赤と青をずらす色収差 |
| `scanlines` | `spacing` 4（2–40）、`opacity` 0.3（0–1） |
| `letterbox` | `ratio` 2.39（1.78–4）、`color` black。上下の黒帯 |
| `fade` | `in` 0、`out` 0（秒、0–5）、`color` `black` / `white` |
| `zoom` | `from` 1、`to` 1.15（1–3）。ゆっくり寄る |
| `lut` | `file`（必須）。`.cube` の 3D LUT |
| `text` | 下の表 |
| `image` | `file`（必須、PNG / JPEG）、`position` center、`margin` 0、`width` 1710（px）、`opacity` 1、`from` / `until`（秒） |

`text`:

| キー | 既定 | |
|---|---|---|
| `text` | （必須） | 200字まで。改行は `\n`。下の変数が使える |
| `font` | `sans` | `sans` / `sans-bold` / `serif` / `mono`（PC のフォント）か、リポジトリ内の `.ttf` `.otf` `.ttc` |
| `size` | 48 | 文字の大きさ（px、8–400） |
| `color` | white | |
| `position` | `bottom-right` | `top-left` `top` `top-right` `left` `center` `right` `bottom-left` `bottom` `bottom-right` |
| `margin` | 48 | 枠の端からの距離（px） |
| `uppercase` | false | 大文字にする |
| `box` / `box_color` | false / `#00000080` | 文字の後ろに帯 |
| `shadow` / `shadow_color` | 0 / `#000000B0` | 影のずれ（px） |
| `border` / `border_color` | 0 / black | 縁取りの太さ（px） |
| `from` / `until` | 0 / 0 | 表示する時間（秒）。0 は最初から / 最後まで |

変数: `{caption}`（ショートカットで入れた一言）、`{format}`（フォーマット名）、`{speed}`（再生倍率）、
`{date}` `2026.09.28`、`{time}` `21:07`、`{datetime}`、`{year}` `{month}` `{day}` `{hour}` `{minute}` `{second}`、
`{weekday}` `Mon`、`{weekday_ja}` `月`。日時の変数は `{date:%b. %d %Y}` のように strftime の書式も取れる。
日時は動画の撮影時刻（無ければ受け取った時刻）。

### ファイル

`lut` の `file`、`image` の `file`、`text` の `font` は、その format.json からの相対パス。リポジトリの外は指せない。
共通のファイルは `assets/` に置いて `../../assets/xxx` と書く。1ファイル 20MB まで。
`assets/teal-orange.cube` は `tools/make_cube.py` で作っている。

### 確かめる

setlog-remix を手元に置いて:

```sh
python3 ../setlog-remix/render.py check formats/*                                       # 書式の確認
python3 ../setlog-remix/render.py render formats/vhs 動画.mov out.mp4 --caption "一言"    # 描いてみる
python3 ../setlog-remix/render.py sheet out.mp4 out.png                                  # 4コマに並べる
```

## ライセンス

[MIT License](LICENSE)。作: [horiyu](https://github.com/horiyu)。
