---
title: 06 · 方法論
toc: false
---

<div class="chapter-tag">
  <div class="num">第 06 章 · 必讀</div>
  <div class="rule orange"></div>
  <div class="label">方法論</div>
</div>

# 數據係咩、唔係咩、邊個來源、有咩 caveat。

<p class="lede">呢個 dashboard 唔係話另一套講法「錯」，係話用「機場港人淨流」呢個 label 講 emigration 對唔對得正。下面逐項拆。</p>

<h2 style="display:flex;align-items:baseline;gap:12px;"><span style="font-family:Inter,sans-serif;font-weight:700;font-size:13px;letter-spacing:0.08em;color:var(--color-ink);">§1</span> 統計處點計人口</h2>

<div style="display:flex;flex-direction:column;gap:16px;padding:32px;background:var(--color-ground-soft);border-left:4px solid var(--color-ink);margin:24px 0;">
  <div style="font-family:var(--font-body);font-weight:500;font-size:14px;color:var(--color-slate);">每年公布嘅人口會計恆等式：</div>
  <div style="font-family:Inter,sans-serif;font-weight:700;font-size:40px;line-height:1.2;letter-spacing:-0.01em;color:var(--color-ink);">ΔPop = 自然變動 + 單程證 + 其他淨遷移</div>
  <div style="display:flex;flex-direction:column;gap:8px;font-family:var(--font-body);font-weight:400;font-size:15px;line-height:1.55;color:var(--color-ink-2);padding-top:8px;">
    <div><strong style="color:var(--color-slate);">自然變動</strong> ＝ 出生人數 − 死亡人數。2020 年起為負值，香港死亡多過出生。</div>
    <div><strong style="color:var(--color-cyan-dark);">單程證</strong> ＝ 由保安局公布，每日 150 個內地移入配額嘅實際使用人數。</div>
    <div><strong style="color:var(--color-yellow-dark);">其他淨遷移</strong> ＝ 恆等式扣減出嚟（總人口變化 − 自然變動 − 單程證）。包括高才通／優才／專才入境、外籍工人、回流港人、海外移民出境等等。坊間用空運估嘅就係呢條。</div>
  </div>
</div>

<h2 style="display:flex;align-items:baseline;gap:12px;"><span style="font-family:Inter,sans-serif;font-weight:700;font-size:13px;letter-spacing:0.08em;color:var(--color-ink);">§2</span> 已知 caveat <span style="font-family:var(--font-body);font-weight:400;font-size:14px;color:var(--color-slate);margin-left:8px;">呢啲嘢 dashboard 唔識掩飾。</span></h2>

<div class="caveat">
  <div class="num">01</div>
  <div class="body">
    <h4>2024 嘅「其他淨遷移」未計算到</h4>
    <p>自然變動已知（出生 36,723 − 死亡 52,393 = −15,670）但 2024 年單程證實際使用數要等統計處《香港統計年刊 2025》（預計 2026 年 9 月）。Dashboard 嘅 2024 column 留空。</p>
  </div>
  <div class="src">來源：ISSF04/2025</div>
</div>

<div class="caveat">
  <div class="num">02</div>
  <div class="body">
    <h4>年中人口會修訂</h4>
    <p>立法會月度 ISSF01 嘅「臨時」人口數字會喺 Annual Digest 修訂。例如 2024 年中由 7,531,800 修訂到 7,524,100。Dashboard 永遠引最新版本。</p>
  </div>
  <div class="src">來源：ISSF01/2025 Jan + Dec</div>
</div>

<div class="caveat">
  <div class="num">03</div>
  <div class="body">
    <h4>HKIA flight API 只保留 ~91 日</h4>
    <p>「機場目的地」第 03 章嘅 destination mix 用 rolling 91 日 window 推算。隱含假設：歷史比例同最近 3 個月差唔多。2023 重開前嘅 mix 唔啱呢個假設。</p>
  </div>
  <div class="src">來源：hongkongairport.com</div>
</div>

<div class="caveat">
  <div class="num">04</div>
  <div class="body">
    <h4>高才通累計 ≠ 現時 stock</h4>
    <p>第 05 章嘅 75K 抵港數係累計到 2024 年底，包括家屬。當中部分會離開、部分等緊續簽。首批高才通簽證 2024 年底先到期，續簽率仲未夠樣本作統計分析。</p>
  </div>
  <div class="src">來源：LegCo Q&amp;A 2025-01-22</div>
</div>

<div class="caveat">
  <div class="num">05</div>
  <div class="body">
    <h4>內地港人 stock 係 2020 普查數字</h4>
    <p>371,380 個內地港人嘅數字嚟自 2020 全國人口普查。下一次普查係 2026 年。中間冇官方修訂。廣東「通常逗留」港人數字（49.6 萬）每年更新。</p>
  </div>
  <div class="src">來源：ISSH33/2024</div>
</div>

<h2 style="display:flex;align-items:baseline;gap:12px;"><span style="font-family:Inter,sans-serif;font-weight:700;font-size:13px;letter-spacing:0.08em;color:var(--color-ink);">§3</span> 畀番原作者嘅好評</h2>

<div class="quote">
  <div class="mark">"</div>
  <div class="body">
    <div>原作者揀「機場」做 IMMD 嘅 cleanest signal 係<strong>啱嘅</strong> ── 機場控制點嘅旅客 vs 居民比例比羅湖／落馬洲清楚好多。佢嘅「round-trip 會 cancel」argument 喺長 horizon 上係<strong>正確</strong>。</div>
    <div>Dashboard 嘅 quarrel 範圍細：用「international emigration」呢個 label 對唔住一個 metric 同時 (a) 漏咗主要入境通道、(b) 同 C&amp;SD 識別式 disagrees by sign。<strong>數據冇變，係解讀要修正。</strong></div>
  </div>
