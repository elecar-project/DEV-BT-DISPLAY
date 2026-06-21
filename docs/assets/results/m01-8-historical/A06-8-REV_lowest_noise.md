# A06-8-REV BERTopic + A05-8.4(human) stopwords + representation models - lowest_noise

## Run Info

| started_at | finished_at | dataset | embedding_model | embedding_note | custom_stopword_count | llm_provider | llm_models |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-05T11:59:07.575467+00:00 | 2026-06-05T12:01:15.969947+00:00 | Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset | all-MiniLM-L6-v2 | 重用 A04-8(orig) embeddings 快取並複製到 M01-8。 | 170 | OpenRouter | anthropic/claude-opus-4.7, openai/gpt-5.5, google/gemini-3.1-pro-preview |

## Parameters

| selection_label | selection_reason | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise | 最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。 | 15 | 10 | 0.0500 | cosine | 42 | 225 | 5 | eom | 0.0000 | euclidean |

## Metrics

| n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 0.1029 | 1146 | 8653 | 660 | 8653 | 0.7770 | 0.8728 | 0.3837 | 0.3935 |

## Compared With Provided Baseline

| selection_label | baseline_noise_ratio | a06_noise_ratio | baseline_n_clusters | a06_n_clusters | baseline_largest_topic_ratio | a06_largest_topic_ratio | baseline_top3_topic_ratio | a06_top3_topic_ratio | baseline_balance_score | a06_balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise | 0.0055 | 0.1029 | 2 | 4 | 0.9701 | 0.7770 | 0.9945 | 0.8728 | 0.3244 | 0.3935 |

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
| -1 | 1146 | -1_ioniq_new_polestar_nissan | ['ioniq', 'new', 'polestar', 'nissan', 'crown', 'mustang', 'electric', 'hyundai', 'car', 'leaf'] |
| 0 | 8653 | 0_car_new_vehicle_electric | ['car', 'new', 'vehicle', 'electric', 'driving', 'design', 'drive', 'bmw', 'rear', 'charging'] |
| 1 | 660 | 1_hybrid_prius_available_toyota | ['hybrid', 'prius', 'available', 'toyota', 'standard', 'corolla', 'rav4', 'highlander', 'drive', 'camry'] |
| 2 | 406 | 2_elantra_sonata_hyundai_accord | ['elantra', 'sonata', 'hyundai', 'accord', 'new', 'features', 'hyundai sonata', 'design', 'car', 'hybrid'] |
| 3 | 271 | 3_volvo_xc90_new_car | ['volvo', 'xc90', 'new', 'car', 's60', 'xc40', 'safety', 'new xc90', 'cars', 'design'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | ioniq, new, polestar, nissan, crown, mustang, electric, hyundai, car, leaf |
| 0 | car, new, vehicle, electric, driving, design, drive, bmw, rear, charging |
| 1 | hybrid, prius, available, toyota, standard, corolla, rav4, highlander, drive, camry |
| 2 | elantra, sonata, hyundai, accord, new, features, hyundai sonata, design, car, hybrid |
| 3 | volvo, xc90, new, car, s60, xc40, safety, new xc90, cars, design |
### keybert

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 1146 | -1_mustang_ev_nissan_hyundai | ['mustang', 'ev', 'nissan', 'hyundai', 'design', 'vehicle', 'vehicles', 'car', 'electric', 'toyota'] |
| 0 | 8653 | 0_bmw_car_cars_vehicle | ['bmw', 'car', 'cars', 'vehicle', 'design', 'driving', 'drive', 'rear', 'driver'] |
| 1 | 660 | 1_rav4_hybrid_toyota_vehicle | ['rav4', 'hybrid', 'toyota', 'vehicle', 'prius', 'corolla', 'drivers', 'standard', 'highlander'] |
| 2 | 406 | 2_hyundai_sonata_elantra_sedan | ['hyundai', 'sonata', 'elantra', 'sedan', 'accord', 'hybrid', 'elr', 'car', 'interior', 'design'] |
| 3 | 271 | 3_volvo_xc90_ex90_xc40 | ['volvo', 'xc90', 'ex90', 'xc40', 's90', 'cars', 'car', 'engine', 'design'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | mustang, ev, nissan, hyundai, design, vehicle, vehicles, car, electric, toyota |
| 0 | bmw, car, cars, vehicle, design, driving, drive, rear, driver |
| 1 | rav4, hybrid, toyota, vehicle, prius, corolla, drivers, standard, highlander |
| 2 | hyundai, sonata, elantra, sedan, accord, hybrid, elr, car, interior, design |
| 3 | volvo, xc90, ex90, xc40, s90, cars, car, engine, design |
### pos

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 1146 | -1_new_nissan_electric_car | ['new', 'nissan', 'electric', 'car', 'leaf', 'first', 'drive', 'design', 'technology'] |
| 0 | 8653 | 0_car_new_vehicle_first | ['car', 'new', 'vehicle', 'first', 'driver'] |
| 1 | 660 | 1_hybrid_available_standard_corolla | ['hybrid', 'available', 'standard', 'corolla', 'system', 'drive', 'safety'] |
| 2 | 406 | 2_accord_new_features_design | ['accord', 'new', 'features', 'design', 'car', 'hybrid', 'look'] |
| 3 | 271 | 3_new_car_s60_safety | ['new', 'car', 's60', 'safety', 'cars', 'design', 'world', 'first', 'system'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | new, nissan, electric, car, leaf, first, drive, design, technology |
| 0 | car, new, vehicle, first, driver |
| 1 | hybrid, available, standard, corolla, system, drive, safety |
| 2 | accord, new, features, design, car, hybrid, look |
| 3 | new, car, s60, safety, cars, design, world, first, system |
### mmr

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 1146 | -1_ioniq_polestar_nissan | ['ioniq', 'polestar', 'nissan'] |
| 0 | 8653 | 0_car_new | ['car', 'new'] |
| 1 | 660 | 1_hybrid_prius_toyota_standard | ['hybrid', 'prius', 'toyota', 'standard', 'corolla', 'rav4', 'system', 'highlander', 'camry'] |
| 2 | 406 | 2_elantra_sonata_hyundai_accord | ['elantra', 'sonata', 'hyundai', 'accord', 'new', 'features', 'design', 'car'] |
| 3 | 271 | 3_volvo_xc90_you_s60 | ['volvo', 'xc90', 'you', 's60', 'xc40', 'safety', 'cars', 'design'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | ioniq, polestar, nissan |
| 0 | car, new |
| 1 | hybrid, prius, toyota, standard, corolla, rav4, system, highlander, camry |
| 2 | elantra, sonata, hyundai, accord, new, features, design, car |
| 3 | volvo, xc90, you, s60, xc40, safety, cars, design |
### llm_anthropic_claude_opus_4_7

- status: `ok`
- topics_with_custom_stopword_hits: 0

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 1146 | -1_EV Discussions and Interviews | ['EV Discussions and Interviews'] |
| 0 | 8653 | 0_Acura ILX Vehicle Features | ['Acura ILX Vehicle Features'] |
| 1 | 660 | 1_Standard Features and Trim Options | ['Standard Features and Trim Options'] |
| 2 | 406 | 2_Cadillac ELR Plug-in Hybrid | ['Cadillac ELR Plug-in Hybrid'] |
| 3 | 271 | 3_Volvo XC90 Vehicle Features | ['Volvo XC90 Vehicle Features'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | EV Discussions and Interviews |
| 0 | Acura ILX Vehicle Features |
| 1 | Standard Features and Trim Options |
| 2 | Cadillac ELR Plug-in Hybrid |
| 3 | Volvo XC90 Vehicle Features |
### llm_openai_gpt_5_5

- status: `ok`
- topics_with_custom_stopword_hits: 5

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 1146 | -1_LLM label unavailable: the, and, to, of, we, you, that, in, it, is | ['LLM label unavailable: the, and, to, of, we, you, that, in, it, is'] |
| 0 | 8653 | 0_LLM label unavailable: the, and, to, of, you, it, in, is, that, we | ['LLM label unavailable: the, and, to, of, you, it, in, is, that, we'] |
| 1 | 660 | 1_LLM label unavailable: and, with, the, to, hybrid, prius, available, toyota, of, standard | ['LLM label unavailable: and, with, the, to, hybrid, prius, available, toyota, of, standard'] |
| 2 | 406 | 2_LLM fallback: the, and, elantra, to | ['LLM fallback: the, and, elantra, to'] |
| 3 | 271 | 3_LLM label unavailable: the, volvo, and, to, new, xc90, we, of, in, car | ['LLM label unavailable: the, volvo, and, to, new, xc90, we, of, in, car'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | LLM label unavailable: the, and, to, of, we, you, that, in, it, is |
| 0 | LLM label unavailable: the, and, to, of, you, it, in, is, that, we |
| 1 | LLM label unavailable: and, with, the, to, hybrid, prius, available, toyota, of, standard |
| 2 | LLM fallback: the, and, elantra, to |
| 3 | LLM label unavailable: the, volvo, and, to, new, xc90, we, of, in, car |
### llm_google_gemini_3_1_pro_preview

- status: `ok`
- topics_with_custom_stopword_hits: 2

#### Topic Info Top 20

| Topic | Count | Name | Representation |
| --- | --- | --- | --- |
| -1 | 1146 | -1_General | ['General'] |
| 0 | 8653 | 0_A | ['A'] |
| 1 | 660 | 1_LLM label unavailable: and, with, the, to, hybrid, prius, available, toyota, of, standard | ['LLM label unavailable: and, with, the, to, hybrid, prius, available, toyota, of, standard'] |
| 2 | 406 | 2_LLM label unavailable: the, and, elantra, to, sonata, hyundai, of, that, you, in | ['LLM label unavailable: the, and, elantra, to, sonata, hyundai, of, that, you, in'] |
| 3 | 271 | 3_Volvo | ['Volvo'] |

#### Topic Words Top 20

| topic | words |
| --- | --- |
| -1 | General |
| 0 | A |
| 1 | LLM label unavailable: and, with, the, to, hybrid, prius, available, toyota, of, standard |
| 2 | LLM label unavailable: the, and, elantra, to, sonata, hyundai, of, that, you, in |
| 3 | Volvo |

## Output Files

| topic_info_default | topic_words_default | topic_info_keybert | topic_words_keybert | topic_info_pos | topic_words_pos | topic_info_mmr | topic_words_mmr | document_topics | representative_docs | topic_size_distribution | final_config | representation_errors | topic_info_llm_anthropic_claude_opus_4_7 | topic_words_llm_anthropic_claude_opus_4_7 | topic_info_llm_openai_gpt_5_5 | topic_words_llm_openai_gpt_5_5 | topic_info_llm_google_gemini_3_1_pro_preview | topic_words_llm_google_gemini_3_1_pro_preview |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise/topic_info_default.csv | lowest_noise/topic_words_default.csv | lowest_noise/topic_info_keybert.csv | lowest_noise/topic_words_keybert.csv | lowest_noise/topic_info_pos.csv | lowest_noise/topic_words_pos.csv | lowest_noise/topic_info_mmr.csv | lowest_noise/topic_words_mmr.csv | lowest_noise/document_topics.csv | lowest_noise/representative_docs.csv | lowest_noise/topic_size_distribution.csv | lowest_noise/final_config.json | lowest_noise/representation_errors.json | lowest_noise/topic_info_llm_anthropic_claude_opus_4_7.csv | lowest_noise/topic_words_llm_anthropic_claude_opus_4_7.csv | lowest_noise/topic_info_llm_openai_gpt_5_5.csv | lowest_noise/topic_words_llm_openai_gpt_5_5.csv | lowest_noise/topic_info_llm_google_gemini_3_1_pro_preview.csv | lowest_noise/topic_words_llm_google_gemini_3_1_pro_preview.csv |

## Representation Errors

```json
[
  {
    "representation_model": "llm_openai_gpt_5_5",
    "model": "openai/gpt-5.5",
    "topic": "2",
    "error": "'NoneType' object is not subscriptable",
    "traceback": "Traceback (most recent call last):\n  File \"/workspaces/Dev-BT/Result/.m06.05_Main01-run/M01-8(orig)_tok(para12-80)/run_M01_8_orig_tok_para12_80_human_stopwords_repr.py\", line 193, in extract_topics\n    label = (response.choices[0].message.content or \"\").strip()\n             ~~~~~~~~~~~~~~~~^^^\nTypeError: 'NoneType' object is not subscriptable\n"
  }
]
```

## Notes

KeyBERT-Inspired、POS、MMR 與 LLM 只更新 topic representation，不改變 UMAP/HDBSCAN topic labels，因此三者的 clustering metrics 會相同。
