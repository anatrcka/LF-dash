import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import sys
import pickle
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import opt
from glob import glob as _glob

def glob(*argv, **kwargv):

    return sorted(_glob(*argv, **kwargv))

# def L_to_Mab(L, lam):  # in L_sun, microns
#     pc = 3.085677581e16
#     nu = opt.speed_c()/(lam*1e-6)
#     return -2.5 * np.log10(L * opt.L_Sun()/(4*np.pi*(10*pc)**2 * nu  * 3631 * 1e-26))

def Mab_to_L(M, lam):  # in mag, microns
    pc = 3.085677581e16
    nu = opt.speed_c()/(lam*1e-6)
    return nu * (4*np.pi*(10*pc)**2) * 3631 * 1e-26 * 10**(-0.4 * M) / opt.L_Sun()

#  ------------- UV ---------------------------
def budavari05(path_obs_data):
    # Budavari et al. 2005

    Budavari05 = {}
    for band in ["GALEX_FUV", "GALEX_NUV"]:    

        Budavari05[band] = pd.read_csv(path_obs_data + "Budavari05_{}.csv".format(band.replace('GALEX_','')),
                                    header=None, sep=';')
        Budavari05[band] = Budavari05[band].rename(columns={0: "M", 1: "MF", 2: "dMF_u", 3:'dMF_l'})
        Budavari05[band].M = Budavari05[band].M - 5 * np.log10(0.7/opt.TNG_h()) 
        Budavari05[band].MF = Budavari05[band].MF * (0.7/opt.TNG_h()) ** 3 
        Budavari05[band]['dMF_u'] = Budavari05[band]['dMF_u']*(0.7/opt.TNG_h())**3-Budavari05[band]['MF']
        Budavari05[band]['dMF_l'] = Budavari05[band]['MF']-Budavari05[band]['dMF_l']*(0.7/opt.TNG_h())**3
    return Budavari05


def wyder05(path_obs_data):
    # UV mag from Wyder et al. 2005

    Wyder05 = {}
    for band  in ["GALEX_FUV", "GALEX_NUV"]:    
        Wyder05[band] = pd.read_csv(path_obs_data + "Wyder05_{}.csv".format(band.replace('GALEX_','')),
                                    header=None, sep=';')
        Wyder05[band] = Wyder05[band].rename(columns={0: "M", 1: "log_MF", 2: "log_dMF_u", 3:'log_dMF_l'})
        Wyder05[band].M = Wyder05[band].M - 5 * np.log10(0.7/opt.TNG_h()) 
        Wyder05[band].log_MF = Wyder05[band].log_MF + np.log10((0.7/opt.TNG_h()) ** 3)    
        Wyder05[band]['dMF_u'] = 10**Wyder05[band]['log_dMF_u']*(0.7/opt.TNG_h())**3-10**Wyder05[band]['log_MF']
        Wyder05[band]['dMF_l'] = 10**Wyder05[band]['log_MF']-10**Wyder05[band]['log_dMF_l']*(0.7/opt.TNG_h())**3
    return Wyder05


def driver12uv(path_obs_data):
    # UV mag from Driver et al. 2012
    
    Driver12_UV = {}
    for band in ['GALEX_FUV', 'GALEX_NUV']:        
        Driver12_UV[band] = pd.read_csv(path_obs_data + "Driver12_{}.csv".format(band.replace('GALEX_','')),
                                    header=None, sep=';')
        Driver12_UV[band] = Driver12_UV[band].rename(columns={0: "M", 1: "log_MF", 2: "log_dMF_u", 3:'log_dMF_l'})
        Driver12_UV[band].M = Driver12_UV[band].M + 5 * np.log10(opt.TNG_h()) 
        Driver12_UV[band].log_MF = Driver12_UV[band].log_MF + np.log10(opt.TNG_h() ** 3/0.5)    
        Driver12_UV[band]['dMF_u'] = 10**Driver12_UV[band]['log_dMF_u']*opt.TNG_h()**3/0.5-10**Driver12_UV[band]['log_MF']
        Driver12_UV[band]['dMF_l'] = 10**Driver12_UV[band]['log_MF']-10**Driver12_UV[band]['log_dMF_l']*opt.TNG_h()**3/0.5

    return Driver12_UV


