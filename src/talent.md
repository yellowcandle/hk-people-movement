---
title: 05 · 人才與移居
toc: false
---

<div class="chapter-tag">
  <div class="num">第 05 章</div>
  <div class="rule yellow"></div>
  <div class="label">人才與移居</div>
</div>

# 高才通入境同英加澳移居對比

<p class="lede">機場淨流出講法只見港人離港，唔見人才入境。實際上 2022 年底起推出嘅高才通計劃，已經將 <mark>9.2 萬人獲批</mark>、<mark class="cyan">7.5 萬人實際抵港</mark>。同期英加澳累計移居約 19 萬。兩邊嘅人口流量嘅數量級相當，但方向相反。</p>

<div class="section-head">
  <h2>香港人才入境計劃 · 年度獲批</h2>
  <div class="meta" style="margin-left:0;color:var(--color-slate);font-size:14px;">7 項計劃合計</div>
</div>

```js
const annual = FileAttachment("data/annual.csv").csv({typed: true});
```

```js
const talent = annual.filter(d => d.total_talent_approved != null && d.total_talent_approved > 0);
```

```js
Plot.plot({
  width: 1200,
  height: 360,
  marginLeft: 70,
  x: {label: null, tickFormat: d => `${d}`, type: "band", padding: 0.4},
  y: {label: null, grid: true, tickFormat: d => d3.format(",")(d)},
  marks: [
    Plot.barY(talent, {x: "year", y: "total_talent_approved", fill: "#a8f1ff", stroke: "#4ed7f1", tip: true}),
    Plot.barY(talent, {x: "year", y: "top_talent_approved", fill: "#0369a1", tip: {format: {y: ",d"}}}),
    Plot.text(talent, {x: "year", y: "total_talent_approved", text: d => d3.format(",")(d.total_talent_approved), dy: -10, fontSize: 13, fontWeight: 700})
  ]
})
```

<div style="display:flex;align-items:center;gap:20px;margin:-16px 0 32px;font-family:var(--font-body);font-size:13px;color:var(--color-slate);">
  <div style="display:flex;align-items:center;gap:8px;"><div style="width:14px;height:12px;background:#0369a1;"></div>高才通計劃</div>
  <div style="display:flex;align-items:center;gap:8px;"><div style="width:14px;height:12px;background:#a8f1ff;border:1px solid #4ed7f1;"></div>其他 6 項合計</div>
</div>

<div class="section-head">
  <h2>高才通累計 · 2024 年底</h2>
</div>

<div class="tile-row">
  <div class="tile">
    <div class="tile-label">收到申請</div>
    <div class="big-num">116K</div>
    <div class="tile-note">2022.12 推出至 2024.12 累計。</div>
  </div>
  <div class="tile cyan">
    <div class="tile-label">獲批</div>
    <div class="big-num">92K</div>
    <div class="tile-note">79% 批准率。</div>
  </div>
  <div class="tile yellow">
    <div class="tile-label">實際抵港（含家屬）</div>
    <div class="big-num">75K</div>
    <div class="tile-note">獲批人士實際嚟港。多數係內地專業人士帶埋家庭。</div>
  </div>
</div>

<div class="section-head">
  <h2>英加澳移居 · 2021 起累計</h2>
  <div class="meta" style="margin-left:0;color:var(--color-slate);font-size:14px;">根據目的地政府記錄</div>
</div>

<div class="tile-row">
  <div class="dest-tile-big dark" style="flex:1.4;">
    <div class="header">
      <div class="head-tag">英國 · BNO Visa</div>
      <div class="pill">最大通道</div>
    </div>
    <div>
      <div class="num-row"><span class="num">180K</span><span class="num-suffix">已批簽證</span></div>
      <div class="detail">2021.01—2025.03 累計 ≈ 高才通抵港數 2.4 倍。</div>
    </div>
    <div class="source">來源：UK Home Office，經 UK Data Service Blog（2025.07.30）</div>
  </div>
  <div class="dest-tile-big outlined">
    <div class="header">
      <div class="head-tag">加拿大 · Stream A</div>
      <div class="head-meta">In-Canada Graduates</div>
    </div>
    <div>
      <div class="num-row"><span class="num">6.4K</span><span class="num-suffix" style="color:var(--color-slate);">人已抵加</span></div>
      <div class="detail" style="color:var(--color-ink-2);">10,250 申請（18,270 人）· 4,000 獲批 · 11,495 等待中</div>
    </div>
    <div class="source">來源：IRCC Q-493（2025.12.05）· 截至 2025.08.31</div>
  </div>
  <div class="dest-tile-big outlined">
    <div class="header">
      <div class="head-tag">加拿大 · Stream B</div>
      <div class="head-meta">Canadian Work Experience</div>
    </div>
    <div>
      <div class="num-row"><span class="num">5.6K</span><span class="num-suffix" style="color:var(--color-slate);">人已抵加</span></div>
      <div class="detail" style="color:var(--color-ink-2);">13,485 申請（20,325 人）· 3,835 獲批 · 14,035 等待中</div>
    </div>
    <div class="source">來源：IRCC Q-493（2025.12.05）· 截至 2025.08.31</div>
  </div>
</div>

<div class="callout">
  <div class="stripe"></div>
  <div class="cell lead">
    <div class="label">加拿大 · backlog</div>
    <div class="headline">想去但仲未去到嘅人，仲有 25,530 個。</div>
  </div>
  <div class="cell center">
    <div class="big">25,530</div>
    <div class="small">個 Stream A+B 等待中</div>
  </div>
  <div class="cell center">
    <div class="big">10+</div>
    <div class="small">年 · 新申請預計等候</div>
  </div>
  <div class="cell note">
    <div class="desc">IRCC 2025 年 H&amp;C 配額僅 10,000，2026 年再縮到 6,900。「真正去咗邊」嘅 pipeline 比已抵港數字大兩倍。</div>
    <div class="source">來源：IRCC Q-493（2025.12.05）</div>
  </div>
</div>

<div class="reading-note">
  <div class="lead-col">
    <div class="label">睇整體</div>
    <div class="headline">入境 ≈ 出境</div>
  </div>
  <div class="body">高才通 7.5 萬抵港 + 單程證 2021—2024 約 10 萬 + 其他簽證入境 ≈ <strong>20 萬人入境</strong>。<br>英加澳累計移居 17.3 萬 + 其他國家 ≈ <strong>20 萬人出境</strong>。<br>呢個就係統計處「其他淨遷移」3 年累計只係 +1.3 萬嘅原因——兩條 flow 量級相當，淨值接近零。</div>
</div>

<div class="cite">
  <span>來源：ISSH23/2024、RT01/2025、LegCo Q&amp;A 2025-01-22、IN15/2025、IRCC Q-493、UK Home Office。</span>
  <a href="/methodology">完整方法論 →</a>
</div>
