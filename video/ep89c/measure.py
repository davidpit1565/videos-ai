import sys, librosa, numpy as np, soundfile as sf
def meas(path, t0, t1, words):
    """words: {name:(a,b)} seconds in file. prints peak dB, rms dB, median/max pitch (semitones vs line median), onset slope"""
    y,sr=librosa.load(path,sr=16000,offset=t0,duration=t1-t0)
    f0,_,_=librosa.pyin(y,fmin=70,fmax=400,sr=sr,frame_length=1024,hop_length=256)
    t=np.arange(len(f0))*256/sr+t0; ok=~np.isnan(f0); med=np.nanmedian(f0)
    st=12*np.log2(f0/med)
    print(path,'line median f0 %.0f Hz, range p10-p90 %.1f st'%(med,np.nanpercentile(st[ok],90)-np.nanpercentile(st[ok],10)))
    x,_=librosa.load(path,sr=16000)
    for n,(a,b) in words.items():
        seg=x[int(a*sr):int(b*sr)]
        pk=20*np.log10(np.abs(seg).max()+1e-9); rm=20*np.log10(np.sqrt((seg**2).mean())+1e-9)
        m=(t>=a)&(t<=b)&ok
        p=st[m]
        if len(p)==0: print('  %-6s peak %.1f dB rms %.1f dB  (unvoiced)'%(n,pk,rm)); continue
        slope=(p[-3:].mean()-p[:3].mean()) if m.sum()>=6 else float('nan')
        # onset slope: rms rise 20ms->60ms
        print('  %-6s peak %.1f dB rms %.1f dB  pitch med %+.1f st max %+.1f min %+.1f  first->last %+.1f st'%(n,pk,rm,np.nanmedian(p),np.nanmax(p),np.nanmin(p),slope))
if __name__=='__main__':
    meas(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),eval(sys.argv[4]))