# -------------------- Optical -----------

def hill10(path_obs_data):
    # Hill et al. 2010
    
    Hill10 = {}
    for band,con in zip(
        ["UKIDSS_K", "UKIDSS_H", "UKIDSS_J", "UKIDSS_Y"],
        [1.9,1.38,0.94,0.63]
    ):
        Hill10[band] = pd.read_csv(
            path_obs_data + "Hill10_{}.csv".format(band.replace('UKIDSS_','')), header=None, sep=';')
        Hill10[band] = Hill10[band].rename(columns={0: "M", 1: "log_MF", 2: "log_dMF_u", 3:'log_dMF_l'})
        Hill10[band].M = Hill10[band].M + 5 * np.log10(opt.TNG_h()) + con
        Hill10[band].log_MF = Hill10[band].log_MF + np.log10(opt.TNG_h() ** 3/0.5)    
        Hill10[band]['dMF_u'] = 10**Hill10[band]['log_dMF_u']*opt.TNG_h()**3/0.5-10**Hill10[band]['log_MF']
        Hill10[band]['dMF_l'] = 10**Hill10[band]['log_MF']-10**Hill10[band]['log_dMF_l']*opt.TNG_h()**3/0.5
    return Hill10


def loveday12(path_obs_data):
    # Loveday et al. 2012
    
    Loveday12 = {}
    for band in ["SDSS_u", "SDSS_g", "SDSS_r", "SDSS_i", "SDSS_z"]:
        Loveday12[band] = pd.read_csv(
            path_obs_data + "Loveday12_{}.csv".format(band), header=None
        )
        Loveday12[band] = Loveday12[band].rename(columns={0: "M", 1: "MF"})
        Loveday12[band].M = Loveday12[band].M + 5 * np.log10(opt.TNG_h())
        Loveday12[band].MF = Loveday12[band].MF * opt.TNG_h() ** 3
    return Loveday12


def driver12(path_obs_data):
    # Driver et al. 2012
    
    Driver12 = {}
    for band in ["SDSS_u", "SDSS_g", "SDSS_r", "SDSS_i", "SDSS_z" ,"UKIDSS_Y", "UKIDSS_J","UKIDSS_H", "UKIDSS_K"]:
        Driver12[band] = pd.read_csv(path_obs_data +'Driver12_{}.csv'.format(band.replace("UKIDSS_","")), header=None, sep=';')
        Driver12[band] = Driver12[band].rename(columns={0: "M", 1: "log_MF", 2: "log_dMF_u", 3:'log_dMF_l'})
        Driver12[band].M = Driver12[band].M + 5 * np.log10(opt.TNG_h())
        Driver12[band].log_MF = Driver12[band].log_MF + np.log10(opt.TNG_h() ** 3/0.5)
        Driver12[band]['dMF_u'] = 10**Driver12[band]['log_dMF_u']*opt.TNG_h()**3/0.5-10**Driver12[band]['log_MF']
        Driver12[band]['dMF_l'] = 10**Driver12[band]['log_MF']-10**Driver12[band]['log_dMF_l']*opt.TNG_h()**3/0.5
    return Driver12


# -------------------- IR -----------

def dunne11(path_obs_data):
    # SPIRE250 from Dunne et al. 2011
    Dunne11 = pickle.load( open( path_obs_data + "Dunne11", "rb" ) )
    return Dunne11

def negrello14(path_obs_data):
    # SPIRE350 from Negrello et al. 2014
    Negrello14 = pickle.load( open( path_obs_data + "Negrello14", "rb" ) )
    return Negrello14

def marchetti16(path_obs_data):
    # SPIRE and TIR from Marchetti et al. 2011
    Marchetti16 = pickle.load( open( path_obs_data + "Mar16", "rb" ) )
    return Marchetti16

