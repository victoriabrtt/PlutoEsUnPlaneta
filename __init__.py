from obspy import read

st = read(r"./data/*.mseed")
st.merge()
tr = st[8]
print(st.__str__(extended=True))
tr.plot()