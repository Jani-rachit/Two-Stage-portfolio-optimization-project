import yfinance as yf
import os

def download_and_save(tickers, start, end, save_path="data/raw"):
    os.makedirs(save_path, exist_ok=True)

    for ticker in tickers:
        print(f"Downloading {ticker}...")

        try:
            df = yf.download(ticker, start=start, end=end)

            if df.empty:
                print(f"❌ No data for {ticker}")
                continue

            file_path = os.path.join(save_path, f"{ticker}.csv")
            df.to_csv(file_path)

            print(f"✅ Saved {ticker}")

        except Exception as e:
            print(f"❌ Error for {ticker}: {e}")

    print("🎉 All downloads completed!")