# -------------------- SIMS ----------------
# def read_sim1M(path_obs_data):
#     MagF_TNG_1_allz = pd.read_pickle(path_obs_data+'MagF_TNG_1_allz')
#     return MagF_TNG_1_allz


# def read_sim2M(path_obs_data):
#     MagF_TNG_2_allz = pd.read_pickle(path_obs_data+'MagF_TNG_2_allz')
#     return MagF_TNG_2_allz

def read_sim1L(path_obs_data):
    LumF_TNG_1_allz = pd.read_pickle(path_obs_data+'LF_TNG_1_allb_allz')
    return LumF_TNG_1_allz


def read_sim2L(path_obs_data):
    LumF_TNG_2_allz = pd.read_pickle(path_obs_data+'LF_TNG_2_allb_allz')
    return LumF_TNG_2_allz



# ------------------ plots ----------------------

def plot_uv_obs(Budavari05, Wyder05, Driver12_UV):
    fig_uv = make_subplots(rows=1, cols=2, shared_yaxes=True,shared_xaxes=True, vertical_spacing=0.001, horizontal_spacing=0.001)

    for br, band in enumerate(["GALEX_FUV", "GALEX_NUV"]):
        lamb = opt.pivot()[1][opt.pivot()[1].index==band].values[0][0]
        trace_B05 = go.Scatter(
            x=np.log10(Mab_to_L(Budavari05[band]["M"],lamb)),
            y=Budavari05[band]["MF"]*2.5,
            error_y=dict(
                        type="data",
                        symmetric=False,
                        array=Budavari05[band].dMF_u*2.5,
                        arrayminus=Budavari05[band].dMF_l*2.5,
                        thickness=0.5,
                    ),
            mode="markers",
            marker=dict(
                color="gold", symbol='triangle-down', size=8, opacity=1, line=dict(width=0.5, color="black")
            ),
            name="Budavari et al. 2005",
            showlegend=True if band == "GALEX_FUV" else False,
            hoverinfo="none",
            hoveron="points",
        )
                    

        trace_W05 = go.Scatter(
            x=np.log10(Mab_to_L(Wyder05[band]["M"],lamb)),
            y=10 ** (Wyder05[band]["log_MF"])*2.5,
            error_y=dict(
                        type="data",
                        symmetric=False,
                        array=Wyder05[band].dMF_u*2.5,
                        arrayminus=Wyder05[band].dMF_l*2.5,
                        thickness=0.5,
                    ),
            mode="markers",
            marker=dict(
                color="red", size=8, opacity=1, line=dict(width=0.5, color="black")
            ),
            showlegend=True if band == "GALEX_FUV" else False,
            hoverinfo="none",
            hoveron="points",
            name="Wyder et al. 2005",
        )

        trace_D12 = go.Scatter(
            x=np.log10(Mab_to_L(Driver12_UV[band]["M"],lamb)),
            y=10 ** (Driver12_UV[band]["log_MF"])*2.5,
            error_y=dict(
                        type="data",
                        symmetric=False,
                        array=Driver12_UV[band].dMF_u*2.5,
                        arrayminus=Driver12_UV[band].dMF_l*2.5,
                        thickness=0.5,
                    ),
            name="Driver et al. 2012",
            mode="markers",
            marker=dict(
                color="lime", size=8, symbol='diamond', opacity=1, line=dict(width=0.5, color="black")
            ),
            showlegend=True if band == "GALEX_FUV" else False,
            hoverinfo="none",
            hoveron="points",
        )

        fig_uv.append_trace(trace_B05, 1, br + 1)
        fig_uv.append_trace(trace_W05, 1, br + 1)
        fig_uv.append_trace(trace_D12, 1, br + 1)

        fig_uv.add_annotation(
            x=10,
            y=-1.5,
            xref="x" + str(br + 1),
            yref="y" + str(br + 1),
            text=band.replace("_", " "),
            showarrow=False,
        )
    fig_uv.update_xaxes(
        linecolor="#000000",
        showgrid=False,
        linewidth=1,
        mirror=True,
        ticks="inside",
        title="log L [ L"
        + u"\u2299"
        +"]",
    )

    fig_uv.update_yaxes(
        linecolor="#000000",
        showgrid=False,
        linewidth=1,
        mirror=True,
        type="log",
        ticks="inside",
        range=[-5.9,-1],
        
    )
    fig_uv["layout"].update(
        autosize=False,
        height=539,
        width=863.3333333333334,
        margin=dict(
        l=70,
        r=5,
        b=70,
        t=100,
        pad=0
        ),
        yaxis_title=u"\u03D5"
        + "[Mpc"
        + u"\u207B"
        + u"\u00B3"
        + "dex"
        + u"\u207B"
        + u"\u00B9"
        + "]",
        plot_bgcolor="white",
        font=dict(size=13),
        legend=dict(orientation="h", yanchor="top", y=1.205, xanchor="left", x=0.),
        hovermode="x",
        
    )
    return fig_uv


