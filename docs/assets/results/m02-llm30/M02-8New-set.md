# M02-8New BERTopic + A05-8.4(human) stopwords + c-TF-IDF reduction - M02-8New

## Run Info

| started_at | finished_at | dataset | embedding_model | embedding_note | custom_stopword_count | llm_provider | llm_model | llm30_runs_per_topic | representative_docs_per_topic |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-05T14:49:27.276463+00:00 | 2026-06-05T15:02:27.826930+00:00 | Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset | all-MiniLM-L6-v2 | 使用 M02-8New 既有 embeddings 快取。 | 170 | OpenRouter | openai/gpt-5.5 | 30 | 6 |

## Parameters

| selection_label | selection_reason | bertopic_nr_topics | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M02-8New | 使用者指定單組參數，並以 BERTopic nr_topics='auto' 做 c-TF-IDF topic reduction。 | auto | 10 | 15 | 0.0000 | cosine | 42 | 50 | 5 | eom | 0.2000 | euclidean |

## Metrics

| n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 24 | 0.2403 | 2676 | 4697 | 876 | 4697 | 0.4218 | 0.5561 | 0.5980 | 0.6821 |

## Stopword Setting

- stopword source: `Result/06.05_A05_stopword/A05-8(orig)REV_tok(para12-80)/A05-8.4(human)_stopword.md`
- 使用 A05-8.4(human) 報告表格第三欄建議停用詞，並加上 sklearn English stop words。
- stopwords 只作用於 BERTopic c-TF-IDF / topic words 表示；embedding 與 HDBSCAN 分群仍使用原始 orig 文本向量。

## Representation Models

- default: BERTopic c-TF-IDF
- keybert: KeyBERT-Inspired
- pos: Part-of-Speech
- mmr: Maximal Marginal Relevance
- llm_openai_gpt_5_5: OpenRouter `openai/gpt-5.5` topic labels

## LLM30 Validation

- 每個非 noise topic 使用 `openai/gpt-5.5` 對相同 keywords 與 6 個代表原句重跑 30 次。
- 穩定判定：normalized label 眾數比例 >= 0.70，或平均 token Jaccard similarity >= 0.65。
- 詳細輸出：`M02-8New_LLM30.md`、`M02-8New_LLM30.csv`。

## Combined Topic Representations

