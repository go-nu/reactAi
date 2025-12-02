import flask
from dash import Dash, html, dcc, Input, Output
from .graphql_client import fetch_sales_view_all

flask_app = flask.Flask(__name__)

dash_app = Dash(
    __name__,
    server=flask_app,
    requests_pathname_prefix="/dashboard/",
    suppress_callback_exceptions=True,
)

def card_style():
    return {
        "flex": "1",
        "margin": "0 10px",
        "padding": "20px",
        "backgroundColor": "#F8F9FA",
        "borderRadius": "10px",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.15)",
        "textAlign": "center",
    }


dash_app.layout = html.Div(
    style={"padding": "20px"},
    children=[
        html.H2("매출 분석 대시보드", style={"textAlign": "center"}),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "30px",
            },
            children=[
                html.Div(id="total_sales", style=card_style(),  children =[html.H4('총매출액')]),
                html.Div(id="total_profit", style=card_style(), children =[html.H4('전체 순이익')]),
                html.Div(id="total_customers", style=card_style(),children =[html.H4('총 고객수')]),
                html.Div(id="total_qnty", style=card_style(), children =[html.H4('총 판매수량')])
            ]
        )
    ]
)


# Output: return, Input: parameter
@dash_app.callback(
    [
        Output("total_sales", "children"),
        Output("total_profit", "children"),
        Output("total_customers", "children"),
        Output("total_qnty", "children"),
    ],
    Input("total_sales", "value"),
)
def update_dashboard(value):
    df = fetch_sales_view_all()
    return (
        [html.H4("총매출액"),html.H2("1200원")],
        [html.H4("총매출액"), html.H2("1200원")],
        [html.H4("총매출액"), html.H2("1200원")],
        [html.H4("총매출액"), html.H2("1200원")],
    )