def plot_uv(selected_sims, selected_recs, selected_apers, selected_oris,Budavari05, Wyder05, Driver12_UV, LuF_TNG_1_allz, LuF_TNG_2_allz):
    fig_uv = plot_uv_obs(Budavari05, Wyder05, Driver12_UV)
    for br, bandt in enumerate(["GALEX_FUV", "GALEX_NUV"]):
        band = "F_" + bandt
        br_tot = 0
        if selected_sims and selected_recs and selected_apers and selected_oris:
            for j, sim in enumerate(selected_sims):
                if sim == "TNG50 1":
                    data = LuF_TNG_1_allz
                elif sim == "TNG50 2":
                    data = LuF_TNG_2_allz
                for i, rec in enumerate(selected_recs):
                    for k, aper in enumerate(selected_apers):
                        for l, ori in enumerate(selected_oris):
                            xx = data[band][rec][aper][ori][0][
                                data[band][rec][aper][ori][2] > 0
                            ]
                            yy = data[band][rec][aper][ori][2][
                                data[band][rec][aper][ori][2] > 0
                            ]
                            yyE = np.array(data[band][rec][aper][ori][3])
                            yyE = yyE[data[band][rec][aper][ori][2] > 0]
                            
                            yyU = list(yy + yyE)
                            yyD = list(yy - yyE)

                            brg = np.array(data[band][rec][aper][ori][4])
                            brg = brg[data[band][rec][aper][ori][2] > 0]

                            traceE = go.Scatter(
                                x=list(xx) + list(xx[::-1]),
                                y=yyU + yyD[::-1],
                                fill="toself",
                                fillcolor=opt.colors_rgba[aper] if sim=="TNG50 1" else opt.colors_rgba_2[aper],
                                line=dict(color="rgba(7, 68, 0, 1)"),
                                hoverinfo="skip",
                                mode="none",
                                showlegend=False,
                            )
                            trace = go.Scatter(
                                x=xx,
                                y=yy,
                                mode="lines+markers",
                                marker=dict(
                                    symbol=opt.mark[sim][ori],
                                    line_width=1,
                                    line_color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                    color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                    size=6,
                                    opacity=1,
                                ),
                                line=dict(
                                    color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                    dash="solid"
                                    if rec == "tau3_fdust2_best_apers"
                                    else "dash",
                                ),
                                    name=sim.replace("TNG50 ", "")
                                    + " "
                                    + opt.rec_l[rec]
                                    + " "
                                    + opt.apers_l[aper]
                                    + " "
                                    + opt.oris_l[ori],
                                showlegend=True if band.find(
                                    "FUV") > -1 else False,
                                text=["{}".format(a) for a in brg],
                                hovertemplate="%{text}<extra></extra>",
                            )
                            fig_uv.append_trace(traceE, 1, br + 1)
                            fig_uv.append_trace(trace, 1, br + 1)
                            br_tot = br_tot + 0.3
                            fig_uv.add_annotation(
                                x=7.5,
                                y=np.log10(10**br_tot*5e-6),
                                xref="x" + str(br + 1),
                                yref="y" + str(br + 1),
                                text=str(sum(brg))+ opt.oris_s[ori],
                                font= {'color': opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper]},
                                showarrow=False,
								)

    return fig_uv

