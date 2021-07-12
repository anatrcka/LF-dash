recipes = [
    "tau3_fdust2_best_apers",
    "tau11_fdust1_best_apers",
    
]
apers = ["inf", "10", "2R", "30"]

oris = ["or", "fo", "eo"]

colors = {
    "inf": "#072F5F",
    "10": "#58CCED",
    "2R": "#3895D3",
    "30": "#1261A0",
    "E100": "#2ca02c",
    "ERecal": "#ff7f0e",
}
colors_rgba = {
    "inf": "rgba(7, 47, 95, 0.2)",
    "10": "rgba(88, 204, 237, 0.2)",
    "2R": "rgba(56, 149, 211, 0.2)",
    "30":"rgba(18, 97, 160, 0.2)",
    "E100":"rgba(44, 160, 44, 0.2)",
    "ERecal":"rgba(255, 127, 14, 0.2)",
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
mark = {
    "TNG50 1": {"or": "hexagram", "fo": "circle", "eo": "diamond-wide"},
    "TNG50 2": {"or": "hexagram-open", "fo": "circle-open", "eo": "diamond-wide-open"},
}