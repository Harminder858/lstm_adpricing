import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_model(y_true, y_pred):
    """
    Evaluate the model using various metrics.
    """
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    return {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'R2': r2
    }

def calculate_roas(revenue, spend):
    """
    Calculate Return on Ad Spend (ROAS).
    """
    return revenue / spend

def calculate_cpc(spend, clicks):
    """
    Calculate Cost per Click (CPC).
    """
    return spend / clicks

def calculate_cpa(spend, conversions):
    """
    Calculate Cost per Acquisition (CPA).
    """
    return spend / conversions