import pandas as pd

def trend_value(df: pd.DataFrame) -> pd.DataFrame:
    df = check_ema_trend(df)
    df = check_macd_trend(df)
    df = check_rsi_trend(df)
    df = check_volume(df)
    df = check_alerts(df)
    return df
# Hàm kiểm tra xu hướng EMA
def check_ema_trend(df: pd.DataFrame) -> pd.DataFrame:
    # Khởi tạo cột nếu chưa tồn tại
    if 'ema_check' not in df.columns:
        df['ema_check'] = ''
    
    # Tìm các bản ghi chưa có giá trị (rỗng hoặc NaN)
    mask = (df['ema_check'] == '') | (df['ema_check'].isna())
    
    # Chỉ tính toán cho các bản ghi chưa có giá trị
    if mask.sum() == 0:
        return df
    
    conditions_1 = df.loc[mask, 'ema_20'] > df.loc[mask, 'ema_50']
    conditions_2 = (df.loc[mask, 'ema_20'] > df.loc[mask, 'ema_50']) & (df.loc[mask, 'ema_50'] > df.loc[mask, 'ema_90'])
    conditions_3 = df.loc[mask, 'ema_20'] < df.loc[mask, 'ema_50']
    conditions_4 = (df.loc[mask, 'ema_20'] < df.loc[mask, 'ema_50']) & (df.loc[mask, 'ema_50'] < df.loc[mask, 'ema_90'])
    
    # Tính toán giá trị cho các bản ghi cần tính
    ema_check_values = [''] * mask.sum()
    for idx, i in enumerate(df[mask].index):
        if conditions_2.iloc[idx]:
            ema_check_values[idx] = '+++'
        elif conditions_1.iloc[idx]:
            ema_check_values[idx] = '+'
        elif conditions_4.iloc[idx]:
            ema_check_values[idx] = '---'
        elif conditions_3.iloc[idx]:
            ema_check_values[idx] = '--'
        else:
            ema_check_values[idx] = '.'
    
    # Chỉ cập nhật các bản ghi chưa có giá trị
    df.loc[mask, 'ema_check'] = ema_check_values
    return df

# Hàm kiểm tra xu hướng RSI
def check_rsi_trend(df: pd.DataFrame) -> pd.DataFrame:
    # Khởi tạo cột nếu chưa tồn tại
    if 'rsi_check' not in df.columns:
        df['rsi_check'] = ''
    
    # Tìm các bản ghi chưa có giá trị (rỗng hoặc NaN)
    mask = (df['rsi_check'] == '') | (df['rsi_check'].isna())
    
    # Chỉ tính toán cho các bản ghi chưa có giá trị
    if mask.sum() == 0:
        return df
    
    rsi_check_values = [''] * mask.sum()
    for idx, i in enumerate(df[mask].index):
        rsi_12 = df.loc[i, 'rsi_12']
        rsi_24 = df.loc[i, 'rsi_24'] if 'rsi_24' in df.columns else None

        if pd.isna(rsi_12) or pd.isna(rsi_24):
            rsi_check_values[idx] = ''
        elif rsi_12 > rsi_24:
            if rsi_12 > 80:
                rsi_check_values[idx] = '+++'
            elif rsi_12 > 70:
                rsi_check_values[idx] = '++'
            elif rsi_12 > 50:
                rsi_check_values[idx] = '+'
            else:
                rsi_check_values[idx] = '.'
        elif rsi_12 < rsi_24:
            if rsi_12 < 20:
                rsi_check_values[idx] = '---'
            elif rsi_12 < 30:
                rsi_check_values[idx] = '--'
            elif rsi_12 < 50:
                rsi_check_values[idx] = '-'
            else:
                rsi_check_values[idx] = '.'
        else:
            rsi_check_values[idx] = '.'

    # Chỉ cập nhật các bản ghi chưa có giá trị
    df.loc[mask, 'rsi_check'] = rsi_check_values
    return df

