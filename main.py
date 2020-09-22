from typing import Optional
from fastapi import FastAPI
app = FastAPI()

import uvicorn

#необходимо, чтобы работать с json'ом
import json

#необходимо для работы с API openweathermap
import pyowm
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps

config_dict = get_default_config()
config_dict['language'] = 'ru'

#тут находится ключ с сайта OpenWeatherMap
#поместить его в переменную окружения
owm = pyowm.OWM('6e91084d708cf0dcdabc8e852960d090', config_dict)

@app.get("/v1/current/")
#city=<name city>
#http://127.0.0.1:8000/v1/current/?city=Moscow
def current(city: str):
	mgr = owm.weather_manager()

	observation = mgr.weather_at_place(city)
	w = observation.weather
	temp = w.temperature('celsius')['temp']
	#вывод в консоль
	print(" request: " + city + "\t" + w.detailed_status + "\t" + str( temp ))
	return json.dumps({"city": city,"unit": "celsius", "temperature": temp})


@app.get("/v1/forecast/")
#city=<name city>&timestamp=<timestamp>
#http://127.0.0.1:8000/v1/forecast/?city=Moscow&timestamp=3h
def forecast(city: str, timestamp: str):
	mgr = owm.weather_manager()

	observation = mgr.forecast_at_place(city, "3h") #данной командой стягивается прогноз погоды на ближайшие 5 дней с частотой 3 часа
	if timestamp == "1h":
		time = timestamps.next_hour()
	elif timestamp == "3h":
		time = timestamps.next_three_hours() 
	elif timestamp == "tomorrow":
		time = timestamps.tomorrow()
	elif timestamp == "yesterday":
		time = timestamps.yesterday()
	else:
		time = timestamps.now();
	w = observation.get_weather_at(time)
	temp = w.temperature('celsius')['temp']
	#вывод в консоль
	print(" request: " + city + "\ttime: "+ str(time) + "\t" + w.detailed_status + "\t" + str( temp ))
	return json.dumps({"city": city,"unit": "celsius", "temperature": temp})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)





