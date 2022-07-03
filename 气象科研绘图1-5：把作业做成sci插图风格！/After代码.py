import netCDF4 as nc
import datetime as dt
import numpy as np
from eofs.standard import Eof
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import cartopy.crs as ccrs
import cartopy.feature as cf

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

#计算时间系数
pc1 = []
pc2 = []
for i in range(43):
    pc1.append((u_pc[:,0][i*3]+u_pc[:,0][i*3+1]+u_pc[:,0][i*3+2])/3)
    pc2.append((u_pc[:,1][i*3]+u_pc[:,0][i*3+1]+u_pc[:,0][i*3+2])/3)

#画图
fig = plt.figure(figsize=(16,8))

ax1 = fig.add_axes([0,0.7,1,1],projection=ccrs.PlateCarree(central_longitude=180))
ax1.set_xticks(np.arange(130,290,10), crs=ccrs.PlateCarree())
ax1.set_yticks(np.arange(-20,20,10), crs=ccrs.PlateCarree())
ax1.set_extent([130, 290, -20, 20], crs=ccrs.PlateCarree())
ax1.add_feature(cf.COASTLINE,lw=0.5,zorder=2) #海岸线
con1 = ax1.contourf(X,Y,u_eof[0,:,:],levels=np.arange(-0.9,1.1,0.1),transform=ccrs.PlateCarree(),cmap='RdBu',extend='both')
ax1.set_xticks([-40,-20,0,20,40,60,80,100])
ax1.set_xticklabels(['140E','160E','180','160W','140W','120W','100W','80W'],fontsize=30)
ax1.xaxis.set_minor_locator(MultipleLocator(10))
ax1.tick_params(axis='x',which='major',direction='out',length=12,width=1.5)
ax1.tick_params(axis='x',which='minor',direction='out',length=8,width=1)
ax1.set_yticks([-20,-10,0,10,20])
ax1.set_yticklabels(['20S','10S','0','10N','20N'],fontsize=30)
ax1.yaxis.set_minor_locator(MultipleLocator(5))
ax1.tick_params(axis='y',which='major',direction='out',length=12,width=1.5)
ax1.tick_params(axis='y',which='minor',direction='out',length=8,width=1)
ax1.set_title('EOF1(53.70%)',fontsize=40)
    
ax2 = fig.add_axes([1.1,0.95,0.5,0.5])
ax2.plot(years,pc1,c='k')
ax2.axhline(y=0,c='k')
ax2.xaxis.set_major_locator(MultipleLocator(10))
ax2.xaxis.set_minor_locator(MultipleLocator(1))
ax2.yaxis.set_major_locator(MultipleLocator(0.5))
ax2.yaxis.set_minor_locator(MultipleLocator(0.1))
ax2.tick_params(axis='x',which='major',direction='out',length=12,width=1.5,labelsize=30)
ax2.tick_params(axis='x',which='minor',direction='out',length=8,width=1)
ax2.tick_params(axis='y',which='major',direction='out',length=12,width=1.5,labelsize=30)
ax2.tick_params(axis='y',which='minor',direction='out',length=8,width=1)
ax2.set_title('PC1',fontsize=40)

ax3 = fig.add_axes([0,0,1,1],projection=ccrs.PlateCarree(central_longitude=180))
ax3.set_xticks(np.arange(130,290,10), crs=ccrs.PlateCarree())
ax3.set_yticks(np.arange(-20,20,10), crs=ccrs.PlateCarree())
ax3.set_extent([130, 290, -20, 20], crs=ccrs.PlateCarree())
ax3.add_feature(cf.COASTLINE,lw=0.5,zorder=2) #海岸线
ax3.contourf(X,Y,u_eof[1,:,:],levels=np.arange(-0.9,1.1,0.1),transform=ccrs.PlateCarree(),cmap='RdBu_r')
ax3.set_xticks([-40,-20,0,20,40,60,80,100])
ax3.set_xticklabels(['140E','160E','180','160W','140W','120W','100W','80W'],fontsize=30)
ax3.xaxis.set_minor_locator(MultipleLocator(10))
ax3.tick_params(axis='x',which='major',direction='out',length=12,width=1.5)
ax3.tick_params(axis='x',which='minor',direction='out',length=8,width=1)
ax3.set_yticks([-20,-10,0,10,20])
ax3.set_yticklabels(['20S','10S','0','10N','20N'],fontsize=30)
ax3.yaxis.set_minor_locator(MultipleLocator(5))
ax3.tick_params(axis='y',which='major',direction='out',length=12,width=1.5)
ax3.tick_params(axis='y',which='minor',direction='out',length=8,width=1)
ax3.set_title('EOF2(17.26%)',fontsize=40)

ax4 = fig.add_axes([1.1,0.25, 0.5, 0.5])
ax4.plot(years,pc2,c='k')
ax4.axhline(y=0,c='k')
ax4.xaxis.set_major_locator(MultipleLocator(10))
ax4.xaxis.set_minor_locator(MultipleLocator(1))
ax4.yaxis.set_major_locator(MultipleLocator(0.5))
ax4.yaxis.set_minor_locator(MultipleLocator(0.1))
ax4.tick_params(axis='x',which='major',direction='out',length=12,width=1.5,labelsize=30)
ax4.tick_params(axis='x',which='minor',direction='out',length=8,width=1)
ax4.tick_params(axis='y',which='major',direction='out',length=12,width=1.5,labelsize=30)
ax4.tick_params(axis='y',which='minor',direction='out',length=8,width=1)
ax4.set_title('PC2',fontsize=40)

#设置colorbar
l,b,w,h = -0.1, 0.5, 0.015, 0.8
rect = [l,b,w,h]
cbar_ax = fig.add_axes(rect)
cb = fig.colorbar(con1, cax = cbar_ax,orientation='vertical',extend='both',ticklocation='left')
cb.ax.tick_params(labelsize=28)

