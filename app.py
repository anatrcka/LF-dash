import dash
import dash_core_components as dcc
import dash_html_components as html
import LFs.LFs as LFs
import LFs.opt as opt
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    title="Luminosity functions",
    external_stylesheets=[
        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css"
    ],
)
server = app.server

path_obs_data = './LFs/'

fig_uv = make_subplots(rows=1, cols=2)
fig_opt = make_subplots(rows=3, cols=3)
fig_ir = make_subplots(rows=2, cols=2)

tabs_styles = {"height": "44px", "width": "100vw"}
tab_style = {
    "borderBottom": "2px solid #5a1459",
    "padding": "6px",
    "fontWeight": "bold",
}

tab_selected_style_uv = {
    "borderBottom": "1px solid #d2bbe8",
    "borderTop": "2px solid #5a1459",
    "borderLeft": "2px solid #5a1459",
    "borderRight": "2px solid #5a1459",
    "backgroundColor": "#d2bbe8",
    "color": "white",
    "padding": "6px",
    "fontWeight": "bold",
}

tab_selected_style_opt = {
    "borderBottom": "1px solid #7eb5dc",
    "borderTop": "2px solid #5a1459",
    "borderLeft": "2px solid #5a1459",
    "borderRight": "2px solid #5a1459",
    "backgroundColor": "#7eb5dc",
    "color": "white",
    "padding": "6px",
    "fontWeight": "bold",
}
tab_selected_style_ir = {
    "borderBottom": "1px solid #c7696e",
    "borderTop": "2px solid #5a1459",
    "borderLeft": "2px solid #5a1459",
    "borderRight": "2px solid #5a1459",
    "backgroundColor": "#c7696e",
    "color": "white",
    "padding": "6px",
    "fontWeight": "bold",
}
app.layout = html.Div(
    [
        html.Div(
            children=[
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="two columns div-user-controls",
                            children=[
                                html.H6(
                                    "Recipes",
                                    style={
                                        "color": "darkmagenta",
                                        "fontWeight": "bold",
                                    },
                                ),
                                dcc.Checklist(
                                    id="rec",
                                    options=[
                                        {"label": k[1], "value": k[0]}
                                        for k in opt.rec_l.items()
                                    ],
                                    inputStyle={
                                        "cursor": "pointer",
                                        "width": "15px",
                                        "height": "15px",
                                        "filter": "invert(0%) hue-rotate(90deg) brightness(1.0)",
                                    },
                                    labelStyle={"display": "block", "color": "white",},
                                ),
                            ],
                        ),
                        html.Div(
                            className="two columns div-for-charts bg-grey",
                            children=[
                                html.H6(
                                    "Apertures",
                                    style={
                                        "color": "darkmagenta",
                                        "fontWeight": "bold",
                                    },
                                ),
                                dcc.Checklist(
                                    id="aper",
                                    options=[
                                        {"label": k[1], "value": k[0]}
                                        for k in opt.apers_l.items()
                                    ],
                                    value=[],
                                    inputStyle={
                                        "cursor": "pointer",
                                        "width": "15px",
                                        "height": "15px",
                                        "filter": "invert(0%) hue-rotate(90deg) brightness(1)",
                                    },
                                    labelStyle={
                                        "display": "block",
                                        "box": dict(color="darkmagenta"),
                                        "color": "white",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            className="two columns div-for-charts bg-grey",
                            children=[
                                html.H6(
                                    "Orientations",
                                    style={
                                        "color": "darkmagenta",
                                        "fontWeight": "bold",
                                    },
                                ),
                                dcc.Checklist(
                                    id="ori",
                                    options=[
                                        {"label": k[1], "value": k[0]}
                                        for k in opt.oris_l.items()
                                    ],
                                    value=[],
                                    inputStyle={
                                        "cursor": "pointer",
                                        "width": "15px",
                                        "height": "15px",
                                        "filter": "invert(0%) hue-rotate(90deg) brightness(1)",
                                    },
                                    labelStyle={"display": "block", "color": "white",},
                                ),
                            ],
                        ),
                        html.Div(
                            className="two columns div-for-charts bg-grey",
                            children=[
                                html.H6(
                                    "Simulations",
                                    style={
                                        "color": "darkmagenta",
                                        "fontWeight": "bold",
                                    },
                                ),
                                dcc.Checklist(
                                    id="sim",
                                    inputStyle={
                                        "cursor": "pointer",
                                        "width": "15px",
                                        "height": "15px",
                                        "filter": "invert(0%) hue-rotate(90deg) brightness(1)",
                                    },
                                    labelStyle={"display": "block", "color": "white",},
                                ),
                            ],
                        ),
                        html.Div(
                            className="two columns div-for-charts bg-grey",
                            children=[
                                html.H3(
                                    "Galaxy luminosity functions",
                                    style={"color": "white", "fontWeight": "bold",},
                                ),
                            ],
                        ),
                    ],
                    style={
                        "background-image": 'url("/assets/Picture1.png")',
                        "background-size": "100vw",
                        "background-repeat": "no-repeat",
                    },
                ),
            ],
            style={"width": "100vw"},
        ),
        dcc.Tabs(
            id="tabs",
            value="uv",
            children=[
                dcc.Tab(
                    label="UV",
                    value="uv",
                    children=[
                        html.Div(
                            className="twelve columns div-for-charts bg-grey",
                            children=[
                                dcc.Graph(
                                    id="LF_uv",
                                    figure=fig_uv,
                                    config={"displayModeBar": True},
                                    animate=True,
                                )
                            ],
                            style={"height": "100%", "width": "100%"},
                        ),
                    ],
                    style=tab_style,
                    selected_style=tab_selected_style_uv,
                ),
                dcc.Tab(
                    label="Optical + NIR",
                    value="opt",
                    children=[
                        html.Div(
                            className="twelve columns div-for-charts bg-grey",
                            children=[
                                dcc.Graph(
                                    id="LF_opt",
                                    figure=fig_opt,
                                    config={"displayModeBar": True},
                                    animate=True,
                                )
                            ],
                            style={"height": "100%", "width": "100%"},
                        ),
                    ],
                    style=tab_style,
                    selected_style=tab_selected_style_opt,
                ),
                dcc.Tab(
                    label="IR",
                    value="ir",
                    children=[
                        html.Div(
                            className="twelve columns div-for-charts bg-grey",
                            children=[
                                dcc.Graph(
                                    id="LF_ir",
                                    figure=fig_ir,
                                    config={"displayModeBar": True},
                                    animate=True,
                                )
                            ],
                            style={"height": "100%", "width": "100%"},
                        ),
                    ],
                    style=tab_style,
                    selected_style=tab_selected_style_ir,
                ),
            ],
            style=tabs_styles,
        ),
    ]
)


