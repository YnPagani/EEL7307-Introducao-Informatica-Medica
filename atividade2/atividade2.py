# Importe os dados do arquivo "DEEP_BREATHING_90.csv" de um dos seis voluntários
# disponibilizados aqui. Tente alterar as características do filtro 
# (frequências e ordem) para ressaltar seguintes características do canal 2 (ch2):
# a) complexos p,q,r,s e t constituintes do sinal de ECG;
# b) componente baixa frequência do sinal.

## Bibliotecas ----------------------------------------------------------------
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, lfilter_zi

def getExGSignal():
    sRate = 500 # Amostras/s
    ch1, ch2, ch3  = [], [], []
    path_to_signal_data = Path(r"atividade2/Volunt1/DEEP_BREATHING_90.csv")
    
    if path_to_signal_data.exists():
        fileDir = path_to_signal_data
    else:
        raise IOError

    samples = 1
    with open(fileDir) as dataFile:
        next(dataFile)
        for line in dataFile:
            aux = line.split(';')
            ch1.append(float(aux[0]))
            ch2.append(float(aux[1]))
            ch3.append(float(aux[2]))
           
            samples +=1

    ch1 = ch1[1:5001]
    ch2 = ch2[1:5001]
    ch3 = ch3[1:5001]
 
    samples = 5000

    # Generate X Axis.
    xAxis = np.linspace(0, samples/sRate, samples)

    return xAxis, ch1, ch2, ch3, samples, sRate
#end def

# Calcula a função para o Filtro Butterworth 
def butter_bandpass(lowcut, highcut, sRate, order=4):
    nyq = 0.5 * sRate
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, 1/nyq, btype='lowpass')
    return b, a
#end def

#def butter_bandpass_filter(data, lowcut, highcut, sRate, order=5):
#    b, a = butter_bandpass(lowcut, highcut, sRate, order=order)
#    y = lfilter(b, a, data)
#    return y
##end def

# Aplica o filtro considerando o transiente inicial.
def butter_bandpass_filter_zi(data, lowcut, highcut, sRate, order=4):
    b, a = butter_bandpass(lowcut, highcut, sRate, order=order)
    zi = lfilter_zi(b, a)
    y,zo = lfilter(b, a, data, zi=zi*data[0])
    return y
#end def
   
# Plota os canais

def plotChannels(ax, ch1, ch2, name):
    plt.figure('ECG Signals from: ' + name, figsize=(20, 10))
    plt.subplot(2,1,1)
    plt.title("Raw")
    plt.ylabel("amplitude")
    plt.plot(ax, ch1, "black")
    plt.grid()

    plt.subplot(2,1,2)
    plt.title("Low Frequency")
    plt.plot(ax, ch2, "blue")
    plt.grid()
    

    plt.show()

def main():
    # Get data
    x, c1, c2, c3, samp, sps = getExGSignal()

    # Apply bandpass filter into raw signals
    # For good filtering: [0.1, 28] 4th order
    # For QRS complex: [18, 52] 3th order
    # For low frequency: change butter() call to wn=1/nyq and btype="lowpass" 
    lowcut = 0.001
    highcut = 1
    order = 4
    c2f = butter_bandpass_filter_zi(c2, lowcut, highcut, sps, order)
    c2 = c2[1:5000]
    c2f = c2f[1:5000]
    x = x[1:5000]

    # Plota sinais raw
    plotChannels(x, c2, c2f, "Volunteer1")
    

if __name__ == "__main__":
    main()