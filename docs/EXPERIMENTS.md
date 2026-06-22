# 實驗登錄維護

_data/experiments.json 是結果網站的單一實驗登錄檔。它集中管理：

- 詳細結果頁的識別碼、標題、說明與分組
- 詳細頁左側的實驗設定面板
- 結果總覽的索引表
- 實驗地圖的節點連結

網站公開使用的 assets/data/experiments.json 是同步輸出，不直接編輯。

## 新增一個已整理實驗

1. 建立 results/<slug>.md，在 front matter 加入 experiment_id: <slug>。
2. 在 _data/experiments.json 的 experiments 陣列複製一筆相近實驗，修改 id、page、title、description、group、map 與 settings_lines。
3. 若要在地圖開啟，將 draw.io 節點的 data-label 或 data-id 填入該筆的 map.labels 或 map.node_ids。
4. 執行同步與檢查：

~~~~bash
python3 scripts/build_experiment_registry.py
python3 scripts/build_experiment_registry.py --check
~~~~

第一個指令會同步結果索引、公開 JSON 與既有 SVG 地圖中的連結；第二個指令會檢查頁面與登錄資料是否對得上。

若是先執行舊的匯入腳本，而它重新產生了內嵌設定側欄，改用以下指令做一次遷移，再執行檢查：

~~~~bash
python3 scripts/build_experiment_registry.py --migrate
python3 scripts/build_experiment_registry.py --check
~~~~

## 設定面板

詳細頁使用共用樣板 _includes/result-settings.html。settings_lines 的每一個陣列元素就是面板的一行 Markdown 或 HTML，因此可沿用既有的 settings-table 表格格式。

頁面內如要連到另一個結果頁，請使用同資料夾內的相對檔名，例如 a05-8-orig-rev-human-stopwords.html；Jekyll 會在 GitHub Pages 正確保留網站的 base URL。
