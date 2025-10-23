from fastapi import FastAPI
import yfinance as yf
import numpy as np
from datetime import date

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Regime Pulse API. Try /nasdaq"}

@app.get("/nasdaq")
def nasdaq_signal():
    try:
        qqq = yf.download("QQQ", period="30d", progress=False)["Close"]
        if len(qqq) < 10:
            raise Exception("Not enough data")
        returns = qqq.pct_change().dropna()
        vol_ann = returns.std() * (252 ** 0.5)
        return {
            "market": "NASDAQ-100 (QQQ)",
            "annualized_volatility": round(vol_ann, 4),
            "data_points": len(returns),
            "as_of": str(date.today())
        }
    except Exception as e:
        return {"error": str(e)}
