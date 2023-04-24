# machine-learning-projekt
**KEINE DATENSETS, NUR DAS EINZIG WAHRE, WENN ES FERTIG IST**

Repository für das Machine Learning Projekt

Titel: Vorhersage von Unfallzahlen mit Wetterdaten und Auslastungsdaten

Langbeschreibung: *TBD*

Rohdatensets: *TBD*

Algorithmen: Neuronales Netz & Random Forest

Model Performances: *TBD*

## Repo-Struktur:
* /datasets: Datensets (Gesamt, Train-Split, Test-Split)  
* /preparation: Skripte zur Vorbereitung der Daten bzw. zum Zusammenfügen der Datensets  
* /scalers: joblib dumps der Scaler für die Unfallzahlen für jede Wetterstation
* /training: Training der Modelle
* /models: Checkpoints und full_saves der Modelle  
* /prediction: Prediction des Test-Splits und Vergleich der Algorithmen mit der MSE Metrik

## Aufteilung

Robin: Skript aufräumen, Scaling der Unfälle, ggf. keras-tuning, Folien: Ergebnisse und Gegenüberstellung der Algorithmen

Fynn: Skripte aufräumen, Webservice, Ausblick

Steffen: Skripte aufräumen, Folie 1, Frontend 

# Plots
1. training ohne equalizing => equalizen
2. training mit equalizing => mehr Daten und Hyperparameter-Optimierung
3. optimal 64 64 training nach tuning => mehr Daten mit besserem Equalizing
4. _64x64 mit besserem equalizing



