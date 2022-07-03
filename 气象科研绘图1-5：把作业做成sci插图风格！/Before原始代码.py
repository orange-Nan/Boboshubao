import netCDF4 as nc
import datetime as dt
import numpy as np
from eofs.standard import Eof
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

#导入文件
filename = r'C:/Users/LULU/Desktop/sstmnmean.nc'
f = nc.Dataset(filename)

#读取数据
lat = f.variables['lat'][34:55]
lon = f.variables['lon'][65:146]
time1 = list(f.variables['time'][:])
time_index = []
years = [i for i in range(1979,2022)]
months = [6,7,8]
dates = []
x = []
for year in years:
    for month in months:
        day = dt.datetime.strptime(str(year)+'-'+str(month)+'-1', '%Y-%m-%d')-dt.datetime.strptime('1800-1-1', '%Y-%m-%d')
        x.append(str(year)+'-'+str(month))
        dates.append(day.days)        
for day in dates:
    time_index.append(time1.index(day))
sst = f.variables['sst'][time_index,34:55,65:146]

#计算纬度权重
lat0 = np.array(lat)
coslat = np.cos(np.deg2rad(lat0))
wgts = np.sqrt(coslat)[..., np.newaxis]

#EOF
eof = Eof(sst,weights=wgts)
u_eof = eof.eofsAsCorrelation(neofs=2)
u_pc = eof.pcs(npcs=2, pcscaling=1)
u_var = eof.varianceFraction(neigs=2)

#画图网格
X,Y = np.meshgrid(lon,lat)

#画图
fig = plt.figure(figsize=(15,10))
ax1 = plt.subplot(2,2,1)
ax1.contourf(X,Y,u_eof[0,:,:], levels=np.arange(-0.8,0.9,0.1), extend = 'both',zorder=0, cmap=plt.cm.RdBu_r)
ax2 = plt.subplot(2,2,2)
ax2.plot(x,u_pc[:,0])
ax2.xaxis.set_major_locator(MultipleLocator(15))
ax3 = plt.subplot(2,2,3)
ax3.contourf(X,Y,u_eof[1,:,:], levels=np.arange(-0.8,0.9,0.1), extend = 'both',zorder=0, cmap=plt.cm.RdBu_r)
ax4 = plt.subplot(2,2,4)
ax4.plot(x,u_pc[:,1])
ax4.xaxis.set_major_locator(MultipleLocator(15))

