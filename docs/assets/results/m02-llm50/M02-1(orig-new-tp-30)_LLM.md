# M02-1(orig-new-tp-30) LLM Topic Results

- model: `openai/gpt-5.5` via OpenRouter
- runs per non-noise topic: 50
- representative docs per topic: 6
- stable rule: `mode_ratio >= 0.70` or `avg_jaccard_to_mode >= 0.65`
- stable topics: 20 / 34
- successful validation calls: 1700 / 1700

## Combined Topic Representations

| Topic | Count | Name | LLM | KeyBERT | POS | MMR |
| --- | --- | --- | --- | --- | --- | --- |
| -1 | 2758 | -1_car_new_vehicle_driving | Noise / Outlier | toyota, car, vehicle, cars, hybrid, driving, drive, new, design | car, new, vehicle, first, system, design | the, this, car, new |
| 0 | 2459 | 0_bmw_new_car_design | Luxury Car Interior Design | volvo, mercedes, bmw, design, cars, benz, car, vehicle, hybrid, rear | new, car, design, rear, interior, seats, seat, series | new, bmw, car, design, also, rear, has |
| 1 | 1272 | 1_charging_electric_kia_charge | EV Charging and Powertrain | charging, charge, ev, electric, hybrid, ev6, battery, plug, car, vehicle | electric, charge, battery, power, range, car, vehicle, engine, new | charging, electric, kia, charge, battery, power, range |
| 2 | 959 | 2_steering_control_car_display | Driver Assistance and Displays | steering, navigation, driving, driver, view, drive, android, vehicle, carplay, road | car, steering, control, system, display, driver, assist, navigation, parking, screen | car, steering, control, system, display, driver, assist, driving, navigation, parking |
| 3 | 616 | 3_auto_episode_season_press | Automotive Podcast Episodes | next, go, you | show, auto | for, show |
| 4 | 204 | 4_ioniq_hyundai_charging_electric | Hyundai IONIQ EV Lineup | ioniq, hybrid, hyundai, ev, id4, electric, vehicle, powertrains, vehicles, egmp | electric, vehicle, rear, platform, new, limited, first, design | ioniq, hyundai, charging, electric, vehicle, rear, platform, ev, limited |
| 5 | 200 | 5_sonata_accord_hyundai sonata_hyundai | Midsize Sedan Market | sonata, hyundai, sedan, accord, hybrid, car, honda, engine, performance, civic | accord, new, features, safety, standard, car, performance | sonata, accord, hyundai, camry, new, features, honda, 2020, gian |
| 6 | 198 | 6_nissan_leaf_aria_nissan leaf | Nissan Leaf EV Features | nissanusa, nissan, leaf, ev, vehicle, sedan, electric, altima, mobility, battery | nissan, leaf, new, intelligent, technology, driving, drive, first, mobility | nissan, leaf, aria, altima, new, propilot, ev, intelligent, technology, driving |
| 7 | 193 | 7_audi_tron_quattro_q8 | Audi e-tron Models | audi, car, quattro, suv, a6, a8, a7, vehicle, q5, headlights | tron, quattro, new, electric, design, car, first, name | audi, quattro, q8, light, a7, a3, q5, a6, design, a8 |
| 8 | 169 | 8_elantra_hyundai_new elantra_elr | Cadillac ELR Plug-In Hybrid | elantra, hyundai, sedan, hybrid, elr, car, cadillac, 2021, trim, design | new, design, features, generation, compact, segment, hybrid, car, sedan | elantra, hyundai, elr, new, design, features, generation, cadillac, compact, segment |
| 9 | 165 | 9_drive_driving_car_truck | EV Test Drives | drive, driving, driver, driven, car, road, ride, roads, truck | drive, driving, car, driver, fun, thing, road | drive, it, driving, car, would, go |
| 10 | 136 | 10_polestar_car_brand_electric | Polestar EV Brand Launch | polestar, volvo, electric, factory, brand, car, cars, performance, battery, design | car, electric, brand, powerful, cars, pouch, performance, battery, customers, world | polestar, car, electric, brand, they, volvo, china |
| 11 | 128 | 11_prius_prius prime_prime_hybrid | Toyota Prius Plug-in Hybrid | prius, hybrid, toyota, efficiency, prime, vehicle, convenience, per, performance, efficient | hybrid, efficiency, available, plug, seats, drive | prius, hybrid, prime, toyota, efficiency, seats, drive, fuel |
| 12 | 108 | 12_infiniti_q50_infinity_brand | Infiniti Hybrid Vehicles | q50, infiniti, q60, sedan, hybrid, brand, engine, luxury, cars, driver | infinity, brand, new, performance, market, future, technology, car, design, first | infiniti, q50, infinity, brand, new, in, performance, market, future, johan |
| 13 | 108 | 13_mustang_mach_mustang mach_ford | Ford Mustang Mach-E | mustang, mustangs, ford, car, suv, vehicle, drive, mach, pony | mustang, mustangs, vehicle, drive, electric, customers | mustang, mach, mustangs, vehicle, ford, from, drive |
| 14 | 106 | 14_eqs_eqe_eq_mercedes | Mercedes EQ Electric Models | eqs, eqe, eq, mercedes, electric, car, benz, vehicles, design, luxury | electric, new, car, driving, about, performance, first, range, light | eqs, eqe, eq, mercedes, electric, new, car, amg, about |
| 15 | 100 | 15_president_ladies_vice_vice president | Automotive Executive Presentations | hyundai, vice, acura, gm, auto, mayor, tesla, ceo, van, executive | president, ladies, vice, name, product, manager | president, vice, manager, chief, global, tesla |
| 16 | 90 | 16_corolla_corolla hybrid_hybrid_toyota | Toyota Corolla Hybrid Features | corolla, toyota, hybrid, hatchback, rear, steering, lane, driving | hybrid, safety, available, features, assist, lane, system, black, standard | corolla, hybrid, toyota, safety, apex, features, lane, standard, drivers |
| 17 | 89 | 17_door_open_cover_tailgate | Tailgate and Cargo Access | trunk, push, soft, pulling, lift, top, pull, press, pushing, rear | door, top, cover, tailgate, hood, place, trunk, release | door, cover, tailgate, hood, trunk, release, pull, soft |
| 18 | 89 | 18_crown_toyota crown_toyota_platinum | Toyota Crown Sedan | crown, toyota, flagship, car, hybrid, vehicle, sedan, platinum, electrified, premium | crown, performance, sedan, available, generation, driving, new, chief, system, drive | crown, toyota, platinum, performance, sedan, japan, generation, limited, drive |
| 19 | 82 | 19_connect_audio_wireless_available | In-Car Multimedia Connectivity | toyota, carplay, devices, android, drivers, apple, touchscreen, wireless, iphone, multimedia | available, audio, wireless, standard, multimedia, compatibility, touchscreen, drivers, maps | audio, wireless, toyota, compatibility, drivers, maps, iphone, connects, carplay, jbl |
| 20 | 80 | 20_amg_gt_amg gt_door | Electric GT Performance Coupes | amg, gt3, gt4, steering, gtr, gtc, car, gtb, engine, mercedes | door, performance, steering, coupe, racing, buttons, line, features, driving | amg, door, gt3, steering, coupe, racing, roadster, buttons, features |
| 21 | 79 | 21_taycan_porsche_turbo_electric | Porsche Taycan Turbo EV | taycan, porsche, car, cars, turbo, charging, 4s, macan, charger | electric, turbo, car, sports, performance, first, charger, volt | taycan, porsche, turbo, performance, alex, spyder, charger, about, 800, volt |
| 22 | 77 | 22_battery_lithium_ion_lithium ion | Lithium-Ion Battery Packs | battery, batteries, lithium, vehicle, car, laptop, energy, cells, electric, power | battery, lithium, ion, batteries, pack, iron, cooling, cells, range, chemistry | battery, lithium, ion, batteries, pack, cooling, cells, chemistry, system, phosphate |
| 23 | 73 | 23_highlander_grand highlander_standard_hybrid | Toyota Highlander Hybrid SUV | highlander, suv, toyota, hybrid, horsepower, turbocharged, drive, traction, mpg, performance | hybrid, standard, available, grade, row, power | highlander, hybrid, standard, platinum, heated, toyota, suv, seating |
| 24 | 72 | 24_k27_america_auto evolution_ev | Affordable American EVs | ev, cars, car, vehicles, promotional, vehicle, dealer, affordability, northpoint | electric, affordable, vehicles, evolution, inventory, first, pre | k27, kandy, ev, affordable, vehicles, northpoint, inventory, promotional |
| 25 | 68 | 25_black_color_red_colors | Vehicle Color Options | colors, colours, red, color, blue, yellow, green, black, orange, white | black, color, red, colors, tone, sport, blue, beautiful, orange, available | black, color, red, colors, tone, juke, blue, orange, kicks, interior |
| 26 | 65 | 26_nsx_acura_supercar_performance | Acura Sport Hybrid Performance | nsx, acura, supercar, rlx, ilx, hybrid, vehicle, engine, car, driver | supercar, new, performance, sports, brief, driver, global, manufacturing, brand | nsx, acura, supercar, performance, ilx, sports, driver, global, brand |
| 27 | 61 | 27_sound_quiet_noise_sounds | EV Cabin Acoustics | acoustic, sound, noise, noises, quietness, noisy, silent, exhaust, vibrations, ear | sound, quiet, noise, sounds, exhaust, car, silence, engine, ear, cabin | sound, quiet, noise, exhaust, car, silence, engine, acoustic, cook, ear |
| 28 | 58 | 28_buick_brand_lacrosse_sportback | Buick Brand Lineup | buick, buicks, regal, brand, brands, car, suv, luxury, sales, industry | regal, brand, new, market, lineup, customers, industry | buick, regal, brand, lacrosse, sportback, market, buicks, duncan, encore |
| 29 | 57 | 29_clarity_electrified_honda_fuel cell | Honda Clarity Electrified Vehicles | clarity, hybrid, honda, electrification, plug, electrified, fuel, vehicles, battery, electric | clarity, electrified, plug, in, series, cell, vehicles, electric, customers, fuel | clarity, electrified, honda, plug, cell, fuel, hybrid, three, range, rating |
| 30 | 56 | 30_pedal_braking_brake_accelerator | Regenerative Braking Pedals | braking, pedal, brakes, brake, slowing, accelerator, drive, acceleration, driving, speed | pedal, braking, brake, accelerator, regenerative, energy, battery, brakes, stop, drive | pedal, braking, accelerator, regenerative, energy, battery, brakes, drive, slow, recuperation |
| 31 | 56 | 31_air_turn_temperature_degrees | Automatic Climate Control | heaters, heating, hvac, vents, temperature, heat, warm, vent, automatic, air | air, turn, temperature, degrees, control, zone, climate, button, blow, automatic | air, turn, temperature, control, zone, climate, automatic, adjust, fan, outside |
| 32 | 55 | 32_panamera_porsche_new panamera_wego | Porsche Panamera Gran Turismo | panamera, porsche, chassis, engine, models, vehicle, engines, model, car, systems | new, comfort, chassis, engine, terms, sports, design, performance, identity, turbo | panamera, porsche, wego, new, comfort, chassis, engine, performance, turbo, brand |
| 33 | 50 | 33_pacifica_minivan_chrysler_segment | Chrysler Pacifica Minivan | pacifica, chrysler, minivans, minivan, innovations, vehicle, drivetrain, design, passenger, advanced | minivan, segment, new, safety, minivans, only, family, about | pacifica, minivan, chrysler, the, segment, new, safety, minivans, eight, most |

## LLM50 Validation Summary

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

## Interpretation

若 `stable=True`，代表同一組 keywords 與文本重跑時，模型給出的主題名稱在字面或詞彙組成上大致一致；若為 `False`，建議人工檢查該 topic 的 keywords 是否過於混雜。