def plot_opt_obs(Loveday12, Driver12, Hill10):
    fig_opt = make_subplots(
        rows=3,
        cols=3,
        shared_yaxes=True,
        vertical_spacing=0.001,
        shared_xaxes=True,
        horizontal_spacing=0.001,
    )
    br = 0
    for bn1 in [0, 1, 2]:
        for bn2 in [0, 1, 2]:
            band = opt.bands_o[bn1][bn2]
            lamb = opt.pivot()[1][opt.pivot()[1].index==band].values[0][0]
            if band.find("SDSS") > -1:
                trace_L12 = go.Scatter(
                    x=np.log10(Mab_to_L(Loveday12[band]["M"],lamb)),
                    y=Loveday12[band]["MF"]*2.5,
                    name="Loveday et al. 2012",
                    mode="markers",
                    marker=dict(
                        color="purple",
                        size=7,
                        opacity=1,
                        symbol='square',
                        line=dict(width=0.5, color="black"),
                    ),
                    showlegend=True if (bn1 == 0) and (bn2 == 0) else False,
                    hoverinfo="none",
                    hoveron="points",
                )
                fig_opt.append_trace(trace_L12, bn1 + 1, bn2 + 1)
            if (band.find("UKIDSS") > -1):
                trace_H10 = go.Scatter(
                    x=np.log10(Mab_to_L(Hill10[band]["M"],lamb)),
                    y=10**Hill10[band]["log_MF"]*2.5,
                    error_y=dict(
                        type="data",
                        symmetric=False,
                        array=Hill10[band].dMF_u*2.5,
                        arrayminus=Hill10[band].dMF_l*2.5,
                        thickness=0.5,
                    ),
                    name="Hill et al. 2010",
                    mode="markers",
                    marker=dict(
                        color="magenta",
                        size=7,
                        opacity=1,
                        symbol='triangle-right',
                        line=dict(width=0.5, color="black"),
                    ),
                    showlegend=True if (bn1 == 2) and (bn2 == 2) else False,
                    hoverinfo="none",
                    hoveron="points",
                )
                fig_opt.append_trace(trace_H10, bn1 + 1, bn2 + 1)
                
            trace_D12 = go.Scatter(
                x=np.log10(Mab_to_L(Driver12[band]["M"],lamb)),
                y=10 ** (Driver12[band]["log_MF"])*2.5,
                error_y=dict(
                        type="data",
                        symmetric=False,
                        array=Driver12[band].dMF_u*2.5,
                        arrayminus=Driver12[band].dMF_l*2.5,
                        thickness=0.5,
                    ),
                name="Driver et al. 2012",
                mode="markers",
                marker=dict(
                    color="lime", size=7, opacity=1,symbol='diamond', line=dict(width=0.5, color="black")
                ),
                showlegend=True if (bn1 == 0) and (bn2 == 0) else False,
                hoverinfo="none",
                hoveron="points",
            )
            br = br + 1
            fig_opt.append_trace(trace_D12, bn1 + 1, bn2 + 1)
            fig_opt.add_annotation(
                x=11,
                y=-1.5,
                xref="x" + str(br),
                yref="y" + str(br),
                text=band.replace("_", " "),
                showarrow=False,
            )

            fig_opt.update_xaxes(
                row=bn1 + 1, col=bn2 + 1,
                title="log L [ L"
                + u"\u2299"
                +"]" 
                if bn1 == 2 else "",
                range=[6.3,12],

            )
            fig_opt.update_yaxes(
                row=bn1 + 1,
                col=bn2 + 1,
                title=u"\u03D5"
                + "[Mpc"
                + u"\u207B"
                + u"\u00B3"
                + "dex"
                + u"\u207B"
                + u"\u00B9"
                + "]"
                if bn2 == 0
                else "",
 
            )
    fig_opt.update_yaxes(
        linecolor="#000000",
        showgrid=False,
        linewidth=1,
        mirror=True,
        type="log",
        ticks="inside",
        range=[-5.9,-1],
    )
    fig_opt.update_xaxes(
        linecolor="#000000", showgrid=False, linewidth=1, mirror=True, ticks="inside",
    )
    fig_opt["layout"].update(
        autosize=False,
        height=1251,
        width=1251,
        margin=dict(
        l=70,
        r=5,
        b=70,
        t=100,
        pad=0
        ),
        plot_bgcolor="white",
        font=dict(size=13),
        legend=dict(orientation="h", yanchor="top", y=1.07, xanchor="left", x=0),
        hovermode="x",
    )
    return fig_opt

