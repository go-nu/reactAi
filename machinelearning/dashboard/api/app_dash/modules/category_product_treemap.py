import plotly.express as px

def category_product_graph(df, selected_category):
    if(selected_category == "categoryName"):
        treemap_option = "대분류"
        path = ["categoryName"]
    elif(selected_category == "productCategoryName"):
        treemap_option = "중분류"
        path = ["categoryName", "productCategoryName"]
    else:
        treemap_option = "소분류"
        path = ["categoryName", "productCategoryName", "productName"]

    treemap_df = df.groupby(path)["salesAmount"].sum().reset_index()
    fig_treemap = px.treemap(
        treemap_df,
        path = path,
        values = "salesAmount",
        color = "salesAmount",
    )

    return treemap_option, fig_treemap