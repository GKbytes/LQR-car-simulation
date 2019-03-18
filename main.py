import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import sys
import keyboard
from math import *
from LQR import LQR
from RHS import RHS
from get_theta import get_theta
from path import path
from matrices_AB import Jacob_AB
from euler_method import euler_method
from draw_car import draw_car

#wymiary odpowiednich macierzy
n = 6
m = 2

#zdefiniowanie macierzy wagowej R
R = np.identity(m)
R[0][0] = 1
R[1][1] = 1

#zdefiniowanie macierzy wagowej Q
Q = np.identity(n)
Q[0][0] = 500
Q[1][1] = 0
Q[2][2] = 0
Q[3][3] = 0
Q[4][4] = 500
Q[5][5] = 0

#wartosci referencyjne
y0 = 10.0
Vx_ref = 60/3.6
Vy_ref = 0.0
teta_0 = get_theta(0.0)

#zainicjalizowanie macierzy stanu, wektorow sterowania i uchybu
x = np.array([Vx_ref, Vy_ref, 0.0, 0.0, y0, teta_0])
u = np.array([0.0, 0.0])
e = np.zeros((n,1))

#krok czasowy
dt = 0.005
t  = 0.0

tp, up, y_left, y_right, yp = [], [], [], [], []
x_act, y_act, th_act, th_ref = [], [], [], []

#stworzenie glownego okna symulacji
fig1 = plt.figure(figsize = (17, 10))
fig1.suptitle("\nSymulacja ruchu samochodu z regulatorem liniowo-kwadratowym" +
          "\nNacisnij 'Q' aby zakonczyc\n")
plt.subplots_adjust(wspace=0.4, hspace=0.4)

#stworzenie duzego okna z jadacym samochodem
ax1 = plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=3)
ax1.axis([0.0, 100.0, 0, 100])

line_left_y, = ax1.plot([], [], 'k')
line_right_y, = ax1.plot([], [], 'k')
line_mid_y, = ax1.plot([] ,[] ,'g')
line_act_y, = ax1.plot([], [], 'm')
lines_car, = ax1.plot([], [], 'k')

ax2 = plt.subplot2grid((3,3), (0,2), colspan=1, rowspan=1)
ax2.axis([0.0, 10, -5, 5])
ax2.grid()
ax2.tick_params(axis='x', labelsize=14)
ax2.tick_params(axis='y', labelsize=14)
plt.xlabel('Czas [s]', fontsize = 12)
plt.ylabel('Uchyb współrzędnej y', fontsize = 12)
line_y_error, = ax2.plot([], [], 'r')

ax3 = plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=1)
ax3.axis([0.0, 10, 50, 70])
ax3.grid()
ax3.tick_params(axis='x', labelsize=14)
ax3.tick_params(axis='y', labelsize=14)
plt.xlabel('Czas [s]', fontsize = 12)
plt.ylabel('Predkosc wzdluzna [km/h]', fontsize = 12)
line_vx, = ax3.plot([], [], 'b')

ax4 = plt.subplot2grid((3,3), (2,2), colspan=1, rowspan=1)
ax4.axis([0, 10, -5, 5])
ax4.grid()
ax4.tick_params(axis='x', labelsize=14)
ax4.tick_params(axis='y', labelsize=14)
plt.xlabel('Czas [s]', fontsize = 12)
plt.ylabel('Predkosc poprzeczna [km/h]', fontsize = 12)
line_vy, = ax4.plot([], [], 'g')

#rysowanie trasy
for i in range(10000):
  
  y_ref = path(i)
  x_act.append(i)
  y_left.append(y_ref + 2.0)
  y_right.append(y_ref - 2.0)
  yp.append(y_ref)
  
  line_left_y.set_data(x_act, y_left)
  line_right_y.set_data(x_act, y_right)
  line_mid_y.set_data(x_act, yp)
 
y_left, y_right, yp, x_act, y_act, y_err, vx, vy = [],[],[],[],[],[],[],[]

#glowna petla programu
while (t <= 10):

  #wyjscie z programu za pomoca klawisza Q
  if (keyboard.is_pressed('q') or keyboard.is_pressed('Q')): 
    sys.exit(0)

  #obliczenie referencyjnych wartosci y i teta
  y_ref = path(x[3])
  teta_ref = get_theta(x[3])

  #uaktualnienie list polozenia/predkosci o nowo policzone w danej iteracji
  tp.append(t)
  up.append(u)
  yp.append(y_ref)
  th_ref.append(teta_ref)
  x_act.append(x[3])
  y_act.append(x[4])
  th_act.append(x[5])
  y_err.append(x[4] - y_ref)

  vx.append(x[0]*3.6)
  vy.append(x[1]*3.6)
    
  #wektor uchybu
  e[0] = x[0] - Vx_ref
  e[1] = x[1] - Vy_ref
  e[2] = x[2] - 0
  e[3] = 0
  e[4] = x[4] - y_ref
  e[5] = x[5] - teta_ref

  #linearyzacja macierzy A i B
  A, B = Jacob_AB(RHS, x, t, u, n, m)

  #wyznaczenie macierzy sterowania za pomoca LQR
  K, P, eig_val = LQR(A, B, Q, R)

  #wyznaczenie wektora sterowania u
  u = -K*e

  #ucinanie sterowania po przekroczeniu wartości granicznej
  '''if(u[1] > 30*deg2rad):
    u[1] = 30*deg2rad

  elif(u[1] < -30*deg2rad):
    u[1] = -30*deg2rad'''
    
  #rozwiazanie ukladu rownan rozniczkowych metoda Eulera, dodanie kroku czasowego
  x = euler_method(RHS, x, t, dt, u)
  t = t + dt

  #zmienna wartość prędkości podczas trwania symulacji
  '''if(t>=0 and t<7.5):
    Vx_ref += 0.04/3.6

  if(t>=10 and t<12.5):
    Vx_ref += 0.04/3.6

  if(t>=15 and t<17.5):
    Vx_ref += 0.04/3.6
  '''
  if(i % 10 == 0):

    #wyskalowanie osi
    x_min = max(0, x[3] - 40)
    x_max = x_min + 50
    ax1.axis([x_min, x_max, -15, 40])
    ax1.set_title('Czas: t = ' + str(round(t, 2)) + ' s')

    #stworzenie rysunku samochodu w aktualnym polozeniu
    xs, ys = draw_car(x[3], x[4], x[5])
    lines_car.set_data(xs, ys)

    #linia aktualnej trasy
    line_act_y.set_data(x_act, y_act)
    
    #rysowanie bledu y od czasu
    line_y_error.set_data(tp, y_err)

    #rysowanie vx od czasu
    line_vx.set_data(tp, vx)

    #rysowanie vy od czasu
    line_vy.set_data(tp, vy)
    plt.pause(0.005)
