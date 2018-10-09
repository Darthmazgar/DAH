import matplotlib.pyplot as plt

y = [2.16, 1.6, 0.56, 0.008]
x = [2.12,  1.59, 0.54, 0.05] 

plt.plot(x,y)
plt.xlabel("Input Voltage (V)")
plt.ylabel("ADC Voltage (V)")
plt.title("Calibration Plot")
plt.show()


