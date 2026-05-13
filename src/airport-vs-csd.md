---
title: 02 · 空運 vs 統計處
toc: false
---

<div class="chapter-tag">
  <div class="num">第 02 章</div>
  <div class="rule yellow"></div>
  <div class="label">空運 vs 統計處</div>
</div>

# 同一個香港、同一啲年份，<br>兩條線講緊兩個故事。

<p class="lede">坊間嘅入境處「港人空運淨流」其實係<mark>總計數字</mark>，受短途來回完全主導。統計處嘅「其他淨遷移」係<mark class="cyan">識別式扣減</mark>，捕捉真正結構性遷移。下面把兩條線轉成同一單位（淨流入為正），直接重疊。</p>

<div class="section-head">
  <h2>兩條 series 並排</h2>
  <div class="meta" style="margin-left:0;color:var(--color-slate);font-size:14px;">單位：千人 · 統計處慣例（淨流入為正）· atseed.co 嘅符號已倒轉。</div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:20px;font-family:var(--font-body);font-size:13px;">
    <div style="display:flex;align-items:center;gap:8px;"><div style="width:16px;height:12px;background:var(--color-red);"></div>機場淨流出</div>
    <div style="display:flex;align-items:center;gap:8px;"><div style="width:16px;height:12px;background:var(--color-cyan);"></div>統計處其他淨遷移</div>
  </div>
</div>

```js
const annual = FileAttachment("data/annual.csv").csv({typed: true});
```

```js
const pairs = annual
  .filter(d => d.year >= 2021 && d.year <= 2023)
  .map(d => ({
    year: d.year,
    airport: d.atseed_airport_hk_net_out != null ? -d.atseed_airport_hk_net_out : null,
    csd: d.other_net_migration
  }))
  .filter(d => d.airport != null && d.csd != null);
```

```js
const maxAbs = d3.max(pairs, d => Math.max(Math.abs(d.airport), Math.abs(d.csd)));
const fmt = n => (n > 0 ? "+" : "") + d3.format(",")(Math.round(n/1000)) + "K";
const root = document.createElement("div");
root.className = "compare-bars";
for (const d of pairs) {
  const yr = document.createElement("div");
  yr.className = "cmp-year";
  const axis = document.createElement("div");
  axis.className = "cmp-axis";

  const pos = document.createElement("div");
  pos.className = "cmp-bar-area cmp-pos";
  if (d.airport > 0) {
    const b = document.createElement("div");
    b.className = "cmp-bar red";
    b.style.height = (d.airport / maxAbs * 100).toFixed(1) + "%";
    const lbl = document.createElement("span"); lbl.className = "cmp-label"; lbl.textContent = fmt(d.airport); b.appendChild(lbl);
    pos.appendChild(b);
  }
  if (d.csd > 0) {
    const b = document.createElement("div");
    b.className = "cmp-bar cyan" + (d.year === 2023 ? " hilite" : "");
    b.style.height = (d.csd / maxAbs * 100).toFixed(1) + "%";
    const lbl = document.createElement("span"); lbl.className = "cmp-label dark"; lbl.textContent = fmt(d.csd); b.appendChild(lbl);
    pos.appendChild(b);
  }

  const zero = document.createElement("div"); zero.className = "cmp-zero";

  const neg = document.createElement("div");
  neg.className = "cmp-bar-area cmp-neg";
  if (d.airport < 0) {
    const b = document.createElement("div");
    b.className = "cmp-bar red";
    b.style.height = (Math.abs(d.airport) / maxAbs * 100).toFixed(1) + "%";
    const lbl = document.createElement("span"); lbl.className = "cmp-label"; lbl.textContent = fmt(d.airport); b.appendChild(lbl);
    neg.appendChild(b);
  }
  if (d.csd < 0) {
    const b = document.createElement("div");
    b.className = "cmp-bar cyan";
    b.style.height = (Math.abs(d.csd) / maxAbs * 100).toFixed(1) + "%";
    const lbl = document.createElement("span"); lbl.className = "cmp-label dark"; lbl.textContent = fmt(d.csd); b.appendChild(lbl);
    neg.appendChild(b);
  }

  axis.appendChild(pos);
  axis.appendChild(zero);
  axis.appendChild(neg);
  const yl = document.createElement("div"); yl.className = "cmp-year-label"; yl.textContent = d.year;
  yr.appendChild(axis);
  yr.appendChild(yl);
  root.appendChild(yr);
}
display(root);
```

<div class="section-head">
  <h2>3 年累計 · 差距 53 萬人，方向相反</h2>
</div>

<div class="tile-row">
  <div class="tile" style="border-color:var(--color-red);">
    <div class="tile-label" style="color:var(--color-red);">機場淨流出講法累計 2021—2023</div>
    <div class="big-num red"><span class="sign">−</span>485K</div>
    <div class="tile-note" style="color:var(--color-ink-2);">港人空運出境 − 入境（已倒符號 = 淨流入慣例）。讀者會理解為「香港 3 年淨流失 48.5 萬人」。</div>
  </div>
  <div class="tile" style="border-color:var(--color-cyan);">
    <div class="tile-label" style="color:var(--color-cyan-dark);">統計處其他淨遷移 累計 2021—2023</div>
    <div class="big-num"><span class="sign">+</span>42K</div>
    <div class="tile-note" style="color:var(--color-ink-2);">由人口會計恆等式扣除嚟。3 年加埋實際係<mark class="cyan">淨流入</mark>，主要由 2023 年人才入境大爆發推動。</div>
  </div>
  <div class="tile orange">
    <div class="tile-label">兩者差距</div>
    <div class="big-num" style="color:#fff;">527K</div>
    <div class="tile-note">絕對值相差 52.7 萬人，方向亦相反。即係呢套 framing 喺 3 年 horizon 上錯咗一個量級。</div>
  </div>