| Topic | Count | Name | LLM | KeyBERT | POS | MMR | Original_Sentences |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -1 | 2676 | -1_car_new_vehicle_design | Noise / Outlier | car, vehicle, design, hybrid, new, drive, technology, driving, so, what | car, new, vehicle, system, first, design, drive | you, car, have, new | The real star of the show, however, is Toyota Safety Sense 2.5 Plus. This active safety system includes a pre-collision system with pedestrian detection, lane departure alert with steering assist, automatic high beams, full speed range dynamic radar cruise control, lane tracing assist, and road sign assist. For added visibility from the driver's seat, blind spot monitor with rear cross traffic alert is standard on the LE grade and above. \|\| Wireless Android Auto compatibility makes it easy to stay connected to Android devices. Plus, there's a standard three month SiriusXM PlatinumPlan trial subscription that includes over 165 channels available in cabin and even more on the SXM mobile app, making it easier than ever to enjoy not just ad free music, but also sports comedy and more. Drivers looking for even more audio enhancements will appreciate that Prius Limited features a JBL premium audio system. \|\| In addition, wireless Android Auto compatibility makes it easy to stay connected to Android devices. Plus, there's a standard 3-month SiriusXM PlatinumPlan trial subscription that includes over 165 channels available in cabin, and even more on the SXM mobile app, making it easier than ever to enjoy not just ad-free music, but also sports, comedy, and more. \|\| start ignition standard active sound control standard multi-view rear camera standard and as if all that wasn't enough Acura went ahead and made its Acura watch advanced safety and driver assistance technology package standard huh standard that has a nice ring to it doesn't it this package includes forward collision warning collision mitigation braking lane departure warning lane keeping assist road departure mitigation and adaptive cruise control standard across all trims. \|\| Let's go. I need my car to look great. I want the kind of automobile that when I walk out of the grocery store, I see it in the parking lot and I say, that's my car. \|\| And as if all that wasn't enough, Acura went ahead and made its Acura watch, advanced safety a driver assistance technology package, standard, huh, standard, that has a nice ring to it doesn't it? This package includes forward collision warning, collision mitigation braking, lane departure warning, lane keeping assist, road departure mitigation and adaptive cruise control, standard across all trims. |
| 0 | 4697 | 0_new_car_design_electric | Hybrid Vehicle Design | vehicle, car, cars, hybrid, design, bmw, drive, kia, engine, driving | new, car, design, vehicle, power, interior, performance | of, new, car, design | The plug-in hybrid models are expected to have an electric driving range of up to a hundred and two kilometers according to WLTP and the new digital hybrid drive settings menu and BMW operating system 8.5 offers intelligent automatic regulation and easy individual switch between drive modes so the combination of reliable long-distance traveling and efficient city driving reaches new heights of convenience and sustainability and then there are the all-new BMW i5 models with cutting-edge holistically sustainable all-electric drive and high-voltage technology. \|\| The new four. Ladies and gentlemen, hello and welcome to BMW. The 4, the all-new BMW 4 Series coupe. \|\| This year, we'll be also launching the all-electric BMW iX3, our first pure electric sports activity vehicle, and the trailblazer for our all-new fifth-generation BMW eDrive technology. We will also be launching further plug-in hybrids during the course of 2020. For example, the new BMW X1 plug-in hybrid and the BMW X2 and the electrified BMW 3 Series Touring will be attractive additions to our wide range. \|\| Hey, I'm Bradley Hasenmaier, and I am thrilled to share a few highlights of the 2020 Acura ILX with incredible standard features and bold new styling. It'll help you stand out when you're ready to step up. Ready to see for yourself? \|\| Let's go. When you get to the ILX, you really see some style with these sharp July LED headlights and that bold pentagon grill. And it only gets better on the inside with paddle shifters and redesigned sports seats. \|\| And if you really want to up the the Annie, opt for the NSX inspired ultra suede trimmed sport seat on the a-spec package engineered with lateral grip to keep you firmly planted in your seat. And you can really tell that the car's been designed around the driver. |
| 1 | 876 | 1_display_control_car_navigation | Driver Assistance and Infotainment | steering, navigation, driving, driver, mode, view, drive, auto, vehicle, carplay | system, car, display, driver, assist, navigation, driving, vehicle, screen, parking | system, display, control, driver, also, assist, navigation, driving, when | Plus you're going to get a host of advanced driving aids like lane keeping assist, lane following assist, driver attention warning, and smart cruise control with stop and go. Additional available safety features and driving tech include highway driving assist two, forward collision avoidance assist with junction turning, surround view monitor, and blind spot view monitor. \|\| Additionally, the standard Blind Spot Monitor with Rear Cross Traffic Alert and Safe Exit Alert are designed to help warn drivers if a vehicle has entered a blind spot, while the available Front and Rear Parking Assist with Automatic Braking and Panoramic View Monitor are designed to help drivers maneuver in tight spaces. \|\| These active safety suites include advanced features like a Pre-Collision System with Pedestrian Detection, Lane Departure Alert with Steering Assist, Automatic High Beams, Full Speed Range Dynamic Radar Cruise Control, Lane Tracing Assist, and Road Sign Assist. Plus, available features like Blind Spot Monitor with Rear Cross-Traffic Alert, front and rear parking assist with automatic braking, and a panoramic view monitor helps see what's surrounding the vehicle, especially in tight spaces. Thanks to its expansive lineup, RAV4 has mass appeal. \|\| You've got easy access buttons and knobs and an easy place to just plug your phone right in too so you can access the available Apple CarPlay and Android Auto integration and it pulls up using these dual screen displays. Oh, this is great. \|\| I mean, it's like we're all riding first class, baby. How about this for convenience? The dual action armrest opens for the driver, Opens for the passenger, one push button, slides all the way back, revealing a place to plug in your phone, that's super smart for your super smart phone. \|\| It's made it to a five-speed automatic transmission. Right. Nice blend of features for each person that's in the market for a car like this. |
| 2 | 620 | 2_auto_happy_episode_season | Automotive Test Drive Episodes | happy, you, go | show, auto | for, show, so | This is, we love the auto show season and New York's the official end of the auto show season so it's been a great run. The shows themselves are incredibly important in terms of getting our brand out in front of a lot of people both media and consumers. This show in and of itself is very important because It is IONIQ. \|\| But we're going to show you what the Auto Show looks like the day before the show. Let's take a look at that video. Hi, I'm Kristin Burt for Hyundai Motor America and we're at the 2015 Los Angeles Auto Show in downtown LA. \|\| Hello, everyone, and thank you for joining us this afternoon. I know it's been a long day. It's great to be kicking off yet another auto show season right here in Los Angeles. \|\| My weekend was absolutely fabulous. I felt like a celebrity. I don't want it to end. \|\| Hey, Tyson. Hey, Lee. How you doing? \|\| Doing great. How are you? Good. |
| 3 | 203 | 3_ioniq_hyundai_charging_electric | Hyundai IONIQ EV Lineup | ioniq, hybrid, hyundai, ev, electric, id4, powertrains, vehicle, vehicles, egmp | electric, vehicle, new, rear, platform, first, design, fast | ioniq, hyundai, charging, electric, vehicle, rear, platform, ev | Now, IONIQ 6 is the newest member of the IONIQ family of electric vehicles, and it's built on the same electric global modular platform as our immensely popular IONIQ 5. And to me, it's the perfect example of Hyundai's electric innovations. Let's start by taking a look at an exterior design that's unlike anything Hyundai has put on the road before. \|\| As a critical pillar in Hyundai's electrification strategy, IONIQ 5 introduces our first dedicated battery electric platform, the eGMP, or Electric Global Modular Platform. We are thrilled to introduce you to Hyundai's first ever IONIQ 5. Our design mission with IONIQ 5 was to create a new mobility experience for the next generation. \|\| Let's just say it. Let's put it out there. What makes Hyundai IONIQ stand out? \|\| Hello everyone, we are here at the New York International Auto Show. My name is Peter Chaney, product information specialist for Hyundai, and I am here with John Shun who is going to talk to us more about the IONIQ lineup. So John, can you break down this vehicle that might be here? \|\| Yes, this is the IONIQ Hybrid. It is the first of three IONIQ models that will be launched very shortly. The IONIQ Hybrid is currently available for sale in all 50 states. \|\| Also here, you see 17-inch alloy wheel design that is an uto-stoke alloy wheel. So even the wheel design itself helps the coefficient of drag and overall dynamics, which of course helps the vehicle's class-leading fuel competition. The 2017 IONIQ lighter vehicle has all the latest advanced active safety features. |
| 4 | 200 | 4_sonata_accord_hyundai sonata_hyundai | Midsize Sedan Market | sonata, hyundai, sedan, hybrid, accord, car, honda, engine, performance, turbo | accord, new, features, safety, standard, car, performance | sonata, accord, hyundai, camry, new, features, honda, 2020, gian | The 2018 Hyundai Sonata. \|\| The 2018 Hyundai Sonata, our best Sonata ever. \|\| The 2018 Hyundai Sonata, our best Sonata ever. \|\| I think it's the best track I've ever been in Abu Dhabi. So modern and it's in another level, compared to the normal tracks. It has been hard because 12 hours is a lot, especially very hot on the inside of the car. \|\| But what we might not realize is that Camry and Accord never recovered. They saw further sales and share losses more than a year before the 2011 earthquake in tsunami. Camry sales in 2010 dipped 31% in their 2007 fee. \|\| Accord sales dropped 28% during the same period. And this slide has continued. Even with triple digits, then it increases in incentive spending. |
| 5 | 187 | 5_charging_charge_level_stations | EV Charging Infrastructure | charging, charge, charger, charged, i3, bmw, chargers, level, outlet, battery | charging, charge, level, plug, stations, home, vehicle, cable, station, i3 | charging, charge, level, plug, cable, station, i3, mercedes, dc | There are several ways you can charge your BMW i3 at home. BMW recommends Level 2 charging using the wall-mounted BMW i-charging station designed to complement your BMW i-vehicle, which reduces charging time for the BMW i3 to around three and a half hours. Now this station and other Level 2 home charging stations charge your BMW i3 at 240 volts from the convenience of your own home. \|\| There are several ways to charge your BMW i3's high voltage battery, giving you a variety of convenient home and public charging options. Level 2 charging from a Level 2 home or public charging station, Level 1 charging from the occasional use cable, which comes with every BMW i3 vehicle, or DC charging from a DC charging station. Let's take a closer look at each of these. \|\| For BMW i3 vehicles equipped with the DC fast charging, SAE option, a DC public charging station will charge the BMW i3 to an 80% state of charge in 20 to 30 minutes depending on the charging station. Level 2 charging stations are currently the most common public charging stations available. The network of DC public charging stations will expand in the near future. \|\| The ability to get a full tank or charge right at home is a feature where we'll one day think, wait, we used to regularly drive somewhere else for this? Weird. and there are many home charging options to fit your needs. \|\| With experience earned on the racetrack. This is full throttled and fully connected. This is a new way to drive with high-speed charging capabilities and with the full backing of a global dealer network. \|\| Raine's anxiety will become a thing of the past. And the open road, you'll know exactly where a charge is ready and waiting. But in most cases of everyday life, you will not wait for a car to charge at all, because you will regain power at locations that you never filled up your gas tank, and that's at home and at work. |
| 6 | 153 | 6_drive_driving_car_ride | EV Test Drives | drive, driving, driver, driven, car, road, ride, roads, truck, brake | drive, driving, car, ride, fun, driver, road | drive, it, driving, car, take, would | You should let me drive the car. How was his driving? The car is incredible. \|\| Can I drive it? I just want to drive it. Really? \|\| When do I get to drive it? How about right now? \|\| Okay, yeah, sounds good. They're not gonna let me drive it, but I really, really wanna drive it. Oh, look at that heat exchange here. \|\| Back is so long, man. We're here at golden hour. Buddy Jason from Engineering Explained. \|\| So you must be wondering what's going on right now. A little bit. Do you drive cars often? |
| 7 | 137 | 7_polestar_car_electric_brand | Polestar Electric Car Brand | polestar, volvo, electric, factory, brand, car, cars, performance, battery, design | car, electric, brand, customer, cars, powerful, performance, battery, pouch, customers | polestar, car, electric, brand, volvo, china | Polestar stands for pure, progressive performance. And this is our first product, Polestar 1. \|\| So, this great awesome design became our Polestar 2, and we're going to show it to you in a minute. But there's another reason why this is a truly exciting day for us here today, because Polestar 2 is our first pure electric Polestar, a true battery electric car. Now, Polestar is dedicated to electric mobility. \|\| Bye-bye, Dumbo. Next, let me show you around inside Polestar 2. Now, how do we get in? \|\| We decided that we use prismatic cells and pouch cells. So prismatic ones are like little boxes and then you have also the other version that are called pouch, that are little pouch bags we call it. We had to find solutions to bring these different kind of cell formats into the battery that we are flexible and can use both of them. \|\| In this case, we have to go to the lab in Germany and with one extract we have to use a leaf balm. So we have to do a short process and then a long process and then we have to do it again. You can see the whole area here, the batteries and so on, all of them are recycled. \|\| So it's a really good moment now to cross way over the world on the other side to Shanghai and see how our launch of Focus has been unfolding there in just the last few hours. Let's take a look. Hi Jim, hi Steve, hello there everybody. |
| 8 | 132 | 8_prius_prius prime_hybrid_prime | Toyota Prius Plug-In Hybrid | prius, hybrid, toyota, toyotacare, prime, efficiency, mileage, vehicle, per, convenience | hybrid, efficiency, in, plug, drive, available, seats | prius, hybrid, prime, toyota, efficiency, drive, seats, system | Stay tuned to learn more about Prius Prime later in the video, but for now, let's find out more about Prius. The latest Prius generation offers six distinct takes on the hybrid experience. First, L-Eco boasts the best fuel efficiency of the entire Prius lineup, while also having the lowest starting price. \|\| And whether you prefer Prius LE AWD E's off-road utility or Prius Prime's electric capabilities, there's no shortage of reasons why the Prius family is home to the world's most iconic hybrids. Both Prius and Prius Prime are offered at an approachable starting price, with a strong track record for long-term cost estimates and overall resale value. Factor in the two-year, 25,000-mile ToyotaCare no-cost maintenance plan with enhanced three-year roadside assistance, as well as exceptional hybrid warranty coverage. \|\| Add in that every new Prius Prime includes ToyotaCare, which provides 2 years or 25,000 miles of scheduled maintenance, along with enhanced 3-year unlimited mileage of 24-hour roadside assistance, as well as exceptional hybrid warranty coverage like the 10-year, 150,000-mile Hybrid Battery Warranty. And it's easy to see how Prius Prime is ready to take the lead. Learn more today at toyota.com slash Prius Prime. \|\| Set for a spring 2009 release, the 2010 Honda Insight Hybrid hopes to answer the fuel-efficient gauntlet thrown down by Toyota. The Insight is Honda's response to the Toyota Prius, and like the Prius, is expected to receive over 40 miles per gallon for both city and highway driving. The Insight uses a complete gas-electric hybrid system and features a 1.3-liter, 98-horsepower, 4-cylinder engine and is paired to an electric motor. \|\| So critically important car for us, and it's very, very competitive. It looks great, it drives great, it's got better range and better fuel economy than our competitor Prius. So we're really excited about it. \|\| There you go. Perfect. Can't have too much on our hands, but you know, this is a very competitive market and I want you to know you're going head to head with the Prius. |
| 9 | 116 | 9_steering_suspension_car_control | EV Chassis Dynamics Control | steering, tire, rear, chassis, suspension, stability, driving, driver | steering, suspension, car, rear, control, system, axle, chassis | steering, suspension, car, rear, control, system, axle, also | Yeah, so around these turns, the rear axle steering helps you get just a little bit more responsive turn in for the car. \|\| Steering wheel feedback automatically balances for comfort while cruising and provides more responsive control while driving dynamically. The rear wheel steering turns the rear wheels up to five degrees. The available adaptive damping suspension brings yet another level of driver focused innovation to the A7. \|\| The The new dynamic all-wheel steering system connects the driver to the road like never before. Steering wheel feedback automatically balances for comfort while cruising and provides more responsive control while driving dynamically. Rear wheel steering turns the rear wheels up to 5 degrees, giving the long wheelbase A8 a turning radius similar to a much smaller A4. \|\| Hopefully something for everybody. I noticed that the car definitely stays planted when I'm cornering like this. Are there any suspension improvements that were made? \|\| This vehicle does have amplitude reactive dampers to help to keep the body flat and keep control over the bumps. I really like the way Acura has put a lot of the features and functionality into keeping connected whether it be by music or by the phone. \|\| Yeah, that's how it's like in your car Yeah, as you're coming up to a corner the second you let off the throttle it starts regen braking So before you even on the brake, so let's say we're coming around this bank right here This tire right here is gonna have a negative torque applied to it and an outside tire can actually rotate faster than the inside wheel to help push the car out of the corner and accelerate you out. |
| 10 | 110 | 10_infiniti_q50_infinity_brand | Infiniti Hybrid Vehicles | q50, infiniti, sedan, hybrid, engine, cars, car, luxury, brand, driver | infinity, new, brand, performance, market, future, car, design, technology | infiniti, q50, infinity, brand, performance, market, also, future, car | Technology. Ever wonder who's in command? In an Infiniti Q50 there's no question. \|\| Hello, I'm Jane, a product specialist for Infiniti, and this is the all-new Infiniti Q50. If the Q50 name is new to you, you can be assured it's not going to be unfamiliar for long. The Q50 is the latest premium performance sedan from Infiniti. \|\| So today, the Q50 has yet again moved forward to the next level, becoming even better and more advanced. So ladies and gentlemen, please welcome the new Infiniti Q50. Here it is, the new Infiniti Q50. \|\| So most commonly you see this used for your heated steering wheel or your garage door opener once you have that program. I want to say thank you for taking time out of your day to take a look at the 2020 Q7 with us. And if you have any questions at all feel free to give us a call right here and we'll get those questions answered for you. \|\| I don't want to open my mouth, but this is one of the most important roles. As I said before, when you look at the auto-toucoups, you can see the brakes and the glims, the orange and the black, you know what I mean? That is one of the things I really like about Captain Future. \|\| While Nissan has already had a hybrid on the market for a few years in the U.S., their upmarket Infiniti brand didn't have an alternative fuel vehicle of their own. But that all changes with the introduction of the 2012 Infiniti M35H. |
| 11 | 106 | 11_eqs_eqe_eq_mercedes | Mercedes EQS and EQE | eqs, eqe, eq, mercedes, electric, car, benz, vehicles, design, luxury | electric, new, car, driving, about, first, performance, range, light | eqs, eqe, eq, mercedes, electric, car, driving, about, amg | The all electric EQE. \|\| My name is Amanda Stretton and today we've got something very special for you. So join me as I get to spend the day with the new EQE by Mercedes EQ. The EQE is the latest all electric business saloon by Mercedes EQ with its cutting edge exterior design and truly pioneering levels of engineering. \|\| So EQE, newest member of Mercedes EQ. Walking up to it, it's a familiar design language. Yeah, the EQS and the EQE share a lot of the same design signatures that make it true to the Mercedes EQ family. \|\| What an emotion! The very first Cinque Chateau just landed and I'm about to take it for a spin on America's electric corridor between LA and Vegas. This is the all-new, all-electric 500E. \|\| The Mercedes-AMG EQS is a new vision for the future of high performance and embodies the motorsports heritage of AMG while delivering a rush of all-electric excitement. My name is Nick and I'm here to meet Brian to see the all-new Mercedes-Benz AMG EQS. Hey Nick. \|\| That looked like fun. Yeah, it's an absolute blast. So what do you think of the EQS 580? |
| 12 | 101 | 12_president_vice_ladies_vice president | Automotive Executive Presentations | hyundai, vice, acura, mclaren, dealers, volvo, gm, auto, mayor, tesla | president, ladies, vice, name, global | president, vice, america, tesla, global, chief | And we are all very proud of it. And now, to share some of the engineering advances, please welcome the Vice President of Corporate Product Planning at Hyundai Motor America, Mike O'Brien. Thank you, Peter. \|\| We've assembled the right group of people here to help make today newsworthy and productive for you, including key members of our executive team. Joining us are Michael Simcoe, Vice President of GM Global Design, Helen Emsley, Executive Director of Global Buick and GMC Design, Mark Royce, Executive Vice President of GM Global Product Development, And Alan Beattie, President of GM North America, will also be joining us shortly. \|\| Ladies and gentlemen, the Senior Vice President and General Manager of the Acura Division, Mr. Mike Accovetti. Good morning. Hi, everyone. \|\| Thank you for being with us. Now Mr. Ito will be available for a few quick photos then please join us and the rest of the Acura team on stage for a closer look at the future of Acura. \|\| We're at the right location. This is the right place. This is also the biggest Sam & Nico brand integration we've ever had. \|\| Ladies and gentlemen, Executive Vice President of the Acura Business Planning Office, Mr. Eric Berkman. Well, good morning, folks, and thanks for joining us today. This is a big day for the Acura brand. |
| 13 | 90 | 13_corolla_corolla hybrid_hybrid_toyota | Toyota Corolla Hybrid Features | corolla, toyota, hatchback, hybrid, rear, steering, lane, drivers | hybrid, safety, available, features, assist, lane, system, standard, black | corolla, hybrid, toyota, safety, features, lane, system, standard | When these advanced features are considered, it's clear that Corolla is a seriously high-tech compact. Beyond comfort, Corolla's onboard technology puts a big emphasis on safety. Every Toyota Corolla comes with Toyota Safety Sense 3.0, which includes Pre-Collision System with Pedestrian Detection, Lane Departure Alert with Steering Assist, Automatic High Beams, Full-Speed Range Dynamic Radar Cruise Control, Lane Tracing Assist, Road Sign Assist, and Proactive Driving Assist. \|\| This is the all-new 12th generation Toyota Corolla. Building on over 50 years of sales in the US, the 2020 Corolla sedan joins Corolla hatchback as one of the latest vehicles to be enhanced by the Toyota New Global Architecture, or TNGA. This new platform helps enhance Corolla's fun-to-drive charisma, while still maintaining the model's legendary value and dependability. \|\| Well you do! but it's fun to have that back out there and you know there's just not that many offering them anymore but you can get one in a Corolla and just like we made Corolla hatchback greater than ever we're doing the same with the all-new Corolla sedan but before we unveil this car I want to share some important features that you're not going to see when we pull back the silks and they're all focused on safety the new Corolla comes standard with second generation Toyota Safety Sense or TSS Okay, I know. \|\| Classic trim names return for 2020, including the modern L, LE, and XLE, and the sporty SE and XSE grades, while a Corolla Hybrid makes a big debut with the Hybrid LE grade. And more than ever before, Corolla's different flavors mean genuinely different vehicles, with three distinct personalities, features, and specifications for each trim line. Let's take a closer look at some details. \|\| Outside, the 2020 Corolla stands out with not just its bold new character lines, but also a host of details unique to each model. These include a range of stylish wheels, including eye-grabbing 18-inch alloy wheels on sport grades, and unique front and rear styling and trim accents that help to further differentiate the various members of the Corolla family. \|\| For the SE and XSE grades, these include integrated dark gray accents on the 18-inch alloy wheels, as well as the front, rear, and side rocker panels. Regardless of trim, all Corolla models also include standard LED exterior lighting, including headlights, taillights, and daytime running lights. These powerful new looks go hand in hand with the performance to match. |
| 14 | 89 | 14_crown_toyota crown_toyota_platinum | Toyota Crown Sedan History | crown, toyota, flagship, car, hybrid, vehicle, sedan, platinum, electrified, premium | crown, performance, sedan, available, new, generation, driving, system, drive, chief | crown, toyota, platinum, performance, sedan, japan, generation, driving, limited | Toyota Crown sets the bar for premium sedans. With its distinct lift-up appearance and an all-hybrid electric powertrain lineup, this icon redefines the sedan. Available in four grades with standard all-wheel drive, XLE, Limited, the new Nightshade Edition, and Platinum, the 2025 Toyota Crown wraps upscale appointments, comfort, and performance into a striking package. \|\| Take all of these factors together and it's clear that Toyota Crown is a leader, an electrified flagship packed with style, performance, and technology. Discover Toyota Crown today at toyota.com. \|\| Toyota Crown sets the bar for premium sedans. With its distinct lift-up appearance and an all-hybrid electric powertrain lineup, this icon redefines the sedan across all fronts. Available in three grades, XLE, Limited, and Platinum, all of which come standard with all-wheel drive, Toyota Crown emphasizes upscale appointments, comfort, and performance wrapped in an eye-catching package unlike anything else. \|\| Hello, everyone. Even though we are here today to spotlight the launch of a new model, we arranged 15 generations of the crown for you to see on the way in. Some of you may have wondered why. \|\| Let me begin by telling you a crown story woven by successive chief engineers. The crown's origin can be traced back to Toyota's founding era. 90 years ago, our founder Keiichiro Toyoda decided to take on the challenge of entering the automobile business. \|\| Driving the ambitious dream was his philosophy of enriching the lives of the Japanese people by creating a passenger car for the masses. Production of Toyota's longed-for domestic passenger car finally began in January 1952, 15 years after the company's founding. It was Ketro himself who named the vehicle Crown. |
| 15 | 88 | 15_open_cover_door_hood | Tailgate and Cargo Access | trunk, push, soft, pulling, lift, top, pull, press, pushing, rear | top, door, cover, hood, place, release, trunk, tailgate | door, cover, hood, release, pull, trunk, tailgate, soft | To do this, first you must remove the cover behind the rear seats. Place your hands in the recessed grips on the bottom of the cover and push upwards until the cover comes free. Next, open the floor compartment by pulling upward on the handle. \|\| The cargo cover can then be placed inside like this. Next, remove the cover attached to the tailgate. Place your hands around the lower edge of the cover and pull to unclip. \|\| Then push it upwards to disengage and place the cover under the floor compartment. As a last step, simply close the compartment. To put the cargo cover back in place, simply slide the edge of the interior cover over these two retaining pins and then fold it downwards until it engages. \|\| So to use the kick to open function you're going to make sure that the vehicle is locked and once it is locked you're going to have the key on your person. You're going to kick underneath the bumper and immediately back up and the hatch will open up for you. \|\| And as with all of our SUVs you can reset the height for the tailgate as well and whenever you're done doing that you can just kick underneath the bumper again and it'll close for you. \|\| Then slide the edge of the tailgate cover into position and pull it downwards to engage. finally push the cover upwards until it is clipped in position. The rear seat backrests of the 3 Series Gran Turismo can be adjusted forward to boost cargo capacity or backwards to increase passenger comfort. |
| 16 | 87 | 16_amg_gt_amg gt_door | Electric GT Performance Coupes | amg, gt3, steering, gtr, gtc, car, gtb, engine, mercedes, variants | door, performance, steering, coupe, car, racing, buttons, features, driving | amg, gt, door, steering, gt3, coupe, car, racing | AMG Drive Unit's steering wheel buttons can also be used to toggle between different settings for other features. For instance, exhaust flaps for the AMG Performance Exhaust, if equipped, or to enable manual shifting mode. Now, let's get inside the GT 63 S and take a look at some of the interior innovations that are now standard for the entire AMG GT model line. \|\| The AMG of AMGs. \|\| You are a GT owner yourself. Yeah. So you're the perfect person to ask what is the essence of an AMG GT and what makes this so AMG? \|\| I did many cars with my team but the e-tron GT is by far the most attractive car I designed in my career. \|\| a four-door with all that as well. Yes, the Charger Daytona will be available as a two-door coupe and the four-door sedan hatch, both with the same wide-body stance that will put the passive world on notice. And what else puts the passive world on notice is our frasonic chambered exhaust system. \|\| We consider the 2017 GTB as an ultimate base for the development and competition of the GT3. We believe that, as we have said for the past 50 years, we will not allow others to value the symbolic value of this GT3. We are very happy to be able to achieve such a great value, which has inspired us and has affected our sport. |
| 17 | 82 | 17_connect_audio_available_wireless | In-Car Multimedia Connectivity | toyota, carplay, devices, android, drivers, apple, touchscreen, wireless, iphone, multimedia | available, audio, wireless, standard, multimedia, compatibility, touchscreen, drivers, maps | audio, toyota, compatibility, drivers, prius, maps, devices, iphone, connects, carplay | It also packs intuitive technologies that keep everyone connected. Every Grand Highlander comes standard with the Toyota Audio Multimedia Platform with a 12.3-inch touchscreen and includes standard wireless compatibility for Apple CarPlay, which connects drivers to the apps on their iPhone, including maps, messages, podcasts, and music subscriptions. In addition, wireless Android Auto compatibility makes it easy to stay connected to Android devices and access various apps and services from Google, including YouTube Music and Google Maps. \|\| When it comes to cutting-edge connectivity, Prius delivers thanks to the intuitive Toyota Audio Multimedia platform. Featuring an 8-inch or an available 12.3-inch touchscreen, it includes standard wireless compatibility for Apple CarPlay, which connects drivers to the apps on their iPhone, including maps, messages, podcasts, and music subscriptions. In addition, wireless Android Auto compatibility makes it easy to stay connected to Android devices and access various apps and services from Google, including YouTube Music and Google Maps. \|\| Toyota Crown features the newest technologies from Toyota. Every grade comes standard with the latest Toyota Audio Multimedia platform with a 12.3-inch touchscreen, and includes standard wireless compatibility for Apple CarPlay, which connects drivers to the apps on their iPhone, including maps, messages, podcasts, and music subscriptions. In addition, wireless Android Auto compatibility makes it easy to stay connected to Android devices and access various apps and services from Google, including YouTube Music and Google Maps. \|\| There are also available dual USB charging ports to keep your devices charged on the go. Available heated front and rear seats will keep you comfy on those cold mornings and chilly nights. And the Elantra's available integrated memory system remembers the position of the driver's seat and the side mirrors you prefer for those times someone else has been behind the wheel. \|\| Every model in the Corolla lineup features Toyota's latest Audio Multimedia systems, complete with 7-inch touchscreen on Corolla L and 8-inch touchscreens on all other models. These systems also all feature standard Apple CarPlay compatibility. Apple CarPlay is the smarter way to use your iPhone in the car. \|\| Service Connect, which can connect Corolla to your dealership of choice, offering vehicle status updates and maintenance alerts. And even standard Wi-Fi Connect, which enables up to five mobile devices to connect to an in-vehicle Wi-Fi hotspot. Also standard equipment on hybrid and X-grade models is a slick digital instrument panel that includes a 7-inch color multi-information display seamlessly integrated into the surrounding analog gauge cluster. |
| 18 | 75 | 18_highlander_grand highlander_hybrid_available | Toyota Highlander Hybrid | highlander, suv, toyota, hybrid, horsepower, turbocharged, drive, traction, mpg, performance | hybrid, available, standard, grade, power, row | highlander, hybrid, standard, platinum, row, heated, suv, toyota | Highlander doesn't come up short on comfort offerings either, with standard three-zone automatic climate control, several available features like heated and ventilated front seats, heated second-row seats, and heated steering wheel, and even standard leather-trimmed seating on Limited and Platinum grades. And speaking of seating, Highlander XLE, Limited, and Platinum all now include a front passenger seat with 8-way power adjustability for 2022. \|\| Toyota Grand Highlander redefines the family SUV with its clean, sophisticated design and impressive versatility. Featuring seating for up to eight and intuitive technologies that are designed to help keep everyone connected and safe on the road, Grand Highlander is all about making the journey fun and easy. Together with its three responsive powertrain choices, as well as the added traction of available all-wheel drive, Grand Highlander is the ultimate SUV. \|\| Discover Highlander today on toyota.com slash Highlander. \|\| Yes, you can get over 150 mpg. The exact number, of course, is at NissanUSA.com. Alright, this is the LA Auto Show and you can see how excited people are about these new Nissan vehicles. \|\| For the past four years, the Toyota Highlander has been the best-selling retail vehicle in the extremely competitive midsize SUV segment, and this fourth generation raises the bar even further, thanks to its injection of serious style, performance, and premium features. Highlander's lineup includes gasoline and hybrid, front-wheel drive, and all-wheel drive variations across six grades, with some new configurations, including the all-new XSE. Let's learn more. \|\| To craft Highlander's exterior appearance, Toyota's designers sought to achieve an organic blend of power and sophistication. With its sculpted styling, Highlander makes a statement whether it's pulling up to the restaurant for date night or cruising down the highway with your crew on an epic road trip. This exterior isn't just about looks, though, with Highlander also offering standard LED lighting on all grades, including the freshly updated projector-style lamps that were previously only featured on Limited and Platinum. |
| 19 | 73 | 19_battery_lithium_lithium ion_ion | Lithium-Ion Battery Packs | battery, batteries, lithium, vehicle, car, laptop, energy, cells, electric, power | battery, lithium, ion, batteries, pack, iron, cooling, cells, chemistry, cold | battery, lithium, ion, batteries, pack, iron, cooling, chemistry, cold, car | As you go down Through the car, you'll see it has a lot of spotty shape. You get to the back of the car, you see the big haunches on the rear, how the car really sits on its wheels, very dynamic, very powerful. Through the center of the car, we have a dominant center console, which houses the lithium ion battery pack, which is very large, and therefore the chassis is specifically designed to house this battery pack. \|\| The i3's lithium-ion battery pack is encased in a sealed aluminum shell that is fully integrated into the underbody of the vehicle. The battery consists of eight separate modules, each consisting of 12 lithium-ion cells. Each of the eight modules weighs approximately 55 pounds for easy shipping and storage. \|\| cars you know the battery race continues here you are breaking away with lithium iron yeah it's the same family of chemistry in the lithium chemistry but we're using lithium iron instead of lithium ion or lithium ion phosphate so we give up a little bit of power density but it's a much safer battery pack we don't have runaway thermal issues if you'll remember a few years ago there were laptop computers that were catching on fire that was the lithium ion chemistry because they continue to be used today yeah and if If you have a proper cooling system, you're fine. \|\| And you have to imagine that the full techniques behind the cables, the contacts and all the step around the cooling of the high-voltage system. Regarding the cooling system, it's really important that the cells are always in a stable temperature area, so they don't like it if it is too cold or if it is too hot. My name is Andreas Nöst. \|\| For us at Audi it's about optimizing the power from the battery. This has been achieved by innovative developments in the battery cell chemistry itself. Energy management is essential to what we do. \|\| In order to ensure optimal driving range and longevity, a significant portion of the car's design went around the battery pack to make sure it was of proper size without negatively impacting interior space. The aluminum container measures 57.5 inches long, 14.2 inches high, and 13 inches wide, and contains 96 lithium-ion battery cells weighing 216 pounds in total. |
| 20 | 72 | 20_k27_america_auto evolution_electric | Affordable American EVs | ev, cars, car, vehicles, promotional, vehicle, dealer, northpoint, northpointe | electric, vehicles, affordable, evolution, first, inventory, pre | k27, kandy, electric, ev, vehicles, affordable, northpoint, inventory | Now you know what we mean when we say candy is the auto evolution for all. As you can see, Candy America is committed to offering the most affordable vehicles on the U.S. market, so anyone who wants to drive one can do so. Now, let's take a look at the model K23. \|\| It's not a typo. The K27 really is that affordable. Introducing the all-electric Kandy K27. \|\| Today, after much anticipation and with growing market demand, we are proud to announce that Candy is enabling the auto evolution for all with its line of affordable electric vehicles. We are excited to present the first two models of our electric vehicles, K23 and K27, for the U.S. market, which are currently the most affordable models on the market. Today we mark this event as a milestone for the new era. \|\| Absolutely unreal. I can't believe that's 260 kph. Frick. \|\| This is an electric muscle car that will make the rule makers, the suits, and the lawyers wish they hadn't had a kale smoothie for lunch when they launched this thing. What's a kale smoothie? I don't really know, but you don't want one. \|\| 260? T! Oh yeah, you got it right there. |
| 21 | 61 | 21_sound_quiet_noise_sounds | EV Acoustic Silence | acoustic, sound, noise, noises, noisy, silent, exhaust, vibrations, ear, quiet | sound, quiet, noise, car, sounds, exhaust, engine, silence, ear, cabin | sound, quiet, noise, it, exhaust, engine, silence, acoustic, cook, ear | Well, I'm just excited. That sound is amazing. What is it? \|\| Don't say that. Sound, sound, sound. Feel it, feel it. \|\| And it's interesting. It's a noise that's meant to sound like an AMG while not trying to sound like an internal combustion engine. Why don't we step on the gas and you'll hear what I'm talking about. \|\| And then with an Acura, I've come to expect things like a quiet road driving experience. So what kind of measures were taken on your end to make sure that the driver's somewhat isolated from those noises? Yeah, there's extra insulation placed throughout the vehicle, inside the cabin and in the engine bay throughout the vehicle that help keep that unwanted noise outside the car. \|\| The sound of silence is actually a really important concept for us in air acoustics development for the e-tron because it doesn't have a combustion engine it's extremely quiet so that means that all other noise sources will be all the more prominent so we set ourselves the target of making a really really quiet vehicle for the e-tron. The e-tron was a very interesting project for an aerodynamicist. \|\| We took the best of everything that we had in our toolbox and we developed it into this vehicle. and the result is what you see now, or actually better, what you hear now. It's an extremely quiet vehicle, and it's one of the quietest vehicles in its class. |
| 22 | 54 | 22_air_temperature_degrees_turn | Automatic Climate Control | heaters, vents, heating, heat, temperature, vent, settings, setting, warm, control | air, temperature, degrees, turn, control, climate, button, automatic, blow, outside | air, temperature, climate, button, automatic, adjust, outside, fan, zone, intensity | With less buttons, thanks to operating system 8, you can now fully benefit from the BMW Intelligent Personal Assistant, for example, to control the temperature. Hey BMW, set the temperature to 22 degrees. I will set the temperature to 22 degrees celsius for the driver. \|\| They added in also these new neck heaters that you can manually control and adjust the vent for depending on how tall you are as an individual driving or being a passenger in the vehicle. That is all connected into Lexus Climate Concierge. And another great addition is the open air control, where the system automatically detects whether the top is up or down and pays attention to the sunlight, vehicle speed, and also the outside ambient temperature. \|\| They added in also these new neck heaters that you can manually control and adjust the vent for depending on how tall you are as an individual driving or being a passenger in the vehicle. That is all connected into Lexus Climate Concierge. And another great addition is the open air control, where the system automatically detects whether the top is up or down and pays attention to the sunlight, vehicle speed, and also the outside ambient temperature. \|\| Speaking of super smart, how about a GPS linked solar sensing system that measures the sun's position and intensity to adjust cabin temperatures. What? Mind blown! \|\| Simply say, set the temperature to 70 degrees. I am increasing the temperature to 70 degrees Fahrenheit. That seems futuristic. \|\| As we're continuing on the center console, right beneath the center mounted aluminum air vent, you have some basic radio controls, rewind, seek, tune, fast forward by that button there, presets in the middle, and change in the different radio mode. Down beneath that is a standard dual zone electronic automatic climate control with three-stage heated seats for both sides, fan speed in the middle, different zones, automatic recycling, and more. |
| 23 | 51 | 23_clarity_plug_series_fuel cell | Honda Clarity Electrified Series | clarity, hybrid, electrification, electrified, plug, fuel, honda, electric, battery, vehicles | clarity, plug, in, series, electric, electrified, cell, customers, fuel, vehicles | clarity, plug, electrified, cell, honda, fuel, hybrid, three, initiative, rating | Hello everyone. We're thrilled to bring you this first look at our innovative new Clarity Series. The Clarity Fuel Cell, Clarity Electric, and Clarity Plug-in Hybrid. \|\| Today we're proud and excited to showcase our entire Clarity series of electrified vehicles with the focus on the world debut of the Clarity Electric and Clarity Plug-in Hybrid. We kicked off the launch last December with the first deliveries of the Clarity fuel cell to customers in Southern and Northern California. \|\| Today we're proud and excited to showcase our entire Clarity series of electrified vehicles with the focus on the world debut of the Clarity Electric and Clarity Plug-in Hybrid. We kicked off the launch last December with the first deliveries of the Clarity fuel cell to customers in Southern and Northern California. \|\| Along with the Accurate team and Global Honda, I am excited about this new model and I sincerely hope our customers around the world will share our passion. Thank you. Thank you. \|\| This is the new 2021 Pinnacle trim level shown on our plug-in hybrid and it's fitting that we're showing you this interior that goes further than anything we've ever done before in a vehicle that can take you further and it makes sense that a vehicle that gets 80 mpg equivalent showcases an interior that you won't want to get out of. \|\| Today we introduce the Honda Clarity line. We have a fuel cell powered Clarity, a pure battery electric Clarity, and a plug-in hybrid. We were able to develop a platform and virtually use the same body for all three incarnations of the car. |

