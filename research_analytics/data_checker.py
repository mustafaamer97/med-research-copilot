import pandas as pd
from scipy.stats import shapiro


def analyze_dataset(file):

    # إعادة ضبط مؤشر قراءة الملف لضمان البدء من البداية
    file.seek(0)

    filename = file.name.lower()

    # محاولة قراءة الملف مع التعامل الآمن مع الأخطاء
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise ValueError(
            f"Failed to read dataset: {str(e)}"
        )

    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": (
            df.isnull()
            .sum()
            .to_dict()
        ),
        "missing_percentage": (
            df.isnull()
            .mean()
            .mul(100)
            .round(2)
            .to_dict()
        ),
        "duplicates": int(df.duplicated().sum()),
        "data_types": df.dtypes.astype(str).to_dict(),
        "numeric_columns": (
            df.select_dtypes(include="number")
            .columns
            .tolist()
        ),
        "categorical_columns": (
            df.select_dtypes(exclude="number")
            .columns
            .tolist()
        ),
        "summary": df.describe().to_dict(),
    }

    # اختبار التوزيع الطبيعي
    normality = {}
    numeric_cols = report["numeric_columns"]

    for col in numeric_cols:
        data = df[col].dropna()

        # Shapiro لا يفضل العينات الضخمة جداً
        if len(data) >= 3 and len(data) <= 5000:
            stat, p = shapiro(data)
            normality[col] = {
                "statistic": round(float(stat), 4),
                "p_value": round(float(p), 4),
                "normal": bool(p > 0.05),
            }

    report["normality"] = normality

    return df, report
