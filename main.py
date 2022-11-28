from data import Data

gps_csv = 'GPS.csv'
pressure_csv = 'Pressure.csv'

data = Data(gps_data=gps_csv,pressure_data=pressure_csv)
dara = data.read_data()
data.derive_data()
data.e_data()
data.up_down_time()
data.elevated_coordinates()

a = data.gps_time
print(dara)