---
title: 01 · 人口恆等式
toc: false
---

<div class="chapter-tag">
  <div class="num">第 01 章</div>
  <div class="rule"></div>
  <div class="label">人口會計恆等式</div>
</div>

# 人口係加減出嚟嘅，唔係望飛機嚟估嘅。

<p class="lede">統計處每年公布嘅恆等式：<mark>ΔPop = 自然變動 + 單程證移入 + 其他淨遷移</mark>。其中「其他」係坊間嘗試用空運數據去估嘅嗰部分，但呢種估法漏咗大量入境人數。</p>

<div class="section-head">
  <h2>每年人口變化分析</h2>
  <div class="meta" style="margin-left:0;color:var(--color-slate);font-size:14px;">單位：千人</div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:20px;font-family:var(--font-body);font-size:13px;">
    <div style="display:flex;align-items:center;gap:8px;"><div style="width:12px;height:12px;background:#94a3b8;"></div>自然變動</div>
    <div style="display:flex;align-items:center;gap:8px;"><div style="width:12px;height:12px;background:var(--color-cyan);"></div>單程證</div>
    <div style="display:flex;align-items:center;gap:8px;"><div style="width:12px;height:12px;background:var(--color-yellow);border:1px solid var(--color-yellow-edge);"></div>其他淨遷移</div>
  </div>
</div>

```js
const annual = FileAttachment("data/annual.csv").csv({typed: true});
```

```js
const data = annual.filter(d => d.year >= 2019 && d.year <= 2023).flatMap(d => [
  {year: d.year, component: "自然變動", value: d.natural_change},
  {year: d.year, component: "單程證", value: d.owp_arrivals},
  {year: d.year, component: "其他淨遷移", value: d.other_net_migration}
]).filter(d => d.value != null);
```

```js
Plot.plot({
  marginLeft: 70,
  marginBottom: 56,
  width: 1200,
  height: 420,
  x: {label: null, tickFormat: d => `${d}`, padding: 0.2},
  y: {label: null, grid: true, tickFormat: d => d3.format("+,")(d), domain: [-100000, 220000]},
  color: {
    legend: false,
    domain: ["自然變動", "單程證", "其他淨遷移"],
    range: ["#94a3b8", "#4ed7f1", "#fffa8d"]
  },
  marks: [
    Plot.ruleY([0], {stroke: "#0a0a0a", strokeWidth: 1.5}),
    Plot.barY(data, {
      x: "year",
      y: "value",
      fill: "component",
      stroke: d => d.component === "自然變動" ? "#64748b" : d.component === "單程證" ? "#0891b2" : "#eab308",
      strokeWidth: 1.5,
      tip: true
    }),
    Plot.text(annual.filter(d => d.year >= 2019 && d.year <= 2023), {
      x: "year", y: -100000,
      text: d => `${d.year}\n${d3.format("+,")(d.yoy_pop_change)}`,
      lineAnchor: "top", dy: 8, fontSize: 13, fontWeight: 700,
      fill: d => d.yoy_pop_change > 0 ? (d.year === 2023 ? "#c2410c" : "#0a0a0a") : "#dc2626"
    })
  ]
})
```

<div class="section-head">
  <h2>實例：2022 → 2023</h2>
  <div class="meta">統計處 AD 2024 Table 1.1 + 1.12</div>
</div>

<div class="eq-row">
  <div class="eq-item orange">
    <div class="label">ΔPop 2022→2023</div>
    <div class="num"><span class="sign">+</span>190K</div>
    <div class="meta">7,346,100 → 7,536,100</div>
  </div>
  <div class="eq-op eq">=</div>
  <div class="eq-item gray">
    <div class="label">自然變動</div>
    <div class="num red"><span class="sign">−</span>21.5K</div>
    <div class="meta">33,232 出生 − 54,731 死亡</div>
  </div>
  <div class="eq-op">+</div>
  <div class="eq-item cyan">
    <div class="label">單程證</div>
    <div class="num"><span class="sign">+</span>40.8K</div>
    <div class="meta">每日 150 個內地配額</div>
  </div>
  <div class="eq-op">+</div>
  <div class="eq-item yellow">
    <div class="label">其他淨遷移 · 機場淨流出講法估呢條</div>
    <div class="num"><span class="sign">+</span>170.7K</div>
    <div class="meta">高才通 + 簽證入境 + 回流 − 移民流出</div>
  </div>
</div>

<div class="reading-note">
  <div class="lead-col">
    <div class="label">點解重要</div>
    <div class="headline">+170.7K「其他」</div>
  </div>
  <div class="body">2023 年「其他淨遷移」<mark>+170,681 人</mark>，當中至少包含高才通累計約 7.5 萬抵港（含家屬）、各類專業簽證、以及回流嘅前移民。呢三條入境通道，<strong style="color:var(--color-red);">完全唔出現喺機場「港人空運」嘅數據入面</strong>，因為新到港嘅人喺入境處數據裡係「內地訪客」或「其他訪客」，唔係「香港居民」。</div>
</div>

<div class="cite">
  <span>來源：政府統計處《香港統計年刊 2024》表 1.1 + 1.12（2024 年 9 月版，修訂後）。立法會 ISSF04/2025 提供 2024 年自然變動數字。</span>
  <a href="/methodology">完整方法論 →</a>
</div>
