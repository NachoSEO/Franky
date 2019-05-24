from google.colab import files # Only for Google colab
import pandas as pd
import io
from pytrends.request import TrendReq
from tqdm import tqdm
import time

uploaded = files.upload()  # Only for Google colab

def franky_trends(csv):
    df = pd.read_csv(io.BytesIO(uploaded[csv])) # io.BytesIO(uploaded[csv]) for Colab
    kw_list = df["Keyword"].tolist()
    efk = [kw_list[item:item+5] for item in range(0, len(kw_list),5)]
    kw_trends = []

    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq()

    for kw in tqdm(efk):
      pytrend.build_payload(kw_list=kw, timeframe='today 5-y')
      interest_over_time_df = pytrend.interest_over_time()
      df = pd.DataFrame(interest_over_time_df)
      kw_trends.append(df)
      time.sleep(1)

    list_df = iter(kw_trends)
    output = next(list_df)

    while list_df:
      try:
        output = pd.concat([output, next(list_df)], axis=1, join_axes=[output.index])
      except StopIteration as e:
        print(e)
        break

    result = output.drop(['isPartial'], axis=1)
    result_t = result.T
    result_t.to_csv('result_t.csv')
    files.download('result_t.csv') # Only for Google colab
    
franky_trends('test_100.csv') # Put the name of the file or the path
