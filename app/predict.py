import pandas as pd
import pickle
import numpy as np
from sklearn import metrics


def find_percentile(value, arr):
    sorted_arr = np.sort(arr)
    rank = np.searchsorted(sorted_arr, value)
    total_points = len(arr)
    percentile = (rank - 0.5) / total_points * 100
    return max(0, percentile)


def predict(input_file_path):
    dict_label_res = {}

    for label in ["dead1y", "gvhd1y", "rej1y", "rel1y", "efs1y"]:
        dict_label_res[label] = {}
        test_data = pd.read_csv(input_file_path)

        test_data = test_data.drop(['Unnamed: 0'], axis=1)  # 'pseudoid',

        clf = pickle.load(open(f"models/model_LogReg-{label}.p", "rb"))

        # load mean and std and normalize data
        with open(f"models/cofe_LogReg-{label}.csv") as mean_std_f:
            for line in mean_std_f:
                if "feature,coef" in line:
                    continue
                feature, _, std, _, _, mean = line.strip().split(",")
                test_data[feature] = (test_data[feature] - float(mean)) / float(std)

        """if label == "rel1y":
            features_to_remove = ["disease_170", "disease_200", "disease_300", "disease_310", "disease_400", "disease_500",
                                   "disease_520", "disease_570", "disease_600", "disease_900", ]
            test_data = test_data.drop(features_to_remove, axis=1)  # 'pseudoid',"""

        predict = clf.predict_proba(test_data)

        predict_prob = predict[0][1]
        print("predict_prob", predict_prob)

        list_pred = []
        list_pred_real = []
        with open(f"pred/pred_train_noevent0_LgReg_{label}.csv") as pred_file:
            for line in pred_file:
                line = line.strip().split(',')
                list_pred.append(float(line[1]))
                list_pred_real.append([float(line[0]), float(line[1])])
        # sort list_pred_real by pred
        sorted_list_pred_real = sorted(list_pred_real, key=lambda x: x[1])
        # sorted_list_pred = sorted(list_pred)

        # percentile = find_percentile(predict_prob, np.array(sorted_list_pred))
        # print("percentile", percentile)
        sorted_list_pred_real[0][1] = 0
        sorted_list_pred_real[-1][1] = 1.1
        bin_list = []
        for i in range(20):
            max_list_idx = int((i + 1) * 0.05 * len(sorted_list_pred_real))
            if i == 19:
                max_list_idx -= 1
            if (predict_prob >= sorted_list_pred_real[int(i * 0.05 * len(sorted_list_pred_real))][1]
                    and predict_prob < sorted_list_pred_real[max_list_idx][1]):

                for j in range(int(i * 0.05 * len(sorted_list_pred_real)),
                               int((i + 1) * 0.05 * len(sorted_list_pred_real))):
                    bin_list.append(list_pred_real[j][0])

                break

        bin_risk = sum(bin_list) / len(bin_list)
        print("bin_risk", bin_risk)
        dict_label_res[label]["bin_risk"] = bin_risk
        percentile = f"{int(i * 0.05 * 100)}-{int((i + 1) * 0.05 * 100)}"
        print("percentile", percentile)
        dict_label_res[label]["percentile"] = percentile

    return dict_label_res
