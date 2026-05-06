strategy/strategy_engine.py

from intelligence.historical_context_engine import HistoricalContextEngine
from intelligence.volatility_context_engine import VolatilityContextEngine
import datetime

class StrategyEngine:

def __init__(self):  
    self.historical_engine = HistoricalContextEngine()  
    self.volatility_engine = VolatilityContextEngine()  

# -------------------------------------------------  
def detect(self, symbol, df):  

    if df is None or len(df) < 30:  
        return None  

    trend_strength = self._compute_trend_strength(df)  
    volatility = self._compute_volatility(df)  
    momentum = self._compute_momentum(df)  

    # 🔥 EARLY  
    early, compression, acceleration = self._detect_early_expansion(df, momentum)  

    # 🔥 CONTEXT LAYERS  
    liquidity_score = self._compute_liquidity_score(df)  
    session_score = self._compute_session_score()  
    mtf_score = self._compute_mtf_score(df)  
    context_score = self._compute_context_score(volatility)  
    factor_score = self._compute_factor_score(trend_strength, momentum)  

    structure_score = trend_strength  

    # =========================================  
    # 🔥 CRO BASE SCORE (FUSION LAYER)  
    # =========================================  
    base_score = (  
        momentum * 0.55 +  
        structure_score * 0.15 +  
        mtf_score * 0.15 +  
        factor_score * 0.15  
    )  

    # 🔥 EARLY BOOST  
    if early:  
        base_score += 0.05  

    # 🔥 VOLATILITY BOOST  
    if volatility > 0.6:  
        base_score += 0.03  

    # -------------------------------------------------  
    pattern_boost = self._detect_liquidity_compression_breakout(df)  
    base_score += pattern_boost  

    # -------------------------------------------------  
    # CONSISTENCY  
    scores = [structure_score, liquidity_score, factor_score]  
    mean_score = sum(scores) / len(scores)  
    variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)  
    std = variance ** 0.5  

    consistency = max(0.0, min(1.0, 1 - std))  
    adjustment = (consistency - 0.5) * 0.1  

    base_score = base_score * (1 + adjustment)  

    # 🔥 FINAL CLAMP  
    base_score = max(0.0, min(1.0, base_score))  

    # -------------------------------------------------  
    volatility_score = self.volatility_engine.evaluate(df)  

    market_features = {  
        "trend_strength": trend_strength,  
        "volatility": volatility,  
        "momentum": momentum,  
        "liquidity_state": liquidity_score,  
        "session_context": session_score  
    }  

    historical_score = self.historical_engine.evaluate(market_features)  

    # -------------------------------------------------  
    if momentum > 0.52:  
        direction = "up"  
    elif momentum < 0.48:  
        direction = "down"  
    else:  
        direction = "neutral"  

    # -------------------------------------------------  
    signal = {  
        "symbol": symbol,  
        "base_score": base_score,  

        "momentum": direction,  
        "strength": abs(momentum - 0.5) * 2,  

        # 🔥 EARLY (مهم)  
        "early_entry": early,  
        "compression": compression,  
        "acceleration": acceleration,  

        # SCORES  
        "structure_score": structure_score,  
        "liquidity_score": liquidity_score,  
        "session_score": session_score,  
        "context_score": context_score,  
        "mtf_score": mtf_score,  
        "factor_score": factor_score,  
        "historical_score": historical_score,  
        "volatility_score": volatility_score  
    }  

    return signal  

# -------------------------------------------------  
def _compute_mtf_score(self, df):  

    closes = df["close"]  

    trend_1 = (closes.iloc[-1] - closes.iloc[-5]) / closes.iloc[-5]  
    trend_5 = (closes.iloc[-1] - closes.iloc[-15]) / closes.iloc[-15]  
    trend_15 = (closes.iloc[-1] - closes.iloc[-30]) / closes.iloc[-30]  

    def normalize(x):  
        return max(0.0, min(1.0, 0.5 + x))  

    return (normalize(trend_1) + normalize(trend_5) + normalize(trend_15)) / 3  

