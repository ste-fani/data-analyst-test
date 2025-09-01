import pandas as pd;
import numpy as np;

#applying fraud detection rules
def preprocess_transactions(df: pd.DataFrame) -> pd.DataFrame:
    #converting and sorting datetime
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    df = df.sort_values(['user_id', 'transaction_date'])

    #verifying previous chargeback
    if 'has_cbk' not in df.columns:
        df['has_cbk'] = False

    #creating a new column with user's purchases count
    df['user_tx_count'] = df.groupby('user_id').cumcount()

    #creating a new column that counts the user's average spending
    df['user_mean_amount'] = df.groupby('user_id')['transaction_amount'].transform(
        lambda x: x.expanding().mean()
    )

    #defining rules 1: max range of purchase about user history
    df['rule_high_amount'] = (
        (df['user_tx_count'] >= 1) &
        (df['transaction_amount'] > 1.5 * df['user_mean_amount'])
    ).astype(int)

    #defining rules 2: same merchant with minimium interval
    df['prev_merchant'] = df.groupby('user_id')['merchant_id'].shift(1)
    df['prev_amount'] = df.groupby('user_id')['transaction_amount'].shift(1)
    df['prev_time'] = df.groupby('user_id')['transaction_date'].shift(1)

    df['minutes_diff'] = (df['transaction_date'] - df['prev_time']).dt.total_seconds() / 60
    df['rule_quick_repeat'] = (
        (df['merchant_id'] == df['prev_merchant']) &
        (df['minutes_diff'] <= 10) &
        (abs(df['transaction_amount'] - df['prev_amount']) / df['prev_amount'] <= 0.05)
    ).astype(int)

    #defining rules 3: time permission, purchase value permission, has chargeback and has device
    df['hour'] = df['transaction_date'].dt.hour
    df['has_device'] = df['device_id'].notnull()
    df['has_cbk'] = df['has_cbk'].astype(str).str.upper() == 'TRUE'

    df['rule_night_purchase'] = (
        ((df['hour'] >= 20) | (df['hour'] < 6)) &
        (df['transaction_amount'] >= 2500) &
        (df['has_cbk'] | ~df['has_device'])
    ).astype(int)

    #rules of fraud label
    df['is_fraud'] = (
        (df['rule_high_amount'] == 1) |
        (df['rule_quick_repeat'] == 1) |
        (df['rule_night_purchase'] == 1)
    ).astype(int)

    return df

#creating a user history with data information
def build_user_features(df: pd.DataFrame) -> pd.DataFrame:

    #identifying the time between each purchase
    def avg_time_between_purchases(group):
        if len(group) > 1:
            return group['transaction_date'].diff().mean().total_seconds() / 3600
        return np.nan

    #identifying repeat merchants
    def most_common_merchant(group):
        mode = group['merchant_id'].mode()
        return mode.iloc[0] if not mode.empty else 'None'

    #identifying night time shopping
    def count_night_transactions(group):
        return ((group['transaction_date'].dt.hour >= 20) | (group['transaction_date'].dt.hour < 6)).sum()

    #grouping rules in user history
    def extract_user_features(group):
        return pd.Series({
            'total_purchases': len(group),
            'average_value': group['transaction_amount'].mean(),
            'maximum_value': group['transaction_amount'].max(),
            'minimum_value': group['transaction_amount'].min(),
            'value_deviation': group['transaction_amount'].std(),
            'average_time_between_purchases_hours': avg_time_between_purchases(group),
            'quant_merchants': group['merchant_id'].nunique(),
            'most_common_merchant': most_common_merchant(group),
            'night_transaction': count_night_transactions(group),
            'cbk_count': group['has_cbk'].sum(),
            'high_amount_freq': group['rule_high_amount'].mean(),
            'quick_repeat_freq': group['rule_quick_repeat'].mean(),
            'night_purchase_freq': group['rule_night_purchase'].mean()
        })

    user_features = df.groupby('user_id', group_keys=False).apply(extract_user_features).reset_index()

    #identifying fraud history
    if 'is_fraud' in df.columns:
        user_fraud_history = df.groupby('user_id')['is_fraud'].max().reset_index()
        user_features = user_features.merge(user_fraud_history, on='user_id')
    else:
        user_features['is_fraud'] = 0

    return user_features

#incrementing my previous rules in a general pipeline
def process_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df_processed = preprocess_transactions(df)
    user_features = build_user_features(df_processed)
    return user_features