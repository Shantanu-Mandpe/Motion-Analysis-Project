from data import Data

gps_data = 'GPS.csv'
pressure_data = 'Pressure.csv'

data = Data(gps_data=gps_data,pressure_data=pressure_data)
data.read_data()
data.derive_data()
data.e_data()
data.up_down_time()
data.elevated_coordinates()

a = data.gps_time
print(a)