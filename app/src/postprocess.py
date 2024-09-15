import pandas as pd
import re

entity_unit_map = {
    "width": {"centimetre", "foot", "inch", "metre", "millimetre", "yard"},
    "depth": {"centimetre", "foot", "inch", "metre", "millimetre", "yard"},
    "height": {"centimetre", "foot", "inch", "metre", "millimetre", "yard"},
    "item_weight": {
        "gram",
        "kilogram",
        "microgram",
        "milligram",
        "ounce",
        "pound",
        "ton",
    },
    "maximum_weight_recommendation": {
        "gram",
        "kilogram",
        "microgram",
        "milligram",
        "ounce",
        "pound",
        "ton",
    },
    "voltage": {"kilovolt", "millivolt", "volt"},
    "wattage": {"kilowatt", "watt"},
    "item_volume": {
        "centilitre",
        "cubic foot",
        "cubic inch",
        "cup",
        "decilitre",
        "fluid ounce",
        "gallon",
        "imperial gallon",
        "litre",
        "microlitre",
        "millilitre",
        "pint",
        "quart",
    },
}
missing_unit_map = {
    "width": "centimetre",
    "depth": "centimetre",
    "height": "centimetre",
    "item_weight": "gram",
    "maximum_weight_recommendation": "gram",
    "voltage": "volt",
    "wattage": "watt",
    "item_volume": "litre",
}

allowed_units = {unit for entity in entity_unit_map for unit in entity_unit_map[entity]}


def common_mistake(unit):
    if unit in allowed_units:
        return unit
    if unit.replace("ter", "tre") in allowed_units:
        return unit.replace("ter", "tre")
    if unit.replace("feet", "foot") in allowed_units:
        return unit.replace("feet", "foot")
    return unit


def parse_string(s):
    s_stripped = "" if s == None or str(s) == "nan" else s.strip()
    if s_stripped == "":
        return None, None
    pattern = re.compile(r"^-?\d+(\.\d+)?\s+[a-zA-Z\s]+$")
    if not pattern.match(s_stripped):
        raise ValueError("Invalid format in {}".format(s))
    parts = s_stripped.split(maxsplit=1)
    number = float(parts[0])
    unit = common_mistake(parts[1])
    if unit not in allowed_units:
        raise ValueError(
            "Invalid unit [{}] found in {}. Allowed units: {}".format(
                unit, s, allowed_units
            )
        )
    return number, unit


common_map = {
    "cm": "centimetre",
    "in": "inch",
    "g": "gram",
    "gm": "gram",
    "kg": "kilogram",
    "oz": "ounce",
    "mm": "millimetre",
    "w": "watts",
    "v": "volts",
    "m": "metre",
    "lbs": "pounds",
    "ft": "feet",
    "ml": "millilitre",
    "hz": "hertz",
    "pa": "pascal",
}


def postprocess(val: str):
    val = val.strip()
    val = val.split("/")[0].strip()
    val = val.split("(")[0].strip()

    val = re.sub(r"(^\d*\.*\d*)(\w+)$", lambda s: s[1] + " " + s[2], val)
    val = re.sub(
        f"(.*)\\s(cm|in|gm|kg|oz|mm|ml|lbs|ft|hz|pa|g|w|v|m)$",
        lambda s: s[1] + " " + common_map[s[2]],
        val,
    )
    val = re.sub(
        f'^"(\d*\.*\d*)"""$',
        lambda s: s[1] + " inches",
        val,
    )
    val = "" if ("unanswerable" in val or "VLM" in val) else val

    return val


def fill_missing(val):
    ent = test_df.iloc[int(val["index"])]["entity_name"]
    pred = val["prediction"]
    return re.sub(r"^(\d*\.*\d*)$", lambda s: s[0] + f" {missing_unit_map[ent]}", pred)


test_df = pd.read_csv("app/dataset/test.csv")

df = pd.read_csv("app/result/25000-32706.csv")
print(df.head(20))

df["prediction"] = df.apply(lambda row: fill_missing(row), axis=1)
df["prediction"] = df["prediction"].apply(lambda val: postprocess(val))
print(df.head())

df.to_csv("processed.csv", index=False)

# Sanity check
# df.apply(lambda x: parse_string(x["prediction"]), axis=1)
