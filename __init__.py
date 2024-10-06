import obspy
from obspy import read
from obspy.signal.trigger import classic_sta_lta, trigger_onset, plot_trigger
import numpy
import matplotlib.pyplot as plt

st = read(r"./data/mars/*.mseed")
#st = read(r"./data/mars/*.mseed")
triggers = []
for tr in st:
    #tr.filter('lowpass', freq=3.0)
    duration = (tr.times()[len(tr.times())-1]-tr.times()[0])
    df = tr.stats.sampling_rate
    nsta = duration*df*0.01
    nlta = nsta*10
    sta_lta = classic_sta_lta(tr.data, int(nsta), int(nlta))
    
    thres_on = 5
    thres_off = 0.5
    triggers = trigger_onset(sta_lta, thres_on, thres_off)

    on_off = numpy.array(triggers)
    if(len(on_off)):
        print(tr)
        fig,ax =  plt.subplots(2,1,figsize=(12,3))
        tr_times = tr.times()
        ax[0].plot(tr_times,sta_lta)
        ax[0].set_xlim([min(tr_times), max(tr_times)])
        ax[0].set_xlabel("Time (secs)")
        ax[0].set_ylabel("Ratio STA/LTA")

        for i in numpy.arange(0,len(on_off)):
            triggs = on_off[i]
            ax[1].axvline(x=tr_times[triggs[0]], color='red', label='Trig On')
            ax[1].axvline(x=tr_times[triggs[1]], color='green', label='Trig Off')
        ax[1].plot(tr_times, tr.data)
        ax[1].set_xlim([min(tr_times), max(tr_times)])
        ax[1].set_xlabel("Time (Secs)")
        ax[1].set_ylabel("Counts")
        plt.show()