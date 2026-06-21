# A06-8-REV BERTopic + A05-8.4(human) stopwords + representation models - most_topics

## Run Info

| started_at | finished_at | dataset | embedding_model | embedding_note | custom_stopword_count | llm_provider | llm_models |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-05T12:01:16.155126+00:00 | 2026-06-05T12:15:00.940066+00:00 | Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset | all-MiniLM-L6-v2 | 重用 A04-8(orig) embeddings 快取並複製到 M01-8。 | 170 | OpenRouter | anthropic/claude-opus-4.7, openai/gpt-5.5, google/gemini-3.1-pro-preview |

## Parameters

| selection_label | selection_reason | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics | 在可接受 noise_ratio 下保留最多有效主題。 | 5 | 5 | 0.0000 | cosine | 42 | 50 | 5 | leaf | 0.0000 | euclidean |

## Metrics

| n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 70 | 0.2974 | 3312 | 374 | 245 | 374 | 0.0336 | 0.0754 | 0.9673 | 0.8856 |

## Compared With Provided Baseline

| selection_label | baseline_noise_ratio | a06_noise_ratio | baseline_n_clusters | a06_n_clusters | baseline_largest_topic_ratio | a06_largest_topic_ratio | baseline_top3_topic_ratio | a06_top3_topic_ratio | baseline_balance_score | a06_balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics | 0.3337 | 0.2974 | 73 | 70 | 0.0286 | 0.0336 | 0.0663 | 0.0754 | 0.8781 | 0.8856 |

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
| -1 | 3312 | -1_car_new_vehicle_rear | ['car', 'new', 'vehicle', 'rear', 'electric', 'driving', 'hybrid', 'design', 'battery', 'charging'] |
| 0 | 374 | 0_ladies_interesting_fun_congratulations | ['ladies', 'interesting', 'fun', 'congratulations', 'moment', 'broadcast', 'liked', 'able', 'answer', 'enjoy'] |
| 1 | 245 | 1_bmw_series_grand tour_tour | ['bmw', 'series', 'grand tour', 'tour', 'grand', 'bmw series', 'new bmw', 'kidney', 'new', 'i4'] |
| 2 | 221 | 2_assist_parking_lane_spot | ['assist', 'parking', 'lane', 'spot', 'blind', 'blind spot', 'alert', 'traffic', 'braking', 'driver'] |
| 3 | 220 | 3_car_cars_customers_design | ['car', 'cars', 'customers', 'design', 'vehicle', 'prototypes', 'world', 'mobility', 'experience', 'lives'] |
| 4 | 219 | 4_ioniq_hyundai_charging_platform | ['ioniq', 'hyundai', 'charging', 'platform', 'electric', 'vehicle', '2025', 'rear', 'ev', 'assist'] |
| 5 | 218 | 5_kia_ev6_ev_india | ['kia', 'ev6', 'ev', 'india', 'new kia', 'gt', 'niro', 'ev6 gt', 'ev9', 'fleet'] |
| 6 | 204 | 6_nissan_leaf_nissan leaf_aria | ['nissan', 'leaf', 'nissan leaf', 'aria', 'new nissan', 'altima', 'propilot', 'new', 'nissan intelligent', 'intelligent'] |
| 7 | 203 | 7_seat_leather_seats_interior | ['seat', 'leather', 'seats', 'interior', 'materials', 'comfort', 'trim', 'space', 'upholstery', 'comfortable'] |
| 8 | 188 | 8_carplay_apple_android_apple carplay | ['carplay', 'apple', 'android', 'apple carplay', 'android auto', 'smartphone', 'phone', 'alexa', 'auto', 'touchscreen'] |
| 9 | 185 | 9_mbux_screen_display_console | ['mbux', 'screen', 'display', 'console', 'center console', 'center', 'control', 'buttons', 'digital', 'functions'] |
| 10 | 183 | 10_drive_car_driving_driver | ['drive', 'car', 'driving', 'driver', 'ride', 'beautiful', 'driven', 'roads', 'drive car', 'does feel'] |
| 11 | 182 | 11_lexus_nx_ux_ls | ['lexus', 'nx', 'ux', 'ls', 'new', 'luxury', 'gs', 'es', 'lc', 'brand'] |
| 12 | 173 | 12_electric_electric cars_cars_ev | ['electric', 'electric cars', 'cars', 'ev', 'electric vehicles', 'vehicles', 'car', 'electrification', 'electric vehicle', 'electric car'] |
| 13 | 172 | 13_elantra_hyundai_new elantra_hyundai elantra | ['elantra', 'hyundai', 'new elantra', 'hyundai elantra', 'new', 'generation', 'generation elantra', 'elr', 'compact', 'super bowl'] |
| 14 | 165 | 14_torque_electric_motor_hybrid | ['torque', 'electric', 'motor', 'hybrid', 'power', 'electric motor', 'engine', 'horsepower', 'plug', 'plug hybrid'] |
| 15 | 160 | 15_mercedes_benz_mercedes benz_class | ['mercedes', 'benz', 'mercedes benz', 'class', 'benz class', 'new mercedes', 'new class', 'new', 'mercedes amg', 'amg'] |
| 16 | 156 | 16_charging_charge_level_stations | ['charging', 'charge', 'level', 'stations', 'mercedes', 'charging stations', 'charger', 'plug', 'home', 'minutes'] |
| 17 | 155 | 17_navigation_display_information_view | ['navigation', 'display', 'information', 'view', 'route', 'destination', 'head display', 'camera', 'head', 'voice'] |
| 18 | 149 | 18_prius_prius prime_prime_hybrid | ['prius', 'prius prime', 'prime', 'hybrid', 'toyota', 'gallon', 'efficiency', 'plug', 'plug hybrid', 'awd'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car, new, vehicle, rear, electric, driving, hybrid, design, battery, charging |
| 0 | ladies, interesting, fun, congratulations, moment, broadcast, liked, able, answer, enjoy |
| 1 | bmw, series, grand tour, tour, grand, bmw series, new bmw, kidney, new, i4 |
| 2 | assist, parking, lane, spot, blind, blind spot, alert, traffic, braking, driver |
| 3 | car, cars, customers, design, vehicle, prototypes, world, mobility, experience, lives |
| 4 | ioniq, hyundai, charging, platform, electric, vehicle, 2025, rear, ev, assist |
| 5 | kia, ev6, ev, india, new kia, gt, niro, ev6 gt, ev9, fleet |
| 6 | nissan, leaf, nissan leaf, aria, new nissan, altima, propilot, new, nissan intelligent, intelligent |
| 7 | seat, leather, seats, interior, materials, comfort, trim, space, upholstery, comfortable |
| 8 | carplay, apple, android, apple carplay, android auto, smartphone, phone, alexa, auto, touchscreen |
| 9 | mbux, screen, display, console, center console, center, control, buttons, digital, functions |
| 10 | drive, car, driving, driver, ride, beautiful, driven, roads, drive car, does feel |
| 11 | lexus, nx, ux, ls, new, luxury, gs, es, lc, brand |
| 12 | electric, electric cars, cars, ev, electric vehicles, vehicles, car, electrification, electric vehicle, electric car |
| 13 | elantra, hyundai, new elantra, hyundai elantra, new, generation, generation elantra, elr, compact, super bowl |
| 14 | torque, electric, motor, hybrid, power, electric motor, engine, horsepower, plug, plug hybrid |
| 15 | mercedes, benz, mercedes benz, class, benz class, new mercedes, new class, new, mercedes amg, amg |
| 16 | charging, charge, level, stations, mercedes, charging stations, charger, plug, home, minutes |
| 17 | navigation, display, information, view, route, destination, head display, camera, head, voice |
| 18 | prius, prius prime, prime, hybrid, toyota, gallon, efficiency, plug, plug hybrid, awd |
### keybert

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 3312 | -1_bmw_car_vehicle_hybrid | ['bmw', 'car', 'vehicle', 'hybrid', 'driving', 'drive', 'electric', 'technology'] |
| 0 | 374 | 0_filtered_topic_terms_unavailable | ['filtered_topic_terms_unavailable'] |
| 1 | 245 | 1_bmw_sedan_coupe_car | ['bmw', 'sedan', 'coupe', 'car', 'touring', 'hybrid', 'tour', 'i4', 'x6'] |
| 2 | 221 | 2_safety_parking_detection_detects | ['safety', 'parking', 'detection', 'detects', 'detect', 'blind', 'pedestrian', 'driving', 'view', 'pedestrians'] |
| 3 | 220 | 3_cars_car_vehicle_prototype | ['cars', 'car', 'vehicle', 'prototype', 'design', 'prototypes', 'technology', 'mobility', 'experience'] |
| 4 | 219 | 4_ioniq_hyundai_hybrid_ev | ['ioniq', 'hyundai', 'hybrid', 'ev', 'electric', 'id4', 'powertrains', 'vehicle', 'vehicles', 'plug'] |
| 5 | 218 | 5_kia_ev6_ev_ev9 | ['kia', 'ev6', 'ev', 'ev9', 'ev4', 'e6', 'evs', 'vehicle', 'vehicles', 'suvs'] |
| 6 | 204 | 6_nissanusa_nissan_leaf_ev | ['nissanusa', 'nissan', 'leaf', 'ev', 'sedan', 'electric', 'altima', 'mobility', 'ariya', 'driving'] |
| 7 | 203 | 7_seats_seat_comfortable_comfort | ['seats', 'seat', 'comfortable', 'comfort', 'interior', 'leather', 'sitting', 'passengers', 'sit', 'design'] |
| 8 | 188 | 8_smartphone_android_iphone_mobile | ['smartphone', 'android', 'iphone', 'mobile', 'touchscreen', 'apps', 'carplay', 'devices', 'app', 'apple'] |
| 9 | 185 | 9_controls_touchscreen_control_mercedes | ['controls', 'touchscreen', 'control', 'mercedes', 'screens', 'screen', 'cockpit', 'steering', 'buttons', 'mbux'] |
| 10 | 183 | 10_drive_driving_driver_driven | ['drive', 'driving', 'driver', 'driven', 'car', 'ride', 'road', 'roads', 'cars'] |
| 11 | 182 | 11_lexus_rx_hybrid_vehicle | ['lexus', 'rx', 'hybrid', 'vehicle', 'vehicles', 'sedan', 'car', 'ilx', 'nx', 'driver'] |
| 12 | 173 | 12_tesla_ev_cars_electrification | ['tesla', 'ev', 'cars', 'electrification', 'car', 'evs', 'vehicles', 'electric', 'emissions', 'vehicle'] |
| 13 | 172 | 13_hyundai_elantra_elr_sedan | ['hyundai', 'elantra', 'elr', 'sedan', 'car', 'brand', '2021', 'design'] |
| 14 | 165 | 14_powertrain_motors_motor_vehicle | ['powertrain', 'motors', 'motor', 'vehicle', 'horsepower', 'hybrid', 'torque', 'hybrids', 'car', 'drive'] |
| 15 | 160 | 15_mercedes_benz_automotive_sedan | ['mercedes', 'benz', 'automotive', 'sedan', 'cars', 'flagship', 'car', 'class', 'model', 'luxury'] |
| 16 | 156 | 16_charging_charge_charger_charged | ['charging', 'charge', 'charger', 'charged', 'level', 'chargers', 'outlet', 'plug', 'cord', 'battery'] |
| 17 | 155 | 17_navigation_steering_view_navigator | ['navigation', 'steering', 'view', 'navigator', 'display', 'screen', 'driving', 'driver', 'settings', 'vehicle'] |
| 18 | 149 | 18_prius_hybrid_toyota_toyotacare | ['prius', 'hybrid', 'toyota', 'toyotacare', 'prime', 'efficiency', 'mileage', 'vehicle', 'per', 'convenience'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | bmw, car, vehicle, hybrid, driving, drive, electric, technology |
| 0 | filtered_topic_terms_unavailable |
| 1 | bmw, sedan, coupe, car, touring, hybrid, tour, i4, x6 |
| 2 | safety, parking, detection, detects, detect, blind, pedestrian, driving, view, pedestrians |
| 3 | cars, car, vehicle, prototype, design, prototypes, technology, mobility, experience |
| 4 | ioniq, hyundai, hybrid, ev, electric, id4, powertrains, vehicle, vehicles, plug |
| 5 | kia, ev6, ev, ev9, ev4, e6, evs, vehicle, vehicles, suvs |
| 6 | nissanusa, nissan, leaf, ev, sedan, electric, altima, mobility, ariya, driving |
| 7 | seats, seat, comfortable, comfort, interior, leather, sitting, passengers, sit, design |
| 8 | smartphone, android, iphone, mobile, touchscreen, apps, carplay, devices, app, apple |
| 9 | controls, touchscreen, control, mercedes, screens, screen, cockpit, steering, buttons, mbux |
| 10 | drive, driving, driver, driven, car, ride, road, roads, cars |
| 11 | lexus, rx, hybrid, vehicle, vehicles, sedan, car, ilx, nx, driver |
| 12 | tesla, ev, cars, electrification, car, evs, vehicles, electric, emissions, vehicle |
| 13 | hyundai, elantra, elr, sedan, car, brand, 2021, design |
| 14 | powertrain, motors, motor, vehicle, horsepower, hybrid, torque, hybrids, car, drive |
| 15 | mercedes, benz, automotive, sedan, cars, flagship, car, class, model, luxury |
| 16 | charging, charge, charger, charged, level, chargers, outlet, plug, cord, battery |
| 17 | navigation, steering, view, navigator, display, screen, driving, driver, settings, vehicle |
| 18 | prius, hybrid, toyota, toyotacare, prime, efficiency, mileage, vehicle, per, convenience |
### pos

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 3312 | -1_car_new_vehicle_electric | ['car', 'new', 'vehicle', 'electric', 'rear', 'first', 'standard', 'available'] |
| 0 | 374 | 0_filtered_topic_terms_unavailable | ['filtered_topic_terms_unavailable'] |
| 1 | 245 | 1_series_grand_new_kidney | ['series', 'grand', 'new', 'kidney', 'design', 'touring', 'driving', 'episode', 'dynamics'] |
| 2 | 221 | 2_assist_parking_lane_spot | ['assist', 'parking', 'lane', 'spot', 'blind', 'alert', 'traffic', 'driver', 'braking', 'emergency'] |
| 3 | 220 | 3_car_cars_design_customers | ['car', 'cars', 'design', 'customers', 'vehicle', 'world', 'experience', 'new'] |
| 4 | 219 | 4_electric_platform_vehicle_rear | ['electric', 'platform', 'vehicle', 'rear', 'interior', 'first', 'assist', 'new', 'design'] |
| 5 | 218 | 5_new_fleet_vehicle_customers | ['new', 'fleet', 'vehicle', 'customers', 'electric', 'sustainable', 'first', 'vehicles', 'world'] |
| 6 | 204 | 6_nissan_leaf_new_intelligent | ['nissan', 'leaf', 'new', 'intelligent', 'technology', 'driving', 'drive', 'first', 'assist'] |
| 7 | 203 | 7_seat_seats_leather_interior | ['seat', 'seats', 'leather', 'interior', 'materials', 'back', 'comfort', 'space', 'trim', 'upholstery'] |
| 8 | 188 | 8_carplay_smartphone_phone_touchscreen | ['carplay', 'smartphone', 'phone', 'touchscreen', 'available', 'connected', 'profile', 'wireless', 'apps', 'car'] |
| 9 | 185 | 9_screen_display_console_center | ['screen', 'display', 'console', 'center', 'control', 'hyperscreen', 'buttons', 'digital', 'functions', 'air'] |
| 10 | 183 | 10_drive_car_driving_driver | ['drive', 'car', 'driving', 'driver', 'beautiful'] |
| 11 | 182 | 11_lexus_new_luxury_brand | ['lexus', 'new', 'luxury', 'brand', 'system', 'safety', 'hybrid'] |
| 12 | 173 | 12_electric_cars_car_vehicles | ['electric', 'cars', 'car', 'vehicles', 'electrification', 'vehicle', 'future', 'battery', 'customers'] |
| 13 | 172 | 13_new_generation_design_compact | ['new', 'generation', 'design', 'compact', 'sedan', 'customers', 'model', 'car'] |
| 14 | 165 | 14_torque_electric_motor_hybrid | ['torque', 'electric', 'motor', 'hybrid', 'power', 'engine', 'horsepower', 'plug', 'drive', 'motors'] |
| 15 | 160 | 15_class_new_car_luxury | ['class', 'new', 'car', 'luxury', 'world', 'safety', 'coupe', 'star', 'cars', 'sedan'] |
| 16 | 156 | 16_charging_charge_level_stations | ['charging', 'charge', 'level', 'stations', 'plug', 'charger', 'home', 'minutes', 'route', 'volt'] |
| 17 | 155 | 17_navigation_display_information_view | ['navigation', 'display', 'information', 'view', 'route', 'system', 'destination', 'camera', 'head', 'driver'] |
| 18 | 149 | 18_hybrid_gallon_efficiency_plug | ['hybrid', 'gallon', 'efficiency', 'plug', 'drive', 'fuel', 'available'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car, new, vehicle, electric, rear, first, standard, available |
| 0 | filtered_topic_terms_unavailable |
| 1 | series, grand, new, kidney, design, touring, driving, episode, dynamics |
| 2 | assist, parking, lane, spot, blind, alert, traffic, driver, braking, emergency |
| 3 | car, cars, design, customers, vehicle, world, experience, new |
| 4 | electric, platform, vehicle, rear, interior, first, assist, new, design |
| 5 | new, fleet, vehicle, customers, electric, sustainable, first, vehicles, world |
| 6 | nissan, leaf, new, intelligent, technology, driving, drive, first, assist |
| 7 | seat, seats, leather, interior, materials, back, comfort, space, trim, upholstery |
| 8 | carplay, smartphone, phone, touchscreen, available, connected, profile, wireless, apps, car |
| 9 | screen, display, console, center, control, hyperscreen, buttons, digital, functions, air |
| 10 | drive, car, driving, driver, beautiful |
| 11 | lexus, new, luxury, brand, system, safety, hybrid |
| 12 | electric, cars, car, vehicles, electrification, vehicle, future, battery, customers |
| 13 | new, generation, design, compact, sedan, customers, model, car |
| 14 | torque, electric, motor, hybrid, power, engine, horsepower, plug, drive, motors |
| 15 | class, new, car, luxury, world, safety, coupe, star, cars, sedan |
| 16 | charging, charge, level, stations, plug, charger, home, minutes, route, volt |
| 17 | navigation, display, information, view, route, system, destination, camera, head, driver |
| 18 | hybrid, gallon, efficiency, plug, drive, fuel, available |
### mmr

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 3312 | -1_car | ['car'] |
| 0 | 374 | 0_filtered_topic_terms_unavailable | ['filtered_topic_terms_unavailable'] |
| 1 | 245 | 1_bmw_grand_kidney_design | ['bmw', 'grand', 'kidney', 'design', 'i4', 'touring', 'driving', 'episode', 'dynamics'] |
| 2 | 221 | 2_assist_parking_lane_blind | ['assist', 'parking', 'lane', 'blind', 'alert', 'traffic', 'driver', 'braking', 'cross', 'steering'] |
| 3 | 220 | 3_cars_about_design_customers | ['cars', 'about', 'design', 'customers', 'vehicle'] |
| 4 | 219 | 4_ioniq_hyundai_charging_electric | ['ioniq', 'hyundai', 'charging', 'electric', 'platform', 'vehicle', 'rear', 'interior', 'assist', 'ev'] |
| 5 | 218 | 5_kia_ev6_ev_gt | ['kia', 'ev6', 'ev', 'gt', 'india', 'niro', 'ev9', 'vehicle', 'ev4'] |
| 6 | 204 | 6_nissan_leaf_aria_altima | ['nissan', 'leaf', 'aria', 'altima', 'propilot', 'ev', 'intelligent', 'technology', 'driving', 'ariya'] |
| 7 | 203 | 7_seat_seats_leather_interior | ['seat', 'seats', 'leather', 'interior', 'materials', 'comfort', 'space', 'upholstery', 'comfortable', 'passengers'] |
| 8 | 188 | 8_apple_carplay_android_smartphone | ['apple', 'carplay', 'android', 'smartphone', 'auto', 'alexa', 'touchscreen', 'wireless', 'apps', 'services'] |
| 9 | 185 | 9_mbux_screen_display_console | ['mbux', 'screen', 'display', 'console', 'hyperscreen', 'buttons', 'digital', 'also', 'displays', 'controls'] |
| 10 | 183 | 10_drive_car_driving_no | ['drive', 'car', 'driving', 'no', 'take'] |
| 11 | 182 | 11_lexus_nx_ls_ct | ['lexus', 'nx', 'ls', 'ct', 'luxury', 'gs', 'lc500', 'brand', 'lc'] |
| 12 | 173 | 12_electric_cars_ev_electrification | ['electric', 'cars', 'ev', 'electrification', 'vehicle', 'future'] |
| 13 | 172 | 13_elantra_hyundai_generation_elr | ['elantra', 'hyundai', 'generation', 'elr', 'design', 'compact', 'bowl', 'sedan'] |
| 14 | 165 | 14_torque_electric_hybrid_horsepower | ['torque', 'electric', 'hybrid', 'horsepower', 'drive', 'motors', 'battery', 'hour', 'kilowatt'] |
| 15 | 160 | 15_mercedes_benz_class_the | ['mercedes', 'benz', 'class', 'the', 'amg', 'car', 'luxury', 'about', 'glb'] |
| 16 | 156 | 16_charging_level_mercedes_stations | ['charging', 'level', 'mercedes', 'stations', 'charger', 'minutes', '240', 'volt', 'dc', 'cable'] |
| 17 | 155 | 17_navigation_information_view_route | ['navigation', 'information', 'view', 'route', 'system', 'camera', 'head', 'also', 'driver', 'voice'] |
| 18 | 149 | 18_prius_hybrid_toyota_gallon | ['prius', 'hybrid', 'toyota', 'gallon', 'per', 'efficiency', 'fuel', 'seats', 'awd'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car |
| 0 | filtered_topic_terms_unavailable |
| 1 | bmw, grand, kidney, design, i4, touring, driving, episode, dynamics |
| 2 | assist, parking, lane, blind, alert, traffic, driver, braking, cross, steering |
| 3 | cars, about, design, customers, vehicle |
| 4 | ioniq, hyundai, charging, electric, platform, vehicle, rear, interior, assist, ev |
| 5 | kia, ev6, ev, gt, india, niro, ev9, vehicle, ev4 |
| 6 | nissan, leaf, aria, altima, propilot, ev, intelligent, technology, driving, ariya |
| 7 | seat, seats, leather, interior, materials, comfort, space, upholstery, comfortable, passengers |
| 8 | apple, carplay, android, smartphone, auto, alexa, touchscreen, wireless, apps, services |
| 9 | mbux, screen, display, console, hyperscreen, buttons, digital, also, displays, controls |
| 10 | drive, car, driving, no, take |
| 11 | lexus, nx, ls, ct, luxury, gs, lc500, brand, lc |
| 12 | electric, cars, ev, electrification, vehicle, future |
| 13 | elantra, hyundai, generation, elr, design, compact, bowl, sedan |
| 14 | torque, electric, hybrid, horsepower, drive, motors, battery, hour, kilowatt |
| 15 | mercedes, benz, class, the, amg, car, luxury, about, glb |
| 16 | charging, level, mercedes, stations, charger, minutes, 240, volt, dc, cable |
| 17 | navigation, information, view, route, system, camera, head, also, driver, voice |
| 18 | prius, hybrid, toyota, gallon, per, efficiency, fuel, seats, awd |
### llm_anthropic_claude_opus_4_7

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 3312 | -1_Vehicle Features and Driver Assistance | ['Vehicle Features and Driver Assistance'] |
| 0 | 374 | 0_Casual Conversation Filler | ['Casual Conversation Filler'] |
| 1 | 245 | 1_BMW Vehicle Features and Design | ['BMW Vehicle Features and Design'] |
| 2 | 221 | 2_Driver Assistance and Parking Features | ['Driver Assistance and Parking Features'] |
| 3 | 220 | 3_Driving Experience and Enjoyment | ['Driving Experience and Enjoyment'] |
| 4 | 219 | 4_Hyundai IONIQ EV Lineup | ['Hyundai IONIQ EV Lineup'] |
| 5 | 218 | 5_Kia and BYD EV Models | ['Kia and BYD EV Models'] |
| 6 | 204 | 6_Nissan Leaf and ProPilot | ['Nissan Leaf and ProPilot'] |
| 7 | 203 | 7_EV Interior Seats and Materials | ['EV Interior Seats and Materials'] |
| 8 | 188 | 8_Smartphone Integration and Infotainment | ['Smartphone Integration and Infotainment'] |
| 9 | 185 | 9_MBUX Hyperscreen Infotainment Display | ['MBUX Hyperscreen Infotainment Display'] |
| 10 | 183 | 10_Test Drive Experience | ['Test Drive Experience'] |
| 11 | 182 | 11_Acura and Lexus Hybrid Models | ['Acura and Lexus Hybrid Models'] |
| 12 | 173 | 12_Premium Electric Vehicle Identity | ['Premium Electric Vehicle Identity'] |
| 13 | 172 | 13_Hyundai Elantra Product Updates | ['Hyundai Elantra Product Updates'] |
| 14 | 165 | 14_Hybrid Powertrain Motor Torque | ['Hybrid Powertrain Motor Torque'] |
| 15 | 160 | 15_Mercedes-Benz EV Models | ['Mercedes-Benz EV Models'] |
| 16 | 156 | 16_Home and Fast Charging Options | ['Home and Fast Charging Options'] |
| 17 | 155 | 17_Navigation and Head-Up Display | ['Navigation and Head-Up Display'] |
| 18 | 149 | 18_Toyota Prius Hybrid Efficiency | ['Toyota Prius Hybrid Efficiency'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | Vehicle Features and Driver Assistance |
| 0 | Casual Conversation Filler |
| 1 | BMW Vehicle Features and Design |
| 2 | Driver Assistance and Parking Features |
| 3 | Driving Experience and Enjoyment |
| 4 | Hyundai IONIQ EV Lineup |
| 5 | Kia and BYD EV Models |
| 6 | Nissan Leaf and ProPilot |
| 7 | EV Interior Seats and Materials |
| 8 | Smartphone Integration and Infotainment |
| 9 | MBUX Hyperscreen Infotainment Display |
| 10 | Test Drive Experience |
| 11 | Acura and Lexus Hybrid Models |
| 12 | Premium Electric Vehicle Identity |
| 13 | Hyundai Elantra Product Updates |
| 14 | Hybrid Powertrain Motor Torque |
| 15 | Mercedes-Benz EV Models |
| 16 | Home and Fast Charging Options |
| 17 | Navigation and Head-Up Display |
| 18 | Toyota Prius Hybrid Efficiency |
### llm_openai_gpt_5_5

- status: `ok`
- topics_with_custom_stopword_hits: 48

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 3312 | -1_LLM label unavailable: the, and, to, it, of, in, you, is, we, that | ['LLM label unavailable: the, and, to, it, of, in, you, is, we, that'] |
| 0 | 374 | 0_LLM label unavailable: thank, you, much, good, don, to, see, for, come, going | ['LLM label unavailable: thank, you, much, good, don, to, see, for, come, going'] |
| 1 | 245 | 1_LLM label unavailable: bmw, series, tour, grand, of, the, new, kidney, and, is | ['LLM label unavailable: bmw, series, tour, grand, of, the, new, kidney, and, is'] |
| 2 | 221 | 2_LLM label unavailable: assist, parking, lane, spot, blind, alert, traffic, driver, you, braking | ['LLM label unavailable: assist, parking, lane, spot, blind, alert, traffic, driver, you, braking'] |
| 3 | 220 | 3_LLM label unavailable: we, car, that, our, it, this, of, to, and, the | ['LLM label unavailable: we, car, that, our, it, this, of, to, and, the'] |
| 4 | 219 | 4_LLM label unavailable: ioniq, hyundai, and, charging, with, to, the, for, of, electric | ['LLM label unavailable: ioniq, hyundai, and, charging, with, to, the, for, of, electric'] |
| 5 | 218 | 5_LLM label unavailable: kia, ev6, ev, our, gt, india, of, niro, the, in | ['LLM label unavailable: kia, ev6, ev, our, gt, india, of, niro, the, in'] |
| 6 | 204 | 6_LLM label unavailable: nissan, leaf, aria, altima, propilot, new, you, your, to, the | ['LLM label unavailable: nissan, leaf, aria, altima, propilot, new, you, your, to, the'] |
| 7 | 203 | 7_LLM label unavailable: seat, seats, leather, interior, and, the, materials, in, of, very | ['LLM label unavailable: seat, seats, leather, interior, and, the, materials, in, of, very'] |
| 8 | 188 | 8_LLM fallback: apple, carplay, your, android | ['LLM fallback: apple, carplay, your, android'] |
| 9 | 185 | 9_LLM fallback: mbux, screen, display, console | ['LLM fallback: mbux, screen, display, console'] |
| 10 | 183 | 10_LLM label unavailable: drive, it, car, do, you, driving, me, this, my, let | ['LLM label unavailable: drive, it, car, do, you, driving, me, this, my, let'] |
| 11 | 182 | 11_LLM label unavailable: lexus, nx, the, and, new, ux, ls, ct, to, of | ['LLM label unavailable: lexus, nx, the, and, new, ux, ls, ct, to, of'] |
| 12 | 173 | 12_LLM label unavailable: electric, cars, to, ev, we, our, be, that, car, are | ['LLM label unavailable: electric, cars, to, ev, we, our, be, that, car, are'] |
| 13 | 172 | 13_LLM label unavailable: elantra, hyundai, we, our, new, to, the, for, and, of | ['LLM label unavailable: elantra, hyundai, we, our, new, to, the, for, and, of'] |
| 14 | 165 | 14_Electric Motor Torque Systems | ['Electric Motor Torque Systems'] |
| 15 | 160 | 15_LLM label unavailable: mercedes, benz, class, new, the, is, of, this, to, amg | ['LLM label unavailable: mercedes, benz, class, new, the, is, of, this, to, amg'] |
| 16 | 156 | 16_EV Charging Options | ['EV Charging Options'] |
| 17 | 155 | 17_Navigation Display Interface | ['Navigation Display Interface'] |
| 18 | 149 | 18_LLM label unavailable: prius, hybrid, prime, toyota, with, its, miles, gallon, per, efficiency | ['LLM label unavailable: prius, hybrid, prime, toyota, with, its, miles, gallon, per, efficiency'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | LLM label unavailable: the, and, to, it, of, in, you, is, we, that |
| 0 | LLM label unavailable: thank, you, much, good, don, to, see, for, come, going |
| 1 | LLM label unavailable: bmw, series, tour, grand, of, the, new, kidney, and, is |
| 2 | LLM label unavailable: assist, parking, lane, spot, blind, alert, traffic, driver, you, braking |
| 3 | LLM label unavailable: we, car, that, our, it, this, of, to, and, the |
| 4 | LLM label unavailable: ioniq, hyundai, and, charging, with, to, the, for, of, electric |
| 5 | LLM label unavailable: kia, ev6, ev, our, gt, india, of, niro, the, in |
| 6 | LLM label unavailable: nissan, leaf, aria, altima, propilot, new, you, your, to, the |
| 7 | LLM label unavailable: seat, seats, leather, interior, and, the, materials, in, of, very |
| 8 | LLM fallback: apple, carplay, your, android |
| 9 | LLM fallback: mbux, screen, display, console |
| 10 | LLM label unavailable: drive, it, car, do, you, driving, me, this, my, let |
| 11 | LLM label unavailable: lexus, nx, the, and, new, ux, ls, ct, to, of |
| 12 | LLM label unavailable: electric, cars, to, ev, we, our, be, that, car, are |
| 13 | LLM label unavailable: elantra, hyundai, we, our, new, to, the, for, and, of |
| 14 | Electric Motor Torque Systems |
| 15 | LLM label unavailable: mercedes, benz, class, new, the, is, of, this, to, amg |
| 16 | EV Charging Options |
| 17 | Navigation Display Interface |
| 18 | LLM label unavailable: prius, hybrid, prime, toyota, with, its, miles, gallon, per, efficiency |
### llm_google_gemini_3_1_pro_preview

- status: `ok`
- topics_with_custom_stopword_hits: 4

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 3312 | -1_Advanced | ['Advanced'] |
| 0 | 374 | 0_Convers | ['Convers'] |
| 1 | 245 | 1_BMW | ['BMW'] |
| 2 | 221 | 2_Advanced | ['Advanced'] |
| 3 | 220 | 3_Advanced | ['Advanced'] |
| 4 | 219 | 4_Hyundai | ['Hyundai'] |
| 5 | 218 | 5_Kia | ['Kia'] |
| 6 | 204 | 6_Nissan | ['Nissan'] |
| 7 | 203 | 7_Premium | ['Premium'] |
| 8 | 188 | 8_Smartphone | ['Smartphone'] |
| 9 | 185 | 9_Inf | ['Inf'] |
| 10 | 183 | 10_LLM label unavailable: drive, it, car, do, you, driving, me, this, my, let | ['LLM label unavailable: drive, it, car, do, you, driving, me, this, my, let'] |
| 11 | 182 | 11_L | ['L'] |
| 12 | 173 | 12_Premium | ['Premium'] |
| 13 | 172 | 13_Hyundai | ['Hyundai'] |
| 14 | 165 | 14_Electric | ['Electric'] |
| 15 | 160 | 15_Mercedes | ['Mercedes'] |
| 16 | 156 | 16_EV | ['EV'] |
| 17 | 155 | 17_Head | ['Head'] |
| 18 | 149 | 18_Toyota | ['Toyota'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | Advanced |
| 0 | Convers |
| 1 | BMW |
| 2 | Advanced |
| 3 | Advanced |
| 4 | Hyundai |
| 5 | Kia |
| 6 | Nissan |
| 7 | Premium |
| 8 | Smartphone |
| 9 | Inf |
| 10 | LLM label unavailable: drive, it, car, do, you, driving, me, this, my, let |
| 11 | L |
| 12 | Premium |
| 13 | Hyundai |
| 14 | Electric |
| 15 | Mercedes |
| 16 | EV |
| 17 | Head |
| 18 | Toyota |

## Output Files

| topic_info_default | topic_words_default | topic_info_keybert | topic_words_keybert | topic_info_pos | topic_words_pos | topic_info_mmr | topic_words_mmr | document_topics | representative_docs | topic_size_distribution | final_config | representation_errors | topic_info_llm_anthropic_claude_opus_4_7 | topic_words_llm_anthropic_claude_opus_4_7 | topic_info_llm_openai_gpt_5_5 | topic_words_llm_openai_gpt_5_5 | topic_info_llm_google_gemini_3_1_pro_preview | topic_words_llm_google_gemini_3_1_pro_preview |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics/topic_info_default.csv | most_topics/topic_words_default.csv | most_topics/topic_info_keybert.csv | most_topics/topic_words_keybert.csv | most_topics/topic_info_pos.csv | most_topics/topic_words_pos.csv | most_topics/topic_info_mmr.csv | most_topics/topic_words_mmr.csv | most_topics/document_topics.csv | most_topics/representative_docs.csv | most_topics/topic_size_distribution.csv | most_topics/final_config.json | most_topics/representation_errors.json | most_topics/topic_info_llm_anthropic_claude_opus_4_7.csv | most_topics/topic_words_llm_anthropic_claude_opus_4_7.csv | most_topics/topic_info_llm_openai_gpt_5_5.csv | most_topics/topic_words_llm_openai_gpt_5_5.csv | most_topics/topic_info_llm_google_gemini_3_1_pro_preview.csv | most_topics/topic_words_llm_google_gemini_3_1_pro_preview.csv |

## Representation Errors

```json
[
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "8",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "9",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "31",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "42",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "46",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "50",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "57",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  }
]
```

## Notes

KeyBERT-Inspired、POS、MMR 與 LLM 只更新 topic representation，不改變 UMAP/HDBSCAN topic labels，因此三者的 clustering metrics 會相同。
