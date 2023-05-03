# machine-learning-projekt

Repository für das Machine Learning Projekt

Titel: Vorhersage von Unfallzahlen mit Wetterdaten und Auslastungsdaten

Langbeschreibung: *TBD*

Rohdatensets: *TBD*

Algorithmen: Neuronales Netz & Random Forest

Model Performances: *TBD*

## Repo-Struktur:
* /datasets: Datensets (Gesamt, Train-Split, Test-Split)  
* /preprocessing: Skripte zur Vorbereitung der Daten bzw. zum Zusammenfügen der Datensets  
* prediction/scalers: joblib dumps der Scaler für die Unfallzahlen für jede Wetterstation
* /training: Training der Modelle
* prediction/models: Checkpoints und full_saves der Modelle  
* /prediction: Prediction des Test-Splits und Vergleich der Algorithmen mit der MSE Metrik

## Aufteilung

Robin:  
:white_check_mark: Skript aufräumen  
:white_check_mark: Scaling der Unfälle  
:white_check_mark: keras-tuning  
:large_orange_diamond: Folien Ergebnisse und Gegenüberstellung der Algorithmen

Fynn:   
:white_check_mark: Skripte aufräumen  
:large_orange_diamond: Webservice  

Steffen:  
:large_orange_diamond: Skripte aufräumen  
:large_orange_diamond: Folie 1  
:large_orange_diamond: Ausblick
:large_orange_diamond: Frontend   

# Plots
1. training ohne equalizing => equalizen
2. training mit equalizing => mehr Daten und Hyperparameter-Optimierung
3. optimal 64 64 training nach tuning => mehr Daten mit besserem Equalizing
4. _64x64 mit besserem equalizing



