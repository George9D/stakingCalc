import asyncio
from tokenClass import Token
from function import calcRewards
from forecastStakingAPR import calcRewardsNew
import inflationSchedules as ifs
from math import pow
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template
from function import convertPeriods

Evmos = Token("EVMOS", 2, ifs.evmosInflationSchedule, 145519475, 53.33, 0, 142905189, 634500)
Juno = Token("JUNO", 6, ifs.junoInflationSchedule, 46557652, 100, 0, 46396533, 77278)
Stars = Token("STARS", 0.04, ifs.starsInflationSchedule, 714676032, 35, 0, 715897972.8, 2198121.21)
Osmo = Token("OSMO", 1.18, ifs.osmosInflationSchedule, 217193183, 25, 0, 217861152, 495080.83)
Rebus = Token("REBUS", 0.2, ifs.rebusInflationSchedule, 22305908, 100, 0, 22305908, 160941.21)
#Atom = Token("ATOM", 12, ifs.atomInflationSchedule, 199242406, 100, 13140)
# sifchain = Token("ROWAN", 0.007, ifs.sifchainInflationSchedule, 955550000, 0, 0)
# tori = Token("TORI", 0.25, ifs.toriInflationSchedule, 15000000, 40, 0)

# secret -> future
# rebus - future (inflation schedule?!)

Chains = [Evmos, Juno, Stars, Osmo, Rebus]
print(Chains[0].get_token_name())

nbrTokenStaked = 100
stakingPeriod = 365
commission = 5
compoundingShare = 0



########################################################################################################################
#load_figure_template(["sketchy", "Flatly", "Minty", "cyborg", "vapor", "minty"])
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])
server = app.server

chains = ["EVMOS", "JUNO"]

heading = html.H4(
    "Staking Calculator", className="text-center bg-primary text-white p-2"
)

networks = html.Div(
    [
        dbc.Label("Network"),
        dcc.Dropdown(
            id="network",
            options=[
                {"label": chain, "value": chain}
                for chain in chains
            ],
            value=chains[0]
        ),
    ],
    className="dbc",
)

stakingAmountToken = html.Div(
    [dbc.Label("Staking Amount Token", html_for="stakingAmountToken"),
     dbc.Input(id="stakingAmountToken", type="number", value=0, debounce=True, readonly=False),
     ], className="dbc",
)

stakingAmountUSD = html.Div(
    [dbc.Label("Staking Amount USD", html_for="stakingAmountUSD"),
     dbc.Input(id="stakingAmountUSD", type="number", value=0, readonly=True),
     ], className="dbc",
)

slider = html.Div(
    [
        dbc.Label("Number of token staked", html_for="stakingSlider"),
        dcc.Slider(0, 10000, 1, value=1, id="stakingSlider", marks=None, tooltip={"placement": "bottom", "always_visible": False},),
    ], className="dbc my-2",
)

current_price = html.Div(
            [dbc.Label("Current Price USD", html_for="currentPrice"),
             dbc.Input(id="currentPrice", type="number", value=1, readonly=False, style={'float': 'right','margin': 'auto'}),
            ], className="dbc"
        )

future_price = html.Div(
            [dbc.Label("Future Price USD", html_for="futurePrice"),
             dbc.Input(id="futurePrice", type="number", value=1, debounce=True, readonly=False, style={'float': 'right','margin': 'auto'}),
            ], className="dbc"
        )

