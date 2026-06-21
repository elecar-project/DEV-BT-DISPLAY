# M02-1(orig-new-tp-30) LLM50 Validation

- model: `openai/gpt-5.5` via OpenRouter
- runs per non-noise topic: 50
- successful validation calls: 1700 / 1700
- stable topics: 20 / 34

| topic | successful_runs | unique_normalized_labels | mode_label | mode_ratio | avg_jaccard_to_mode | stable | keywords |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 50 | 14 | Luxury Car Interior Design | 0.3000 | 0.6483 | False | bmw, new, car, design, rear, interior, lexus, volvo, class, seat |
| 1 | 50 | 14 | EV Charging and Powertrain | 0.2000 | 0.5487 | False | charging, electric, kia, charge, battery, power, ev, range, vehicle, car |
| 2 | 50 | 18 | Driver Assistance and Displays | 0.2800 | 0.6557 | True | steering, control, car, display, driver, assist, navigation, driving, parking, screen |
| 3 | 50 | 16 | Automotive Podcast Episodes | 0.2800 | 0.5453 | False | auto, episode, season, press, fun, got, enjoy, absolutely, hello, new |
| 4 | 50 | 5 | Hyundai IONIQ EV Lineup | 0.4400 | 0.8250 | True | ioniq, hyundai, charging, electric, platform, vehicle, rear, ev, limited, xrt |
| 5 | 50 | 5 | Midsize Sedan Market | 0.9000 | 0.9350 | True | sonata, accord, hyundai sonata, hyundai, camry, 2018, 2018 hyundai, honda, gian, 2020 |
| 6 | 50 | 5 | Nissan Leaf EV Features | 0.3800 | 0.6113 | False | nissan, leaf, aria, nissan leaf, new nissan, altima, new, propilot, nissan intelligent, ev |
| 7 | 50 | 4 | Audi e-tron Models | 0.9400 | 0.9700 | True | audi, tron, quattro, q8, audi tron, a7, a3, light, q5, q8 tron |
| 8 | 50 | 9 | Cadillac ELR Plug-In Hybrid | 0.3200 | 0.5257 | False | elantra, hyundai, new elantra, elr, hyundai elantra, new, cadillac, design, features, generation |
| 9 | 50 | 9 | EV Test Drives | 0.4600 | 0.6373 | False | drive, driving, car, truck, driver, drive car, driven, roads, fun, thing |
| 10 | 50 | 11 | Polestar EV Brand Launch | 0.5200 | 0.7589 | True | polestar, car, brand, electric, volvo, china, electric car, customer, powerful, pouch |
| 11 | 50 | 6 | Toyota Prius Plug-in Hybrid | 0.6800 | 0.8430 | True | prius, prius prime, prime, hybrid, toyota, efficiency, plug, available, seats, combined |
| 12 | 50 | 15 | Infiniti Hybrid Vehicles | 0.3000 | 0.6117 | False | infiniti, q50, infinity, brand, new, market, performance, future, johan, technology |
| 13 | 50 | 3 | Ford Mustang Mach-E | 0.5400 | 0.8767 | True | mustang, mach, mustang mach, ford, vehicle, drive, proportions, customers, electric, different |
| 14 | 50 | 2 | Mercedes EQ Electric Models | 0.5600 | 0.6229 | False | eqs, eqe, eq, mercedes, mercedes eq, new eqs, electric, new, new eqe, amg |
| 15 | 50 | 9 | Automotive Executive Presentations | 0.8200 | 0.8880 | True | president, ladies, vice, vice president, mr, america, manager, product, chief, tesla |
| 16 | 50 | 2 | Toyota Corolla Hybrid Features | 0.5800 | 0.8950 | True | corolla, corolla hybrid, hybrid, toyota, safety, apex, available, new corolla, features, assist |
| 17 | 50 | 8 | Tailgate and Cargo Access | 0.2400 | 0.5987 | False | door, open, cover, tailgate, hood, release, place, close, trunk, pull |
| 18 | 50 | 8 | Toyota Crown Sedan | 0.3200 | 0.7547 | True | crown, toyota crown, toyota, platinum, performance, japan, sedan, new crown, available, platinum grade |
| 19 | 50 | 16 | In-Car Multimedia Connectivity | 0.2800 | 0.5283 | False | connect, audio, wireless, available, audio multimedia, multimedia, compatibility, toyota, standard, touchscreen |
| 20 | 50 | 12 | Electric GT Performance Coupes | 0.3200 | 0.7150 | True | amg, gt, amg gt, door, gt door, gt3, amg line, door coupe, steering, coupe |
| 21 | 50 | 4 | Porsche Taycan Turbo EV | 0.6800 | 0.8387 | True | taycan, porsche, turbo, electric, sports, sports car, porsche electric, car, spyder, alex |
| 22 | 50 | 3 | Lithium-Ion Battery Packs | 0.5800 | 0.7500 | True | battery, lithium, ion, lithium ion, batteries, battery pack, pack, iron, cooling, cells |
| 23 | 50 | 4 | Toyota Highlander Hybrid SUV | 0.6200 | 0.8510 | True | highlander, grand highlander, standard, hybrid, grand, grade, available, platinum, row, heated |
| 24 | 50 | 8 | Affordable American EVs | 0.4600 | 0.6000 | False | k27, america, auto evolution, ev, electric, affordable, evolution, vehicles, inventory, electric vehicles |
| 25 | 50 | 16 | Vehicle Color Options | 0.3000 | 0.5107 | False | black, color, red, colors, tone, sport, blue, orange, beautiful, kicks |
| 26 | 50 | 6 | Acura Sport Hybrid Performance | 0.7400 | 0.8920 | True | nsx, acura, supercar, performance, new, ilx, brief, sports, sport hybrid, manufacturing |
| 27 | 50 | 6 | EV Cabin Acoustics | 0.3600 | 0.5440 | False | sound, quiet, noise, sounds, exhaust, silence, acoustic, car sound, cook, ear |
| 28 | 50 | 10 | Buick Brand Lineup | 0.3600 | 0.6210 | False | buick, brand, lacrosse, sportback, buick brand, market, new, china, lineup, sell |
| 29 | 50 | 3 | Honda Clarity Electrified Vehicles | 0.9600 | 0.9840 | True | clarity, electrified, honda, fuel cell, plug, electrified vehicles, cell, series, vehicles, fuel |
| 30 | 50 | 6 | Regenerative Braking Pedals | 0.4600 | 0.7217 | True | pedal, braking, brake, accelerator, regenerative, regenerative braking, energy, battery, brakes, regen |
| 31 | 50 | 4 | Automatic Climate Control | 0.8400 | 0.9200 | True | air, turn, temperature, degrees, control, zone, climate, button, blow, automatic climate |
| 32 | 50 | 10 | Porsche Panamera Gran Turismo | 0.6400 | 0.7737 | True | panamera, porsche, new panamera, wego, www, net, new, comfort, chassis, terms |
| 33 | 50 | 7 | Chrysler Pacifica Minivan | 0.5600 | 0.6983 | True | pacifica, minivan, chrysler, segment, chrysler pacifica, safety, new, 2017, minivans, rating |
