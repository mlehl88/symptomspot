import glob
import json
import numpy as np
import os

from symptomspot.extractor import SymptomExtractor

LABEL_PATH = 'data/labels/*.txt'
META_PATH = 'data/meta.json'


def get_errors(gold, extracted):
    tps = []
    fps = []
    fns = []
    for term in set(extracted + gold):
        if term in gold and term in extracted:
            tps.append(term)
        elif term in gold:
            fns.append(term)
        else:
            fps.append(term)
    return tps, fps, fns


def get_metrics(tps, fps, fns):
    precision = len(tps) / (len(tps) + len(fps))
    recall = len(tps) / (len(tps) + len(fns))
    f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1


def print_doc_results(url, tps, fps, fns, precision, recall, f1):
    print("URL: ", url)
    print("True Positives: ", tps)
    print("False Positives: ", fps)
    print("False Negatives: ", fns)
    print("Precision: ", precision, ", Recall: ", recall, ", F1: ", f1)
    print("-------------------------------")


def run_evaluation():
    extractor = SymptomExtractor()

    with open(META_PATH, 'r') as meta_file:
        id_to_url = json.load(meta_file)

    precisions = []
    recalls = []
    f1s = []
    for file_path in glob.glob(LABEL_PATH):
        file_id = os.path.splitext(os.path.basename(file_path))[0]
        url = id_to_url[file_id]

        with open(file_path, 'r') as file:
            gold = [line.strip().lower() for line in file.readlines()]
        extracted = extractor.extract(url=url)

        tps, fps, fns = get_errors(gold, extracted)
        precision, recall, f1 = get_metrics(tps, fps, fns)
        print_doc_results(url, tps=tps, fps=fps, fns=fns, precision=precision, recall=recall, f1=f1)

        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)

    print("Avg. Precision: ", np.mean(precisions))
    print("Avg. Recall: ", np.mean(recalls))
    print("Avg. F1: ", np.mean(f1s))


if __name__ == "__main__":
    run_evaluation()
