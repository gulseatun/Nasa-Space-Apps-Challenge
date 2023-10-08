import pandas as pd
import os
import requests

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
print(desktop_path)
merged_url = "https://raw.githubusercontent.com/gulseatun/Nasa-Space-Apps-Challenge/main/AceData.lst"
input_path = desktop_path + "\MergedData.lst"
output_path = desktop_path + "\MergedOutput.xlsx"
response = requests.get(merged_url)

with open(input_path, "wb") as MergedData:
    MergedData.write(response.content)

def output_to_excel(data, output):
    df = pd.DataFrame(data, columns=["year", "day", "hour", "change"])
    df.to_excel(output, index=False)

def analyse(input, output):
    if os.path.exists(output):
        os.remove(output)
    
    with open(input, "r") as file:
        contents = file.readlines()

    change_data = set()
    excel_data = []

    for line, next_line in zip(contents[:-1], contents[1:]):
        data = line.split()
        next_data = next_line.split()

        if '9999.99' not in (data[3], next_data[3]):
            change = abs(float(next_data[3]) - float(data[3]))
            if change > 10 and data[1] not in change_data:  
                excel_data.append([int(data[0]), int(data[1]), int(data[2]), change])
                change_data.add(data[1])
    
    output_to_excel(excel_data, output)

analyse(input_path, output_path)
