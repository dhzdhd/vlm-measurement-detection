import pandas as pd

idx = 3

df = pd.DataFrame({"index": [], "prediction": []})

with open("msg.txt") as f:
    lines = f.readlines()

    while True:
        if idx // 3 >= 7708:
            break

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    {
                        "index": [str(25000 + idx // 3 - 1)],
                        "prediction": [lines[idx - 1].replace("\n", "")],
                    }
                ),
            ],
            ignore_index=True,
        )
        idx += 3

print(df.head())
df.to_csv("res.csv", index=False)