def plot_opt(selected_sims, selected_recs, selected_apers, selected_oris,Loveday12, Driver12, Hill10, LuF_TNG_1_allz, LuF_TNG_2_allz):
    fig_opt = plot_opt_obs(Loveday12, Driver12, Hill10)  
    br = 0
    for bn1 in [0, 1, 2]:
        for bn2 in [0, 1, 2]:
            br_tot = 0
            bandt = opt.bands_o[bn1][bn2]
            band = "F_" + bandt
            br = br + 1
            if selected_sims and selected_recs and selected_apers and selected_oris:
                for j, sim in enumerate(selected_sims):
                    if sim == "TNG50 1":
                        data = LuF_TNG_1_allz
                    elif sim == "TNG50 2":
                        data = LuF_TNG_2_allz
                    for i, rec in enumerate(selected_recs):
                        for k, aper in enumerate(selected_apers):
                            for l, ori in enumerate(selected_oris):
                                xx = data[band][rec][aper][ori][0][
                                    data[band][rec][aper][ori][2] > 0
                                ]
                                yy = data[band][rec][aper][ori][2][
                                    data[band][rec][aper][ori][2] > 0
                                ]
                                yyE = np.array(data[band][rec][aper][ori][3])
                                yyE = yyE[data[band][rec][aper][ori][2] > 0]
                                yyU = list(yy + yyE)
                                yyD = list(yy - yyE)

                                brg = data[band][rec][aper][ori][4][
                                    data[band][rec][aper][ori][2] > 0
                                ]

                                traceE = go.Scatter(
                                    x=list(xx) + list(xx[::-1]),
                                    y=yyU + yyD[::-1],
                                    fill="toself",
                                    fillcolor=opt.colors_rgba[aper] if sim=="TNG50 1" else opt.colors_rgba_2[aper],
                                    line=dict(color="rgba(7, 68, 0, 1)"),
                                    hoverinfo="skip",
                                    mode="none",
                                    showlegend=False,
                                )
                                trace = go.Scatter(
                                    x=xx,
                                    y=yy,
                                    mode="lines+markers",
                                    marker=dict(
                                        symbol=opt.mark[sim][ori],
                                        line_width=1,
                                        line_color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                        color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                        size=6,
                                        opacity=1,
                                    ),
                                    line=dict(
                                        color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                        dash="solid"
                                        if rec == "tau3_fdust2_best_apers"
                                        else "dash",
                                    ),
                                    name=sim.replace("TNG50 ", "")
                                    + " "
                                    + opt.rec_l[rec]
                                    + " "
                                    + opt.apers_l[aper]
                                    + " "
                                    + opt.oris_l[ori],
                                    showlegend=True
                                    if (bn1 == 0) and (bn2 == 0)
                                    else False,
                                    text=["{}".format(a) for a in brg],
                                    hovertemplate="%{text}<extra></extra>",
                                )
                                fig_opt.append_trace(traceE, bn1 + 1, bn2 + 1)
                                fig_opt.append_trace(trace, bn1 + 1, bn2 + 1)
                            
                                br_tot = br_tot + 0.3
                                fig_opt.add_annotation(
                                    x=7,
                                    y=np.log10(10**br_tot*5e-6),
                                    xref="x" + str(br),
                                    yref="y" + str(br),
                                    text=str(sum(brg)) + opt.oris_s[ori],
                                    font= {'color': opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper]},
                                    showarrow=False,
    								)
    return fig_opt

