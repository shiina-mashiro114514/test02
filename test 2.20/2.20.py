from pathlib import Path


def build_html() -> str:
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>全球主要股市地图看盘</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  <style>
    :root {
      --bg: #0b1220;
      --panel: #111b2f;
      --text: #e7eefc;
      --muted: #97a7c7;
      --line: #273754;
      --up: #ef4444;
      --down: #22c55e;
      --flat: #9ca3af;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    .wrap {
      max-width: 1200px;
      margin: 0 auto;
      padding: 16px;
    }
    .top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }
    .title {
      font-size: 24px;
      font-weight: 700;
      margin: 0;
    }
    .meta {
      color: var(--muted);
      font-size: 13px;
      text-align: right;
    }
    .panel {
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 12px;
      overflow: hidden;
    }
    #map {
      width: 100%;
      height: 72vh;
      min-height: 520px;
    }
    .legend {
      display: flex;
      gap: 14px;
      padding: 10px 12px;
      border-top: 1px solid var(--line);
      color: var(--muted);
      font-size: 13px;
      flex-wrap: wrap;
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
      margin-right: 6px;
      vertical-align: middle;
    }
    .m-up { background: var(--up); }
    .m-down { background: var(--down); }
    .m-flat { background: var(--flat); }
    .badge {
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 12px;
      border: 1px solid var(--line);
      color: var(--muted);
    }
    .leaflet-popup-content-wrapper,
    .leaflet-popup-tip {
      background: #0f1729;
      color: var(--text);
      border: 1px solid #2a3c61;
    }
    .leaflet-container a { color: #93c5fd; }
    .market-marker {
      min-width: 86px;
      padding: 4px 7px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.25);
      background: rgba(17, 27, 47, 0.92);
      color: #fff;
      text-align: center;
      font-size: 12px;
      line-height: 1.2;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
    }
    .market-marker .name { font-weight: 700; }
    .market-marker.up { border-color: var(--up); }
    .market-marker.down { border-color: var(--down); }
    .market-marker.flat { border-color: var(--flat); }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <h1 class="title">全球主要股市地图看盘</h1>
      <div class="meta">
        <div id="refresh-time">更新时间：-</div>
        <div>数据源：Yahoo Finance（约每60秒刷新）</div>
      </div>
    </div>

    <div class="panel">
      <div id="map"></div>
      <div class="legend">
        <span><i class="dot m-up"></i>上涨</span>
        <span><i class="dot m-down"></i>下跌</span>
        <span><i class="dot m-flat"></i>平/休市或数据暂缺</span>
        <span class="badge" id="status-text">状态：加载中</span>
      </div>
    </div>
  </div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script>
    const MARKETS = [
      { name: "美国 标普500", symbol: "^GSPC", lat: 40.7128, lng: -74.0060, city: "纽约" },
      { name: "美国 纳斯达克", symbol: "^IXIC", lat: 40.7128, lng: -74.0000, city: "纽约" },
      { name: "美国 道琼斯", symbol: "^DJI", lat: 40.7138, lng: -74.0030, city: "纽约" },
      { name: "英国 富时100", symbol: "^FTSE", lat: 51.5072, lng: -0.1276, city: "伦敦" },
      { name: "德国 DAX", symbol: "^GDAXI", lat: 50.1109, lng: 8.6821, city: "法兰克福" },
      { name: "法国 CAC40", symbol: "^FCHI", lat: 48.8566, lng: 2.3522, city: "巴黎" },
      { name: "日本 日经225", symbol: "^N225", lat: 35.6762, lng: 139.6503, city: "东京" },
      { name: "中国 上证指数", symbol: "000001.SS", lat: 31.2304, lng: 121.4737, city: "上海" },
      { name: "香港 恒生指数", symbol: "^HSI", lat: 22.3193, lng: 114.1694, city: "香港" },
      { name: "印度 NIFTY50", symbol: "^NSEI", lat: 19.0760, lng: 72.8777, city: "孟买" },
      { name: "澳洲 ASX200", symbol: "^AXJO", lat: -33.8688, lng: 151.2093, city: "悉尼" },
      { name: "加拿大 TSX", symbol: "^GSPTSE", lat: 43.6532, lng: -79.3832, city: "多伦多" },
      { name: "巴西 Bovespa", symbol: "^BVSP", lat: -23.5505, lng: -46.6333, city: "圣保罗" }
    ];

    const map = L.map("map", {
      worldCopyJump: true,
      minZoom: 2,
      maxZoom: 6
    }).setView([22, 20], 2);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    const markers = new Map();

    function formatNumber(value) {
      if (value === null || value === undefined || Number.isNaN(value)) {
        return "-";
      }
      return Number(value).toLocaleString("en-US", { maximumFractionDigits: 2 });
    }

    function formatPct(value) {
      if (value === null || value === undefined || Number.isNaN(value)) {
        return "-";
      }
      const sign = value > 0 ? "+" : "";
      return `${sign}${value.toFixed(2)}%`;
    }

    function marketStateLabel(state) {
      const mapState = {
        "REGULAR": "实时",
        "PRE": "盘前",
        "POST": "盘后",
        "PREPRE": "盘前",
        "POSTPOST": "盘后",
        "CLOSED": "收盘"
      };
      return mapState[state] || "未知";
    }

    function movementClass(changePct) {
      if (changePct === null || changePct === undefined || Number.isNaN(changePct)) {
        return "flat";
      }
      if (changePct > 0.02) {
        return "up";
      }
      if (changePct < -0.02) {
        return "down";
      }
      return "flat";
    }

    function markerHtml(name, price, changePct, state) {
      const cls = movementClass(changePct);
      return `
        <div class="market-marker ${cls}">
          <div class="name">${name}</div>
          <div>${formatNumber(price)}</div>
          <div>${formatPct(changePct)} | ${marketStateLabel(state)}</div>
        </div>
      `;
    }

    function popupHtml(market, quote) {
      const ts = quote.regularMarketTime
        ? new Date(quote.regularMarketTime * 1000).toLocaleString("zh-CN")
        : "-";

      return `
        <div style="min-width:220px;line-height:1.45;">
          <div style="font-weight:700;margin-bottom:4px;">${market.name}</div>
          <div>城市：${market.city}</div>
          <div>代码：${market.symbol}</div>
          <div>点位：${formatNumber(quote.regularMarketPrice)}</div>
          <div>涨跌：${formatNumber(quote.regularMarketChange)} (${formatPct(quote.regularMarketChangePercent)})</div>
          <div>状态：${marketStateLabel(quote.marketState)}</div>
          <div>行情时间：${ts}</div>
        </div>
      `;
    }

    function upsertMarker(market, quote) {
      const icon = L.divIcon({
        className: "",
        html: markerHtml(market.name, quote.regularMarketPrice, quote.regularMarketChangePercent, quote.marketState),
        iconSize: [96, 44],
        iconAnchor: [48, 22]
      });

      if (!markers.has(market.symbol)) {
        const marker = L.marker([market.lat, market.lng], { icon }).addTo(map);
        marker.bindPopup(popupHtml(market, quote));
        markers.set(market.symbol, marker);
      } else {
        const marker = markers.get(market.symbol);
        marker.setIcon(icon);
        marker.setPopupContent(popupHtml(market, quote));
      }
    }

    function fallbackQuote() {
      return {
        regularMarketPrice: null,
        regularMarketChange: null,
        regularMarketChangePercent: null,
        regularMarketTime: null,
        marketState: "CLOSED"
      };
    }

    async function refreshQuotes() {
      const statusEl = document.getElementById("status-text");
      const timeEl = document.getElementById("refresh-time");

      try {
        statusEl.textContent = "状态：刷新中";
        const symbols = MARKETS.map((x) => x.symbol).join(",");
        const url = `https://query1.finance.yahoo.com/v7/finance/quote?symbols=${encodeURIComponent(symbols)}`;

        const resp = await fetch(url, { cache: "no-store" });
        if (!resp.ok) {
          throw new Error(`HTTP ${resp.status}`);
        }

        const data = await resp.json();
        const list = data?.quoteResponse?.result || [];
        const mapBySymbol = new Map(list.map((q) => [q.symbol, q]));

        for (const market of MARKETS) {
          const quote = mapBySymbol.get(market.symbol) || fallbackQuote();
          upsertMarker(market, quote);
        }

        timeEl.textContent = `更新时间：${new Date().toLocaleString("zh-CN")}`;
        statusEl.textContent = "状态：正常";
      } catch (err) {
        statusEl.textContent = `状态：刷新失败 (${err.message})`;
      }
    }

    refreshQuotes();
    setInterval(refreshQuotes, 60000);
  </script>
</body>
</html>
"""


def main() -> None:
    output_path = Path(__file__).with_name("global_market_dashboard.html")
    output_path.write_text(build_html(), encoding="utf-8")
    print(f"已生成: {output_path}")
    print("打开方式: 直接在浏览器打开该 HTML 文件。")


if __name__ == "__main__":
    main()