</div>

<h2 style="display:flex;align-items:baseline;gap:12px;"><span style="font-family:Inter,sans-serif;font-weight:700;font-size:13px;letter-spacing:0.08em;color:var(--color-ink);">§4</span> 所有來源 <span style="font-family:var(--font-body);font-weight:400;font-size:14px;color:var(--color-slate);margin-left:8px;">Pin 入 git repo · 13 份政府／立法會文件 + 2 個 live data feed。</span></h2>

<div class="sources-table">
  <div class="row header-row">
    <div class="col-id">文件編號</div>
    <div class="col-content">內容</div>
    <div class="col-pub">發布</div>
    <div class="col-type">類型</div>
  </div>
  <div class="row">
    <div class="col-id">AD 2024</div>
    <div class="col-content">統計處《香港統計年刊 2024》Table 1.1 + 1.12（修訂版人口、出生死亡、單程證）</div>
    <div class="col-pub">統計處 · 2024.09</div>
    <div class="col-type">PDF</div>
  </div>
  <div class="row">
    <div class="col-id">IMMD CSV</div>
    <div class="col-content">入境處每日 passenger traffic 開放數據（atseed.co 同一上游）</div>
    <div class="col-pub">入境處 · 每日</div>
    <div class="col-type">CSV · live</div>
  </div>
  <div class="row">
    <div class="col-id">HKIA Flight API</div>
    <div class="col-content">hongkongairport.com flight info REST API · 91 日 rolling window</div>
    <div class="col-pub">機管局 · 每日</div>
    <div class="col-type">JSON · live</div>
  </div>
  <div class="row">
    <div class="col-id">CAD Stat</div>
    <div class="col-content">民航處 Civil International Air Transport Movements 1998—2026</div>
    <div class="col-pub">民航處 · 每月</div>
    <div class="col-type">XLSX</div>
  </div>
  <div class="row">
    <div class="col-id">ISSH33/2024</div>
    <div class="col-content">立法會〈香港居民在內地生活的數目〉— 內地港人 371K stock + 廣東通常逗留 49.6 萬</div>
    <div class="col-pub">立法會 · 2024.12</div>
    <div class="col-type">PDF</div>
  </div>
  <div class="row">
    <div class="col-id">ISSH23/2024</div>
    <div class="col-content">立法會〈人才輸入計劃〉— 全部 7 項計劃年度獲批數，含高才通 49,737</div>
    <div class="col-pub">立法會 · 2024.10</div>
    <div class="col-type">PDF</div>
  </div>
  <div class="row">
    <div class="col-id">RT01/2025</div>
    <div class="col-content">立法會〈選定地方引進人才的支援政策〉— 高才通累計 92K 獲批 / 75K 抵港</div>
    <div class="col-pub">立法會 · 2025.02</div>
    <div class="col-type">PDF</div>
  </div>
  <div class="row">
    <div class="col-id">IN15/2025</div>
    <div class="col-content">立法會〈英國和加拿大資助公營醫療服務的享用資格〉— 2021—2024 移居英澳加 17.3 萬</div>
    <div class="col-pub">立法會 · 2025.08</div>
    <div class="col-type">PDF</div>
  </div>
  <div class="row">
    <div class="col-id">ISSH10/2025</div>
    <div class="col-content">立法會〈跨境長者福利服務〉— 廣東 65+ 港人 99,600（2024）</div>
    <div class="col-pub">立法會 · 2025.05</div>
    <div class="col-type">PDF</div>
  </div>
  <div class="row">
    <div class="col-id">ISSF04/2025</div>
    <div class="col-content">立法會〈選定亞太地方的主要人口指標〉— 2024 香港出生 36,723 / 死亡 52,393</div>
    <div class="col-pub">立法會 · 2025.10</div>
    <div class="col-type">PDF</div>
  </div>
  <div class="row">
    <div class="col-id">FS05/2022</div>
    <div class="col-content">立法會〈吸引人才政策〉— 2016—2022 人口會計恆等式分解（含外傭）</div>
    <div class="col-pub">立法會 · 2022.10</div>
    <div class="col-type">PDF</div>
  </div>
  <div class="row">
    <div class="col-id">LegCo Q&amp;A 2025</div>
    <div class="col-content">立法會書面質詢 P2025012200216 — 勞工及福利局局長確認高才通 2024 年底累計數字</div>
    <div class="col-pub">勞福局 · 2025.01.22</div>
    <div class="col-type">HTML</div>
  </div>
  <div class="row">
    <div class="col-id">IRCC Q-493</div>
    <div class="col-content">加拿大移民部回覆國會書面質詢 Q-493（Sessional Paper 8555-451-493）— 港人 Open Work Permit + Stream A + Stream B 申請／批准／抵港人數，截至 2025.08.31</div>
    <div class="col-pub">IRCC · 2025.12.05</div>
    <div class="col-type">HTML</div>
  </div>
  <div class="row">
    <div class="col-id">UK Home Office</div>
    <div class="col-content">英國內政部 BN(O) Visa 季度統計 — 經 UK Data Service Blog（2025.07.30）引用：2021.01—2025.03 累計批出約 18 萬個 BN(O) 簽證</div>
    <div class="col-pub">UK Home Office · 季度</div>
    <div class="col-type">HTML</div>
  </div>
  <div class="row credit">
    <div class="col-id">atseed.co/hkborder</div>
    <div class="col-content">機場淨流出講法嘅原始 dashboard。呢個 project 嘅出發點。Credit 畀作者揀清楚 IMMD「機場港人」做最乾淨嘅 control point series。</div>
    <div class="col-pub">原作者 · live</div>
    <div class="col-type">HTML · live</div>
  </div>
</div>
