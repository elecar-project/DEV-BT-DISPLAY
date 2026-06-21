# A05-8 客製停用詞建議 - repl_tok(para12-80)

## 資料來源

- 主要參考：`Result/06.03_A04_min-test/A04-6(repl)_tok(para12-80)/topic_words.csv`
- 輔助參考：
  - `Result/06.03_A04_min-test/A04-6(repl)_tok(para12-80)/final_models/best_balance/topic_words.csv`
  - `Result/06.03_A04_min-test/A04-6(repl)_tok(para12-80)/final_models/most_topics/topic_words.csv`
  - `Result/06.03_A04_min-test/A04-6(repl)_tok(para12-80)/final_models/lowest_noise/topic_words.csv`

判斷原則：保留與電動車技術、能源、充電、電池、續航、電驅、再生煞車、混合動力直接相關的詞；移除逐字稿口語填充詞、品牌/車款替換佔位詞、影片寒暄、泛用汽車詞，以及會讓 BERTopic 產生非 EV 主題的外觀、內裝、車機、操作示範詞。

## 核心建議停用詞

| 停用詞類型 | 原因 | 停用詞 |
| --- | --- | --- |
| repl 佔位詞與衍生片語 | `repl` 語料把品牌/車款替換成 `brand`、`model` 後，這些詞在 topic words 中高頻出現，但不提供可解釋的 EV 語意，會形成「品牌/車款佔位」主題。 | brand, model, brand model, brand brand, new brand, new model, brand charge |
| 逐字稿寒暄與影片流程詞 | 這些詞來自主持人開場、結尾、問候或訪談流程，與電動車主題無直接關聯，且已形成獨立 topic。 | thank, thanks, welcome, bye, joining, today, doing, hope, good, great, gentlemen, questions |
| 口語填充與對話慣用詞 | `don know`、`yeah`、`okay` 等詞反映口語互動，不代表 EV 技術或產品語意，會稀釋 topic words。 | okay, yeah, don, know, don know, know don, said, let, going, want, right, really, just, like, kind, sort, ve |
| 過度泛用汽車詞 | `car`、`vehicle`、`new` 在幾乎所有汽車文本都會出現，區分力低；若保留，容易讓 topic words 變成泛汽車描述，而不是 EV 子主題。 | car, cars, vehicle, vehicles, new, available |
| 人名、來源與辨識雜訊 | topic words 中出現主持人/受訪者姓名、來源名稱或疑似轉寫/品牌殘留，對 EV 主題分類沒有穩定解釋力。 | robin, chris, auto evolution, candy, k23 |
| 保固/數字片段雜訊 | `000`、`whichever comes` 等通常來自保固條款句型，容易形成售後條款或數字噪音 topic；若研究不分析保固，建議停用。 | 000, 000 mile, 000 miles, whichever, whichever comes |

## 可選擇停用詞

若你的研究目標是「電動車技術、能源與充電敘事」，而不是完整車評主題，以下詞也建議加入。若你仍想分析外觀、內裝、車機或產品定位，則不要全部加入。

| 停用詞類型 | 原因 | 停用詞 |
| --- | --- | --- |
| 外觀/設計主題詞 | 這些詞會讓 BERTopic 分出外觀、燈具、車身線條、設計流程等主題，但它們多半不是 EV 專屬語意。 | design, look, beautiful, grille, rear, led, light, lights, headlights, signature, laser, tail, beam, line, lines, shape, stance, hood, sketch, sketches, clay, designers, black |
| 輪圈/等級/尺寸詞 | 多出現在配備與車型等級介紹，與 EV 核心主題關聯弱。 | wheels, wheel, alloy, alloy wheels, inch, grades, xse, xle, se |
| 內裝/座椅/空間詞 | 這些詞會產生內裝舒適性或行李空間主題；若目標是 EV 技術主題，可視為非核心。 | seats, seat, seating, leather, comfort, interior, massage, driver seat, comfort seat, trimmed, inside, space, room, cargo, cubic, cubic feet, feet, luggage, row |
| 車機/娛樂/連線詞 | topic words 中已形成 Apple CarPlay、Android Auto、MBUX、Blue Link 等車機主題；這些不是 EV 技術本體。 | audio, apple, carplay, apple carplay, android, android auto, wireless, touchscreen, mbux, display, displays, screen, navigation, functions, head display, information, blue link, link, google, profile, smartphone, phone, connected, remote |
| 操作示範詞 | 這些詞多來自車評影片中示範按鍵、尾門、門把或介面操作，不代表 EV 主題。 | door, temperature, tailgate, button, open, press, turn, release, cover, key, digital key, digital |
| ICE 或非 EV 車型語境 | 若研究只看純 EV/電動化敘事，傳統燃油引擎、變速箱、汽缸等詞會引入 ICE 主題；但若要比較 hybrid/ICE，請不要停用整組。 | engine, liter, cylinder, transmission, turbo, gas |
| 車身級距與市場定位詞 | sedan、coupe、SUV、luxury 等會形成車型級距/市場定位主題；若 EV 主題要更聚焦，建議停用。 | sedan, coupe, midsize, segment, suv, fleet, luxury |
| 市場/商業泛詞 | 這些詞可解釋為市場或品牌策略，但不是 EV 技術語意；若研究不做市場策略分析，建議停用。 | product, products, customer, customers, sales, market, markets, global, world, china, america |

## 建議給 CountVectorizer 的單字停用詞清單

`CountVectorizer(stop_words=...)` 主要會先移除單字 token，因此多字片語通常應透過移除組成單字來處理。以下清單偏向可直接使用的單字版。

```text
000
alloy
america
android
apple
audio
available
beam
beautiful
black
blue
brand
button
bye
candy
car
carplay
cars
china
chris
clay
connected
coupe
cover
cubic
customer
customers
cylinder
design
designers
digital
display
displays
doing
don
door
engine
feet
fleet
functions
gas
gentlemen
global
good
google
grades
great
grille
headlights
hood
hope
inch
information
inside
interior
joining
just
k23
key
kind
know
laser
leather
led
let
light
lights
like
line
lines
link
liter
luggage
luxury
market
markets
mbux
midsize
model
navigation
new
okay
open
phone
press
product
products
profile
questions
rear
release
remote
really
robin
room
row
said
sales
screen
se
seat
seating
seats
sedan
shape
signature
sketch
sketches
smartphone
sort
space
stance
tail
tailgate
temperature
thank
thanks
today
touchscreen
transmission
trimmed
turbo
turn
ve
vehicle
vehicles
welcome
wheel
wheels
whichever
wireless
world
xle
xse
yeah
```

## 不建議加入停用詞的 EV 核心詞

以下詞在目前 topic words 中雖然高頻，但它們是電動車主題的重要語意錨點，不建議加入停用詞：

```text
electric
ev
electrification
electrified
charging
charge
charger
charging stations
charging station
battery
battery pack
range
miles
kilometers
volt
kilowatt
dc
motor
torque
horsepower
performance
plug
plug hybrid
hybrid
regenerative
regenerative braking
regen
brake
brakes
energy
lithium
lithium ion
ion
cells
cooling
pack
batteries
```

## 使用建議

1. 先使用「核心建議停用詞」重跑 BERTopic，檢查 topic words 是否仍有寒暄、佔位詞與口語詞。
2. 若仍有大量外觀/內裝/車機 topic，且研究問題只關心 EV 技術，再逐步加入「可選擇停用詞」。
3. 不建議一次刪掉所有汽車詞，尤其不要刪除 `charging`、`battery`、`range`、`ev`、`electric`，否則會把真正的 EV 語意也清掉。
