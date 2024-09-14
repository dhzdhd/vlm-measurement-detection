import os
import random
import pandas as pd


def predictor(image_link, category_id, entity_name):

    return ""


if __name__ == "__main__":
    DATASET_FOLDER = "dataset/"

    test = pd.read_csv(os.path.join(DATASET_FOLDER, "sample_test.csv"))

    test["prediction"] = test.apply(
        lambda row: predictor(row["image_link"], row["group_id"], row["entity_name"]),
        axis=1,
    )

    output_filename = os.path.join(DATASET_FOLDER, "dev_test_out.csv")
    test[["index", "prediction"]].to_csv(output_filename, index=False)