</div>

<div class="section-head">
  <h2>點解差距咁大</h2>
</div>

<div class="reason-row">
  <div class="reason red">
    <div class="num">原因一</div>
    <h4>短途來回唔完全抵銷</h4>
    <p>旅遊、公幹、探親毛流量極大。Window-edge（年尾出年頭返）同邊境重開不對稱，殘留噪音壓倒結構性訊號。</p>
  </div>
  <div class="reason cyan">
    <div class="num">原因二</div>
    <h4>高才通入境唔計港人</h4>
    <p>高才通到 2024 年底獲批 9.2 萬，實際抵港 7.5 萬（含家屬）。首次入境身份係「其他訪客」，機場淨流出講法只睇「香港居民」column，呢條入境通道完全唔見。</p>
  </div>
  <div class="reason yellow">
    <div class="num">原因三</div>
    <h4>回流醫病算「入境」</h4>
    <p>長期離港嘅永久居民返港求醫／探親，喺 入境處 上係「港人入境」一次。佢哋唔係真正回流，但會沖淡機場淨流出嘅訊號。政府近期承認呢個現象。</p>
  </div>
  <div class="reason orange">
    <div class="num">原因四</div>
    <h4>陸路移居完全略咗</h4>
    <p>ISSH33/2024 顯示廣東「通常逗留」港人約 49.6 萬。呢班人主要由羅湖／港珠澳大橋／深圳灣陸路出入，呢套講法因「陸路數據嘅 noise 太大」直接棄用。</p>
  </div>
</div>

<div class="section-head">
  <h2>真正去咗邊</h2>
  <div class="rule orange"></div>
  <div class="meta">根據目的地政府嘅入境簽證紀錄，唔係香港空運估算。</div>
</div>

<div class="tile-row">
  <div class="dest-tile-big dark" style="flex:1.4;">
    <div class="header">
      <div class="head-tag">英國 · BNO Visa</div>
      <div class="pill">最大通道</div>
    </div>
    <div>
      <div class="num-row"><span class="num">180K</span><span class="num-suffix">已批簽證</span></div>
      <div class="detail">約 18 萬人獲批 BN(O) 簽證 · 2021.01—2025.03 累計</div>
    </div>
    <div class="source">推出 2021.01.31 · 對象：BN(O) 護照持有人及家屬 · 5 年居留 + 1 年永居路徑<br>來源：UK Home Office，經 UK Data Service Blog（2025.07.30）</div>
  </div>
  <div class="dest-tile-big outlined">
    <div class="header">
      <div class="head-tag">加拿大 · Stream A</div>
      <div class="head-meta">In-Canada Graduates</div>
    </div>
    <div>
      <div class="num-row"><span class="num">6.4K</span><span class="num-suffix" style="color:var(--color-slate);">人已抵加</span></div>
      <div class="detail" style="color:var(--color-ink-2);">10,250 個申請（18,270 人）· 4,000 個獲批 · 6,415 人已成永居 · 11,495 人等待中</div>
    </div>
    <div class="source">推出 2021.06.01 · 對象：3 年內在加拿大專上院校畢業嘅港人 · 直接 PR<br>來源：IRCC 回覆國會書面質詢 Q-493（2025.12.05）· 數據截至 2025.08.31</div>
  </div>
  <div class="dest-tile-big outlined">
    <div class="header">
      <div class="head-tag">加拿大 · Stream B</div>
      <div class="head-meta">Canadian Work Experience</div>
    </div>
    <div>
      <div class="num-row"><span class="num">5.6K</span><span class="num-suffix" style="color:var(--color-slate);">人已抵加</span></div>
      <div class="detail" style="color:var(--color-ink-2);">13,485 個申請（20,325 人）· 3,835 個獲批 · 5,635 人已成永居 · 14,035 人等待中</div>
    </div>
    <div class="source">推出 2021.06.01 · 對象：3 年內在加拿大累計 1 年全職工作經驗嘅港人<br>來源：IRCC 回覆國會書面質詢 Q-493（2025.12.05）· 數據截至 2025.08.31</div>
  </div>
</div>

<aside class="editorial-aside">
  <div class="kicker"><span class="rule"></span>一個常見嘅反駁</div>
  <p>當然，近年係有唔少內地人落嚟香港，某程度上<mark class="cyan">溝淡咗本地人口比例</mark>，呢點都幾明顯，亦同<strong>《基本法》第 22 條相關條文嘅漏洞</strong>有關。不過<strong>講返數據</strong>，香港未至於真係有<mark>成百幾萬人</mark>已經移民。</p>
</aside>

<div class="cite">
  <span>來源：入境處 每日 passenger traffic CSV（atseed.co 同一上游）；C&amp;SD AD 2024 Tables 1.1 + 1.12；LegCo ISSH33/2024、ISSH23/2024、RT01/2025。</span>
  <a href="/methodology">完整方法論 →</a>
</div>
