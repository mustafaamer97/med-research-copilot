def auto_select_group_comparison_test(
    df,
    report,
    group_col,
    outcome_col
):
    # 1. التحقق من وجود الأعمدة في Dataframe
    if group_col not in df.columns:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "reason": f"Group column '{group_col}' not found."
        }
        
    if outcome_col not in df.columns:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "reason": f"Outcome column '{outcome_col}' not found."
        }

    # التأكد أن المتغير الناتج رقمي
    if outcome_col not in report.get("numeric_columns", []):
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "reason": "Outcome variable must be numeric."
        }

    # 2. التحقق من عدد المجموعات
    groups = df[group_col].dropna().nunique()
    if groups < 2:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "reason": "At least two groups are required for comparison."
        }

    # 3. التحقق من حجم العينة داخل كل مجموعة (مهم طبعاً للأبحاث الطبية)
    group_sizes = df.groupby(group_col)[outcome_col].count()
    if group_sizes.min() < 5:
        return {
            "test": None,
            "posthoc": None,
            "effect_size": None,
            "reason": "One or more groups contain fewer than 5 non-null observations."
        }

    # 4. التعامل مع غياب تقرير التوزيع الطبيعي (Conservative approach)
    normal = False
    normality_dict = report.get("normality", {})
    if outcome_col in normality_dict:
        normal = normality_dict[outcome_col].get("normal", False)

    # 5 & 6. تحديد الاختبار مع Post-hoc و Effect Size

    # مجموعتان
    if groups == 2:
        if normal:
            return {
                "test": "Independent t-test",
                "posthoc": None,
                "effect_size": "Cohen's d",
                "reason": "Two groups with normal distribution."
            }

        return {
            "test": "Mann-Whitney U Test",
            "posthoc": None,
            "effect_size": "Rank-Biserial Correlation",
            "reason": "Two groups with non-normal distribution."
        }

    # أكثر من مجموعتين
    if groups > 2:
        if normal:
            return {
                "test": "ANOVA",
                "posthoc": "Tukey HSD",
                "effect_size": "Eta Squared",
                "reason": "Multiple groups with normal distribution."
            }

        return {
            "test": "Kruskal-Wallis",
            "posthoc": "Pairwise Mann-Whitney (Dunn's test)",
            "effect_size": "Epsilon Squared",
            "reason": "Multiple groups with non-normal distribution."
        }

    return {
        "test": None,
        "posthoc": None,
        "effect_size": None,
        "reason": "Unable to determine appropriate test."
    }
