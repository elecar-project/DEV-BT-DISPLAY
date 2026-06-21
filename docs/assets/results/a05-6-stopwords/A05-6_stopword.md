# A05-6 客製停用詞建議 - repl_tok(para12-80)

資料來源：`Result/06.03_A04_min-test/A04-6(repl)_tok(para12-80)/`

檢視重點：

- `final_models/best_balance/topic_words.csv`
- `final_models/best_balance/topic_info.csv`
- `topic_words.csv`
- `topic_info.csv`

本清單目標是移除與「電動車、電動化、充電、電池、續航、動力系統、能源效率、減碳與車用技術」無直接關聯、但在 BERTopic topic words 中反覆出現並干擾主題命名的詞。

## 建議停用詞表

| 停用詞類型 | 原因 | 停用詞 |
|---|---|---|
| 資料匿名化替代詞 | `Brand`、`Model` 是前處理替換後的佔位詞，會大量主導 topic words，但不能提供具體 EV 語意。 | brand, model, brand model, brand brand, new brand, new model, model brand, brand new, model hybrid, model ev, model electric |
| 過度泛化車輛詞 | 這些詞雖和汽車有關，但太泛用，會讓主題停留在「車」而不是 EV 技術、充電、電池或市場議題。建議先列為可選停用詞，若後續 topic 太碎可保留部分詞。 | car, cars, vehicle, vehicles, auto, automotive |
| 新品發表泛詞 | 常見於新車發表稿，不指向 EV 主題本身，容易把不同車型介紹混在一起。 | new, all new, latest, generation, lineup, grade, grades, trim, trims, version, variants, package, packages, product, products |
| 口語填充詞 | 來自逐字稿口語，對主題命名沒有貢獻，會產生 `don/know/right/yeah/going` 類型的無意義主題。 | just, like, really, actually, basically, kind, kind of, sort, sort of, pretty, quite, little, lot, bit, maybe, probably, simply, certainly |
| 對話與認知動詞 | 多出現在試駕、訪談或主持人講話中，與 EV 主題無關。 | know, think, want, going, gonna, don, dont, don know, let, let me, see, look, looking, feel, feels, get, got, make, made, makes, come, comes, came |
| 方向與操作泛詞 | 在車內功能示範中高頻出現，但多是操作步驟，不是 EV 研究核心。 | right, left, front, back, inside, outside, open, close, press, push, pull, turn, release, button, buttons, cover, tab, place, use, using |
| 發表會寒暄詞 | 形成 `thank/good/bye/welcome` 等獨立主題，與車輛技術或 EV 市場無關。 | thank, thanks, thank you, good, morning, afternoon, evening, bye, goodbye, welcome, joining, join, joined, doing, hope, great, today, tonight |
| 舞台與媒體流程詞 | 來自車展、發表會、拍照流程，會把語料切成活動流程主題，而不是 EV 主題。 | stage, invite, like invite, photo, photos, photographer, photographers, gentlemen, ladies, everyone, audience, applause, presentation, show, unveil, reveal |
| 人名與稱謂 | 這類詞通常代表主持人、設計師或主管名字，對 EV 主題分類沒有穩定意義。 | mr, mrs, ms, mark, chris, robin, jeff |
| 時間與年份泛詞 | 年份與時間單位本身通常不構成 EV 主題，除非研究問題特別要分析年份演進。 | year, years, day, days, month, months, week, weeks, spring, summer, fall, winter, 2010, 2015, 2020, 2021, 2022, 2023, 2024, 2025 |
| 數字與保固模板詞 | `000`、`whichever comes` 等來自保固/里程模板，容易產生低價值 topic。保留 `mile/miles` 可視研究是否分析續航；若續航主題受影響，不建議刪除 miles。 | 000, 100 000, 000 mile, 000 miles, whichever, whichever comes, comes first, unlimited mileage, scheduled maintenance, roadside assistance |
| 市場與銷售泛詞 | 可描述品牌營運，但不直接對應 EV 技術；若研究包含市場策略，可改列為可選停用詞。 | market, markets, sales, sell, selling, sold, customers, customer, people, owner, owners, buyer, buyers |
| 價格購買泛詞 | 價格可作為市場議題，但目前 topic words 中常與口語購買建議混雜，若主題目標是 EV 技術，建議移除。 | price, cost, affordable, buy, buying, pay, paid, value |
| 地名與車展詞 | 多反映發表地點或車展場景，不是 EV 主題本身。 | detroit, la, los, angeles, los angeles, america, china, us, u s, motor city, auto show, auto season |
| 影片與頻道詞 | 來源於 YouTube/媒體語境，會干擾車輛主題。 | video, videos, channel, subscribe, youtube, stream, streaming, clip, episode |
| 一般評價形容詞 | 情緒或評價詞太泛化，不能區分 EV 子議題。 | beautiful, nice, exciting, excited, impressive, amazing, perfect, strong, better, best, important, successful |
| 內裝舒適泛詞 | 若研究主題聚焦 EV，這類座椅/內裝詞會形成與電動車無關的舒適配備主題；若要保留完整汽車產品分析，則可不刪。 | seats, seat, interior, space, leather, heated, ventilated, cargo, cabin, comfort |
| 車身外觀泛詞 | 外觀設計可形成非 EV 主題；若目標是電動車技術與市場，建議刪除或降權。 | grille, rear, led, light, lights, headlights, tail, beam, signature, look, design, sketch, sketches, clay |
| 一般資訊娛樂詞 | `Apple CarPlay/Android Auto` 是車機配備，不直接代表 EV；若研究包含智慧座艙，則可保留。 | audio, apple, carplay, apple carplay, android, android auto, touchscreen, screen, display, displays, information, navigation, functions |
| 車門與空調操作詞 | 多是使用手冊或功能示範語言，不構成 EV 子題。 | door, doors, tailgate, hood, temperature, climate control, key fob, footwell |
| 非研究核心品牌/車系詞 | A04 topic words 中出現部分品牌/車系或展演詞，若研究已用 `Brand/Model` 匿名化，殘留專名會造成偏移。 | toyotacare, siriusxm, mymazda, mazda, mbux, amg, quattro, tnga, egmp, xse, xle, se, gt, gt3, k23, candy |

