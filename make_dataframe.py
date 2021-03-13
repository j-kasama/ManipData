import pandas as pd
import re

def make_dataframe():
    url = "https://en.wikipedia.org/wiki/NBA_All-Star_Game"
    data_list = pd.read_html(url)

    all_star_df = data_list[2].set_index("Year")
    all_star_df.dropna(how="any", inplace=True)
    all_star_df.drop("1999", inplace=True)
    result = all_star_df["Result"].str.split(",", expand=True).rename({0: "East", 1: "West"}, axis=1)
    city = all_star_df["Host city"]

    pattern = re.compile("West")
    for index, row in result.iterrows():
        if re.match(pattern, result.at[index, "East"]):
            tmp = result.at[index, "East"]
            result.at[index, "East"] = result.at[index, "West"]
            result.at[index, "West"] = tmp

    East = result["East"].str.extract(r'([0-9]+)').astype("float").rename({0: "East"}, axis=1)
    West = result["West"].str.extract(r'([0-9]+)').astype("float").rename({0: "West"}, axis=1)
    
    city = city.str.replace(r', .*', "")

    return pd.concat([East, West, city], axis=True)

if __name__ == "__main__":
    data = make_dataframe()
    diff = data.drop("Host city", axis=1).diff(axis=1).dropna(axis=1).rename({"West": "Diff"}, axis=1).abs()
    diff = pd.DataFrame(diff).value_counts()
    
    print(diff)

    mean = data.set_index("Host city")
    mean = mean.groupby("Host city").mean()
    count = pd.DataFrame(data["Host city"].value_counts()).rename({'Host city': "count"}, axis=1)
    output = pd.concat([mean, count], axis=1).query('count > 1').sort_values('count')
    
    print(output)

