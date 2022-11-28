import pandas as pd #package for reading data
import numpy as np
import statistics

class Data:
    def __init__(self,gps_data,pressure_data) :
        self.gps_data = gps_data
        self.pressure_data = pressure_data

        self.gps_time = []
        self.gps_latitude = []
        self.gps_longitude = []

        self.pressure = []
        self.pressure_time = []

        self.slopes = []
        self.aslopes = []
        self.times = []

        self.elevated_data = []
        self.dervied_data = []

        self.range = 0

        self.gps = []
        self.up = []
        self.down =[]

        self.range_p = []
        self.range_p_flat = []
        self.range_t = []
        self.range_t_flat = []
        self.range_a = []
        self.range_a_flat = []

    def read_data(self):
        data1 = pd.read_csv(self.gps_data)
        data2 = pd.read_csv(self.pressure_data)

        self.gps_time = data1["time"]
        self.gps_longitude = data1["Longitude"]
        self.gps_latitude = data1["Latitude"]

        self.pressure = data2["Pressure"]
        self.pressure_time = data2["time"]
        return [[self.gps_time,self.gps_longitude,self.gps_latitude],[self.pressure,self.pressure_time]]

    def derive_data(self):
        i = 0
        time = self.pressure_time
        value = self.pressure

        while i < len(self.pressure_data)-1: 
            x0, x1 = time.iat[i], time.iat[i+1]
            y0, y1 = value[i], value[i+1]
            numerator = y1-y0
            num = numerator
            if numerator < 0 :  # somehow abs() doesn't work
                numerator *= -1
            slope = numerator/(x1-x0)
            aslope = num /(x1-x0)
            self.slopes.append(slope)
            self.times.append(x0)
            self.aslopes.append(aslope)
            i+=1
        self.slopes.append(0)
        self.times.append(0)
        self.aslopes.append(0)
        self.derive_data = [self.slopes,self.aslopes,self.times]
        return [self.slopes,self.aslopes,self.times]
        

    def der_range(self):
        mean = self.derive_data[2]
        std = statistics.stdev(self.slopes)
        self.range =  std
        print(mean)
        return self.range  

    def e_data(self):
        mean = self.derive_data[2]
        std = statistics.stdev(self.slopes)
        range =  std
        

        for i in self.slopes:
            if i >= range:
                self.range_p.append(i)
                self.range_t.append(self.times[self.slopes.index(i)])
                self.range_a.append(self.aslopes[self.slopes.index(i)])
            else:
                self.range_p_flat.append(i)
                self.range_t_flat.append(self.times[self.slopes.index(i)])
                self.range_a_flat.append(self.aslopes[self.slopes.index(i)])
        
        
    def up_down_time(self):
        self.up_time = []
        self.down_time = []
        for n in self.range_a:
            if n < 0:
                self.up_time.append(self.range_t[self.range_a.index(n)])
            else:
                self.down_time.append(self.range_t[self.range_a.index(n)])

    def gather_function(self,time_data,data1,data2):
        i = 0
        x = 0
        while i < len(time_data) - 1:
            for n in self.gps_time:
                if(time_data[i] <= n <=time_data[i+1]):
                    data1.append(self.gps_latitude[x])
                    data2.append(self.gps_longitude[x])
                    x = x + 1
            i = i + 1 
        return [data1,data2]

    def elevated_coordinates(self):
        gps_hill_la = []
        gps_hill_lo = []
        up_la = []
        down_lo = []
        up_lo = []
        down_la = []
        self.gps = self.gather_function( self.range_t,gps_hill_la, gps_hill_lo)
        self.up = self.gather_function( self.up_time,up_la, up_lo)
        self.down = self.gather_function(self.down_time, down_la, down_lo)

    