## 建議保留的 EV 核心詞

以下詞雖然高頻，但與電動車主題直接相關，不建議放入停用詞：

| 類型 | 建議保留詞 |
|---|---|
| 電動化核心 | electric, ev, electrification, electrified, electric vehicle, electric car, battery electric |
| 充電與補能 | charging, charge, charger, charging station, charging stations, dc, fast charging, level 1, level 2, level 3 |
| 電池與能源 | battery, battery pack, lithium, lithium ion, cells, kilowatt, kilowatt hour, kwh, volt |
| 續航與效率 | range, miles, kilometers, mpge, fuel economy, efficiency |
| 動力與控制 | motor, torque, regenerative, regenerative braking, regen, brake, braking, pedal |
| 環境與政策語意 | emissions, zero, co2, sustainable, climate, environment |

## Python list 版本

```python
custom_stopwords = [
    "brand", "model", "brand model", "brand brand", "new brand", "new model", "model brand",
    "brand new", "model hybrid", "model ev", "model electric",
    "car", "cars", "vehicle", "vehicles", "auto", "automotive",
    "new", "all new", "latest", "generation", "lineup", "grade", "grades", "trim", "trims",
    "version", "variants", "package", "packages", "product", "products",
    "just", "like", "really", "actually", "basically", "kind", "kind of", "sort", "sort of",
    "pretty", "quite", "little", "lot", "bit", "maybe", "probably", "simply", "certainly",
    "know", "think", "want", "going", "gonna", "don", "dont", "don know", "let", "let me",
    "see", "look", "looking", "feel", "feels", "get", "got", "make", "made", "makes",
    "come", "comes", "came",
    "right", "left", "front", "back", "inside", "outside", "open", "close", "press", "push",
    "pull", "turn", "release", "button", "buttons", "cover", "tab", "place", "use", "using",
    "thank", "thanks", "thank you", "good", "morning", "afternoon", "evening", "bye",
    "goodbye", "welcome", "joining", "join", "joined", "doing", "hope", "great", "today",
    "tonight",
    "stage", "invite", "like invite", "photo", "photos", "photographer", "photographers",
    "gentlemen", "ladies", "everyone", "audience", "applause", "presentation", "show",
    "unveil", "reveal",
    "mr", "mrs", "ms", "mark", "chris", "robin", "jeff",
    "year", "years", "day", "days", "month", "months", "week", "weeks", "spring", "summer",
    "fall", "winter", "2010", "2015", "2020", "2021", "2022", "2023", "2024", "2025",
    "000", "100 000", "000 mile", "000 miles", "whichever", "whichever comes",
    "comes first", "unlimited mileage", "scheduled maintenance", "roadside assistance",
    "market", "markets", "sales", "sell", "selling", "sold", "customers", "customer",
    "people", "owner", "owners", "buyer", "buyers",
    "price", "cost", "affordable", "buy", "buying", "pay", "paid", "value",
    "detroit", "la", "los", "angeles", "los angeles", "america", "china", "us", "u s",
    "motor city", "auto show", "auto season",
    "video", "videos", "channel", "subscribe", "youtube", "stream", "streaming", "clip",
    "episode",
    "beautiful", "nice", "exciting", "excited", "impressive", "amazing", "perfect",
    "strong", "better", "best", "important", "successful",
    "seats", "seat", "interior", "space", "leather", "heated", "ventilated", "cargo",
    "cabin", "comfort",
    "grille", "rear", "led", "light", "lights", "headlights", "tail", "beam", "signature",
    "look", "design", "sketch", "sketches", "clay",
    "audio", "apple", "carplay", "apple carplay", "android", "android auto", "touchscreen",
    "screen", "display", "displays", "information", "navigation", "functions",
    "door", "doors", "tailgate", "hood", "temperature", "climate control", "key fob",
    "footwell",
    "toyotacare", "siriusxm", "mymazda", "mazda", "mbux", "amg", "quattro", "tnga",
    "egmp", "xse", "xle", "se", "gt", "gt3", "k23", "candy",
]
```

## 使用建議

1. 第一輪建議先套用「資料匿名化替代詞、口語填充詞、發表會寒暄詞、舞台與媒體流程詞、數字與保固模板詞」。
2. 第二輪再視主題需求加入「過度泛化車輛詞、內裝舒適泛詞、車身外觀泛詞、一般資訊娛樂詞」。
3. 若研究問題包含市場策略、智慧座艙或整體產品定位，不建議一次刪除市場、資訊娛樂、內裝與外觀類詞。
4. 不建議刪除 `electric`、`ev`、`battery`、`charging`、`range`、`hybrid`、`motor`、`regenerative` 等 EV 核心詞。
