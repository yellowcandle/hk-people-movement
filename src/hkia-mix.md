---
title: 03 · 機場目的地
toc: false
---

<div class="chapter-tag">
  <div class="num">第 03 章</div>
  <div class="rule"></div>
  <div class="label">機場目的地</div>
</div>

# HKIA 91 日 outbound 航班結構

<p class="lede">機場淨流出講法假設「離開香港 ≈ 移民」。但 HKIA 飛去邊度？滾動 91 日數據顯示：<mark>~80% 短途旅遊主導</mark>，去英加澳呢條傳統移民走廊嘅航班只佔 <mark class="cyan">~7%</mark>。</p>

```js
const mix = FileAttachment("data/hkia-mix.csv").csv({typed: true});
```

```js
const regionNames = {
  "SE Asia": "東南亞",
  "Mainland China": "中國內地",
  "Japan": "日本",
  "Taiwan": "台灣",
  "South Korea": "南韓",
  "Australia/NZ/Pacific": "澳洲／紐西蘭／太平洋",
  "USA": "美國",
  "Europe/Mongolia": "歐洲／蒙古",
  "South Asia": "南亞",
  "UK/Ireland": "英國／愛爾蘭",
  "Middle East/CAsia": "中東／中亞",
  "Canada": "加拿大",
  "Africa": "非洲",
  "Other": "其他"
};
const shortHaul = new Set(["中國內地", "台灣", "日本", "南韓", "東南亞"]);
const angloEmig = new Set(["英國／愛爾蘭", "加拿大", "澳洲／紐西蘭／太平洋", "美國"]);
const annotated = mix.map(d => ({
  ...d,
  region: regionNames[d.region] || d.region,
  group: shortHaul.has(regionNames[d.region]) ? "短途旅遊主導"
       : angloEmig.has(regionNames[d.region]) ? "英加澳移民走廊"
       : "其他"
}));
```

<div class="section-head">
  <h2>91 日航班 by 目的地</h2>
  <div class="meta" style="margin-left:0;color:var(--color-slate);font-size:14px;">每個目的地嘅航班數量佔比</div>
</div>

```js
Plot.plot({
  width: 1200,
  height: 460,
  marginLeft: 180,
  marginBottom: 50,
  x: {label: "航班數量佔比 (%)", grid: true},
  y: {label: null, domain: annotated.map(d => d.region)},
  color: {
    legend: true,
    domain: ["短途旅遊主導", "英加澳移民走廊", "其他"],
    range: ["#94a3b8", "#dc2626", "#cbd5e1"]
  },
  marks: [
    Plot.barX(annotated, {y: "region", x: "share_pct", fill: "group", tip: true}),
    Plot.text(annotated, {y: "region", x: "share_pct", text: d => d.share_pct.toFixed(1) + "%", dx: 6, textAnchor: "start", fontSize: 12, fontWeight: 600})
  ]
})
```

<div class="tile-row">
  <div class="tile">
    <div class="tile-label">短途旅遊主導</div>
    <div class="big-num">~80%</div>
    <div class="tile-note">中國內地 + 台灣 + 日本 + 南韓 + 東南亞。Round-trip 主導，淨流冇結構性意義。</div>
  </div>
  <div class="tile cyan">
    <div class="tile-label">英加澳移民走廊</div>
    <div class="big-num">~7%</div>
    <div class="tile-note">英國 + 加拿大 + 澳洲 + 紐西蘭。將呢條同其他 73% 噪音混埋一個 series 嚟講 emigration 唔成立。</div>
  </div>
  <div class="tile yellow">
    <div class="tile-label">其他（中東、歐洲、南亞...）</div>
    <div class="big-num">~13%</div>
    <div class="tile-note">轉機 + 商務。冇明確 emigration 意義。</div>
  </div>
</div>

<div class="cite">
  <span>來源：hongkongairport.com flight info REST API · 91 日 rolling window · 由 OpenFlights airport 數據 join destination region · IATA code 對應國家。</span>
  <a href="/methodology">完整方法論 →</a>
</div>