@app.callback(Output("sim", "options"), [Input("rec", "value")])
def set_rec(selected_recs):
    if selected_recs:
        if len(selected_recs) == 1:
            return [{"label": k, "value": k} for k in opt.rec[selected_recs[0]]]
        elif len(selected_recs) == 2:
            return [{"label": k, "value": k} for k in opt.rec["tau11_fdust1_best_apers"]]

    else:
        return []


@app.callback(Output("sim", "value"), [Input("sim", "options")])
def set_rec_2(option_sims):
    return []


@app.callback(
    Output("LF_uv", "figure"),
    Output("LF_opt", "figure"),
    Output("LF_ir", "figure"),
    [
        Input("sim", "value"),
        Input("rec", "value"),
        Input("aper", "value"),
        Input("ori", "value"),
        Input("tabs", "value"),
    ],
)
def update_graph(
    selected_sims, selected_recs, selected_apers, selected_oris, selected_tab
):
    Budavari05 = LFs.budavari05(path_obs_data)
    Wyder05 = LFs.wyder05(path_obs_data)
    Driver12_UV = LFs.driver12uv(path_obs_data)
    fig_uv = LFs.plot_uv_obs(Budavari05,Wyder05,Driver12_UV)
    
    Loveday12 = LFs.loveday12(path_obs_data)
    Driver12 = LFs.driver12(path_obs_data)
    Hill10 = LFs.hill10(path_obs_data)

    fig_opt = LFs.plot_opt_obs(Loveday12,Driver12,Hill10)
    
    Dunne11 = LFs.dunne11(path_obs_data)
    Negrello14 = LFs.negrello14(path_obs_data)
    Marchetti16 = LFs.marchetti16(path_obs_data)
    fig_ir = LFs.plot_ir_obs(Dunne11,Negrello14,Marchetti16)

    LuF_TNG_1_allz = LFs.read_sim1L(path_obs_data)
    LuF_TNG_2_allz = LFs.read_sim2L(path_obs_data)
    
    
    if selected_tab == "uv":
        fig_uv = LFs.plot_uv(selected_sims, selected_recs, selected_apers, selected_oris,Budavari05, Wyder05, Driver12_UV, LuF_TNG_1_allz, LuF_TNG_2_allz)

    if selected_tab == "opt":
        fig_opt = LFs.plot_opt(selected_sims, selected_recs, selected_apers, selected_oris,Loveday12,Driver12,Hill10, LuF_TNG_1_allz, LuF_TNG_2_allz)

    if selected_tab == "ir":
        fig_ir = LFs.plot_ir(selected_sims, selected_recs, selected_apers, selected_oris,Dunne11,Negrello14,Marchetti16,LuF_TNG_1_allz, LuF_TNG_2_allz)

    return fig_uv, fig_opt, fig_ir


if __name__ == "__main__":
    app.run_server(debug=True)