# Hàm kiểm tra xu hướng MACD
def check_macd_trend(df: pd.DataFrame) -> pd.DataFrame:
    # Khởi tạo cột nếu chưa tồn tại
    if 'macd_check' not in df.columns:
        df['macd_check'] = ''
    
    # Tìm các bản ghi chưa có giá trị (rỗng hoặc NaN)
    mask = (df['macd_check'] == '') | (df['macd_check'].isna())
    
    # Chỉ tính toán cho các bản ghi chưa có giá trị
    if mask.sum() == 0:
        return df
    
    macd_check_values = [''] * mask.sum()
    for idx, i in enumerate(df[mask].index):
        macd_val = df.loc[i, 'macd']
        signal_val = df.loc[i, 'macd_signal']

        if pd.isna(macd_val) or pd.isna(signal_val):
            macd_check_values[idx] = ''
        elif macd_val > signal_val and macd_val > 0:
            macd_check_values[idx] = '+ ++'
        elif macd_val < signal_val and macd_val > 0:
            macd_check_values[idx] = '+ --'
        elif macd_val < signal_val and macd_val < 0:
            macd_check_values[idx] = '- --'
        elif macd_val > signal_val and macd_val < 0:
            macd_check_values[idx] = '- ++'
        else:
            macd_check_values[idx] = '.'
    
    # Chỉ cập nhật các bản ghi chưa có giá trị
    df.loc[mask, 'macd_check'] = macd_check_values
    return df

def check_volume(df, window=30):
    # Tính volume_ma và volume_strength cho tất cả (cần thiết cho rolling)
    df['volume_ma'] = df['volume'].rolling(window).mean()
    df['volume_strength'] = df['volume'] / df['volume_ma']
    
    # Khởi tạo cột nếu chưa tồn tại
    if 'volume_signal' not in df.columns:
        df['volume_signal'] = ''
    
    # Tìm các bản ghi chưa có giá trị (rỗng hoặc NaN)
    mask = (df['volume_signal'] == '') | (df['volume_signal'].isna())
    
    # Chỉ tính toán cho các bản ghi chưa có giá trị
    if mask.sum() == 0:
        return df
    
    def volume_label(x):
        if pd.isna(x) or x < 1:
            return '-'
        elif 1 <= x < 1.5:
            return '1+'
        elif 1.5 <= x < 2:
            return '1.5+'
        elif 2 <= x < 3:
            return '2+'
        else:
            return '3++'
    
    # Chỉ tính toán cho các bản ghi chưa có giá trị
    df.loc[mask, 'volume_signal'] = df.loc[mask, 'volume_strength'].apply(volume_label)
    return df

def check_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Kiểm tra các tín hiệu cần chú ý:
    1. EMA: '+++' hoặc '---'
    2. RSI + Volume: volume_strength > 1 và (RSI12 > 50 khi RSI12 > RSI24 hoặc RSI12 < 50 khi RSI12 < RSI24)
    """
    # Khởi tạo cột nếu chưa tồn tại
    if 'alert_signal' not in df.columns:
        df['alert_signal'] = ''
    
    # Tìm các bản ghi chưa có giá trị (rỗng hoặc NaN)
    mask = df['alert_signal'].isna() | (df['alert_signal'] == '')
    # Chỉ tính toán cho các bản ghi chưa có giá trị
    if mask.sum() == 0:
        return df
    
    alert_values = [''] * mask.sum()
    for idx, i in enumerate(df[mask].index):
        alerts = []
        
        # Kiểm tra EMA signal
        ema_check = df.loc[i, 'ema_check']
        if ema_check == '+++' or ema_check == '---':
            alerts.append(f'EMA:{ema_check}')
        
        # Kiểm tra RSI + Volume
        volume_strength = df.loc[i, 'volume_strength']
        rsi_12 = df.loc[i, 'rsi_12']
        rsi_24 = df.loc[i, 'rsi_24'] if 'rsi_24' in df.columns else None
        
        if not pd.isna(volume_strength) and not pd.isna(rsi_12) and not pd.isna(rsi_24):
            if volume_strength > 1:
                if rsi_12 > rsi_24 and rsi_12 > 50:
                    alerts.append(f'RSI:Up')
                elif rsi_12 < rsi_24 and rsi_12 < 50:
                    alerts.append(f'RSI:down')
        
        # Gán giá trị alert
        if alerts:
            alert_values[idx] = ' | '.join(alerts)
        else:
            alert_values[idx] = 'None'
    # Chỉ cập nhật các bản ghi chưa có giá trị
    df.loc[mask, 'alert_signal'] = alert_values
    return df
