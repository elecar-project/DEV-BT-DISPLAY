# M02-8New LLM30 Validation

- model: `openai/gpt-5.5` via OpenRouter
- runs per non-noise topic: 30
- input per topic: same default c-TF-IDF keywords and same first 6 representative topic documents
- stable rule: `mode_ratio >= 0.70` or `avg_jaccard_to_mode >= 0.65`
- stable topics: 20 / 24

| topic | successful_runs | unique_normalized_labels | mode_label | mode_ratio | avg_jaccard_to_mode | stable | keywords |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 30 | 13 | Hybrid Vehicle Design | 0.2333 | 0.6817 | True | new, car, design, electric, bmw, rear, drive, vehicle, hybrid, power |
| 1 | 30 | 10 | Driver Assistance and Infotainment | 0.5000 | 0.7733 | True | display, control, car, navigation, assist, driver, driving, parking, screen, traffic |
| 2 | 30 | 15 | Automotive Test Drive Episodes | 0.3333 | 0.6370 | False | auto, happy, episode, season, press, fun, got, absolutely, hello, enjoy |
| 3 | 30 | 2 | Hyundai IONIQ EV Lineup | 0.9000 | 0.9750 | True | ioniq, hyundai, charging, electric, vehicle, platform, rear, ev, new, interior |
| 4 | 30 | 7 | Midsize Sedan Market | 0.4000 | 0.6500 | True | sonata, accord, hyundai sonata, hyundai, camry, 2018, features, new, honda, 2020 |
| 5 | 30 | 3 | EV Charging Infrastructure | 0.6667 | 0.8300 | True | charging, charge, level, stations, plug, home, charging stations, cable, level charging, station |
| 6 | 30 | 10 | EV Test Drives | 0.3333 | 0.5800 | False | drive, driving, car, ride, truck, drive car, fun, driver, driven, roads |
| 7 | 30 | 10 | Polestar Electric Car Brand | 0.2333 | 0.5352 | False | polestar, car, electric, brand, volvo, china, electric car, customer, powerful, cars |
| 8 | 30 | 7 | Toyota Prius Plug-In Hybrid | 0.3000 | 0.7067 | True | prius, prius prime, hybrid, prime, toyota, efficiency, plug, seats, drive, available |
| 9 | 30 | 11 | EV Chassis Dynamics Control | 0.1667 | 0.6583 | True | steering, suspension, car, control, rear, rear axle, feel, axle, axle steering, chassis |
| 10 | 30 | 7 | Infiniti Hybrid Vehicles | 0.7000 | 0.8417 | True | infiniti, q50, infinity, brand, new, performance, market, future, johan, technology |
| 11 | 30 | 2 | Mercedes EQS and EQE | 0.9667 | 0.9867 | True | eqs, eqe, eq, mercedes, electric, new eqs, mercedes eq, new, driving, new eqe |
| 12 | 30 | 8 | Automotive Executive Presentations | 0.7000 | 0.8578 | True | president, vice, ladies, vice president, america, mr, tesla, chief, global, division |
| 13 | 30 | 2 | Toyota Corolla Hybrid Features | 0.8333 | 0.9583 | True | corolla, corolla hybrid, hybrid, toyota, safety, available, apex, new corolla, features, assist |
| 14 | 30 | 8 | Toyota Crown Sedan History | 0.3333 | 0.7233 | True | crown, toyota crown, toyota, platinum, performance, sedan, japan, new crown, available, generation |
| 15 | 30 | 6 | Tailgate and Cargo Access | 0.4000 | 0.6689 | True | open, cover, door, hood, place, close, release, pull, tailgate, trunk |
| 16 | 30 | 6 | Electric GT Performance Coupes | 0.4000 | 0.7517 | True | amg, gt, amg gt, door, gt door, gt3, amg line, steering, performance, door coupe |
| 17 | 30 | 4 | In-Car Multimedia Connectivity | 0.8000 | 0.9083 | True | connect, audio, available, wireless, audio multimedia, toyota, standard, multimedia, compatibility, touchscreen |
| 18 | 30 | 4 | Toyota Highlander Hybrid | 0.4000 | 0.8500 | True | highlander, grand highlander, hybrid, available, standard, grand, grade, platinum, power, row |
| 19 | 30 | 2 | Lithium-Ion Battery Packs | 0.8000 | 0.9500 | True | battery, lithium, lithium ion, ion, batteries, pack, battery pack, iron, cooling, cells |
| 20 | 30 | 8 | Affordable American EVs | 0.3333 | 0.5317 | False | k27, america, auto evolution, electric, ev, affordable, vehicles, evolution, inventory, electric vehicles |
| 21 | 30 | 4 | EV Acoustic Silence | 0.4333 | 0.6567 | True | sound, quiet, noise, sounds, exhaust, silence, acoustic, car, cook, car sound |
| 22 | 30 | 3 | Automatic Climate Control | 0.8667 | 0.9333 | True | air, temperature, degrees, turn, control, climate, button, set temperature, blow, automatic climate |
| 23 | 30 | 2 | Honda Clarity Electrified Series | 0.9000 | 0.9600 | True | clarity, plug, series, fuel cell, electrified, cell, plug hybrid, honda, electric, customers |

## Interpretation

若 `stable=True`，代表同一組 keywords 與文本重跑時，模型給出的主題名稱在字面或詞彙組成上大致一致；若為 `False`，建議人工檢查該 topic 的 keywords 是否過於混雜。
