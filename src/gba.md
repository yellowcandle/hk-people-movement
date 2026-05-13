---
title: 04 · 大灣區陸路
toc: false
---

<div class="chapter-tag">
  <div class="num">第 04 章</div>
  <div class="rule"></div>
  <div class="label">大灣區陸路</div>
</div>

# 陸路 8 個關口 by direction

<p class="lede">機場淨流出講法直接棄用陸路數據因為數據太 noisy。<mark>但廣東通常逗留港人有 49.6 萬</mark>。唔睇陸路 = 睇唔到移民嘅主要流向。</p>

```js
const gba = FileAttachment("data/gba-land.csv").csv({typed: true});
const cross = FileAttachment("data/cross-channel.csv").csv({typed: true});
```

<div class="section-head">
  <h2>每個 control point 嘅 net out（港人）</h2>
  <div class="meta" style="margin-left:0;color:var(--color-slate);font-size:14px;">紅 = 淨流出香港，藍 = 淨流入香港。每行一個 control point。</div>
</div>

```js
Plot.plot({
  width: 1200,
  height: 480,
  marginLeft: 130,
  marginRight: 40,
  marginTop: 40,
  marginBottom: 60,
  x: {label: null, tickFormat: d => `${d}`, fontSize: 13},
  y: {label: null, domain: [...new Set(gba.filter(d => d.year >= 2023).map(d => d.control_point))].sort()},
  color: {
    scheme: "rdbu",
    reverse: true,
    label: "淨流出（人，紅 = 流出，藍 = 流入）",
    legend: true,
    type: "linear",
    symmetric: true,
    domain: [-1.5e6, 1.5e6]
  },
  marks: [
    Plot.cell(gba.filter(d => d.year >= 2023), {x: "year", y: "control_point", fill: "net_out", tip: true, inset: 1}),
    Plot.text(gba.filter(d => d.year >= 2023), {x: "year", y: "control_point",
      text: d => d3.format(".2s")(d.net_out),
      fontSize: 12, fontWeight: 600,
      fill: d => Math.abs(d.net_out) > 8e5 ? "white" : "#0a0a0a"
    })
  ]
})
```

<div class="section-head">
  <h2>單一 checkpoint 嘅 asymmetry 喺廊道合計後消失</h2>
</div>

```js
const agg = d3.rollups(gba.filter(d => d.year >= 2023), vs => ({year: vs[0].year, net_out: d3.sum(vs, d => d.net_out)}), d => d.year).map(([, v]) => v);
```

```js
Plot.plot({
  width: 1200,
  height: 400,
  marginLeft: 110,
  marginRight: 40,
  marginTop: 56,
  marginBottom: 56,
  x: {label: null, tickFormat: d => `${d}`, type: "band", padding: 0.4, fontSize: 14},
  y: {label: "陸路 8 個關口加埋嘅淨流出（人）", labelArrow: "none", grid: true, tickFormat: d => d3.format("+,")(d), labelAnchor: "center"},
  marks: [
    Plot.ruleY([0], {stroke: "#0a0a0a", strokeWidth: 1.5}),
    Plot.barY(agg, {x: "year", y: "net_out", fill: d => d.net_out >= 0 ? "#dc2626" : "#0369a1", tip: true}),
    Plot.text(agg.filter(d => d.net_out >= 0), {x: "year", y: "net_out",
      text: d => d3.format("+,")(d.net_out),
      lineAnchor: "bottom",
      dy: -8,
      fontSize: 15, fontWeight: 700,
      fill: "#dc2626"
    }),
    Plot.text(agg.filter(d => d.net_out < 0), {x: "year", y: "net_out",
      text: d => d3.format("+,")(d.net_out),
      lineAnchor: "top",
      dy: 8,
      fontSize: 15, fontWeight: 700,
      fill: "#0369a1"
    })
  ]
})
```

<div class="reading-note">
  <div class="lead-col">
    <div class="label">讀法</div>
    <div class="headline">8 個關口加埋，反而細過任何一個</div>
  </div>
  <div class="body">落馬洲（車輛）2024 年港人淨流出 <mark>−113 萬</mark>，但同一個落馬洲支線（鐵路）淨流入 <mark class="cyan">+116 萬</mark>。<strong>同一班人</strong>：揸車去深圳，搭鐵路返香港。單睇任何一個關口都會睇到一個誇張嘅數字，但<strong>8 個關口加埋</strong>只係十幾萬，因為一進一出基本上抵銷。所以分析陸路離境要睇<strong>合計</strong>，唔好淨係睇一個關口。</div>
</div>

<div class="cite">
  <span>來源：入境處 每日 passenger traffic CSV · 8 個陸路控制點 by direction · 港人列。</span>
  <a href="/methodology">完整方法論 →</a>
</div>