### default

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2676 | -1_car_new_vehicle_design | ['car', 'new', 'vehicle', 'design', 'driving', 'drive', 'available', 'technology', 'look', 'electric'] |
| 0 | 4697 | 0_new_car_design_electric | ['new', 'car', 'design', 'electric', 'bmw', 'rear', 'drive', 'vehicle', 'hybrid', 'power'] |
| 1 | 876 | 1_display_control_car_navigation | ['display', 'control', 'car', 'navigation', 'assist', 'driver', 'driving', 'parking', 'screen', 'traffic'] |
| 2 | 620 | 2_auto_happy_episode_season | ['auto', 'happy', 'episode', 'season', 'press', 'fun', 'got', 'absolutely', 'hello', 'enjoy'] |
| 3 | 203 | 3_ioniq_hyundai_charging_electric | ['ioniq', 'hyundai', 'charging', 'electric', 'vehicle', 'platform', 'rear', 'ev', 'new', 'interior'] |
| 4 | 200 | 4_sonata_accord_hyundai sonata_hyundai | ['sonata', 'accord', 'hyundai sonata', 'hyundai', 'camry', '2018', 'features', 'new', 'honda', '2020'] |
| 5 | 187 | 5_charging_charge_level_stations | ['charging', 'charge', 'level', 'stations', 'plug', 'home', 'charging stations', 'cable', 'level charging', 'station'] |
| 6 | 153 | 6_drive_driving_car_ride | ['drive', 'driving', 'car', 'ride', 'truck', 'drive car', 'fun', 'driver', 'driven', 'roads'] |
| 7 | 137 | 7_polestar_car_electric_brand | ['polestar', 'car', 'electric', 'brand', 'volvo', 'china', 'electric car', 'customer', 'powerful', 'cars'] |
| 8 | 132 | 8_prius_prius prime_hybrid_prime | ['prius', 'prius prime', 'hybrid', 'prime', 'toyota', 'efficiency', 'plug', 'seats', 'drive', 'available'] |
| 9 | 116 | 9_steering_suspension_car_control | ['steering', 'suspension', 'car', 'control', 'rear', 'rear axle', 'feel', 'axle', 'axle steering', 'chassis'] |
| 10 | 110 | 10_infiniti_q50_infinity_brand | ['infiniti', 'q50', 'infinity', 'brand', 'new', 'performance', 'market', 'future', 'johan', 'technology'] |
| 11 | 106 | 11_eqs_eqe_eq_mercedes | ['eqs', 'eqe', 'eq', 'mercedes', 'electric', 'new eqs', 'mercedes eq', 'new', 'driving', 'new eqe'] |
| 12 | 101 | 12_president_vice_ladies_vice president | ['president', 'vice', 'ladies', 'vice president', 'america', 'mr', 'tesla', 'chief', 'global', 'division'] |
| 13 | 90 | 13_corolla_corolla hybrid_hybrid_toyota | ['corolla', 'corolla hybrid', 'hybrid', 'toyota', 'safety', 'available', 'apex', 'new corolla', 'features', 'assist'] |
| 14 | 89 | 14_crown_toyota crown_toyota_platinum | ['crown', 'toyota crown', 'toyota', 'platinum', 'performance', 'sedan', 'japan', 'new crown', 'available', 'generation'] |
| 15 | 88 | 15_open_cover_door_hood | ['open', 'cover', 'door', 'hood', 'place', 'close', 'release', 'pull', 'tailgate', 'trunk'] |
| 16 | 87 | 16_amg_gt_amg gt_door | ['amg', 'gt', 'amg gt', 'door', 'gt door', 'gt3', 'amg line', 'steering', 'performance', 'door coupe'] |
| 17 | 82 | 17_connect_audio_available_wireless | ['connect', 'audio', 'available', 'wireless', 'audio multimedia', 'toyota', 'standard', 'multimedia', 'compatibility', 'touchscreen'] |
| 18 | 75 | 18_highlander_grand highlander_hybrid_available | ['highlander', 'grand highlander', 'hybrid', 'available', 'standard', 'grand', 'grade', 'platinum', 'power', 'row'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car, new, vehicle, design, driving, drive, available, technology, look, electric |
| 0 | new, car, design, electric, bmw, rear, drive, vehicle, hybrid, power |
| 1 | display, control, car, navigation, assist, driver, driving, parking, screen, traffic |
| 2 | auto, happy, episode, season, press, fun, got, absolutely, hello, enjoy |
| 3 | ioniq, hyundai, charging, electric, vehicle, platform, rear, ev, new, interior |
| 4 | sonata, accord, hyundai sonata, hyundai, camry, 2018, features, new, honda, 2020 |
| 5 | charging, charge, level, stations, plug, home, charging stations, cable, level charging, station |
| 6 | drive, driving, car, ride, truck, drive car, fun, driver, driven, roads |
| 7 | polestar, car, electric, brand, volvo, china, electric car, customer, powerful, cars |
| 8 | prius, prius prime, hybrid, prime, toyota, efficiency, plug, seats, drive, available |
| 9 | steering, suspension, car, control, rear, rear axle, feel, axle, axle steering, chassis |
| 10 | infiniti, q50, infinity, brand, new, performance, market, future, johan, technology |
| 11 | eqs, eqe, eq, mercedes, electric, new eqs, mercedes eq, new, driving, new eqe |
| 12 | president, vice, ladies, vice president, america, mr, tesla, chief, global, division |
| 13 | corolla, corolla hybrid, hybrid, toyota, safety, available, apex, new corolla, features, assist |
| 14 | crown, toyota crown, toyota, platinum, performance, sedan, japan, new crown, available, generation |
| 15 | open, cover, door, hood, place, close, release, pull, tailgate, trunk |
| 16 | amg, gt, amg gt, door, gt door, gt3, amg line, steering, performance, door coupe |
| 17 | connect, audio, available, wireless, audio multimedia, toyota, standard, multimedia, compatibility, touchscreen |
| 18 | highlander, grand highlander, hybrid, available, standard, grand, grade, platinum, power, row |
### keybert

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2676 | -1_car_vehicle_design_hybrid | ['car', 'vehicle', 'design', 'hybrid', 'new', 'drive', 'technology', 'driving', 'so', 'what'] |
| 0 | 4697 | 0_vehicle_car_cars_hybrid | ['vehicle', 'car', 'cars', 'hybrid', 'design', 'bmw', 'drive', 'kia', 'engine', 'driving'] |
| 1 | 876 | 1_steering_navigation_driving_driver | ['steering', 'navigation', 'driving', 'driver', 'mode', 'view', 'drive', 'auto', 'vehicle', 'carplay'] |
| 2 | 620 | 2_happy_you_go | ['happy', 'you', 'go'] |
| 3 | 203 | 3_ioniq_hybrid_hyundai_ev | ['ioniq', 'hybrid', 'hyundai', 'ev', 'electric', 'id4', 'powertrains', 'vehicle', 'vehicles', 'egmp'] |
| 4 | 200 | 4_sonata_hyundai_sedan_hybrid | ['sonata', 'hyundai', 'sedan', 'hybrid', 'accord', 'car', 'honda', 'engine', 'performance', 'turbo'] |
| 5 | 187 | 5_charging_charge_charger_charged | ['charging', 'charge', 'charger', 'charged', 'i3', 'bmw', 'chargers', 'level', 'outlet', 'battery'] |
| 6 | 153 | 6_drive_driving_driver_driven | ['drive', 'driving', 'driver', 'driven', 'car', 'road', 'ride', 'roads', 'truck', 'brake'] |
| 7 | 137 | 7_polestar_volvo_electric_factory | ['polestar', 'volvo', 'electric', 'factory', 'brand', 'car', 'cars', 'performance', 'battery', 'design'] |
| 8 | 132 | 8_prius_hybrid_toyota_toyotacare | ['prius', 'hybrid', 'toyota', 'toyotacare', 'prime', 'efficiency', 'mileage', 'vehicle', 'per', 'convenience'] |
| 9 | 116 | 9_steering_tire_rear_chassis | ['steering', 'tire', 'rear', 'chassis', 'suspension', 'stability', 'driving', 'driver'] |
| 10 | 110 | 10_q50_infiniti_sedan_hybrid | ['q50', 'infiniti', 'sedan', 'hybrid', 'engine', 'cars', 'car', 'luxury', 'brand', 'driver'] |
| 11 | 106 | 11_eqs_eqe_eq_mercedes | ['eqs', 'eqe', 'eq', 'mercedes', 'electric', 'car', 'benz', 'vehicles', 'design', 'luxury'] |
| 12 | 101 | 12_hyundai_vice_acura_mclaren | ['hyundai', 'vice', 'acura', 'mclaren', 'dealers', 'volvo', 'gm', 'auto', 'mayor', 'tesla'] |
| 13 | 90 | 13_corolla_toyota_hatchback_hybrid | ['corolla', 'toyota', 'hatchback', 'hybrid', 'rear', 'steering', 'lane', 'drivers'] |
| 14 | 89 | 14_crown_toyota_flagship_car | ['crown', 'toyota', 'flagship', 'car', 'hybrid', 'vehicle', 'sedan', 'platinum', 'electrified', 'premium'] |
| 15 | 88 | 15_trunk_push_soft_pulling | ['trunk', 'push', 'soft', 'pulling', 'lift', 'top', 'pull', 'press', 'pushing', 'rear'] |
| 16 | 87 | 16_amg_gt3_steering_gtr | ['amg', 'gt3', 'steering', 'gtr', 'gtc', 'car', 'gtb', 'engine', 'mercedes', 'variants'] |
| 17 | 82 | 17_toyota_carplay_devices_android | ['toyota', 'carplay', 'devices', 'android', 'drivers', 'apple', 'touchscreen', 'wireless', 'iphone', 'multimedia'] |
| 18 | 75 | 18_highlander_suv_toyota_hybrid | ['highlander', 'suv', 'toyota', 'hybrid', 'horsepower', 'turbocharged', 'drive', 'traction', 'mpg', 'performance'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car, vehicle, design, hybrid, new, drive, technology, driving, so, what |
| 0 | vehicle, car, cars, hybrid, design, bmw, drive, kia, engine, driving |
| 1 | steering, navigation, driving, driver, mode, view, drive, auto, vehicle, carplay |
| 2 | happy, you, go |
| 3 | ioniq, hybrid, hyundai, ev, electric, id4, powertrains, vehicle, vehicles, egmp |
| 4 | sonata, hyundai, sedan, hybrid, accord, car, honda, engine, performance, turbo |
| 5 | charging, charge, charger, charged, i3, bmw, chargers, level, outlet, battery |
| 6 | drive, driving, driver, driven, car, road, ride, roads, truck, brake |
| 7 | polestar, volvo, electric, factory, brand, car, cars, performance, battery, design |
| 8 | prius, hybrid, toyota, toyotacare, prime, efficiency, mileage, vehicle, per, convenience |
| 9 | steering, tire, rear, chassis, suspension, stability, driving, driver |
| 10 | q50, infiniti, sedan, hybrid, engine, cars, car, luxury, brand, driver |
| 11 | eqs, eqe, eq, mercedes, electric, car, benz, vehicles, design, luxury |
| 12 | hyundai, vice, acura, mclaren, dealers, volvo, gm, auto, mayor, tesla |
| 13 | corolla, toyota, hatchback, hybrid, rear, steering, lane, drivers |
| 14 | crown, toyota, flagship, car, hybrid, vehicle, sedan, platinum, electrified, premium |
| 15 | trunk, push, soft, pulling, lift, top, pull, press, pushing, rear |
| 16 | amg, gt3, steering, gtr, gtc, car, gtb, engine, mercedes, variants |
| 17 | toyota, carplay, devices, android, drivers, apple, touchscreen, wireless, iphone, multimedia |
| 18 | highlander, suv, toyota, hybrid, horsepower, turbocharged, drive, traction, mpg, performance |
### pos

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2676 | -1_car_new_vehicle_system | ['car', 'new', 'vehicle', 'system', 'first', 'design', 'drive'] |
| 0 | 4697 | 0_new_car_design_vehicle | ['new', 'car', 'design', 'vehicle', 'power', 'interior', 'performance'] |
| 1 | 876 | 1_system_car_display_driver | ['system', 'car', 'display', 'driver', 'assist', 'navigation', 'driving', 'vehicle', 'screen', 'parking'] |
| 2 | 620 | 2_show_auto | ['show', 'auto'] |
| 3 | 203 | 3_electric_vehicle_new_rear | ['electric', 'vehicle', 'new', 'rear', 'platform', 'first', 'design', 'fast'] |
| 4 | 200 | 4_accord_new_features_safety | ['accord', 'new', 'features', 'safety', 'standard', 'car', 'performance'] |
| 5 | 187 | 5_charging_charge_level_plug | ['charging', 'charge', 'level', 'plug', 'stations', 'home', 'vehicle', 'cable', 'station', 'i3'] |
| 6 | 153 | 6_drive_driving_car_ride | ['drive', 'driving', 'car', 'ride', 'fun', 'driver', 'road'] |
| 7 | 137 | 7_car_electric_brand_customer | ['car', 'electric', 'brand', 'customer', 'cars', 'powerful', 'performance', 'battery', 'pouch', 'customers'] |
| 8 | 132 | 8_hybrid_efficiency_in_plug | ['hybrid', 'efficiency', 'in', 'plug', 'drive', 'available', 'seats'] |
| 9 | 116 | 9_steering_suspension_car_rear | ['steering', 'suspension', 'car', 'rear', 'control', 'system', 'axle', 'chassis'] |
| 10 | 110 | 10_infinity_new_brand_performance | ['infinity', 'new', 'brand', 'performance', 'market', 'future', 'car', 'design', 'technology'] |
| 11 | 106 | 11_electric_new_car_driving | ['electric', 'new', 'car', 'driving', 'about', 'first', 'performance', 'range', 'light'] |
| 12 | 101 | 12_president_ladies_vice_name | ['president', 'ladies', 'vice', 'name', 'global'] |
| 13 | 90 | 13_hybrid_safety_available_features | ['hybrid', 'safety', 'available', 'features', 'assist', 'lane', 'system', 'standard', 'black'] |
| 14 | 89 | 14_crown_performance_sedan_available | ['crown', 'performance', 'sedan', 'available', 'new', 'generation', 'driving', 'system', 'drive', 'chief'] |
| 15 | 88 | 15_top_door_cover_hood | ['top', 'door', 'cover', 'hood', 'place', 'release', 'trunk', 'tailgate'] |
| 16 | 87 | 16_door_performance_steering_coupe | ['door', 'performance', 'steering', 'coupe', 'car', 'racing', 'buttons', 'features', 'driving'] |
| 17 | 82 | 17_available_audio_wireless_standard | ['available', 'audio', 'wireless', 'standard', 'multimedia', 'compatibility', 'touchscreen', 'drivers', 'maps'] |
| 18 | 75 | 18_hybrid_available_standard_grade | ['hybrid', 'available', 'standard', 'grade', 'power', 'row'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | car, new, vehicle, system, first, design, drive |
| 0 | new, car, design, vehicle, power, interior, performance |
| 1 | system, car, display, driver, assist, navigation, driving, vehicle, screen, parking |
| 2 | show, auto |
| 3 | electric, vehicle, new, rear, platform, first, design, fast |
| 4 | accord, new, features, safety, standard, car, performance |
| 5 | charging, charge, level, plug, stations, home, vehicle, cable, station, i3 |
| 6 | drive, driving, car, ride, fun, driver, road |
| 7 | car, electric, brand, customer, cars, powerful, performance, battery, pouch, customers |
| 8 | hybrid, efficiency, in, plug, drive, available, seats |
| 9 | steering, suspension, car, rear, control, system, axle, chassis |
| 10 | infinity, new, brand, performance, market, future, car, design, technology |
| 11 | electric, new, car, driving, about, first, performance, range, light |
| 12 | president, ladies, vice, name, global |
| 13 | hybrid, safety, available, features, assist, lane, system, standard, black |
| 14 | crown, performance, sedan, available, new, generation, driving, system, drive, chief |
| 15 | top, door, cover, hood, place, release, trunk, tailgate |
| 16 | door, performance, steering, coupe, car, racing, buttons, features, driving |
| 17 | available, audio, wireless, standard, multimedia, compatibility, touchscreen, drivers, maps |
| 18 | hybrid, available, standard, grade, power, row |
### mmr

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2676 | -1_you_car_have_new | ['you', 'car', 'have', 'new'] |
| 0 | 4697 | 0_of_new_car_design | ['of', 'new', 'car', 'design'] |
| 1 | 876 | 1_system_display_control_driver | ['system', 'display', 'control', 'driver', 'also', 'assist', 'navigation', 'driving', 'when'] |
| 2 | 620 | 2_for_show_so | ['for', 'show', 'so'] |
| 3 | 203 | 3_ioniq_hyundai_charging_electric | ['ioniq', 'hyundai', 'charging', 'electric', 'vehicle', 'rear', 'platform', 'ev'] |
| 4 | 200 | 4_sonata_accord_hyundai_camry | ['sonata', 'accord', 'hyundai', 'camry', 'new', 'features', 'honda', '2020', 'gian'] |
| 5 | 187 | 5_charging_charge_level_plug | ['charging', 'charge', 'level', 'plug', 'cable', 'station', 'i3', 'mercedes', 'dc'] |
| 6 | 153 | 6_drive_it_driving_car | ['drive', 'it', 'driving', 'car', 'take', 'would'] |
| 7 | 137 | 7_polestar_car_electric_brand | ['polestar', 'car', 'electric', 'brand', 'volvo', 'china'] |
| 8 | 132 | 8_prius_hybrid_prime_toyota | ['prius', 'hybrid', 'prime', 'toyota', 'efficiency', 'drive', 'seats', 'system'] |
| 9 | 116 | 9_steering_suspension_car_rear | ['steering', 'suspension', 'car', 'rear', 'control', 'system', 'axle', 'also'] |
| 10 | 110 | 10_infiniti_q50_infinity_brand | ['infiniti', 'q50', 'infinity', 'brand', 'performance', 'market', 'also', 'future', 'car'] |
| 11 | 106 | 11_eqs_eqe_eq_mercedes | ['eqs', 'eqe', 'eq', 'mercedes', 'electric', 'car', 'driving', 'about', 'amg'] |
| 12 | 101 | 12_president_vice_america_tesla | ['president', 'vice', 'america', 'tesla', 'global', 'chief'] |
| 13 | 90 | 13_corolla_hybrid_toyota_safety | ['corolla', 'hybrid', 'toyota', 'safety', 'features', 'lane', 'system', 'standard'] |
| 14 | 89 | 14_crown_toyota_platinum_performance | ['crown', 'toyota', 'platinum', 'performance', 'sedan', 'japan', 'generation', 'driving', 'limited'] |
| 15 | 88 | 15_door_cover_hood_release | ['door', 'cover', 'hood', 'release', 'pull', 'trunk', 'tailgate', 'soft'] |
| 16 | 87 | 16_amg_gt_door_steering | ['amg', 'gt', 'door', 'steering', 'gt3', 'coupe', 'car', 'racing'] |
| 17 | 82 | 17_audio_toyota_compatibility_drivers | ['audio', 'toyota', 'compatibility', 'drivers', 'prius', 'maps', 'devices', 'iphone', 'connects', 'carplay'] |
| 18 | 75 | 18_highlander_hybrid_standard_platinum | ['highlander', 'hybrid', 'standard', 'platinum', 'row', 'heated', 'suv', 'toyota'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | you, car, have, new |
| 0 | of, new, car, design |
| 1 | system, display, control, driver, also, assist, navigation, driving, when |
| 2 | for, show, so |
| 3 | ioniq, hyundai, charging, electric, vehicle, rear, platform, ev |
| 4 | sonata, accord, hyundai, camry, new, features, honda, 2020, gian |
| 5 | charging, charge, level, plug, cable, station, i3, mercedes, dc |
| 6 | drive, it, driving, car, take, would |
| 7 | polestar, car, electric, brand, volvo, china |
| 8 | prius, hybrid, prime, toyota, efficiency, drive, seats, system |
| 9 | steering, suspension, car, rear, control, system, axle, also |
| 10 | infiniti, q50, infinity, brand, performance, market, also, future, car |
| 11 | eqs, eqe, eq, mercedes, electric, car, driving, about, amg |
| 12 | president, vice, america, tesla, global, chief |
| 13 | corolla, hybrid, toyota, safety, features, lane, system, standard |
| 14 | crown, toyota, platinum, performance, sedan, japan, generation, driving, limited |
| 15 | door, cover, hood, release, pull, trunk, tailgate, soft |
| 16 | amg, gt, door, steering, gt3, coupe, car, racing |
| 17 | audio, toyota, compatibility, drivers, prius, maps, devices, iphone, connects, carplay |
| 18 | highlander, hybrid, standard, platinum, row, heated, suv, toyota |
### llm_openai_gpt_5_5

- status: `ok`
- topics_with_custom_stopword_hits: 3

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 2676 | -1_LLM label unavailable: the, and, to, it, of, you, in, that, we, is | ['LLM label unavailable: the, and, to, it, of, you, in, that, we, is'] |
| 0 | 4697 | 0_LLM label unavailable: the, and, of, to, in, we, is, it, that, you | ['LLM label unavailable: the, and, of, to, in, we, is, it, that, you'] |
| 1 | 876 | 1_Vehicle Infotainment and Driver Assistance | ['Vehicle Infotainment and Driver Assistance'] |
| 2 | 620 | 2_EV Test Drive Conversations | ['EV Test Drive Conversations'] |
| 3 | 203 | 3_Hyundai IONIQ Lineup | ['Hyundai IONIQ Lineup'] |
| 4 | 200 | 4_Honda Accord Sedan History | ['Honda Accord Sedan History'] |
| 5 | 187 | 5_EV Charging Solutions | ['EV Charging Solutions'] |
| 6 | 153 | 6_Test Driving Experience | ['Test Driving Experience'] |
| 7 | 137 | 7_Polestar EV | ['Polestar EV'] |
| 8 | 132 | 8_Toyota Prius Hybrids | ['Toyota Prius Hybrids'] |
| 9 | 116 | 9_EV Handling and Suspension | ['EV Handling and Suspension'] |
| 10 | 110 | 10_LLM fallback: infiniti, q50, infinity, the | ['LLM fallback: infiniti, q50, infinity, the'] |
| 11 | 106 | 11_Mercedes EQ Electric Models | ['Mercedes EQ Electric Models'] |
| 12 | 101 | 12_Executive Event Introductions | ['Executive Event Introductions'] |
| 13 | 90 | 13_Toyota Corolla Hybrid Trims | ['Toyota Corolla Hybrid Trims'] |
| 14 | 89 | 14_Toyota Crown Sedan History | ['Toyota Crown Sedan History'] |
| 15 | 88 | 15_Hands-Free Tailgate Operation | ['Hands-Free Tailgate Operation'] |
| 16 | 87 | 16_LLM label unavailable: amg, gt, the, on, and, with, is, for, so, door | ['LLM label unavailable: amg, gt, the, on, and, with, is, for, so, door'] |
| 17 | 82 | 17_In-Car Connectivity Features | ['In-Car Connectivity Features'] |
| 18 | 75 | 18_Toyota Highlander Hybrid Features | ['Toyota Highlander Hybrid Features'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | LLM label unavailable: the, and, to, it, of, you, in, that, we, is |
| 0 | LLM label unavailable: the, and, of, to, in, we, is, it, that, you |
| 1 | Vehicle Infotainment and Driver Assistance |
| 2 | EV Test Drive Conversations |
| 3 | Hyundai IONIQ Lineup |
| 4 | Honda Accord Sedan History |
| 5 | EV Charging Solutions |
| 6 | Test Driving Experience |
| 7 | Polestar EV |
| 8 | Toyota Prius Hybrids |
| 9 | EV Handling and Suspension |
| 10 | LLM fallback: infiniti, q50, infinity, the |
| 11 | Mercedes EQ Electric Models |
| 12 | Executive Event Introductions |
| 13 | Toyota Corolla Hybrid Trims |
| 14 | Toyota Crown Sedan History |
| 15 | Hands-Free Tailgate Operation |
| 16 | LLM label unavailable: amg, gt, the, on, and, with, is, for, so, door |
| 17 | In-Car Connectivity Features |
| 18 | Toyota Highlander Hybrid Features |

## Output Files

| topic_info_default | topic_words_default | topic_info_keybert | topic_words_keybert | topic_info_pos | topic_words_pos | topic_info_mmr | topic_words_mmr | document_topics | representative_docs | topic_size_distribution | combined_representations_csv | combined_representations_md | final_config | representation_errors | llm30_summary | llm30_report | topic_info_llm_openai_gpt_5_5 | topic_words_llm_openai_gpt_5_5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M02-8New/topic_info_default.csv | M02-8New/topic_words_default.csv | M02-8New/topic_info_keybert.csv | M02-8New/topic_words_keybert.csv | M02-8New/topic_info_pos.csv | M02-8New/topic_words_pos.csv | M02-8New/topic_info_mmr.csv | M02-8New/topic_words_mmr.csv | M02-8New/document_topics.csv | M02-8New/representative_docs.csv | M02-8New/topic_size_distribution.csv | M02-8New_combined_representations.csv | M02-8New_combined_representations.md | M02-8New/final_config.json | M02-8New/representation_errors.json | M02-8New_LLM30.csv | M02-8New_LLM30.md | M02-8New/topic_info_llm_openai_gpt_5_5.csv | M02-8New/topic_words_llm_openai_gpt_5_5.csv |

## Representation Errors

```json
[
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "10",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main02-single/M02-8New(orig)_tok(para12-80)/run_M02_8New_orig_tok_para12_80.py\", line 134, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "5",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "3",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "6",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "4",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "10",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "20",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "19",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "18",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "21",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "22",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "24",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "0",
    "run": "27",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "9",
    "run": "7",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "2",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "6",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "7",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "8",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "11",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "16",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "17",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "23",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "22",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "20",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "10",
    "run": "25",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "1",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "5",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "6",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "9",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "14",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "15",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "16",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "18",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "19",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "21",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned no choices"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "22",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "25",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "27",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned no choices"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "29",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  },
  {
    "representation_model": "llm30",
    "topic": "16",
    "run": "30",
    "model": "openai/gpt-5.5",
    "error": "OpenRouter returned an empty label"
  }
]
```

## Notes

KeyBERT-Inspired、POS、MMR 與 LLM 只更新 topic representation，不改變 UMAP/HDBSCAN topic labels，因此三者的 clustering metrics 會相同。
BERTopic `nr_topics='auto'` 會在初始 HDBSCAN 分群後使用 c-TF-IDF 相似度自動合併主題；本報告 metrics 為 reduction 後的 topic labels。
