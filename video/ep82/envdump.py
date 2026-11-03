import sys; sys.path.insert(0,".")
import numpy as np, librosa, thword, rword
f,a,b=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]); st=int(sys.argv[4]) if len(sys.argv)>4 else 2
y,_=librosa.load(f,sr=16000); y/=np.abs(y).max()+1e-9
db,hop=rword.env_db(y); hf,_=thword.band_env(y,3000,8000); lf,_=thword.band_env(y,80,1500)
for i in range(int(a/hop),min(len(db),int(b/hop)),st):
    print(f"{i*hop*1000:5.0f} env{db[i]:6.1f} lf{lf[i]:6.1f} hf{hf[min(i,len(hf)-1)]:6.1f} "+"#"*int(max(0,(db[i]+45)/1.2)))
