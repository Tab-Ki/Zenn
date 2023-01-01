#%% 一次元データの生成
import numpy as np
import matplotlib.pyplot as plt

# データ生成関数
def func_1D(x):
    return x**2

# 描画関数
def show_data_1D(func, *args):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    func_x = np.linspace(0,9,100)
    ax.plot(func_x, func(func_x), color="black", alpha=0.3)
    for arg in args:
        ax.scatter(arg[0], arg[1])
    ax.set_xlabel('X')
    plt.show()

x = np.linspace(0, 9, 10)
data = func_1D(x)

show_data_1D(func_1D, (x, data))

#%% RegularGridInterpolator
from scipy.interpolate import RegularGridInterpolator

interp = RegularGridInterpolator(np.meshgrid(x), data)

#%% 補間の実行
x2 = np.array([i + 0.5 for i in range(9)])
data2 = interp(x2)

show_data_1D(func_1D, (x, data), (x2, data2))

#%% sin関数の場合
def calc_RMSD_1D(func, x, interpolated_data):
    true_data = func(x)
    temp = sum([(true_data[i] - interpolated_data[i])**2 for i in range(len(true_data))])
    return np.sqrt(temp / len(true_data))

data = np.sin(x)
interp = RegularGridInterpolator(np.meshgrid(x), data) # method = "linear"
data2 = interp(x2)

show_data_1D(np.sin, (x, data), (x2, data2))
print("RMSD(linear):", calc_RMSD_1D(np.sin, x2, data2))

#%% methodの変更
interp.method = "nearest"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))
print("RMSD(nearest):", calc_RMSD_1D(np.sin, x2, data2))

interp.method = "slinear"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))
print("RMSD(slinear):", calc_RMSD_1D(np.sin, x2, data2))

interp.method = "cubic"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))
print("RMSD(cubic):", calc_RMSD_1D(np.sin, x2, data2))

interp.method = "quintic"
data2 = interp(x2)
show_data_1D(np.sin, (x, data), (x2, data2))
print("RMSD(quintic):", calc_RMSD_1D(np.sin, x2, data2))

#%% 三次元データの生成
from mpl_toolkits.mplot3d import Axes3D

# データ生成関数
def func_3D(x, y, z):
    return x**3 + y**2 + z

# 描画
def show_data_3D(*args):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect((1,1,1))
    vmin = np.min(args[0][3])
    vmax = np.max(args[0][3])
    for arg in args:
        ax.scatter(arg[0], arg[1], arg[2], c=(arg[3]-vmin)/(vmax-vmin), cmap='jet')
    ax.view_init(elev=10, azim=85)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

x = y = z = np.linspace(0, 5, 6)
xg, yg, zg = np.meshgrid(x, y, z, indexing='ij')
data = func_3D(xg, yg, zg)

show_data_3D((xg, yg, zg, data))

#%% RegularGridInterpolatorによる補間
def calc_RMSD_3D(func, xg, yg, zg, interpolated_data):
    f_true_data = func(xg, yg, zg).flatten()
    f_interpolated_data = interpolated_data.flatten()
    temp = sum([(f_true_data[i] - f_interpolated_data[i])**2 for i in range(len(f_true_data))])
    return np.sqrt(temp / len(f_true_data))

interp = RegularGridInterpolator((x, y, z), data) # method = "linear"

x2 = y2 = z2 = np.array([i + 0.5 for i in range(5)])
xg2, yg2, zg2 = np.meshgrid(x2, y2, z2, indexing='ij')
data2 = interp((xg2, yg2, zg2))

show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))
print("RMSD(linear):", calc_RMSD_3D(func_3D, xg2, yg2, zg2, data2))

#%% methodの変更
interp.method = "nearest"
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))
print("RMSD(nearest):", calc_RMSD_3D(func_3D, xg2, yg2, zg2, data2))

interp.method = "slinear"
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))
print("RMSD(slinear):", calc_RMSD_3D(func_3D, xg2, yg2, zg2, data2))

interp.method = "cubic"
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))
print("RMSD(cubic):", calc_RMSD_3D(func_3D, xg2, yg2, zg2, data2))

interp.method = "quintic"
data2 = interp((xg2, yg2, zg2))
show_data_3D((xg, yg, zg, data), (xg2, yg2, zg2, data2))
print("RMSD(quintic):", calc_RMSD_3D(func_3D, xg2, yg2, zg2, data2))
# %%
