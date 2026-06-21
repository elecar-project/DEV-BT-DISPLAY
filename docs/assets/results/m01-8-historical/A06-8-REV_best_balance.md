# A06-8-REV BERTopic + A05-8.4(human) stopwords + representation models - best_balance

## Run Info

| started_at | finished_at | dataset | embedding_model | embedding_note | custom_stopword_count | llm_provider | llm_models |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-05T12:15:01.211908+00:00 | 2026-06-05T12:25:31.478729+00:00 | Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset | all-MiniLM-L6-v2 | 重用 A04-8(orig) embeddings 快取並複製到 M01-8。 | 170 | OpenRouter | anthropic/claude-opus-4.7, openai/gpt-5.5, google/gemini-3.1-pro-preview |

## Parameters

| selection_label | selection_reason | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance | 符合指定最佳平衡條件後取最高 balance_score。 | 5 | 5 | 0.0000 | cosine | 42 | 50 | 5 | eom | 0.2000 | euclidean |

## Metrics

| n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 51 | 0.1958 | 2180 | 2129 | 442 | 2129 | 0.1912 | 0.2632 | 0.8659 | 0.8313 |

## Compared With Provided Baseline

| selection_label | baseline_noise_ratio | a06_noise_ratio | baseline_n_clusters | a06_n_clusters | baseline_largest_topic_ratio | a06_largest_topic_ratio | baseline_top3_topic_ratio | a06_top3_topic_ratio | baseline_balance_score | a06_balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance | 0.2768 | 0.1958 | 62 | 51 | 0.0407 | 0.1912 | 0.1061 | 0.2632 | 0.8835 | 0.8313 |

## Stopword Setting

- stopword source: `Result/06.05_A05_stopword/A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md`
- 使用 A05-8.4(human) 報告表格第三欄建議停用詞，並加上 sklearn English stop words。
- stopwords 只作用於 BERTopic c-TF-IDF / topic words 表示；embedding 與 HDBSCAN 分群仍使用原始 orig 文本向量。

## Representation Models

- default: BERTopic c-TF-IDF
- keybert: KeyBERT-Inspired
- pos: Part-of-Speech
- mmr: Maximal Marginal Relevance
- llm_anthropic_claude_opus_4_7: OpenRouter LLM topic labels
- llm_openai_gpt_5_5: OpenRouter LLM topic labels
- llm_google_gemini_3_1_pro_preview: OpenRouter LLM topic labels

