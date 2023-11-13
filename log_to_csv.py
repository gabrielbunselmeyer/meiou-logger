import os, re, csv

os.chdir(os.path.dirname(__file__))

GAME_LOG_FILE_DIR = "script_log.txt"

LINE_HEADER = ":era_statistics_logging::"
REGEX_PROV_DATA = re.compile(r"£[0-9]+px£(£[0-9]+px£)?")
REGEX_EVENT_DATE = re.compile(r"\[\d{4}\.\d{2}\.\d{2}\]")

CSV_DATA = {
    "Total Peasants": "SF Total",
    "Total Residents": "RE Total",
    "Peasant Immigration": "SF I ",
    "Resident Immigration": "RE In",
    "Peasant Wealth": "SF Wealth",
    "Resident Wealth": "RE Wealth",
    "Tax Efficiency": "Tax EfficUni",
    "State Reach": "Prov BUPow",
    "Corruption": "Prov BULoy",
    "Tax Effectiveness": "Admin EfficUni",
    "Tax Revenue": "TaxD Revenue",
    "Tax Farming": "TaxD Farming",
    "Tax Corruption": "TaxD Corruption",
    "Tax Total (net)": "TaxD Total",
}

try:
    with open(GAME_LOG_FILE_DIR) as log_file, open("./meiou.csv", "w", newline="") as csv_file:

        data_per_year = dict()

        for line in log_file:
            if LINE_HEADER in line:
                event_year = re.search(REGEX_EVENT_DATE, line).group().strip("[]").split(".")[0]
                
                if event_year not in data_per_year:
                    data_per_year[event_year] = []

                prov, *data = line[line.find(LINE_HEADER) + len(LINE_HEADER) :].split(", ")
                province_data_array = [prov]

                for entry in data:
                    number_with_decimal_point = re.sub(REGEX_PROV_DATA, "", entry)
                    province_data_array.append(int(str(number_with_decimal_point).replace('.', '')))

                data_per_year[event_year].append(province_data_array)

        highest_province_count = 0
        for year in data_per_year.keys():
            length = len(data_per_year[year])
            if length > highest_province_count:
                highest_province_count = length

        csv_headers = ["Year"]

        for x in range(0, highest_province_count):
            csv_headers += ["Province"] + list(CSV_DATA.keys())

        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(csv_headers)

        for year in data_per_year.keys():
            csv_writer.writerow([year] + [item for sublist in data_per_year[year] for item in sublist])

    print('done')
    # input("Press enter to exit...")

except Exception as e:
    print(e)
