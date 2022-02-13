import pandas as pd
rec = {
    "tau3_fdust2_best_apers": ["TNG50 1", "TNG50 2"],
    "tau11_fdust1_best_apers": ["TNG50 1"],
}
sim = {
    "TNG50 1": ["tau3_fdust2_best_apers", "tau11_fdust1_best_apers"],
    "TNG50 2": ["tau3_fdust2_best_apers"],

}

apers = ["inf", "10", "2R", "30"]

oris = ["or", "fo", "eo"]

colors = {
    "inf": "#072F5F",
    "10": "#58CCED",
    "2R": "#3895D3",
    "30": "#1261A0",
}
colors_rgba = {
    "inf": "rgba(7, 47, 95, 0.2)",
    "10": "rgba(88, 204, 237, 0.2)",
    "2R": "rgba(56, 149, 211, 0.2)",
    "30":"rgba(18, 97, 160, 0.2)",
}

colors_2 = {
    "inf": "#510ac9",
    "10": "#e4cbff",
    "2R": "#ca9bf7",
    "30": "#a55af4",
}
colors_rgba_2 = {
    "inf": "rgba(81, 10, 201, 0.2)",
    "10": "rgba(228, 203, 255, 0.2)",
    "2R": "rgba(202, 155, 247, 0.2)",
    "30":"rgba(165, 90, 244, 0.2)",
}


rec_l = {
    "tau3_fdust2_best_apers": u"\u03C4" + "=3, " + "fdust=0.2",
    "tau11_fdust1_best_apers": u"\u03C4" + "=11, " + "fdust=0.1",
}
apers_l = {
    "inf": "5R" + u"\u00BD",
    "10": "10kpc",
    "2R": "2R" + u"\u00BD",
    "30": "30kpc",
}
apers_lab = {
    "inf": "$5R_{1/2}$",
    "10": "10 kpc",
    "2R": "$2R_{1/2}$",
    "30": "30 kpc",
}
oris_l = {"or": "random", "fo": "face-on", "eo": "edge-on"}
oris_s = {"or": u"\u2736", "fo": u"\u25CF", "eo": u"\u2B2C"}
mark = {
    "TNG50 1": {"or": "hexagram", "fo": "circle", "eo": "diamond-wide"},
    "TNG50 2": {"or": "hexagram", "fo": "circle", "eo": "diamond-wide"},
}

bands_o = [
        ["SDSS_u", "SDSS_g", "SDSS_r"],
        ["SDSS_i", "SDSS_z", "UKIDSS_Y"],
        ["UKIDSS_J", "UKIDSS_H", "UKIDSS_K"],
    ]

bands_ir = [["S250", "S350"], ["S500", "TIR"]]
bands_ir_sim = [["SPIRE_250", "SPIRE_350"], ["SPIRE_500", "LIR"]]

def pivot():
    piv_f = pd.DataFrame(columns=['F', 'lam'])
    piv_f['F'] = ['F_GALEX_FUV','F_GALEX_NUV',
                'F_SDSS_u','F_SDSS_g','F_SDSS_r','F_SDSS_i','F_SDSS_z',\
               'F_TwoMASS_J','F_TwoMASS_H','F_TwoMASS_Ks',\
                'F_UKIDSS_Z','F_UKIDSS_Y','F_UKIDSS_J','F_UKIDSS_H','F_UKIDSS_K',\
                'F_Johnson_U','F_Johnson_B','F_Johnson_V','F_Johnson_R','F_Johnson_I','F_Johnson_J','F_Johnson_M',\
                'F_WISE_W1','F_WISE_W2','F_WISE_W3','F_WISE_W4',\
                'F_IRAS_12','F_IRAS_25','F_IRAS_60','F_IRAS_100',\
                'F_IRAC_I1','F_IRAC_I2','F_IRAC_I3','F_IRAC_I4',\
                'F_MIPS_24','F_MIPS_70','F_MIPS_160',\
                'F_PACS_70','F_PACS_100','F_PACS_160',\
                'F_SPIRE_250','F_SPIRE_350','F_SPIRE_500',\
                'F_SCUBA2_450','F_SCUBA2_850',
                'F_ALMA_10','F_ALMA_9','F_ALMA_8','F_ALMA_7','F_ALMA_6',
                'F_PLANCK_857','F_PLANCK_545','F_PLANCK_353']
    piv_f['lam'] = [0.1535,0.2301,\
                  0.3557,0.4702,0.6176,0.7490,0.8947,\
                  1.239,1.649,2.164,\
                  0.8826,\
                 1.031,1.250,1.635,2.206,0.3525,0.4417,0.5525,0.6899,0.8739,1.243,5.012,\
                  3.390,4.641,12.57,22.31,\
                  11.41,23.61,60.41,101.1,\
                  3.551,4.496,5.724,7.884,\
                  23.76,71.99,156.4,\
                  70.77,100.8,161.9,\
                  252.5,354.3,515.4,\
                  449.3,853.8,
                 349.9,456.2,689.6,937.9,1244,
                 352,545,839]
    piv_f.set_index('F', inplace=True)
    piv_mag= pd.DataFrame(columns=['M', 'lam'])
    piv_mag['M']=piv_f.index
    piv_mag.M=[s.replace('F_', '') for s in piv_mag.M]
    piv_mag['lam']=piv_f.lam.values
    piv_mag.set_index('M', inplace=True)
    return piv_f, piv_mag


# Constants

# little h for the TNG-50 simulations
def TNG_h():
    return 0.6774

# speed of light
def speed_c():
    return 299792458. # m/s

# L Sun 
def L_Sun():
    return 3.826e26 #W