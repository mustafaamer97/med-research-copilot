import pandas as pd
from scipy.stats import shapiro


def analyze_dataset(file):
    # إعادة ضبط مؤشر قراءة الملف
    file.seek(0)
    filename = file.name.lower()

    # 1. محاولة قراءة الملف مع التعامل مع الأخطاء
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise ValueError(f"Failed to read dataset: {str(e)}")

    # معالجة الملفات الفارغة
    if df.empty:
        raise ValueError("Dataset is empty.")

    # تصنيف الأعمدة الأولي
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    # 2. اكتشاف الأعمدة الثنائية (Binary Variables)
    binary_columns = [
        col for col in df.columns if len(df[col].dropna().unique()) == 2
    ]

    # 3. كشف الأعمدة ذات القيم الثابتة (Constant Columns)
    constant_columns = [
        col for col in df.columns if df[col].nunique(dropna=True) <= 1
    ]

    # 8. اكتشاف المتغيرات الزمنية (Date Columns)
    date_columns = [col for col in df.columns if "date" in col.lower()]

    # 4. كشف القيم الشاذة (Outlier Detection - IQR)
    outliers = {}
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        count = int(((df[col] < lower) | (df[col] > upper)).sum())
        outliers[col] = count

    # تجميع التقرير الأساسي
    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percentage": df.isnull()
        .mean()
        .mul(100)
        .round(2)
        .to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "data_types": df.dtypes.astype(str).to_dict(),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "binary_columns": binary_columns,
        "constant_columns": constant_columns,
        "date_columns": date_columns,
        "outliers": outliers,
        "summary": df.describe().to_dict(),
    }

    # 6. اختبار التوزيع الطبيعي مع حماية Shapiro
    normality = {}
    for col in numeric_cols:
        data = df[col].dropna()
        if 3 <= len(data) <= 5000 and data.nunique() > 2:
            stat, p = shapiro(data)
            normality[col] = {
                "statistic": round(float(stat), 4),
                "p_value": round(float(p), 4),
                "normal": bool(p > 0.05),
            }

    report["normality"] = normality

    # 5. حساب مؤشر جودة البيانات (Dataset Quality Score)
    quality_score = 100
    if report["duplicates"] > 0:
        quality_score -= 10
    if max(report["missing_percentage"].values(), default=0) > 20:
        quality_score -= 20
    if len(report["constant_columns"]) > 0:
        quality_score -= 10
    report["quality_score"] = max(quality_score, 0)

    # 7. جاهزية الانحدار
    report["regression_ready"] = len(report["numeric_columns"]) >= 2

    # 9. ملخص صحة البيانات للواجهة
    report["dataset_health"] = {
        "rows": len(df),
        "variables": len(df.columns),
        "missing_cells": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
    }

    return df, report
