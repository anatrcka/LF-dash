
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

sbands = {'S250':252.5,
          'S350':354.3,
          'S500':515.4,
          'TIR':100,
}


bands_ir = [["S250", "S350"], ["S500", "TIR"]]
bands_ir_sim = [["SPIRE_250", "SPIRE_350"], ["SPIRE_500", "LIR"]]

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