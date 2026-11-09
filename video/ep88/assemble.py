import sys,shutil,os
# usage: assemble.py "1=P1,2=P2,3=A3,4=P3,5=P4,6=P5,7=P6"  -> voice/final/N.wav  (src dir 'voice/<tag>/<idx>.wav')
os.makedirs('voice/final',exist_ok=True)
for kv in sys.argv[1].split(','):
    n,src=kv.split('='); tag,idx=src[0],src[1:]
    shutil.copy(f'voice/{tag}/{idx}.wav',f'voice/final/{n}.wav')
