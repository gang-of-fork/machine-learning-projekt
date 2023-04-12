# TODO fix imports, save model to /models


model = RandomForestRegressor(n_estimators=30, random_state=30)
model.fit(X_train, y_train)