def plot_ir_obs(Dunne11,Negrello14,Marchetti16):
    fig_ir = make_subplots(
        rows=2,
        cols=2,
        shared_yaxes=True,
        vertical_spacing=0.001,
        shared_xaxes=True,
        horizontal_spacing=0.001,
    )
    br = 0
    for bn1 in [0, 1]:
        for bn2 in [0, 1]:
            x = []
            y = []
            dy_u = []
            dy_l = []
            labs = []
            cols = []
            legs = []
            sym = []
            band = opt.bands_ir[bn1][bn2]
            if band in Dunne11:
                x.append(Dunne11[band].log_L)
                y.append(10**Dunne11[band].log_LF)
                dy_u.append(10**Dunne11[band].log_dLF_u)
                dy_l.append(10**Dunne11[band].log_dLF_l)
                labs.append('Dunne et al. 2011')
                cols.append('brown')
                legs.append(0)
                sym.append('hexagon2')
                
                
                
                
            if band in Negrello14:
                x.append(Negrello14[band].log_L)
                y.append(10**Negrello14[band].log_LF)
                dy_u.append(Negrello14[band].dLF_u)
                dy_l.append(Negrello14[band].dLF_l)
                labs.append('Negrello et al. 2013')
                cols.append('green')
                legs.append(1)
                sym.append('star')
                
            
            if band in Marchetti16:
                x.append(Marchetti16[band].log_L)
                y.append(10**Marchetti16[band].log_LF)
                dy_u.append(Marchetti16[band].dLF_u)
                dy_l.append(Marchetti16[band].dLF_l)
                labs.append('Marchetti et al. 2016')
                cols.append('orange')
                legs.append(0)
                sym.append('diamond-tall')
                
            for xt, yt, dyut, dylt, labt, colt, legt,symt in zip(x,y,dy_u,dy_l,labs,cols,legs,sym):
                if xt.any():
                    trace_obs = go.Scatter(
                                        x=xt,
                                        y=yt,
                                        error_y=dict(type="data",
                                                     symmetric=False,
                                                     array=dyut,
                                                     arrayminus=dylt,
                                                     thickness=0.5,
                                        ),
                                        mode="markers",
                                        marker=dict(
                                            color=colt,
                                            size=8,
                                            opacity=1,
                                            symbol=symt,
                                            line=dict(width=0.5, color="black"),
                                        ),
                                        name=labt,
                                        showlegend=True if legt == br else False,
                                        hoverinfo="none",
                                        hoveron="points",
                                    )
                    fig_ir.append_trace(trace_obs, bn1 + 1, bn2 + 1)

            br = br + 1
            fig_ir.add_annotation(
                x=11,
                y=-1.5,
                xref="x" + str(br),
                yref="y" + str(br),
                text=band.replace("S", "SPIRE ")
                if band.find("0") > -1
                else band.replace("L", ""),
                showarrow=False,
            )
            fig_ir.update_xaxes(
                row=bn1 + 1,
                col=bn2 + 1,
                title="log L [ L"
                + u"\u2299"
                +"]"
                if bn1 == 1 else "",
                range=[7, 12],
            )
            fig_ir.update_yaxes(
                row=bn1 + 1,
                col=bn2 + 1,
                title=u"\u03D5"
                + "[Mpc"
                + u"\u207B"
                + u"\u00B3"
                + "dex"
                + u"\u207B"
                + u"\u00B9"
                + "]"
                if bn2 == 0
                else "",
                range=[-5.9, -1],
                
            )
    fig_ir.update_yaxes(
        linecolor="#000000",
        showgrid=False,
        linewidth=1,
        mirror=True,
        type="log",
        ticks="inside",
    )
    fig_ir.update_xaxes(
        linecolor="#000000", showgrid=False, linewidth=1, mirror=True, ticks="inside",
    )
    fig_ir["layout"].update(
        autosize=False,
        height=895,
        width=866.3333333333334,
        margin=dict(
        l=70,
        r=5,
        b=70,
        t=100,
        pad=0
        ),
        plot_bgcolor="white",
        font=dict(size=13),
        legend=dict(orientation="h", yanchor="top", y=1.106, xanchor="left", x=0.),
        hovermode="x",
    )
    return fig_ir

