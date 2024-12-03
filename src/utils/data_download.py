import requests

import sys
import csv
from datetime import datetime
import os


def try_download_visual_crossing_data_and_save_to_csv(
    area_name: str,
    latitute: float,
    longitude: float,
    start: datetime,
    end: datetime,
    forecast: bool,
    hourly: bool,
    data_folder: str = "../data/proprietary/weather",
) -> bool:
    """
    Downloads weather data from Visual Crossing API and saves it to a CSV file.

    Args:
        area_name (str): The name of the area for which to download weather data.
        latitute (float): The latitude of the location.
        longitude (float): The longitude of the location.
        start (datetime): The start date for the data retrieval.
        end (datetime): The end date for the data retrieval.
        forecast (bool): Whether to download forecast data (True) or observed data (False).
        hourly (bool): Whether to download hourly data (True) or daily data (False).
        data_folder (str, optional): The folder where the CSV file will be saved. Defaults to "../data/proprietary".

    Returns:
        True if completed successfully, False otherwise
    """
    api_key = ""
    with open("../.secrets/visual_crossing_api_key.txt", "r") as file:
        api_key = file.read().strip()

    os.makedirs(f"{data_folder}/visual_crossing", exist_ok=True)

    start_date = start.strftime("%Y-%m-%d")
    end_date = end.strftime("%Y-%m-%d")

    # See:
    # https://www.visualcrossing.com/resources/documentation/weather-api/agriculture-elements-in-the-timeline-weather-api/
    # https://www.visualcrossing.com/resources/documentation/weather-api/energy-elements-in-the-timeline-weather-api/
    wind_variables = "winddir,winddir50,winddir80,winddir100,windgust,windspeed,windspeed50,windspeed80,windspeed100,windspeedmean,windspeedmin,windspeedmax,"
    temperature_variables = "temp,tempmax,tempmin,dew,tempwet,deltat,"
    precipitation_variables = "humidity,precip,precipcover,preciptype,snow,snowdepth,"
    misc_variables = "pressure,visibility,solarradiation,dniradiation,difradiation,ghiradiation,gtiradiation,solarenergy,cloudcover,et0,"
    soil_variables = "soiltemp01,soiltemp04,soiltemp10,soiltemp20,soilmoisture01,soilmoisture04,soilmoisture10,soilmoisture20,"

    variables = f"{wind_variables}{temperature_variables}{precipitation_variables}{misc_variables}{soil_variables}"

    frequency = "hours" if hourly else "days"
    # req_observed = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitute},{longitude}/{start_date}/{end_date}?unitGroup=metric&elements=datetime,{variables}&include={frequency},obs,remote&key={api_key}&contentType=csv"
    req = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitute},{longitude}/{start_date}/{end_date}?unitGroup=metric&elements=datetime,{variables}&include={frequency},{"forecast" if forecast else "obs"},remote{"&forecastBasisDay=1" if forecast else ""}&key={api_key}&contentType=csv"

    response = requests.request("GET", req)
    if response.status_code != 200:
        print(response.content)
        return False

    csvText = csv.reader(response.text.splitlines(), delimiter=",", quotechar='"')

    with open(
        f"{data_folder}/visual_crossing/{area_name.lower().replace(" ","_")}_{"forecast" if forecast else "observed"}_{start_date}_{end_date}_{frequency}.csv",
        "w",
        newline="",
    ) as csvfile:
        writer = csv.writer(csvfile)
        for row in csvText:
            writer.writerow(row)

    return True
