from flask import Flask, request, render_template
import pandas as pd
import secrets
import os
from datetime import timedelta
import time
from predict import predict
import json
from os.path import join

random_hex = secrets.token_hex()

app = Flask(__name__, static_folder='static', template_folder="templates")
app.config['UPLOAD_FOLDER'] = os.path.abspath("upload_folder")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
app.config["SECRET_KEY"] = random_hex


def delete_old_files():
    directories_path = ["static/temp_files", "static/output"]

    current_time = time.time()

    for directory_path in directories_path:
        # Iterate over the files in the directory
        for file in os.listdir(directory_path):
            file_time = float(file.split(".")[0])
            if current_time - file_time > 3600:
                os.remove(join(directory_path, file))
                print("Deleted:", join(directory_path, file))


blood_2_blood = {"O": ["A", "B", "AB", "O"],
                 "A": ["A", "AB"],
                 "B": ["B", "AB"],
                 "AB": ["AB"]}


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    delete_old_files()
    return render_template("index.html", result=False)


@app.route("/calculate_data", methods=["POST"])
def calculate():
    """Calculate the data and return the result"""
    # Get the form data
    mdstfaml = request.form.get("mdstfaml")
    amlrxrel = request.form.get("amlrxrel")
    sex = request.form.get("sex")
    cytogene = request.form.get("cytogene")
    disease = request.form.get("disease")
    mdsrxrel = request.form.get("mdsrxrel")
    rcmvpr = request.form.get("rcmvpr")
    venthxpr = request.form.get("venthxpr")
    funghxpr = request.form.get("funghxpr")
    condclas = request.form.get("condclas")
    indcycle = request.form.get("indcycle")
    age = request.form.get("age")
    indxtx = request.form.get("indxtx")
    cytogeneelnt = request.form.get("cytogeneelnt")
    numhires8_1 = request.form.get("numhires8_1")
    himatchdqb1_1 = request.form.get("himatchdqb1_1")
    himatchdpb1_1 = request.form.get("himatchdpb1_1")
    dcmvpr = request.form.get("dcmvpr")
    racegp = request.form.get("racegp")
    coorgscore = request.form.get("coorgscore")
    philgp = request.form.get("philgp")
    allsubgp = request.form.get("allsubgp")
    ipssrdx = request.form.get("ipssrdx")
    mdsdist = request.form.get("mdsdist")
    mdspredisp = request.form.get("mdspredisp")
    related = request.form.get("related")
    urdbmpbdage_up = request.form.get("urdbmpbdage_up")
    urdbmpbdrace = request.form.get("urdbmpbdrace")
    bmpbdsex = request.form.get("bmpbdsex")
    gvhprhrxgp = request.form.get("gvhprhrxgp")
    invivotcd = request.form.get("invivotcd")
    hxmalig = request.form.get("hxmalig")
    bcrrespr = request.form.get("bcrrespr")
    dabotype = request.form.get("dabotype")
    abotyper = request.form.get("abotyper")
    karnofraw = request.form.get("karnofraw")
    dparity1_up = request.form.get("dparity1_up")
    ipssrpr = request.form.get("ipssrpr")
    graftgp = request.form.get("graftgp")
    tbigp = request.form.get("tbigp")
    MEDHINC_CY = request.form.get("MEDHINC_CY")
    mpn = request.form.get("mpn")
    DPB1_permissive_v1 = request.form.get("DPB1_permissive_v1")
    match_class2 = request.form.get("match_class2", None)
    drigp = request.form.get("drigp")
    cytogener = request.form.get("cytogener")

    # Adjustments of the parameters
    cytogene = "cytogene_" + str(cytogene)
    disease = "disease_" + str(disease)
    condclas = "condclas_" + str(condclas)
    cytogeneelnt = "cytogeneelnt_" + str(cytogeneelnt)
    tbigp = "tbigp_" + str(tbigp)
    drigp = "drigp_" + str(drigp)
    cytogener = "cytogener_" + str(cytogener)

    drcmvpr = "drcmvpr_"
    if rcmvpr == "Positive" and dcmvpr == "Positive":
        drcmvpr += "0.0"
    elif rcmvpr == "Positive" and dcmvpr == "Negative":
        drcmvpr += "1.0"
    elif rcmvpr == "Negative" and dcmvpr == "Positive":
        drcmvpr += "2.0"
    elif rcmvpr == "Negative" and dcmvpr == "Negative":
        drcmvpr += "3.0"
    else:
        drcmvpr = "ALl Zeros"

    racegp = "racegp_" + str(racegp)
    allsubgp = "allsubgp_" + str(allsubgp)
    mdsdist = "mdsdist_" + str(mdsdist)
    urdbmpbdrace = "urdbmpbdrace_" + str(urdbmpbdrace)
    bmpbdsex = "bmpbdsex_" + str(bmpbdsex)
    gvhprhrxgp = "gvhprhrxgp_" + str(gvhprhrxgp)

    drabomatch_dots = "drabomatch_dots_"
    pat_abo = abotyper
    don_abo = dabotype
    if pat_abo and don_abo:
        if pat_abo == don_abo:
            drabomatch_dots += "0.0"
        elif pat_abo in blood_2_blood[don_abo]:
            drabomatch_dots += "1.0"
        elif don_abo in blood_2_blood[pat_abo]:
            drabomatch_dots += "2.0"
        else:
            drabomatch_dots += "3.0"

    dnrtype = "dnrtype_"
    numhires8 = numhires8_1
    if related == "Related":
        if str(numhires8) in ["Match", "8"]:
            dnrtype += "MRD"
        else:
            dnrtype += "MMRD"
    else:
        if str(numhires8) in ["Match", "8"]:
            dnrtype += "MUD"
        else:
            dnrtype += "MMUD"

    if numhires8 == "Match":
        numhires8 = 8
    elif numhires8 == "Mismatch":
        if related == "Related":
            numhires8 = 4
        else:
            numhires8 = 7

    if not match_class2:
        if related == "Related":
            if str(numhires8) in ["Match", "8"]:
                match_class2 = 6
            else:
                match_class2 = 4
        else:
            if str(numhires8) in ["Match", "8"]:
                match_class2 = 6
            else:
                match_class2 = 5

    # Load the default df
    df = pd.read_csv("static/input_efs_with_default_values.csv")

    # Update the df with the form data
    df["mdstfaml"] = int(mdstfaml)
    df["amlrxrel"] = int(amlrxrel)
    df["sex"] = int(sex)
    df["age"] = float(age)
    df["mdsrxrel"] = int(mdsrxrel)
    df["venthxpr"] = int(venthxpr)
    df["funghxpr"] = int(funghxpr)
    df["indcycle"] = int(indcycle)
    df["indxtx"] = float(indxtx)
    df["numhires8_1"] = int(numhires8)
    df["himatchdqb1_1"] = int(himatchdqb1_1)
    df["himatchdpb1_1"] = int(himatchdpb1_1)
    df["coorgscore"] = int(coorgscore)
    df["mpn"] = int(mpn)
    df["philgp"] = int(philgp)
    df["ipssrdx"] = int(ipssrdx)
    df["ipssrpr"] = int(ipssrpr)
    df["mdspredisp"] = int(mdspredisp)
    df["invivotcd"] = int(invivotcd)
    df["hxmalig"] = int(hxmalig)
    df["bcrrespr"] = int(bcrrespr)
    df["karnofraw"] = int(karnofraw)
    df["graftgp"] = int(graftgp)
    df["MEDHINC_CY"] = float(MEDHINC_CY)
    df["urdbmpbdage_up"] = float(urdbmpbdage_up)
    df["dparity1_up"] = int(dparity1_up)
    df["match_class2"] = int(match_class2)
    df["DPB1_permissive_v1"] = int(DPB1_permissive_v1)
    df["disease_10"] = 1 if disease == "disease_10" else 0
    df["disease_20"] = 1 if disease == "disease_20" else 0
    df["disease_30"] = 1 if disease == "disease_30" else 0
    df["disease_40"] = 1 if disease == "disease_40" else 0
    df["disease_50"] = 1 if disease == "disease_50" else 0
    df["disease_80"] = 1 if disease == "disease_80" else 0
    df["disease_100"] = 1 if disease == "disease_100" else 0
    df["disease_150"] = 1 if disease == "disease_150" else 0
    df["disease_170"] = 1 if disease == "disease_170" else 0
    df["disease_200"] = 1 if disease == "disease_200" else 0
    df["disease_300"] = 1 if disease == "disease_300" else 0
    df["disease_310"] = 1 if disease == "disease_310" else 0
    df["disease_400"] = 1 if disease == "disease_400" else 0
    df["disease_500"] = 1 if disease == "disease_500" else 0
    df["disease_520"] = 1 if disease == "disease_520" else 0
    df["disease_570"] = 1 if disease == "disease_570" else 0
    df["disease_600"] = 1 if disease == "disease_600" else 0
    df["disease_900"] = 1 if disease == "disease_900" else 0
    df["disease_1460"] = 1 if disease == "disease_1460" else 0
    df["dnrtype_MMRD"] = 1 if dnrtype == "dnrtype_MMRD" else 0
    df["dnrtype_MMUD"] = 1 if dnrtype == "dnrtype_MMUD" else 0
    df["dnrtype_MRD"] = 1 if dnrtype == "dnrtype_MRD" else 0
    df["dnrtype_MUD"] = 1 if dnrtype == "dnrtype_MUD" else 0
    df["drigp_1.0"] = 1 if drigp == "drigp_1.0" else 0
    df["drigp_2.0"] = 1 if drigp == "drigp_2.0" else 0
    df["drigp_3.0"] = 1 if drigp == "drigp_3.0" else 0
    df["drigp_4.0"] = 1 if drigp == "drigp_4.0" else 0
    df["drigp_6.0"] = 1 if drigp == "drigp_6.0" else 0
    df["drigp_76.0"] = 1 if drigp == "drigp_76.0" else 0
    df["drigp_77.0"] = 1 if drigp == "drigp_77.0" else 0
    df["drigp_78.0"] = 1 if drigp == "drigp_78.0" else 0
    df["drigp_88.0"] = 1 if drigp == "drigp_88.0" else 0
    df["drabomatch_dots_0.0"] = 1 if drabomatch_dots == "drabomatch_dots_0.0" else 0
    df["drabomatch_dots_1.0"] = 1 if drabomatch_dots == "drabomatch_dots_1.0" else 0
    df["drabomatch_dots_2.0"] = 1 if drabomatch_dots == "drabomatch_dots_2.0" else 0
    df["drabomatch_dots_3.0"] = 1 if drabomatch_dots == "drabomatch_dots_3.0" else 0
    df["tbigp_1.0"] = 1 if tbigp == "tbigp_1.0" else 0
    df["tbigp_2.0"] = 1 if tbigp == "tbigp_2.0" else 0
    df["tbigp_3.0"] = 1 if tbigp == "tbigp_3.0" else 0
    df["cytogene_1.0"] = 1 if cytogene == "cytogene_1.0" else 0
    df["cytogene_2.0"] = 1 if cytogene == "cytogene_2.0" else 0
    df["cytogene_3.0"] = 1 if cytogene == "cytogene_3.0" else 0
    df["cytogene_4.0"] = 1 if cytogene == "cytogene_4.0" else 0
    df["cytogene_5.0"] = 1 if cytogene == "cytogene_5.0" else 0
    df["conclas_1.0"] = 1 if condclas == "condclas_1.0" else 0
    df["condclas_2.0"] = 1 if condclas == "condclas_2.0" else 0
    df["condclas_3.0"] = 1 if condclas == "condclas_3.0" else 0
    df["racegp_1"] = 1 if racegp == "racegp_1" else 0
    df["racegp_2"] = 1 if racegp == "racegp_2" else 0
    df["gvprrxgp_1.0"] = 1 if gvhprhrxgp == "gvhprhrxgp_1.0" else 0
    df["gvhprhrxgp_2.0"] = 1 if gvhprhrxgp == "gvhprhrxgp_2.0" else 0
    df["gvhprhrxgp_3.0"] = 1 if gvhprhrxgp == "gvhprhrxgp_3.0" else 0
    df["gvhprhrxgp_4.0"] = 1 if gvhprhrxgp == "gvhprhrxgp_4.0" else 0
    df["gvhprhrxgp_5.0"] = 1 if gvhprhrxgp == "gvhprhrxgp_5.0" else 0
    df["gvhprhrxgp_6.0"] = 1 if gvhprhrxgp == "gvhprhrxgp_6.0" else 0
    df["drcmvpr_0.0"] = 1 if drcmvpr == "drcmvpr_0.0" else 0
    df["drcmvpr_1.0"] = 1 if drcmvpr == "drcmvpr_1.0" else 0
    df["drcmvpr_2.0"] = 1 if drcmvpr == "drcmvpr_2.0" else 0
    df["drcmvpr_3.0"] = 1 if drcmvpr == "drcmvpr_3.0" else 0
    df["cytogener_1"] = 1 if cytogener == "cytogener_1" else 0
    df["cytogener_2"] = 1 if cytogener == "cytogener_2" else 0
    df["cytogener_3"] = 1 if cytogener == "cytogener_3" else 0
    df["cytogener_4"] = 1 if cytogener == "cytogener_4" else 0
    df["cytogener_5"] = 1 if cytogener == "cytogener_5" else 0
    df["cytogeneelnt_1"] = 1 if cytogeneelnt == "cytogeneelnt_1" else 0
    df["cytogeneelnt_2"] = 1 if cytogeneelnt == "cytogeneelnt_2" else 0
    df["cytogeneelnt_3"] = 1 if cytogeneelnt == "cytogeneelnt_3" else 0
    df["cytogeneelnt_4"] = 1 if cytogeneelnt == "cytogeneelnt_4" else 0
    df["cytogeneelnt_5"] = 1 if cytogeneelnt == "cytogeneelnt_5" else 0
    df["allsubgp_1"] = 1 if allsubgp == "allsubgp_1" else 0
    df["allsubgp_2"] = 1 if allsubgp == "allsubgp_2" else 0
    df["allsubgp_3"] = 1 if allsubgp == "allsubgp_3" else 0
    df["urdbmpbdrace_1"] = 1 if urdbmpbdrace == "urdbmpbdrace_1" else 0
    df["urdbmpbdrace_2"] = 1 if urdbmpbdrace == "urdbmpbdrace_2" else 0
    df["bmpbdsex_1"] = 1 if bmpbdsex == "bmpbdsex_1" else 0
    df["bmpbdsex_2"] = 1 if bmpbdsex == "bmpbdsex_2" else 0
    df["mdsdist_1"] = 1 if mdsdist == "mdsdist_1" else 0
    df["mdsdist_2"] = 1 if mdsdist == "mdsdist_2" else 0
    df["mdsdist_3"] = 1 if mdsdist == "mdsdist_3" else 0

    # Save the df to a temporary file
    current_time = time.time()
    created_df_path = f"static/temp_files/{current_time}.csv"
    df.to_csv(created_df_path)

    # Predict on the data
    result = predict(created_df_path)

    # Save the results in json format
    with open(f"static/output/{current_time}.json", "w") as file:
        json.dump(result, file)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    # Create the dictionary for temporary files in static
    os.makedirs("static/temp_files", exist_ok=True)
    os.makedirs("static/output", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
