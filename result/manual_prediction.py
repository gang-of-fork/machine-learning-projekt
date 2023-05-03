import sys
#from keras.models import load_model
#from joblib import load

#nn_model = load_model('../prediction/models/accidents_model_nn')
#rf_model = load('../prediction/models/accidents_model_rf.bin')

valid_stations = [
    164, 5643, 6272, 3739, 7351, 5426, 1207, 3612, 5797, 3284, 6310, 3348, 13675, 7393, 4625, 5440, 150, 91,
    131, 2597, 2323, 3485, 2497, 257, 6109, 3257, 1270, 3196, 7099, 757, 4464, 4703, 4548, 78, 4592, 390, 1443, 1584, 390,  
    257, 1602, 6314, 4508, 2700, 1645, 704, 3426, 3730,
    7420, 4911, 5097, 3155, 2704, 5347, 5490, 298, 1346, 2712, 3362, 330, 5546, 3278, 2074, 2638, 1051, 856, 3376, 1694, 2947, 
    2362, 420, 5133, 4480, 7329, 7403, 1161, 7298, 6259, 1357, 3155, 4371, 4127, 5688, 5335, 701, 7368, 979, 2362, 5133, 5839, 
    5335, 6260, 4024, 154, 7395, 2174, 7396, 2856, 891, 3147, 6159, 4189, 3231, 5158, 7341, 13711, 1197, 4189, 3164, 867, 2211, 
    1451, 2110, 1048, 5111, 5146, 1605, 1451, 3513, 1050, 7330, 2023, 3234, 7419, 2814, 2814, 3031, 891, 2575, 1297, 5229, 4642, 
    5871, 4978, 445, 4032, 1300, 6157, 4032, 5109, 5100, 5731, 4300, 6158, 4997, 3925, 7319, 4978, 3540, 840, 1468, 6344, 5371, 
    3540, 617, 853, 5433, 5731, 840, 2629, 433, 314, 4094, 2812
]

def get_number_input(msg):
    while True:
        try:
            val = int(input(msg))

            return val
        except KeyboardInterrupt:
            sys.exit()
        except:
            print("Bitte gib eine valide Zahl ein.")

def get_number_input_in_range(msg, range_min, range_max):
    while True:
        val = get_number_input(msg)

        if val < range_min or val > range_max:
            print(f"Die Zahl ist nicht im Wertebereich von {range_min} bis {range_max}")
            continue
        
        return val

SELECTED_STATION = 617
PREDICTION_MODE = "default"

#month,day,hour,temperature,percipitation,road_usage

print("Manuelle Voraussageerstellung")

while PREDICTION_MODE not in "sc":
    print("s = Sigma")
    print("c = Anzahl skaliert mit Wetterstation")
    PREDICTION_MODE = input("Vorhersagemodes (c/s): ")

if PREDICTION_MODE == "c":
    input_station_yn = "default"

    while input_station_yn not in "yn":
        input_station_yn = input("Eigene Wetterstation auswählen Standard ist 617 (y/n): ")

        if input_station_yn not in "yn":
            print("Bitte nur y oder n eingeben")


    if input_station_yn == "y":
        SELECTED_STATION = int(input("ID der Station: "))

        if SELECTED_STATION not in valid_stations:
            print("Wetterstation existiert nicht")
            sys.exit()

SELECTED_MONTH = get_number_input_in_range("Wochentag (1 bis 12): ", 1, 12)
print("Sonntag = 1")
print("Montag = 2")
print("Dienstag = 3")
print("Mittwoch = 4")
print("...")
SELECTED_DAY = get_number_input_in_range("Wochentag (1 bis 7): ", 1, 7)
SELECTED_HOUR = get_number_input_in_range("2-Stunden-intervall 0 = 0-2, 1 = 2-4, ... (0 bis 11): ", 0, 11)
SELECTED_TEMPERATURE = get_number_input("Temperatur: ")
SELECTED_percipation = get_number_input("Niederschlag: ")

print("sh = sehr hoch")
print("h = hoch")
print("m = mittel")
print("n = niedrig")
print("sn = sehr niedrig")

selected_usage = "default"
SELECTED_USAGE = 0


while selected_usage not in ["sh", "h", "m", "n", "sn"]:
    selected_usage = input("Auslastung (sh/h/m/n/sn): ")
    if selected_usage not in ["sh", "h", "m", "n", "sn"]:
        print("Bitte validen Wert eingeben")

usage_map = {
    "sh": 2,
    "h": 1,
    "m": 0,
    "n": -1,
    "sn": -2
}

SELECTED_USAGE = usage_map[selected_usage]

"""
SELECTED_MONTH
SELECTED_DAY
SELECTED_HOUR
SELECTED_TEMPERATURE
SELECTED_percipation
SELECTED_USAGE
"""