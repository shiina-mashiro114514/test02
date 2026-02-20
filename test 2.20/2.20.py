from pathlib import Path


def build_html() -> str:
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>全球主要股票市场实时看盘</title>
  <style>
    :root {
      --bg: #0c1222;
      --panel: #111a31;
      --text: #e8edf8;
      --muted: #8ea0c8;
      --line: #223357;
      --accent: #2dd4bf;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background: radial-gradient(circle at 20% 10%, #173055, var(--bg));
      color: var(--text);
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      margin-bottom: 16px;
    }
    h1 {
      margin: 0;
      font-size: 26px;
      letter-spacing: 0.3px;
    }
    .meta {
      color: var(--muted);
      font-size: 14px;
    }
    .card {
      border: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.00)), var(--panel);
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 14px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }
    .card-title {
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      font-weight: 600;
      color: var(--accent);
    }
    .footer {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }
    a { color: #93c5fd; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>全球主要股票市场实时看盘</h1>
      <div class="meta" id="time"></div>
    </div>

    <div class="card">
      <div class="card-title">全球指数快照（实时）</div>
      <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
        {
          "symbols": [
            {"description":"美国 标普500","proName":"FOREXCOM:SPXUSD"},
            {"description":"美国 纳斯达克100","proName":"FOREXCOM:NSXUSD"},
            {"description":"美国 道琼斯","proName":"FOREXCOM:DJI"},
            {"description":"中国 上证指数","proName":"SSE:000001"},
            {"description":"香港 恒生指数","proName":"HSI:HSI"},
            {"description":"日本 日经225","proName":"TVC:NI225"},
            {"description":"英国 富时100","proName":"TVC:UKX"},
            {"description":"德国 DAX","proName":"XETR:DAX"},
            {"description":"法国 CAC40","proName":"TVC:CAC40"},
            {"description":"印度 NIFTY 50","proName":"NSE:NIFTY"}
          ],
          "showSymbolLogo": true,
          "isTransparent": true,
          "displayMode": "adaptive",
          "colorTheme": "dark",
          "locale": "zh_CN"
        }
        </script>
      </div>
    </div>

    <div class="card">
      <div class="card-title">全球市场热力图</div>
      <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
        {
          "exchanges": ["US", "CN", "HK", "JP", "GB", "DE", "FR", "IN"],
          "dataSource": "SPX500",
          "grouping": "sector",
          "blockSize": "market_cap_basic",
          "blockColor": "change",
          "locale": "zh_CN",
          "symbolUrl": "",
          "colorTheme": "dark",
          "hasTopBar": true,
          "isDataSetEnabled": true,
          "isZoomEnabled": true,
          "hasSymbolTooltip": true,
          "isMonoSize": false,
          "width": "100%",
          "height": 520
        }
        </script>
      </div>
    </div>

    <div class="card">
      <div class="card-title">重点指数走势图</div>
      <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
        {
          "autosize": true,
          "symbol": "FOREXCOM:SPXUSD",
          "interval": "D",
          "timezone": "Asia/Shanghai",
          "theme": "dark",
          "style": "1",
          "locale": "zh_CN",
          "withdateranges": true,
          "allow_symbol_change": true,
          "watchlist": [
            "FOREXCOM:SPXUSD",
            "FOREXCOM:NSXUSD",
            "SSE:000001",
            "HSI:HSI",
            "TVC:NI225",
            "XETR:DAX",
            "TVC:UKX"
          ],
          "details": true,
          "hotlist": true,
          "calendar": true,
          "height": 560
        }
        </script>
      </div>
    </div>

    <div class="footer">
      <div>说明：该页面依赖 TradingView 在线数据源，需联网打开。</div>
      <div>如果你希望离线或自定义数据源版本，我可以给你再做一个 Python 定时抓取 + 本地自动刷新版本。</div>
    </div>
  </div>

  <script>
    const t = document.getElementById("time");
    const updateTime = () => {
      const now = new Date();
      t.textContent = `本地时间：${now.toLocaleString("zh-CN")}`;
    };
    updateTime();
    setInterval(updateTime, 1000);
  </script>
</body>
</html>
"""


def main() -> None:
    output_path = Path(__file__).with_name("global_market_dashboard.html")
    output_path.write_text(build_html(), encoding="utf-8")
    print(f"已生成: {output_path}")
    print("打开方式: 直接双击 HTML 文件，或在浏览器中打开该文件。")


if __name__ == "__main__":
    main()