# -------------------------------------------------  
def _compute_liquidity_score(self, df):  

    highs = df["high"]  
    lows = df["low"]  

    prev_high = highs.iloc[-10:-5].max()  
    prev_low = lows.iloc[-10:-5].min()  

    last_high = highs.iloc[-1]  
    last_low = lows.iloc[-1]  

    if last_high > prev_high or last_low < prev_low:  
        return 0.4  

    return 0.6  

# -------------------------------------------------  
def _compute_session_score(self):  

    hour = datetime.datetime.utcnow().hour  

    if 7 <= hour <= 16:  
        return 0.65  

    if 0 <= hour <= 6:  
        return 0.45  

    return 0.5  

# -------------------------------------------------  
def _compute_context_score(self, volatility):  

    if volatility > 0.7:  
        return 0.7  

    if volatility < 0.3:  
        return 0.4  

    return 0.5  

# -------------------------------------------------  
def _compute_factor_score(self, trend_strength, momentum):  

    return max(0.0, min(1.0, (trend_strength + momentum) / 2))  

# -------------------------------------------------  
def _detect_early_expansion(self, df, momentum):  

    highs = df["high"]  
    lows = df["low"]  
    closes = df["close"]  

    recent_range = highs.iloc[-10:].max() - lows.iloc[-10:].min()  
    prev_range = highs.iloc[-20:-10].max() - lows.iloc[-20:-10].min()  

    compression = prev_range > 0 and (recent_range / prev_range) < 0.85  

    breakout_up = closes.iloc[-1] > highs.iloc[-5:-1].max()  
    breakout_down = closes.iloc[-1] < lows.iloc[-5:-1].min()  

    breakout = breakout_up or breakout_down  

    prev_momentum = (closes.iloc[-2] - closes.iloc[-11]) / closes.iloc[-11]  
    prev_momentum = max(0.0, min(1.0, 0.5 + prev_momentum))  

    acceleration = momentum > prev_momentum  

    momentum_strength = abs(momentum - 0.5)  

    early = (  
        (compression and breakout) or  
        (breakout and acceleration)  
    ) and momentum_strength > 0.06  

    return early, compression, acceleration  

# -------------------------------------------------  
def _detect_liquidity_compression_breakout(self, df):  

    highs = df["high"]  
    lows = df["low"]  
    closes = df["close"]  

    prev_high = highs.iloc[-10:-5].max()  
    prev_low = lows.iloc[-10:-5].min()  

    last_high = highs.iloc[-6]  
    last_low = lows.iloc[-6]  

    sweep = last_high > prev_high or last_low < prev_low  

    if not sweep:  
        return 0.0  

    compression_range = highs.iloc[-5:].max() - lows.iloc[-5:].min()  
    prior_range = highs.iloc[-15:-5].max() - lows.iloc[-15:-5].min()  

    if prior_range == 0:  
        return 0.0  

    if (compression_range / prior_range) > 0.5:  
        return 0.0  

    breakout = closes.iloc[-1] > highs.iloc[-5:-1].max() or \  
               closes.iloc[-1] < lows.iloc[-5:-1].min()  

    return 0.15 if breakout else 0.0  

# -------------------------------------------------  
def _compute_trend_strength(self, df):  

    closes = df["close"]  
    trend = (closes.iloc[-1] - closes.iloc[-20]) / closes.iloc[-20]  

    return max(0.0, min(1.0, 0.5 + trend))  

# -------------------------------------------------  
def _compute_volatility(self, df):  

    returns = df["close"].pct_change().dropna()  
    vol = returns[-20:].std()  

    return max(0.0, min(1.0, vol * 10))  

# -------------------------------------------------  
def _compute_momentum(self, df):  

    closes = df["close"]  
    momentum = (closes.iloc[-1] - closes.iloc[-10]) / closes.iloc[-10]  

    return max(0.0, min(1.0, 0.5 + momentum))
