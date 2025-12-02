def bring_card_data(df):
    return {
        "total_sales": round(df["salesAmount"].sum()),
        "total_profit": round(df["netProfit"].sum()),
        "total_customers": df["customerName"].nunique(),
        "total_qnty": df["quantity"].sum()
    }