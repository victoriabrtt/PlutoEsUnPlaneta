from obspy import read
from obspy.signal.trigger import classic_sta_lta, trigger_onset, plot_trigger
import numpy
import matplotlib.pyplot as plt

nsta = 1
nlta = 5


st = read(r"./data/*.mseed")
st.merge()
triggers = []
for tr in st:
    sta_lta = classic_sta_lta(tr.data, nsta, nlta)
    triggers = trigger_onset(sta_lta, 1, 0)
    fig,ax =  plt.subplots(1,1,figsize=(12,3))
    tr_times = tr.times()
    ax.plot(tr_times,sta_lta)
    ax.set_xlim([min(tr_times), max(tr_times)])
    ax.set_xlabel("Tiempo (secs)")
    ax.set_ylabel("Ratio STA/LTA")

    thres_on = 1.5
    thres_off = 1
    triggers = trigger_onset(sta_lta, thres_on, thres_off)

    on_off = numpy.array(triggers)
    fig,ax = plt.subplots(1,1, figsize=(12,3))
    print(len(on_off))
    for i in numpy.arange(0,len(on_off)):
        triggs = on_off[i]
        ax.axvline(x=tr_times[triggs[0]], color='pink', label='Trig On')
        ax.axvline(x=tr_times[triggs[1]], color='blue', label='Trig Off')
    ax.plot(tr_times, tr.data)
    ax.set_xlim([min(tr_times), max(tr_times)])
    ax.legend()