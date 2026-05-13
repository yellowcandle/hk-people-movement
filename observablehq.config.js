export default {
  title: "HK People Movement",
  pages: [
    { name: "01 · 人口恆等式", path: "/identity" },
    { name: "02 · 空運 vs 統計處", path: "/airport-vs-csd" },
    { name: "03 · 機場目的地", path: "/hkia-mix" },
    { name: "04 · 大灣區陸路", path: "/gba" },
    { name: "05 · 人才與移居", path: "/talent" },
    { name: "06 · 方法論", path: "/methodology" }
  ],
  root: "src",
  output: "dist",
  theme: ["air", "wide"],
  style: "style.css",
  // MetroSung is licensed for 個人非商用 use — this dashboard is personal /
  // non-commercial (a methodology critique), so the EULA is satisfied. If
  // this ever becomes commercial, swap back to NotoSerifTC-subset (run
  // `make fonts NOTO=1` and flip the URLs + family below).
  head: `
<style>
@font-face {
  font-family: "MetroSung";
  font-style: normal;
  font-weight: 400 900;
  font-display: swap;
  src: url("/static/fonts/MetroSung-subset.woff2") format("woff2"),
       url("/static/fonts/MetroSung-subset.woff") format("woff");
  unicode-range: U+0020-007F, U+2000-206F, U+2E80-9FFF, U+3000-303F, U+FF00-FFEF;
}
</style>`,
  header: `<div class="site-header">
  <a class="brand" href="/"><span class="brand-name">香港人口流動</span> <span class="brand-tag">數據實際上講緊咩</span></a>
  <nav class="site-nav">
    <a href="/identity">人口恆等式</a>
    <a href="/airport-vs-csd">空運 vs 統計處</a>
    <a href="/hkia-mix">機場目的地</a>
    <a href="/gba">大灣區</a>
    <a href="/talent">人才與移居</a>
    <a href="/methodology">方法論</a>
  </nav>
</div>`,
  footer: `每日自動重建 &nbsp;·&nbsp; IMMD 開放數據 + HKIA flight API + LegCo RPDB &nbsp;·&nbsp; <a href='/methodology'>所有來源</a> pin 入 git`,
  sidebar: false,
  toc: false,
  pager: false,
  search: false
};
