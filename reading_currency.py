import requests
import json
import pandas as pd

url = "https://Api.BrsApi.ir/Market/Gold_Currency.php?key=BcVu5MdZbfyfRyZ4hxhXvCj4BDEUUj7B" 

    # تنظیم یوزر ایجنت برای جلوگیری از بلاک شدن به دلیل اینکه یوزر ایجنت پایتون در استاندارد فایروال 6جی مسدود می‌شود

headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",

        "Accept": "application/json, text/plain, */*"

    }

response = requests.get(url, headers=headers)

if response.status_code == 200:

   data = response.json()

# Save as CSV

#    df = pd.DataFrame(data)
#    df.to_csv(
#         "symbols.csv",
#         index=False,
#         encoding="utf-8-sig"
#     )
#    print(df.head())

   with open("currency.json", "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )

   print("Data saved to currency.json")

else:
   print(f"Error: {response.status_code}")