def plot_ir(selected_sims, selected_recs, selected_apers, selected_oris,Dunne11,Negrello14,Marchetti16,LuF_TNG_1_allz,LuF_TNG_2_allz):    
    fig_ir = plot_ir_obs(Dunne11,Negrello14,Marchetti16)
    br = 0
    for bn1 in [0, 1]:
        for bn2 in [0, 1]:
            br = br+1
            br_tot = 0
            band = "F_" + opt.bands_ir_sim[bn1][bn2] if opt.bands_ir_sim[bn1][bn2]!='LIR' else opt.bands_ir_sim[bn1][bn2] 
            if selected_sims and selected_recs and selected_apers and selected_oris:
                for j, sim in enumerate(selected_sims):
                    if sim == "TNG50 1":
                        data = (
                            LuF_TNG_1_allz[band]
                        )

                    elif sim == "TNG50 2":
                        data = (
                            LuF_TNG_2_allz[band]
                        )

                    for i, rec in enumerate(selected_recs):
                        for k, aper in enumerate(selected_apers):
                            for l, ori in enumerate(selected_oris):
                                xx = data[rec][aper][ori][0][
                                    data[rec][aper][ori][2] > 0
                                ]
                                yy = data[rec][aper][ori][2][
                                    data[rec][aper][ori][2] > 0
                                ]
                                yyE = np.array(data[rec][aper][ori][3])
                                yyE = yyE[
                                    np.array(data[rec][aper][ori][2] > 0)
                                ]
                                yyU = list(yy + yyE)
                                yyD = list(yy - yyE)

                                brg = data[rec][aper][ori][4][
                                    data[rec][aper][ori][2] > 0
                                ]

                                traceE = go.Scatter(
                                    x=list(xx) + list(xx[::-1]),
                                    y=yyU + yyD[::-1],
                                    fill="toself",
                                    fillcolor=opt.colors_rgba[aper] if sim=="TNG50 1" else opt.colors_rgba_2[aper],
                                    line=dict(color="rgba(7, 68, 0, 1)"),
                                    hoverinfo="skip",
                                    mode="none",
                                    showlegend=False,
                                )
                                trace = go.Scatter(
                                    x=xx,
                                    y=yy,
                                    mode="lines+markers",
                                    marker=dict(
                                        symbol=opt.mark[sim][ori],
                                        line_width=1,
                                        line_color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                        color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                        size=6,
                                        opacity=1,
                                    ),
                                    line=dict(
                                        color=opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper],
                                        dash="solid"
                                        if rec == "tau3_fdust2_best_apers"
                                        else "dash",
                                    ),
                                    name=sim.replace("TNG50 ", "")
                                    + " "
                                    + opt.rec_l[rec]
                                    + " "
                                    + opt.apers_l[aper]
                                    + " "
                                    + opt.oris_l[ori],
                                    showlegend=True
                                    if (bn1 == 0) and (bn2 == 0)
                                    else False,
                                    text=["{}".format(a) for a in brg],
                                    hovertemplate="%{text}<extra></extra>",
                                )
                                fig_ir.append_trace(traceE, bn1 + 1, bn2 + 1)
                                fig_ir.append_trace(trace, bn1 + 1, bn2 + 1)
                                br_tot = br_tot+0.3
                                fig_ir.add_annotation(
                                x=8,
                                y=np.log10(10**br_tot*5e-6),
                                xref="x" + str(br),
                                yref="y" + str(br),
                                text=str(sum(brg))+ opt.oris_s[ori],
                                font= {'color': opt.colors[aper] if sim=="TNG50 1" else opt.colors_2[aper]},
                                showarrow=False,
								)

    return fig_ir

