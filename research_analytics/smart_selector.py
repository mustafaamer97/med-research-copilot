def auto_select_group_comparison_test(
    df,
    report,
    group_col,
    outcome_col,
    paired=False
):

    # 1. التحقق من وجود الأعمدة في DataFrame
    if group_col not in df.columns:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "confidence": "Low",
            "warning": None,
            "reason": f"Group column '{group_col}' not found."
        }

    if outcome_col not in df.columns:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "confidence": "Low",
            "warning": None,
            "reason": f"Outcome column '{outcome_col}' not found."
        }

    # التأكد أن المتغير الناتج رقمي
    if outcome_col not in report.get("numeric_columns", []):
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "confidence": "Low",
            "warning": None,
            "reason": "Outcome variable must be numeric."
        }

    # 2. التحقق من الصفوف الصالحة بعد حذف المفقودات (Missing Values)
    valid_rows = df[[group_col, outcome_col]].dropna()
    if len(valid_rows) < 10:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "confidence": "Low",
            "warning": None,
            "reason": "Insufficient complete observations (fewer than 10 valid rows)."
        }

    # 3. التحقق من عدد المجموعات وحجمها
    groups = valid_rows[group_col].nunique()
    if groups < 2:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "confidence": "Low",
            "warning": None,
            "reason": "At least two groups are required for comparison."
        }

    group_sizes = valid_rows.groupby(group_col)[outcome_col].count()
    if group_sizes.min() < 5:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "confidence": "Low",
            "warning": None,
            "reason": "One or more groups contain fewer than 5 non-null observations."
        }

    # 4. فحص عدم توازن المجموعات (Group Imbalance Check)
    warning = None
    imbalance_ratio = group_sizes.max() / group_sizes.min()
    if imbalance_ratio > 5:
        warning = f"Groups are highly imbalanced (Ratio {imbalance_ratio:.1f}:1). Interpret results with caution."

    # 5. التحقق من التوزيع الطبيعي ومستوى الثقة
    normality_dict = report.get("normality", {})
    if outcome_col in normality_dict:
        normal = normality_dict[outcome_col].get("normal", False)
        confidence = "High"
    else:
        normal = False  # Conservative assumption
        confidence = "Moderate"

    # 6. تحديد الاختبار (Paired vs Independent)

    # --- البيانات المزدوجة (Paired / Repeated Measures) ---
    if paired:
        if groups == 2:
            if normal:
                return {
                    "test": "Paired t-test",
                    "posthoc": None,
                    "effect_size": "Cohen's d (paired)",
                    "confidence": confidence,
                    "warning": warning,
                    "reason": "Two paired groups with normal distribution."
                }
            return {
                "test": "Wilcoxon Signed-Rank Test",
                "posthoc": None,
                "effect_size": "Matched-pairs Rank-Biserial Correlation",
                "confidence": confidence,
                "warning": warning,
                "reason": "Two paired groups with non-normal distribution."
            }
        else:  # groups > 2
            if normal:
                return {
                    "test": "Repeated Measures ANOVA",
                    "posthoc": "Bonferroni paired t-tests",
                    "effect_size": "Partial Eta Squared",
                    "confidence": confidence,
                    "warning": warning,
                    "reason": "Multiple paired groups with normal distribution."
                }
            return {
                "test": "Friedman Test",
                "posthoc": "Pairwise Wilcoxon with Bonferroni correction",
                "effect_size": "Kendall's W",
                "confidence": confidence,
                "warning": warning,
                "reason": "Multiple paired groups with non-normal distribution."
            }

    # --- البيانات المستقلة (Independent Groups) ---
    if groups == 2:
        if normal:
            return {
                "test": "Independent t-test",
                "posthoc": None,
                "effect_size": "Cohen's d",
                "confidence": confidence,
                "warning": warning,
                "reason": "Two groups with normal distribution."
            }
        return {
            "test": "Mann-Whitney U Test",
            "posthoc": None,
            "effect_size": "Rank-Biserial Correlation",
            "confidence": confidence,
            "warning": warning,
            "reason": "Two groups with non-normal distribution."
        }

    # أكثر من مجموعتين مستقليين
    if normal:
        return {
            "test": "ANOVA",
            "posthoc": "Tukey HSD",
            "effect_size": "Eta Squared",
            "confidence": confidence,
            "warning": warning,
            "reason": "Multiple groups with normal distribution."
        }

    return {
        "test": "Kruskal-Wallis",
        "posthoc": "Pairwise Mann-Whitney (Dunn's test)",
        "effect_size": "Epsilon Squared",
        "confidence": confidence,
        "warning": warning,
        "reason": "Multiple groups with non-normal distribution."
    }