### default

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2180 | -1_car_new_vehicle_driving | ['car', 'new', 'vehicle', 'driving', 'electric', 'rear', 'bmw', 'hybrid', 'range', 'standard'] |
| 0 | 2129 | 0_car_new_design_cars | ['car', 'new', 'design', 'cars', 'customers', 'look', 'product', 'different', 'world', 'brand'] |
| 1 | 442 | 1_interior_seat_seats_leather | ['interior', 'seat', 'seats', 'leather', 'space', 'rear', 'materials', 'design', 'comfort', 'feel'] |
| 2 | 360 | 2_charging_charge_range_charger | ['charging', 'charge', 'range', 'charger', 'minutes', 'hour', 'fast', 'battery', 'volt', 'level'] |
| 3 | 277 | 3_electric_torque_hybrid_motor | ['electric', 'torque', 'hybrid', 'motor', 'pedal', 'power', 'battery', 'engine', 'electric motor', 'drive'] |
| 4 | 245 | 4_bmw_series_grand tour_tour | ['bmw', 'series', 'grand tour', 'tour', 'grand', 'bmw series', 'new bmw', 'kidney', 'new', 'i4'] |
| 5 | 245 | 5_sonata_hyundai_hyundai sonata_safety | ['sonata', 'hyundai', 'hyundai sonata', 'safety', 'elantra', 'features', 'xc40', 'xc40 recharge', 'camry', 'recharge'] |
| 6 | 229 | 6_volvo_xc90_s60_new xc90 | ['volvo', 'xc90', 's60', 'new xc90', 'new', 'ex90', 'safety', 'world', 'car', 'new s60'] |
| 7 | 221 | 7_assist_parking_lane_spot | ['assist', 'parking', 'lane', 'spot', 'blind', 'blind spot', 'alert', 'traffic', 'driver', 'braking'] |
| 8 | 219 | 8_ioniq_hyundai_charging_electric | ['ioniq', 'hyundai', 'charging', 'electric', 'platform', 'vehicle', 'rear', '2025', 'interior', 'assist'] |
| 9 | 218 | 9_kia_ev6_ev_india | ['kia', 'ev6', 'ev', 'india', 'gt', 'new kia', 'niro', 'ev6 gt', 'ev9', 'fleet'] |
| 10 | 204 | 10_nissan_leaf_nissan leaf_aria | ['nissan', 'leaf', 'nissan leaf', 'aria', 'new nissan', 'altima', 'propilot', 'new', 'ev', 'intelligent'] |
| 11 | 188 | 11_apple_carplay_android_apple carplay | ['apple', 'carplay', 'android', 'apple carplay', 'android auto', 'smartphone', 'phone', 'alexa', 'auto', 'touchscreen'] |
| 12 | 186 | 12_audi_tron_quattro_q8 | ['audi', 'tron', 'quattro', 'q8', 'audi tron', 'a7', 'a3', 'light', 'q5', 'q8 tron'] |
| 13 | 185 | 13_mbux_screen_display_console | ['mbux', 'screen', 'display', 'console', 'center', 'center console', 'control', 'buttons', 'digital', 'functions'] |
| 14 | 182 | 14_lexus_nx_ux_ls | ['lexus', 'nx', 'ux', 'ls', 'new', 'luxury', 'gs', 'es', 'lc', 'brand'] |
| 15 | 173 | 15_electric_cars_electric cars_ev | ['electric', 'cars', 'electric cars', 'ev', 'car', 'vehicles', 'electric vehicles', 'electrification', 'electric vehicle', 'electric car'] |
| 16 | 172 | 16_elantra_hyundai_new elantra_new | ['elantra', 'hyundai', 'new elantra', 'new', 'hyundai elantra', 'generation', 'generation elantra', 'elr', 'compact', 'design'] |
| 17 | 161 | 17_grille_hood_lines_car | ['grille', 'hood', 'lines', 'car', 'design', 'line', 'rear', 'shape', 'gives', 'look'] |
| 18 | 160 | 18_mercedes_benz_mercedes benz_class | ['mercedes', 'benz', 'mercedes benz', 'class', 'benz class', 'new mercedes', 'new class', 'new', 'mercedes amg', 'amg'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car, new, vehicle, driving, electric, rear, bmw, hybrid, range, standard |
| 0 | car, new, design, cars, customers, look, product, different, world, brand |
| 1 | interior, seat, seats, leather, space, rear, materials, design, comfort, feel |
| 2 | charging, charge, range, charger, minutes, hour, fast, battery, volt, level |
| 3 | electric, torque, hybrid, motor, pedal, power, battery, engine, electric motor, drive |
| 4 | bmw, series, grand tour, tour, grand, bmw series, new bmw, kidney, new, i4 |
| 5 | sonata, hyundai, hyundai sonata, safety, elantra, features, xc40, xc40 recharge, camry, recharge |
| 6 | volvo, xc90, s60, new xc90, new, ex90, safety, world, car, new s60 |
| 7 | assist, parking, lane, spot, blind, blind spot, alert, traffic, driver, braking |
| 8 | ioniq, hyundai, charging, electric, platform, vehicle, rear, 2025, interior, assist |
| 9 | kia, ev6, ev, india, gt, new kia, niro, ev6 gt, ev9, fleet |
| 10 | nissan, leaf, nissan leaf, aria, new nissan, altima, propilot, new, ev, intelligent |
| 11 | apple, carplay, android, apple carplay, android auto, smartphone, phone, alexa, auto, touchscreen |
| 12 | audi, tron, quattro, q8, audi tron, a7, a3, light, q5, q8 tron |
| 13 | mbux, screen, display, console, center, center console, control, buttons, digital, functions |
| 14 | lexus, nx, ux, ls, new, luxury, gs, es, lc, brand |
| 15 | electric, cars, electric cars, ev, car, vehicles, electric vehicles, electrification, electric vehicle, electric car |
| 16 | elantra, hyundai, new elantra, new, hyundai elantra, generation, generation elantra, elr, compact, design |
| 17 | grille, hood, lines, car, design, line, rear, shape, gives, look |
| 18 | mercedes, benz, mercedes benz, class, benz class, new mercedes, new class, new, mercedes amg, amg |
### keybert

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2180 | -1_steering_driving_car_bmw | ['steering', 'driving', 'car', 'bmw', 'drive', 'driver', 'performance', 'vehicle', 'rear'] |
| 0 | 2129 | 0_car_you_cars | ['car', 'you', 'cars'] |
| 1 | 442 | 1_seats_seat_interior_leather | ['seats', 'seat', 'interior', 'leather', 'upholstery', 'comfortable', 'comfort', 'cabin', 'passengers', 'design'] |
| 2 | 360 | 2_charging_charge_charger_chargers | ['charging', 'charge', 'charger', 'chargers', 'battery', 'electric', 'plug', 'fast', 'kilowatt', 'hour'] |
| 3 | 277 | 3_hybrid_powertrain_electric_horsepower | ['hybrid', 'powertrain', 'electric', 'horsepower', 'motors', 'vehicle', 'motor', 'car', 'engine', 'generator'] |
| 4 | 245 | 4_bmw_sedan_coupe_i4 | ['bmw', 'sedan', 'coupe', 'i4', 'car', 'hybrid', 'i3', 'touring', 'model'] |
| 5 | 245 | 5_sonata_hyundai_hybrid_accord | ['sonata', 'hyundai', 'hybrid', 'accord', 'car', 'engine', 'elantra', 'performance', '2018'] |
| 6 | 229 | 6_xc90_v90_ex90_s90 | ['xc90', 'v90', 'ex90', 's90', 'volvo', 's60', 'design', 'new', 'automotive'] |
| 7 | 221 | 7_safety_parking_detection_detects | ['safety', 'parking', 'detection', 'detects', 'steering', 'detect', 'blind', 'driving', 'pedestrian', 'radar'] |
| 8 | 219 | 8_ioniq_hyundai_hybrid_ev | ['ioniq', 'hyundai', 'hybrid', 'ev', 'electric', 'id4', 'powertrains', 'vehicle', 'vehicles', 'plug'] |
| 9 | 218 | 9_kia_ev6_ev_ev9 | ['kia', 'ev6', 'ev', 'ev9', 'ev4', 'e6', 'evs', 'vehicle', 'car', 'vehicles'] |
| 10 | 204 | 10_nissanusa_nissan_leaf_ev | ['nissanusa', 'nissan', 'leaf', 'ev', 'sedan', 'electric', 'altima', 'mobility', 'battery', 'ariya'] |
| 11 | 188 | 11_smartphone_android_iphone_mobile | ['smartphone', 'android', 'iphone', 'mobile', 'apps', 'touchscreen', 'devices', 'app', 'phone', 'carplay'] |
| 12 | 186 | 12_audi_suv_car_vehicle | ['audi', 'suv', 'car', 'vehicle', 'a8', 'a6', 'a7', 'q5', 'headlights', 'quattro'] |
| 13 | 185 | 13_controls_touchscreen_control_mercedes | ['controls', 'touchscreen', 'control', 'mercedes', 'screens', 'screen', 'cockpit', 'steering', 'buttons', 'mbux'] |
| 14 | 182 | 14_lexus_rx_hybrid_car | ['lexus', 'rx', 'hybrid', 'car', 'vehicle', 'sedan', 'ilx', 'vehicles', 'nx', 'lc500'] |
| 15 | 173 | 15_tesla_ev_cars_electrification | ['tesla', 'ev', 'cars', 'electrification', 'car', 'vehicles', 'electric', 'evs', 'vehicle', 'emissions'] |
| 16 | 172 | 16_hyundai_elantra_elr_sedan | ['hyundai', 'elantra', 'elr', 'sedan', 'car', 'brand', '2021', 'design'] |
| 17 | 161 | 17_design_aerodynamics_stance_rear | ['design', 'aerodynamics', 'stance', 'rear', 'headlights', 'vehicle', 'car'] |
| 18 | 160 | 18_mercedes_benz_automotive_sedan | ['mercedes', 'benz', 'automotive', 'sedan', 'cars', 'flagship', 'car', 'class', 'model', 'luxury'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | steering, driving, car, bmw, drive, driver, performance, vehicle, rear |
| 0 | car, you, cars |
| 1 | seats, seat, interior, leather, upholstery, comfortable, comfort, cabin, passengers, design |
| 2 | charging, charge, charger, chargers, battery, electric, plug, fast, kilowatt, hour |
| 3 | hybrid, powertrain, electric, horsepower, motors, vehicle, motor, car, engine, generator |
| 4 | bmw, sedan, coupe, i4, car, hybrid, i3, touring, model |
| 5 | sonata, hyundai, hybrid, accord, car, engine, elantra, performance, 2018 |
| 6 | xc90, v90, ex90, s90, volvo, s60, design, new, automotive |
| 7 | safety, parking, detection, detects, steering, detect, blind, driving, pedestrian, radar |
| 8 | ioniq, hyundai, hybrid, ev, electric, id4, powertrains, vehicle, vehicles, plug |
| 9 | kia, ev6, ev, ev9, ev4, e6, evs, vehicle, car, vehicles |
| 10 | nissanusa, nissan, leaf, ev, sedan, electric, altima, mobility, battery, ariya |
| 11 | smartphone, android, iphone, mobile, apps, touchscreen, devices, app, phone, carplay |
| 12 | audi, suv, car, vehicle, a8, a6, a7, q5, headlights, quattro |
| 13 | controls, touchscreen, control, mercedes, screens, screen, cockpit, steering, buttons, mbux |
| 14 | lexus, rx, hybrid, car, vehicle, sedan, ilx, vehicles, nx, lc500 |
| 15 | tesla, ev, cars, electrification, car, vehicles, electric, evs, vehicle, emissions |
| 16 | hyundai, elantra, elr, sedan, car, brand, 2021, design |
| 17 | design, aerodynamics, stance, rear, headlights, vehicle, car |
| 18 | mercedes, benz, automotive, sedan, cars, flagship, car, class, model, luxury |
### pos

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2180 | -1_car_new_vehicle_electric | ['car', 'new', 'vehicle', 'electric', 'rear', 'standard', 'first', 'available'] |
| 0 | 2129 | 0_car_design_cars | ['car', 'design', 'cars'] |
| 1 | 442 | 1_interior_seat_seats_leather | ['interior', 'seat', 'seats', 'leather', 'space', 'rear', 'design', 'back', 'materials', 'comfort'] |
| 2 | 360 | 2_charging_charge_range_charger | ['charging', 'charge', 'range', 'charger', 'minutes', 'hour', 'battery', 'fast', 'volt'] |
| 3 | 277 | 3_electric_torque_hybrid_motor | ['electric', 'torque', 'hybrid', 'motor', 'pedal', 'power', 'battery', 'drive', 'engine', 'plug'] |
| 4 | 245 | 4_series_grand_new_kidney | ['series', 'grand', 'new', 'kidney', 'design', 'touring', 'driving', 'car', 'dynamics'] |
| 5 | 245 | 5_safety_features_recharge_assist | ['safety', 'features', 'recharge', 'assist', 'new', 'standard', 'car', 'available'] |
| 6 | 229 | 6_s60_new_car_safety | ['s60', 'new', 'car', 'safety', 'world', 'cars', 'design', 'first', 'seat'] |
| 7 | 221 | 7_assist_parking_lane_spot | ['assist', 'parking', 'lane', 'spot', 'blind', 'driver', 'traffic', 'alert', 'braking', 'emergency'] |
| 8 | 219 | 8_electric_vehicle_platform_rear | ['electric', 'vehicle', 'platform', 'rear', 'new', 'first', 'interior', 'assist', 'design'] |
| 9 | 218 | 9_new_vehicle_fleet_electric | ['new', 'vehicle', 'fleet', 'electric', 'customers', 'first', 'sustainable', 'world'] |
| 10 | 204 | 10_nissan_leaf_new_intelligent | ['nissan', 'leaf', 'new', 'intelligent', 'technology', 'driving', 'drive', 'first', 'assist'] |
| 11 | 188 | 11_carplay_smartphone_phone_touchscreen | ['carplay', 'smartphone', 'phone', 'touchscreen', 'available', 'connected', 'profile', 'car', 'wireless', 'apps'] |
| 12 | 186 | 12_tron_quattro_electric_new | ['tron', 'quattro', 'electric', 'new', 'design', 'first', 'car', 'name'] |
| 13 | 185 | 13_screen_display_console_center | ['screen', 'display', 'console', 'center', 'control', 'hyperscreen', 'buttons', 'digital', 'system', 'air'] |
| 14 | 182 | 14_lexus_new_luxury_system | ['lexus', 'new', 'luxury', 'system', 'brand', 'safety', 'hybrid', 'rear'] |
| 15 | 173 | 15_electric_cars_car_vehicles | ['electric', 'cars', 'car', 'vehicles', 'electrification', 'vehicle', 'future', 'battery', 'customers'] |
| 16 | 172 | 16_new_generation_design_compact | ['new', 'generation', 'design', 'compact', 'sedan', 'customers', 'car', 'model'] |
| 17 | 161 | 17_grille_car_hood_design | ['grille', 'car', 'hood', 'design', 'lines', 'line', 'rear'] |
| 18 | 160 | 18_class_new_car_luxury | ['class', 'new', 'car', 'luxury', 'world', 'safety', 'coupe', 'star', 'cars', 'sedan'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car, new, vehicle, electric, rear, standard, first, available |
| 0 | car, design, cars |
| 1 | interior, seat, seats, leather, space, rear, design, back, materials, comfort |
| 2 | charging, charge, range, charger, minutes, hour, battery, fast, volt |
| 3 | electric, torque, hybrid, motor, pedal, power, battery, drive, engine, plug |
| 4 | series, grand, new, kidney, design, touring, driving, car, dynamics |
| 5 | safety, features, recharge, assist, new, standard, car, available |
| 6 | s60, new, car, safety, world, cars, design, first, seat |
| 7 | assist, parking, lane, spot, blind, driver, traffic, alert, braking, emergency |
| 8 | electric, vehicle, platform, rear, new, first, interior, assist, design |
| 9 | new, vehicle, fleet, electric, customers, first, sustainable, world |
| 10 | nissan, leaf, new, intelligent, technology, driving, drive, first, assist |
| 11 | carplay, smartphone, phone, touchscreen, available, connected, profile, car, wireless, apps |
| 12 | tron, quattro, electric, new, design, first, car, name |
| 13 | screen, display, console, center, control, hyperscreen, buttons, digital, system, air |
| 14 | lexus, new, luxury, system, brand, safety, hybrid, rear |
| 15 | electric, cars, car, vehicles, electrification, vehicle, future, battery, customers |
| 16 | new, generation, design, compact, sedan, customers, car, model |
| 17 | grille, car, hood, design, lines, line, rear |
| 18 | class, new, car, luxury, world, safety, coupe, star, cars, sedan |
### mmr

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2180 | -1_car_new | ['car', 'new'] |
| 0 | 2129 | 0_car | ['car'] |
| 1 | 442 | 1_interior_seat_seats_leather | ['interior', 'seat', 'seats', 'leather', 'space', 'rear', 'design', 'materials'] |
| 2 | 360 | 2_charging_range_charger_hour | ['charging', 'range', 'charger', 'hour', 'battery', 'fast', 'volt', 'level', 'kilometers'] |
| 3 | 277 | 3_electric_torque_hybrid_motor | ['electric', 'torque', 'hybrid', 'motor', 'pedal', 'engine', 'horsepower', 'braking', 'car', 'motors'] |
| 4 | 245 | 4_bmw_series_grand_new | ['bmw', 'series', 'grand', 'new', 'kidney', 'design', 'i4', 'touring', 'driving'] |
| 5 | 245 | 5_sonata_hyundai_elantra_xc40 | ['sonata', 'hyundai', 'elantra', 'xc40', 'camry', 'recharge', 'accord', '2018', 'assist', 'standard'] |
| 6 | 229 | 6_volvo_xc90_s60_safety | ['volvo', 'xc90', 's60', 'safety', 'ex90', 'cars', 'you', 'design'] |
| 7 | 221 | 7_assist_parking_lane_blind | ['assist', 'parking', 'lane', 'blind', 'driver', 'traffic', 'alert', 'braking', 'vehicle', 'rear'] |
| 8 | 219 | 8_ioniq_hyundai_charging_electric | ['ioniq', 'hyundai', 'charging', 'electric', 'vehicle', 'platform', 'rear', 'interior', 'assist'] |
| 9 | 218 | 9_kia_ev6_ev_india | ['kia', 'ev6', 'ev', 'india', 'niro', 'ev9', 'vehicle', 'ev4'] |
| 10 | 204 | 10_nissan_leaf_aria_altima | ['nissan', 'leaf', 'aria', 'altima', 'propilot', 'ev', 'intelligent', 'technology', 'driving'] |
| 11 | 188 | 11_apple_carplay_android_smartphone | ['apple', 'carplay', 'android', 'smartphone', 'auto', 'alexa', 'touchscreen', 'car', 'wireless', 'apps'] |
| 12 | 186 | 12_audi_quattro_a7_a3 | ['audi', 'quattro', 'a7', 'a3', 'q5', 'electric', 'a8', 'a6', 'suv'] |
| 13 | 185 | 13_screen_mbux_display_console | ['screen', 'mbux', 'display', 'console', 'center', 'hyperscreen', 'buttons', 'digital', 'system'] |
| 14 | 182 | 14_lexus_nx_ls_ct | ['lexus', 'nx', 'ls', 'ct', 'luxury', 'gs', 'brand', 'es'] |
| 15 | 173 | 15_electric_cars_ev_electrification | ['electric', 'cars', 'ev', 'electrification', 'vehicle', 'future'] |
| 16 | 172 | 16_elantra_hyundai_new_generation | ['elantra', 'hyundai', 'new', 'generation', 'design', 'compact', 'elr'] |
| 17 | 161 | 17_grille_car_hood_design | ['grille', 'car', 'hood', 'design', 'lines', 'shape', 'look'] |
| 18 | 160 | 18_mercedes_benz_class_new | ['mercedes', 'benz', 'class', 'new', 'is', 'car', 'in', 'amg', 'luxury'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car, new |
| 0 | car |
| 1 | interior, seat, seats, leather, space, rear, design, materials |
| 2 | charging, range, charger, hour, battery, fast, volt, level, kilometers |
| 3 | electric, torque, hybrid, motor, pedal, engine, horsepower, braking, car, motors |
| 4 | bmw, series, grand, new, kidney, design, i4, touring, driving |
| 5 | sonata, hyundai, elantra, xc40, camry, recharge, accord, 2018, assist, standard |
| 6 | volvo, xc90, s60, safety, ex90, cars, you, design |
| 7 | assist, parking, lane, blind, driver, traffic, alert, braking, vehicle, rear |
| 8 | ioniq, hyundai, charging, electric, vehicle, platform, rear, interior, assist |
| 9 | kia, ev6, ev, india, niro, ev9, vehicle, ev4 |
| 10 | nissan, leaf, aria, altima, propilot, ev, intelligent, technology, driving |
| 11 | apple, carplay, android, smartphone, auto, alexa, touchscreen, car, wireless, apps |
| 12 | audi, quattro, a7, a3, q5, electric, a8, a6, suv |
| 13 | screen, mbux, display, console, center, hyperscreen, buttons, digital, system |
| 14 | lexus, nx, ls, ct, luxury, gs, brand, es |
| 15 | electric, cars, ev, electrification, vehicle, future |
| 16 | elantra, hyundai, new, generation, design, compact, elr |
| 17 | grille, car, hood, design, lines, shape, look |
| 18 | mercedes, benz, class, new, is, car, in, amg, luxury |
### llm_anthropic_claude_opus_4_7

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2180 | -1_Vehicle Safety and Convenience Features | ['Vehicle Safety and Convenience Features'] |
| 0 | 2129 | 0_EV Ownership Experience | ['EV Ownership Experience'] |
| 1 | 442 | 1_Interior and Seat Design | ['Interior and Seat Design'] |
| 2 | 360 | 2_EV Charging and Range | ['EV Charging and Range'] |
| 3 | 277 | 3_Hybrid Powertrain Motor Torque | ['Hybrid Powertrain Motor Torque'] |
| 4 | 245 | 4_BMW vehicle features and dealerships | ['BMW vehicle features and dealerships'] |
| 5 | 245 | 5_Vehicle Safety Features and Ratings | ['Vehicle Safety Features and Ratings'] |
| 6 | 229 | 6_Volvo XC90 and S60 Reviews | ['Volvo XC90 and S60 Reviews'] |
| 7 | 221 | 7_Driver Assistance and Parking Features | ['Driver Assistance and Parking Features'] |
| 8 | 219 | 8_Hyundai IONIQ EV Lineup | ['Hyundai IONIQ EV Lineup'] |
| 9 | 218 | 9_BYD E6 and Kia EV6 Models | ['BYD E6 and Kia EV6 Models'] |
| 10 | 204 | 10_Nissan Leaf and ProPilot | ['Nissan Leaf and ProPilot'] |
| 11 | 188 | 11_Smartphone Integration and Infotainment | ['Smartphone Integration and Infotainment'] |
| 12 | 186 | 12_Audi Model Design Features | ['Audi Model Design Features'] |
| 13 | 185 | 13_MBUX Hyperscreen Displays | ['MBUX Hyperscreen Displays'] |
| 14 | 182 | 14_Lexus and Acura Hybrid Models | ['Lexus and Acura Hybrid Models'] |
| 15 | 173 | 15_EV Design Philosophy and Vision | ['EV Design Philosophy and Vision'] |
| 16 | 172 | 16_Hyundai Elantra Product Updates | ['Hyundai Elantra Product Updates'] |
| 17 | 161 | 17_Exterior Styling and Front Grille Design | ['Exterior Styling and Front Grille Design'] |
| 18 | 160 | 18_Mercedes-Benz EV Models | ['Mercedes-Benz EV Models'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | Vehicle Safety and Convenience Features |
| 0 | EV Ownership Experience |
| 1 | Interior and Seat Design |
| 2 | EV Charging and Range |
| 3 | Hybrid Powertrain Motor Torque |
| 4 | BMW vehicle features and dealerships |
| 5 | Vehicle Safety Features and Ratings |
| 6 | Volvo XC90 and S60 Reviews |
| 7 | Driver Assistance and Parking Features |
| 8 | Hyundai IONIQ EV Lineup |
| 9 | BYD E6 and Kia EV6 Models |
| 10 | Nissan Leaf and ProPilot |
| 11 | Smartphone Integration and Infotainment |
| 12 | Audi Model Design Features |
| 13 | MBUX Hyperscreen Displays |
| 14 | Lexus and Acura Hybrid Models |
| 15 | EV Design Philosophy and Vision |
| 16 | Hyundai Elantra Product Updates |
| 17 | Exterior Styling and Front Grille Design |
| 18 | Mercedes-Benz EV Models |
### llm_openai_gpt_5_5

- status: `ok`
- topics_with_custom_stopword_hits: 41

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2180 | -1_LLM label unavailable: the, and, to, of, in, is, you, it, that, with | ['LLM label unavailable: the, and, to, of, in, is, you, it, that, with'] |
| 0 | 2129 | 0_LLM label unavailable: we, it, you, to, that, and, of, this, the, in | ['LLM label unavailable: we, it, you, to, that, and, of, this, the, in'] |
| 1 | 442 | 1_LLM label unavailable: interior, seat, seats, the, and, of, leather, in, it, is | ['LLM label unavailable: interior, seat, seats, the, and, of, leather, in, it, is'] |
| 2 | 360 | 2_LLM label unavailable: charging, charge, you, range, miles, can, to, it, the, charger | ['LLM label unavailable: charging, charge, you, range, miles, can, to, it, the, charger'] |
| 3 | 277 | 3_LLM label unavailable: electric, torque, hybrid, motor, the, pedal, power, battery, drive, engine | ['LLM label unavailable: electric, torque, hybrid, motor, the, pedal, power, battery, drive, engine'] |
| 4 | 245 | 4_LLM label unavailable: bmw, series, tour, of, grand, the, new, kidney, and, is | ['LLM label unavailable: bmw, series, tour, of, grand, the, new, kidney, and, is'] |
| 5 | 245 | 5_LLM label unavailable: sonata, hyundai, safety, the, and, features, to, elantra, now, with | ['LLM label unavailable: sonata, hyundai, safety, the, and, features, to, elantra, now, with'] |
| 6 | 229 | 6_LLM label unavailable: volvo, xc90, s60, new, the, and, we, car, our, safety | ['LLM label unavailable: volvo, xc90, s60, new, the, and, we, car, our, safety'] |
| 7 | 221 | 7_LLM label unavailable: assist, parking, lane, spot, you, blind, driver, traffic, alert, the | ['LLM label unavailable: assist, parking, lane, spot, you, blind, driver, traffic, alert, the'] |
| 8 | 219 | 8_LLM label unavailable: ioniq, hyundai, and, the, to, with, charging, of, for, you | ['LLM label unavailable: ioniq, hyundai, and, the, to, with, charging, of, for, you'] |
| 9 | 218 | 9_LLM label unavailable: kia, ev6, ev, of, our, the, in, to, gt, india | ['LLM label unavailable: kia, ev6, ev, of, our, the, in, to, gt, india'] |
| 10 | 204 | 10_LLM label unavailable: nissan, leaf, aria, altima, you, new, propilot, your, to, the | ['LLM label unavailable: nissan, leaf, aria, altima, you, new, propilot, your, to, the'] |
| 11 | 188 | 11_LLM label unavailable: your, apple, carplay, android, you, smartphone, can, and, phone, auto | ['LLM label unavailable: your, apple, carplay, android, you, smartphone, can, and, phone, auto'] |
| 12 | 186 | 12_LLM label unavailable: audi, tron, the, quattro, of, q8, light, and, a7, a3 | ['LLM label unavailable: audi, tron, the, quattro, of, q8, light, and, a7, a3'] |
| 13 | 185 | 13_LLM label unavailable: screen, mbux, display, the, and, console, you, center, control, hyperscreen | ['LLM label unavailable: screen, mbux, display, the, and, console, you, center, control, hyperscreen'] |
| 14 | 182 | 14_LLM label unavailable: lexus, nx, the, and, new, to, of, with, ux, ls | ['LLM label unavailable: lexus, nx, the, and, new, to, of, with, ux, ls'] |
| 15 | 173 | 15_LLM label unavailable: electric, to, cars, ev, we, that, our, be, car, in | ['LLM label unavailable: electric, to, cars, ev, we, that, our, be, car, in'] |
| 16 | 172 | 16_LLM label unavailable: elantra, hyundai, we, our, the, to, and, new, for, of | ['LLM label unavailable: elantra, hyundai, we, our, the, to, and, new, for, of'] |
| 17 | 161 | 17_Vehicle Front-End Design | ['Vehicle Front-End Design'] |
| 18 | 160 | 18_LLM label unavailable: mercedes, benz, class, new, the, of, is, to, and, this | ['LLM label unavailable: mercedes, benz, class, new, the, of, is, to, and, this'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | LLM label unavailable: the, and, to, of, in, is, you, it, that, with |
| 0 | LLM label unavailable: we, it, you, to, that, and, of, this, the, in |
| 1 | LLM label unavailable: interior, seat, seats, the, and, of, leather, in, it, is |
| 2 | LLM label unavailable: charging, charge, you, range, miles, can, to, it, the, charger |
| 3 | LLM label unavailable: electric, torque, hybrid, motor, the, pedal, power, battery, drive, engine |
| 4 | LLM label unavailable: bmw, series, tour, of, grand, the, new, kidney, and, is |
| 5 | LLM label unavailable: sonata, hyundai, safety, the, and, features, to, elantra, now, with |
| 6 | LLM label unavailable: volvo, xc90, s60, new, the, and, we, car, our, safety |
| 7 | LLM label unavailable: assist, parking, lane, spot, you, blind, driver, traffic, alert, the |
| 8 | LLM label unavailable: ioniq, hyundai, and, the, to, with, charging, of, for, you |
| 9 | LLM label unavailable: kia, ev6, ev, of, our, the, in, to, gt, india |
| 10 | LLM label unavailable: nissan, leaf, aria, altima, you, new, propilot, your, to, the |
| 11 | LLM label unavailable: your, apple, carplay, android, you, smartphone, can, and, phone, auto |
| 12 | LLM label unavailable: audi, tron, the, quattro, of, q8, light, and, a7, a3 |
| 13 | LLM label unavailable: screen, mbux, display, the, and, console, you, center, control, hyperscreen |
| 14 | LLM label unavailable: lexus, nx, the, and, new, to, of, with, ux, ls |
| 15 | LLM label unavailable: electric, to, cars, ev, we, that, our, be, car, in |
| 16 | LLM label unavailable: elantra, hyundai, we, our, the, to, and, new, for, of |
| 17 | Vehicle Front-End Design |
| 18 | LLM label unavailable: mercedes, benz, class, new, the, of, is, to, and, this |
### llm_google_gemini_3_1_pro_preview

- status: `ok`
- topics_with_custom_stopword_hits: 7

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2180 | -1_General | ['General'] |
| 0 | 2129 | 0_General | ['General'] |
| 1 | 442 | 1_Interior | ['Interior'] |
| 2 | 360 | 2_EV | ['EV'] |
| 3 | 277 | 3_Electric | ['Electric'] |
| 4 | 245 | 4_BMW | ['BMW'] |
| 5 | 245 | 5_Hyundai | ['Hyundai'] |
| 6 | 229 | 6_Volvo | ['Volvo'] |
| 7 | 221 | 7_Advanced | ['Advanced'] |
| 8 | 219 | 8_Hyundai | ['Hyundai'] |
| 9 | 218 | 9_Kia | ['Kia'] |
| 10 | 204 | 10_Nissan | ['Nissan'] |
| 11 | 188 | 11_Smartphone | ['Smartphone'] |
| 12 | 186 | 12_Audi | ['Audi'] |
| 13 | 185 | 13_Inf | ['Inf'] |
| 14 | 182 | 14_LLM label unavailable: lexus, nx, the, and, new, to, of, with, ux, ls | ['LLM label unavailable: lexus, nx, the, and, new, to, of, with, ux, ls'] |
| 15 | 173 | 15_Premium | ['Premium'] |
| 16 | 172 | 16_Hyundai | ['Hyundai'] |
| 17 | 161 | 17_filtered_topic_terms_unavailable | ['filtered_topic_terms_unavailable'] |
| 18 | 160 | 18_Mercedes | ['Mercedes'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | General |
| 0 | General |
| 1 | Interior |
| 2 | EV |
| 3 | Electric |
| 4 | BMW |
| 5 | Hyundai |
| 6 | Volvo |
| 7 | Advanced |
| 8 | Hyundai |
| 9 | Kia |
| 10 | Nissan |
| 11 | Smartphone |
| 12 | Audi |
| 13 | Inf |
| 14 | LLM label unavailable: lexus, nx, the, and, new, to, of, with, ux, ls |
| 15 | Premium |
| 16 | Hyundai |
| 17 | filtered_topic_terms_unavailable |
| 18 | Mercedes |

## Output Files

| topic_info_default | topic_words_default | topic_info_keybert | topic_words_keybert | topic_info_pos | topic_words_pos | topic_info_mmr | topic_words_mmr | document_topics | representative_docs | topic_size_distribution | final_config | representation_errors | topic_info_llm_anthropic_claude_opus_4_7 | topic_words_llm_anthropic_claude_opus_4_7 | topic_info_llm_openai_gpt_5_5 | topic_words_llm_openai_gpt_5_5 | topic_info_llm_google_gemini_3_1_pro_preview | topic_words_llm_google_gemini_3_1_pro_preview |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance/topic_info_default.csv | best_balance/topic_words_default.csv | best_balance/topic_info_keybert.csv | best_balance/topic_words_keybert.csv | best_balance/topic_info_pos.csv | best_balance/topic_words_pos.csv | best_balance/topic_info_mmr.csv | best_balance/topic_words_mmr.csv | best_balance/document_topics.csv | best_balance/representative_docs.csv | best_balance/topic_size_distribution.csv | best_balance/final_config.json | best_balance/representation_errors.json | best_balance/topic_info_llm_anthropic_claude_opus_4_7.csv | best_balance/topic_words_llm_anthropic_claude_opus_4_7.csv | best_balance/topic_info_llm_openai_gpt_5_5.csv | best_balance/topic_words_llm_openai_gpt_5_5.csv | best_balance/topic_info_llm_google_gemini_3_1_pro_preview.csv | best_balance/topic_words_llm_google_gemini_3_1_pro_preview.csv |

## Representation Errors

```json
[
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "20",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "26",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "33",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "48",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  }
]
```

## Notes

KeyBERT-Inspired、POS、MMR 與 LLM 只更新 topic representation，不改變 UMAP/HDBSCAN topic labels，因此三者的 clustering metrics 會相同。
