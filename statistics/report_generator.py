def interpret_p_value(p):

    if p < 0.05:

        return (
            "The result is statistically significant "
            "(p < 0.05)."
        )

    else:

        return (
            "No statistically significant difference "
            "was detected."
        )
