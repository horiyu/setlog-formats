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
| `snow` | 雪 | 大粒の雪が吹きつける。手前はぼけて速く、奥は物の後ろに回り込む |
| `sakura` | 花吹雪 | 桜吹雪が風にあおられて画面いっぱいに舞う |
| `bubbles` | シャボン玉 | 大小の虹色シャボン玉が次々に湧き上がる |
| `confetti` | 紙吹雪 | 四隅と真ん中から紙吹雪が何度も打ち上がって、きらきら降ってくる |
| `note` | 置き手紙 | 一言を札にしてその場に置く。カメラが動いても置いた場所に残り、人の後ろに隠れる |
| `speech` | 吹き出し | 写っている人の頭の上に、一言の吹き出しがついていく |
| `aura` | オーラ | 人の輪郭がゆらめく光をまとう |
| `elsewhere` | 異世界 | 人だけ残して、背景を宇宙・水中・絵画のどれかに（投稿ごとにランダム） |
| `afterimage` | 残像 | 動いたものが色を変えながら尾を引く |
| `glitch` | グリッチ | ときどき画面がずれて裂ける |
| `thermal` | サーマル | 熱カメラの色と計測表示 |
| `neon` | ネオン | 景色が暗く沈んで、輪郭だけが色を変えながら光る |

雪から残像までとグリッチ・ネオンは、絵を見て描くエフェクト（下の「AR のエフェクト」）を使う。setlog-remix 側で
`bin/setup-ar.sh` が済んでいること。GPU は要らず、普通のノート PC の CPU で 3 秒の動画が 30 秒ほどで描ける。

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
| `thermal` | `palette` inferno（`inferno` `magma` `plasma` `turbo` `heat` `fiery` `cool`）、`contrast` 1.3（0.5–3）、`blur` 2（0–10）。熱カメラ風の色 |

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

### AR のエフェクト

絵の中身（人の形・奥行き・カメラの動き）を見て描く。小さなモデルを CPU で回す（人の切り抜き MODNet、奥行き
Depth Anything V2 Small）。人がいないときは、人の代わりに一番手前のものを使う。大きさ・長さは枠（1710×962）の高さに対する割合。

| type | パラメータ（既定） |
|---|---|
| `particles` | `kind`（`snow` `petals` `bubbles` `confetti`）、`count`（1–900）、`size`（粒の大きさ、高さに対する割合 0.002–0.1）、`speed`（0–3）、`wind`（横風 -1–1）、`opacity` 0.9、`depth`（奥の粒を物の後ろに隠す。紙吹雪以外は true）、`seed`。紙吹雪だけ `bursts`（打ち上げの回数と場所 1–4、既定 1）と `glitter`（金銀のきらめく粒の割合 0–1、既定 0.2） |
| `pin` | `text` "{caption}"、`style`（`card` 白い札 / `neon` 光る文字）、`size` 60（px）、`tilt` -4（度）、`auto` true（人と重ならない場所を選ぶ。false なら `x` `y` 0–1 の位置）、`behind_people` true（人が前を通ると隠れる）、`appear` 0.15（秒、ぽんと出る）、`font`、`uppercase` |
| `speech` | `text` "{caption}"、`size` 52（px）、`appear` 0.15（秒）、`font`、`uppercase`。人の頭の上についていく吹き出し |
| `aura` | `width` 0.04、`strength` 0.8（0–2）、`cycle` true（色が移り変わる。false なら `color`）、`hue` 0.55、`color` |
| `background` | `files`（必須、画像 1–8 枚のリスト）、`choose`（`random` 投稿ごとに1枚 / `first`）、`subject`（`auto` `person` `near`、何を前に残すか）、`drift` 0.06（背景がゆっくり寄る量） |
| `glitch` | `amount` 0.5（0–1）、`rate` 2（1 秒あたりの乱れの回数）、`seed` |
| `neon` | `thickness` 2（線の太さ 1–6）、`glow` 0.8（0–2）、`dim` 0.12（元の景色の明るさ 0–1）、`cycle` 0.35（色が流れる速さ、0 なら `color` の単色）、`color` |
| `trail` | `decay` 0.9（尾の残り方 0.5–0.99）、`hue_shift` 0.6（尾の色が回る速さ）、`strength` 0.9 |

変数: `{caption}`（ショートカットで入れた一言）、`{format}`（フォーマット名）、`{speed}`（再生倍率）、
`{date}` `2026.09.28`、`{time}` `21:07`、`{datetime}`、`{year}` `{month}` `{day}` `{hour}` `{minute}` `{second}`、
`{weekday}` `Mon`、`{weekday_ja}` `月`。日時の変数は `{date:%b. %d %Y}` のように strftime の書式も取れる。
日時は動画の撮影時刻（無ければ受け取った時刻）。

### ファイル

`lut` の `file`、`image` の `file`、`text` の `font` は、その format.json からの相対パス。リポジトリの外は指せない。
共通のファイルは `assets/` に置いて `../../assets/xxx` と書く。1ファイル 20MB まで。
`assets/teal-orange.cube` は `tools/make_cube.py` で作っている。`assets/backgrounds/` の3枚（宇宙・水中・絵画）は画像生成で作ったもの。

### 確かめる

setlog-remix を手元に置いて:

```sh
python3 ../setlog-remix/render.py check formats/*                                       # 書式の確認
python3 ../setlog-remix/render.py render formats/vhs 動画.mov out.mp4 --caption "一言"    # 描いてみる
python3 ../setlog-remix/render.py sheet out.mp4 out.png                                  # 4コマに並べる
```

## ライセンス

[MIT License](LICENSE)。作: [horiyu](https://github.com/horiyu)。
