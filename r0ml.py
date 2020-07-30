# example of fitting a neural net on x vs x^2
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from numpy import asarray
from matplotlib import pyplot
import pandas as pd

# define the dataset
data = pd.read_csv(
    'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/boro/boroughs-case-hosp-death.csv')

print(data)

caseCount = []
d, h = [], []

totalRemoved = 0

for row, col in data.iterrows():
    if row == 0: continue
    caseCount.append(col['SI_CASE_COUNT'])
    d.append(col['SI_DEATH_COUNT'])

sum = 0
totalCases = []
for i in caseCount:
    sum += caseCount[i]
    totalCases.append(sum)

x = asarray([i for i in range(len(totalCases))])
y = asarray(totalCases)
print(x.min(), x.max(), y.min(), y.max())
# reshape arrays into into rows and cols
x = x.reshape((len(x), 1))
y = y.reshape((len(y), 1))
# separately scale the input and output variables
scale_x = MinMaxScaler()
x = scale_x.fit_transform(x)
scale_y = MinMaxScaler()
y = scale_y.fit_transform(y)
print(x.min(), x.max(), y.min(), y.max())
# design the neural network model
model = Sequential()
model.add(Dense(15, input_dim=1, activation='softplus', kernel_initializer='he_uniform'))
model.add(Dense(30, activation='elu', kernel_initializer='he_uniform'))
model.add(Dense(1, activation='tanh'))
# define the loss function and optimization algorithm
model.compile(loss='mse', optimizer='adam')
# ft the model on the training dataset
model.fit(x, y, epochs=100, batch_size=15, verbose=0)
# make predictions for the input data
yhat = model.predict(x)
# inverse transforms
x_plot = scale_x.inverse_transform(x)
y_plot = scale_y.inverse_transform(y)
yhat_plot = scale_y.inverse_transform(yhat)
# report model error
print('MSE: %.3f' % mean_squared_error(y_plot, yhat_plot))
# plot x vs y
pyplot.scatter(x_plot, y_plot, label='Actual')
# plot x vs yhat
pyplot.scatter(x_plot, yhat_plot, label='Predicted')
pyplot.title('Input (x) versus Output (y)')
pyplot.xlabel('Days Since Pandemic (x)')
pyplot.ylabel('Cases on Day x in SI (y)')
pyplot.legend()
pyplot.show()
