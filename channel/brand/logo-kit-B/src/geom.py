"""Geometry for the Actually Works logo kit, direction B "The Highlight".
All marks are pure polygons on a 1000 x 1000 canvas (y down)."""
import math, itertools
INK="#0B0B0C"; WHITE="#FFFFFF"; SIGNAL="#FFE600"

def A_spec():
    # variant a/c: the letter exactly as specified in the round-2 research
    return [(425,235),(575,235),(788,765),(592,765),(500,521),(408,765),(212,765)]

def A_param(top,bottom,apex_w,base_w,leg_w,cx=500):
    """Flat-topped wedge A. Inner edges parallel to the outer edges, so each leg
    is a constant-width stroke (leg_w measured horizontally)."""
    k=((base_w-apex_w)/2)/(bottom-top)          # dx per dy of the outer edge
    notch=bottom-(base_w/2-leg_w)/k
    return [(cx-apex_w/2,top),(cx+apex_w/2,top),(cx+base_w/2,bottom),(cx+base_w/2-leg_w,bottom),
            (cx,notch),(cx-base_w/2+leg_w,bottom),(cx-base_w/2,bottom)], notch

def swipe(cx,cy,angle,length,vth,cut,ends=None):
    """Chisel band. angle: rise to the right in degrees. length: along the top edge.
    vth: thickness measured along the end cut's vertical extent. cut: angle of the
    end faces against the horizontal (70 = the research value).
    ends: optional (left, right) lists of (ds, t) offsets, t in 0..1 from the top edge
    to the bottom edge, ds along the stroke; replaces the straight cut."""
    a=math.radians(angle); d=(math.cos(a),-math.sin(a))
    e=(-vth/math.tan(math.radians(cut)),vth)     # top edge -> bottom edge
    p0=(cx-d[0]*length/2-e[0]/2, cy-d[1]*length/2-e[1]/2)
    P=lambda s,t:(p0[0]+s*d[0]+t*e[0], p0[1]+s*d[1]+t*e[1])
    L=ends[0] if ends else [(0,0),(0,1)]
    R=ends[1] if ends else [(0,0),(0,1)]
    pts=[P(ds,t) for ds,t in L[:1]]
    pts+=[P(length+ds,t) for ds,t in R]
    pts+=[P(ds,t) for ds,t in reversed(L[1:])]
    return pts

def enclosing_circle(pts):
    best=None
    def ok(c,r): return all(math.hypot(x-c[0],y-c[1])<=r+1e-6 for x,y in pts)
    for p,q in itertools.combinations(pts,2):
        c=((p[0]+q[0])/2,(p[1]+q[1])/2); r=math.hypot(p[0]-q[0],p[1]-q[1])/2
        if ok(c,r) and (best is None or r<best[1]): best=(c,r)
    for p,q,s in itertools.combinations(pts,3):
        ax,ay=p; bx,by=q; cx_,cy_=s
        dd=2*(ax*(by-cy_)+bx*(cy_-ay)+cx_*(ay-by))
        if abs(dd)<1e-9: continue
        ux=((ax*ax+ay*ay)*(by-cy_)+(bx*bx+by*by)*(cy_-ay)+(cx_*cx_+cy_*cy_)*(ay-by))/dd
        uy=((ax*ax+ay*ay)*(cx_-bx)+(bx*bx+by*by)*(ax-cx_)+(cx_*cx_+cy_*cy_)*(bx-ax))/dd
        r=math.hypot(ax-ux,ay-uy)
        if ok((ux,uy),r) and (best is None or r<best[1]): best=((ux,uy),r)
    return best

def fit(A,S,R=390.0,centre=(500,500),wx=0.3,wy=0.4):
    """Place the mark in the avatar. The circle centre sits between the centre of the
    letter and the centre of the smallest circle around letter + swipe (so the A is
    not pushed up by the swipe), then everything is scaled until the farthest point
    is exactly R from the centre."""
    P=A+S; (ex,ey),_=enclosing_circle(P)
    ax=(min(x for x,y in A)+max(x for x,y in A))/2; ay=(min(y for x,y in A)+max(y for x,y in A))/2
    cx=ax+wx*(ex-ax); cy=ay+wy*(ey-ay)
    s=R/max(math.hypot(x-cx,y-cy) for x,y in P)
    f=lambda p:(centre[0]+(p[0]-cx)*s, centre[1]+(p[1]-cy)*s)
    return [f(p) for p in A],[f(p) for p in S], s, (cx,cy)

def pts(poly): return " ".join(f"{round(x,2):g},{round(y,2):g}" for x,y in poly)
def polygon(poly,fill): return f'<polygon points="{pts(poly)}" fill="{fill}"/>'

def mark_svg(A,S,mode,bg=True,size=None):
    """dark: swipe over the letter. light: letter over the swipe."""
    wh=f' width="{size}" height="{size}"' if size else ''
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"{wh}>'
    if mode=="dark":
        if bg: s+=f'<rect width="1000" height="1000" fill="{INK}"/>'
        s+=polygon(A,WHITE)+polygon(S,SIGNAL)
    else:
        if bg: s+=f'<rect width="1000" height="1000" fill="{WHITE}"/>'
        s+=polygon(S,SIGNAL)+polygon(A,INK)
    return s+'</svg>'

def marker_swipe(cx=507.5,cy=584.1,angle=7.0,length=722.0,vth=152.0):
    a=math.radians(angle); d=(math.cos(a),-math.sin(a)); n=(math.sin(a),math.cos(a))  # n: across, downward
    th=vth*math.cos(a)                       # perpendicular thickness at the start
    P=lambda s,v:(cx+s*d[0]+v*n[0], cy+s*d[1]+v*n[1])   # s along from centre, v across from centre line
    h=length/2; t0=th/2; t1=th*0.95/2
    # a straight 70-degree cut would run from s=+39 (top) to s=-39 (bottom) at each end
    return [P(-h+31,-t0),                    # top-left
            P(h+47,-t1),                     # top-right (the hand lifts: a little further out)
            P(h+22,-t1+0.40*th),             # right end, facet break (7 outside the straight cut)
            P(h-33,t1),                      # bottom-right
            P(-h-47,t0),                     # bottom-left
            P(-h-25,t0-0.40*th)]             # left end, facet break (9 outside the straight cut)

# ---------------- the three variants (master coordinates) ----------------
def variants():
    V={}
    # a: B2 clean, exactly as specified
    V['a']=dict(name="B2 clean (as specified)",A=A_spec(),
                S=[(177.3,553.0),(892.3,465.2),(837.7,615.2),(122.7,703.0)])
    # b: optically corrected (see README)
    Ab,notch=A_param(top=228,bottom=772,apex_w=172,base_w=616,leg_w=214)
    V['b']=dict(name="B2 optical",A=Ab,notch=notch,
                S=swipe(cx=506,cy=588,angle=8,length=742,vth=166,cut=66))
    # c: B1 marker. Long edges straight; the band narrows by 5% toward the lift-off
    # end; each end is a two-facet cut at its own angle (no zigzag, no curve).
    V['c']=dict(name="B1 marker (hand-cut ends)",A=A_spec(),S=marker_swipe())
    return V