stakindDuration = html.Div(
    [dbc.Label("Staking Time (days)", html_for="stakindDuration"),
     dbc.Input(id="stakindDuration", type="number", value=100, debounce=True, readonly=False, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

commission = html.Div(
    [dbc.Label("Commission (%)", html_for="commission"),
     dbc.Input(id="commission", type="number", value=5, min=0, max=100, debounce=True, readonly=False, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

compound_period = html.Div(
    [dbc.Label("Compounding Period", html_for="compPeriod"),
     dcc.Dropdown(id="compPeriod",
                  options=[{"label": "daily", "value": "daily"},
                            {"label": "weekly", "value": "weekly"},
                            {"label": "monthly", "value": "monthly"},
                            {"label": "yearly", "value": "yearly"}],
                  value="yearly")
     #dbc.Input(id="compPeriod", type="number", value=0, readonly=False, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

compound_percentage = html.Div(
    [dbc.Label("Compounding Share (%)", html_for="compPercentage"),
    dbc.Input(id="compPercentage", type="number", value=0, min=0, max=100, debounce=True, readonly=False, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

stakingRewards = html.Div(
    [
        dbc.Label("Staking Rewards Token", html_for="stakingRewardsToken"),
        dbc.Input(id="stakingRewardsToken", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

stakingRewardsUSD = html.Div(
    [
        dbc.Label("Staking Rewards USD", html_for="stakingRewardsUSD"),
        dbc.Input(id="stakingRewardsUSD", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

roi = html.Div(
    [
        dbc.Label("ROI", html_for="roiToken"),
        dbc.Input(id="roiToken", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

roiUSD = html.Div(
    [
        dbc.Label("ROI USD", html_for="roiUSD"),
        dbc.Input(id="roiUSD", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

APR = html.Div(
    [
        dbc.Label("APR", html_for="apr"),
        dbc.Input(id="apr", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

APY = html.Div(
    [
        dbc.Label("APY", html_for="apy"),
        dbc.Input(id="apy", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

compRewards = html.Div(
    [
        dbc.Label("Compounded Rewards", html_for="compRewards"),
        dbc.Input(id="compRewards", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

takenOutRewards = html.Div(
    [
        dbc.Label("Claimed Staking Rewards", html_for="takenOutRewards"),
        dbc.Input(id="takenOutRewards", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

basicStakingRewards = html.Div(
    [
        dbc.Label("Rewards without compounding", html_for="basicStakingRewards"),
        dbc.Input(id="basicStakingRewards", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

compoundingRewards = html.Div(
    [
        dbc.Label("Add. rewards from compounding", html_for="compoundingRewards"),
        dbc.Input(id="compoundingRewards", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

increaseRewardsComp = html.Div(
    [
        dbc.Label("Add. rewards compounding (%)", html_for="increaseRewardsComp"),
        dbc.Input(id="increaseRewardsComp", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

stakingAmount = html.Div(
    [
        dbc.Label("Total Staking Amount", html_for="stakingAmount"),
        dbc.Input(id="stakingAmount", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

stakingValue = html.Div(
    [
        dbc.Label("Total Staking Value USD", html_for="stakingValue"),
        dbc.Input(id="stakingValue", type="text", value=0, readonly=True, style={'float': 'right','margin': 'auto'}),
    ], className="dbc"
)

# ----------------------------------------------------------------------------------------------------------------------

collapse = html.Div(
    [
        dbc.Button(
            "Advanced",
            id="advanced-button-in",
            color="primary",
            n_clicks=0,
            class_name="mb-2"
        ),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    commission
                                ],
                                xs=12, sm=12, md=12, lg=4, xl=4
                            ),
                            dbc.Col(
                                [
                                    compound_period
                                ],
                                xs=12, sm=12, md=12, lg=4, xl=4
                            ),
                            dbc.Col(
                                [
                                    compound_percentage
                                ],
                                xs=12, sm=12, md=12, lg=4, xl=4
                            ),
                        ], align="center", justify="center", className="py-3"
                    ),
                    ]
                )
            ),
            id="collapse",
            is_open=False,
            class_name="border-0"
        ),
    ]
)

collapse_out = html.Div(
    [
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    basicStakingRewards
                                ],
                                xs=12, sm=12, md=12, lg=4, xl=4
                            ),
                            dbc.Col(
                                [
                                    compoundingRewards
                                ],
                                xs=12, sm=12, md=12, lg=4, xl=4
                            ),
                            dbc.Col(
                                [
                                    increaseRewardsComp
                                ],
                                xs=12, sm=12, md=12, lg=4, xl=4
                            )
                        ], align="center", justify="center", className="py-3"
                    ),
                    ]
                )
            ),
            id="collapse-out",
            is_open=False,
            class_name="border-0"
        ),
    ]
)

graph = dbc.Card(dbc.CardBody([
     dcc.Graph(id="graph_1", figure={})
]))

graph2 = dbc.Card(dbc.CardBody([
     dcc.Graph(id="graph_2", figure={})
]))

graph3 = dbc.Card(dbc.CardBody([
     dcc.Graph(id="graph_3", figure={})
]))

#graph2 =  dcc.Graph(id="graph_2", figure={})

# ----------------------------------------------------------------------------------------------------------------------

card_in = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [networks],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                        dbc.Col(
                            [stakindDuration],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                    ], align="center", justify="center", className="py-3"
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [stakingAmountToken],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                        dbc.Col(
                            [stakingAmountUSD],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        )
                    ], align="center", justify="center", className="py-3"
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [slider],
                            xs=12, sm=12, md=12, lg=12, xl=12
                        ),
                    ], align="center", justify="center", className="pt-3"
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                current_price
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                        dbc.Col(
                            [
                                future_price
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        )
                    ], align="center", justify="center", className="py-3"
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [collapse],
                            width={"size": 12, "offset": 0},
                        ),
                    ], align="center", justify="center", className="pt-3"
                ),


                    ]
                )
    ], className="border border-0"
)

card_out = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                stakingAmount
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                        dbc.Col(
                            [
                                stakingValue
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                    ], align="center", justify="center", className="py-3"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [stakingRewards],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                        dbc.Col(
                            [stakingRewardsUSD],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        )
                    ], align="center", justify="center", className="py-3"
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                roi
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                        dbc.Col(
                            [
                                roiUSD
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        )
                    ], align="center", justify="center", className="py-3"
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                APR
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                        dbc.Col(
                            [
                                APY
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                    ], align="center", justify="center", className="py-3"
                ),

                dbc.Row(
                    [
                        collapse_out
                    ], align="center", justify="center", className="pt-5 mt-3"
                ),
                    ]
                )
    ], className="border border-0"
)

app.layout = html.Div(
    [
     heading,
     dbc.Row([
         dbc.Col(
             [card_in],
             align='start',
             xs=12, sm=10, md=9, lg=8, xl=6, xxl=4,
             className="p-3"
         ),
            dbc.Col([card_out],
            align='start',
            xs=12, sm=10, md=9, lg=8, xl=6, xxl=4,
            className="p-3")
        ], align="center", justify="center", className="px-3"),

     dbc.Row([
         dbc.Col(graph, xs=12, sm=10, md=9, lg=8, xl=12, xxl=4, className="p-3"),
         dbc.Col(graph2, xs=12, sm=10, md=9, lg=8, xl=12, xxl=4, className="p-3")
        ], align="center", justify="center", className="px-3"),
    dbc.Row([
         dbc.Col(graph3, xs=12, sm=10, md=9, lg=8, xl=12, xxl=8, className="p-3")
        ], align="center", justify="center", className="px-3")
     ]
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("advanced-button-in", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(ni, is_open):
    if ni:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-out", "is_open"),
    [Input("advanced-button-in", "n_clicks")],
    [State("collapse-out", "is_open")],
)
def toggle_collapse(ni, is_open):
    if ni:
        return not is_open
    return is_open

@app.callback(
    Output("stakingAmountToken", "value"),
    [Input("stakingSlider", "value")],
)
def update_staking_amount_slider(slider_value):
    #print(slider_value)
    return slider_value

@app.callback(
    Output("stakingSlider", "value"),
    [Input("stakingAmountToken", "value")],
)
def update_slider_staking_amount(input_value):
    #print(input_value)
    return input_value

@app.callback(
    Output("stakingAmountUSD", "value"),
    [Input("stakingAmountToken", "value"),
     Input("currentPrice", "value")]
)
def staking_amount_usd(stakingAmount, price):
    return stakingAmount * price


@app.callback(
    [Output("stakingRewardsToken", "value"),
     Output("stakingRewardsUSD", "value"),
     Output("roiToken", "value"),
     Output("roiUSD", "value"),
     Output("apr", "value"),
     Output("apy", "value"),
     Output("graph_1", "figure"),
     Output("graph_2", "figure"),
     Output("basicStakingRewards", "value"),
     Output("compoundingRewards", "value"),
     Output("stakingAmount", "value"),
     Output("stakingValue", "value"),
     Output("graph_3", "figure"),
     Output("increaseRewardsComp", "value")],
    [Input("network", "value"),
     Input("stakingAmountToken", "value"),
     Input("currentPrice", "value"),
     Input("futurePrice", "value"),
     Input("stakindDuration", "value"),
     Input("commission", "value"),
     Input("compPeriod", "value"),
     Input("compPercentage", "value")
    ]
)
def update_calc(network, stkAmount, curPrice, futPrice,
                stkDuration, commission, compPeriod, compPerctage):

    for t in Chains:
        if t.get_token_name() == network:
            chain = t
            print("T")
            break

    df = calcRewardsNew(chain, stkAmount, stkDuration, commission, compPeriod, compPerctage)

    print("***************")
    print(df[:10])
    print("***************")

    fig1 = px.line(
        data_frame=df,
        x='Date',
        y='cumStakingRewards',
        title="Cumulative Staking Rewards",
        hover_data=['Date', 'cumStakingRewards'],
        template='plotly_dark',
    )

    fig2 = px.line(
        data_frame=df,
        x='Date',
        y='APR',
        title="APR",
        hover_data=['Date', 'APR'],
        template='plotly_dark',
    )

    fig3 = px.line(
        data_frame=df,
        x='Date',
        y='stakingRewards',
        title="Daily Staking Rewards",
        hover_data=['Date', 'stakingRewards'],
        template='plotly_dark',
    )

    fig = [fig1, fig2, fig3]
    for f in fig:
        f.update_layout(
            title={
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

    fig1.update_layout(
        xaxis_title='Date',
        yaxis_title=f'{network}'
    )

    fig2.update_layout(
        xaxis_title='Date',
        yaxis_title='%'
    )

    fig3.update_layout(
        xaxis_title='Date',
        yaxis_title=f'{network}'
    )

    fig1.update_traces(line=dict(color='#375a7f'))
    fig2.update_traces(line=dict(color='#375a7f'))
    fig3.update_traces(line=dict(color='#375a7f'))
    #fig2.update_traces(line=dict(color='#FF00FF'))

    stkRwds = round(df['stakingRewards'].sum(), 2)
    stkRwdsUSD = round(stkRwds * futPrice, 2)
    roi = round(stkRwds / stkAmount * 100, 2)
    roiUSD = round((stkRwds * futPrice) / (stkAmount * curPrice) * 100, 2)
    # compRwds = round(df['compRewards'].sum(), 2)
    # takenOutRwds = round(df['takenOutRewards'].sum(), 2)
    basicStakingRwds = round(df['basicStakingRewards'].sum(), 2)
    compoundingRwds = round(stkRwds - basicStakingRwds, 2)
    apr = round((basicStakingRwds / stkDuration * 365) / stkAmount * 100, 2)
    apy = round((pow((1 + (apr / convertPeriods(compPeriod) / 100)), (convertPeriods(compPeriod))) - 1) * 100, 2)
    stakingAmount = round(stkAmount + stkRwds, 2)
    stakingValue = round(stakingAmount * futPrice, 2)

    # increase in staking rewards compared to rewards received without compounding in %
    increasedRoiComp = round(compoundingRwds / basicStakingRwds * 100, 2)
    increasedRoiComp = str(increasedRoiComp) + " %"

    stkRwds = str(stkRwds) + " " + chain.get_token_name()
    stkRwdsUSD = str(stkRwdsUSD) + " $"
    roi = str(roi) + " %"
    roiUSD = str(roiUSD) + " %"
    basicStakingRwds = str(basicStakingRwds) + " " + chain.get_token_name()
    compoundingRwds = str(compoundingRwds) + " " + chain.get_token_name()
    apr = str(apr) + " %"
    apy = str(apy) + " %"
    stakingAmount = str(stakingAmount) + " " + chain.get_token_name()
    stakingValue = str(stakingValue) + " $"

    return stkRwds, stkRwdsUSD, roi, roiUSD, apr, apy, fig1, fig2,basicStakingRwds, compoundingRwds,\
           stakingAmount, stakingValue, fig3, increasedRoiComp

#######################################################################################################

"""@app.callback(
    Output(component_id='graph_1', component_property='figure'),
    [Input(component_id='input_1', component_property='value')]
)
def update_graph(value):
    dff = df.copy()
    print("-------------------------------")
    print(value)

    dff['stakingRewards'] = dff['APR'] / 36500 * value

    fig = px.line(
        data_frame=dff,
        x='Date',
        y='stakingRewards',
        title="Daily Staking Rewards (STARS)",
        hover_data=['Date', 'stakingRewards'],
        template='plotly_dark'
    )

    return fig"""

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)


"""app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Staking Rewards Dashboard", style={"textAlign": "center"}),
            width={"size": 6, "offset": 1})
    ], align="center", justify="center"),

    dbc.Row([
        dbc.Col(
            [
                html.Br(),
                number_input
            ],
            width={"size": 4, "offset": 0},
            # xs=12, sm=12, md=12, lg=12, xl=6
        ),

        dbc.Col(
            [
                html.Br(),
                dcc.Graph(id='graph_1',
                          figure={})
            ],
            width={"size": 4, "offset": 0},
            # xs=12, sm=12, md=12, lg=12, xl=6
        ),

        dbc.Col(
            [
                html.Br(),
                dcc.Graph(id='graph_2',
                          figure=px.line(
                              data_frame=df,
                              x='Date',
                              y='cumStakingRewards',
                              title="Cumulative Staking Rewards (STARS)",
                              hover_data=['Date', 'cumStakingRewards'],
                              template='plotly_dark'
                          ))
            ],
            width={"size": 4, "offset": 0},
            # xs=12, sm=12, md=12, lg=12, xl=6
        )
    ], align="center", justify="center"),

    dbc.Row(
        [
            dbc.Col(
                [
                    html.Br(),
                    dcc.Graph(id='graph_3',
                              figure=px.line(
                                  data_frame=df,
                                  x='Date',
                                  y='APR',
                                  title="APR STARS",
                                  hover_data=['Date', 'APR'],
                                  template='plotly_dark'
                              ))
                ],
                width={"size": 8, "offset": 4},
                # xs=12, sm=12, md=12, lg=12, xl=6
            ),
        ]
    )
], fluid=True)"""


""" fig_layout = fig1["layout"]
    fig_layout["yaxis"]["gridcolor"] = "#FF00FF"
    fig_layout["xaxis"]["gridcolor"] = "#FF00FF"
"""


"""
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                compRewards
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                        dbc.Col(
                            [
                                takenOutRewards
                            ],
                            xs=12, sm=12, md=6, lg=6, xl=6
                        ),
                    ], align="center", justify="center", className="py-3"
                ),
"""