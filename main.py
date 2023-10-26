from binance.client import Client
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Substitua com suas próprias chaves de API
api_key = "sua_api_key"
api_secret = "sua_api_secret"

client = Client(api_key, api_secret)

# Pegar informações do trade fiat/spot
symbol = 'BTCUSDT'
info = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")

# Transformar os dados em um DataFrame
df = pd.DataFrame(info, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
df['trade_time'] = pd.to_datetime(df['Open time'], unit='ms')
df['future_price'] = df['trade_time'].shift(-5, freq='Min').apply(lambda x: client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, start_str=x.strftime('%Y-%m-%d %H:%M:%S UTC'))[-1][4])

# Manipulação dos dados
df['price'] = pd.to_numeric(df['Close'])
df['quantity'] = pd.to_numeric(df['Volume'])
df['first_trade'] = pd.to_numeric(df['Open'])
df['last_trade'] = pd.to_numeric(df['Close'])
df['is_market_maker'] = False
df['is_best_price_match'] = False

# Preparar os dados para treinamento do modelo
X = df[['price', 'quantity', 'first_trade', 'last_trade', 'is_market_maker', 'is_best_price_match']].dropna()
y = df['future_price'].dropna()

# Dividir os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar um modelo de regressão linear
model = LinearRegression()
model.fit(X_train, y_train)

# Fazer previsões
predictions = model.predict(X_test)

# Exibir as previsões e os preços reais
for i, prediction in enumerate(predictions):
    print(f"Previsão: {prediction}, Preço Real: {y_test.iloc[i]}")

# Para fazer uma previsão do preço 5 minutos após a última entrada nos dados
latest_data = X.iloc[-1].values.reshape(1, -1)
future_price_prediction = model.predict(latest_data)
print(f"Previsão do preço 5 minutos no futuro: {future_price_prediction[0]}")
