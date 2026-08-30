import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


def _calculate_vif(X: pd.DataFrame) -> pd.DataFrame:
    """حساب معامل تضخم التباين (VIF) للكشف عن التعدد الخطي (Multicollinearity)."""
    # تحويل القيم إلى float وضمان عدم وجود قيم مفقودة لضمان الاستقرار الحسابي
    X_numeric = X.astype(float)
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X_numeric.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X_numeric.values, i)
        for i in range(X_numeric.shape[1])
    ]
    # استبعاد الثابت من مخرجات الـ VIF
    return vif_data[vif_data["Variable"] != "const"].reset_index(drop=True)


def auto_select_regression_model(df: pd.DataFrame, outcome_variable: str) -> str:
    """تحديد نوع نموذج الانحدار المناسب تلقائياً بناءً على طبيعة المتغير التابع (Outcome)."""
    if outcome_variable not in df.columns:
        raise ValueError(f"Outcome variable '{outcome_variable}' not found in DataFrame.")

    series = df[outcome_variable].dropna()
    unique_vals = series.nunique()

    # إذا كان المتغير يحتوي على قيمتين فقط أو ثنائي البنية (0 و 1)
    if unique_vals == 2:
        return "logistic"
    elif pd.api.types.is_numeric_dtype(series):
        return "linear"
    else:
        raise ValueError(
            f"The outcome variable '{outcome_variable}' is non-numeric and has {unique_vals} unique values. "
            "Please select a numeric continuous outcome for Linear Regression or a binary outcome for Logistic Regression."
        )


def run_linear_regression(
    df: pd.DataFrame,
    outcome_variable: str,
    predictor_variables: list
) -> dict:
    columns = predictor_variables + [outcome_variable]
    data = df[columns].dropna()

    # 2. التحقق من حجم العينة الأدنى
    min_required = len(predictor_variables) * 10
    if len(data) < min_required:
        raise ValueError(
            f"Insufficient sample size. At least {min_required} observations recommended "
            f"(10 per predictor), but found {len(data)}."
        )

    X = data[predictor_variables]
    y = data[outcome_variable]

    # 1. تحويل المتغيرات التصنيفية إلى Dummy Variables
    X = pd.get_dummies(X, drop_first=True)

    # إضافة الثابت
    X = sm.add_constant(X)

    # 9. حساب VIF قبل الفيتينج
    vif_df = _calculate_vif(X)

    try:
        model = sm.OLS(y, X.astype(float)).fit()
    except Exception as e:
        raise ValueError(f"Linear regression fitting failed: {str(e)}")

    coefficients = pd.DataFrame(
        {
            "Variable": model.params.index,
            "Coefficient": model.params.values,
            "Standard Error": model.bse.values,  # 5. إضافة Standard Error
            "P-value": model.pvalues.values,
            "CI Lower": model.conf_int()[0].values,
            "CI Upper": model.conf_int()[1].values,
        }
    )

    # 7. استبعاد Intercept (const) من جدول النتائج النهائي
    coefficients = coefficients[coefficients["Variable"] != "const"].reset_index(drop=True)

    return {
        "model_type": "Linear Regression",
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "aic": float(model.aic),  # 4. إضافة AIC
        "bic": float(model.bic),  # 4. إضافة BIC
        "results": coefficients,
        "vif": vif_df,            # 9. إرجاع VIF
        "summary": model.summary().as_text(),
    }


def run_logistic_regression(
    df: pd.DataFrame,
    outcome_variable: str,
    predictor_variables: list
) -> dict:
    columns = predictor_variables + [outcome_variable]
    data = df[columns].dropna()

    # 2. التحقق من حجم العينة الأدنى
    min_required = len(predictor_variables) * 10
    if len(data) < min_required:
        raise ValueError(
            f"Insufficient sample size. At least {min_required} observations recommended "
            f"(10 per predictor), but found {len(data)}."
        )

    X = data[predictor_variables]
    y = data[outcome_variable]

    # 3. منع العمل على Outcome غير ثنائي
    unique_values = y.nunique()
    if unique_values != 2:
        raise ValueError(
            f"Logistic Regression requires a binary outcome variable (found {unique_values} unique values)."
        )

    # 1. تحويل المتغيرات التصنيفية إلى Dummy Variables
    X = pd.get_dummies(X, drop_first=True)

    # إضافة الثابت
    X = sm.add_constant(X)

    # 9. حساب VIF
    vif_df = _calculate_vif(X)

    # 8. التعامل مع Perfect Separation و أخطاء التقارب (Convergence)
    try:
        model = sm.Logit(y, X.astype(float)).fit(disp=False)
    except Exception as e:
        raise ValueError(
            f"Logistic regression failed (possibly due to perfect separation or severe multicollinearity): {str(e)}"
        )

    odds_ratios = np.exp(model.params)
    conf_int = np.exp(model.conf_int())

    results = pd.DataFrame(
        {
            "Variable": odds_ratios.index,
            "Odds Ratio": odds_ratios.values,
            "Standard Error": model.bse.values,
            "P-value": model.pvalues.values,
            "CI Lower": conf_int[0].values,
            "CI Upper": conf_int[1].values,
        }
    )

    # 7. استبعاد Intercept (const) من جدول النتائج
    results = results[results["Variable"] != "const"].reset_index(drop=True)

    # 6. إضافة تفسير الـ Odds Ratio
    results["Interpretation"] = np.where(
        results["Odds Ratio"] > 1,
        "Risk Factor",
        np.where(results["Odds Ratio"] < 1, "Protective Factor", "No Effect")
    )

    return {
        "model_type": "Logistic Regression",
        "pseudo_r_squared": float(model.prsquared),
        "aic": float(model.aic),  # 4. إضافة AIC
        "bic": float(model.bic),  # 4. إضافة BIC
        "results": results,
        "vif": vif_df,            # 9. إرجاع VIF
        "summary": model.summary().as_text(),
    }
