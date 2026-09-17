# Regenerates fig/ladder.pdf and fig/ladder_traj.pdf at two-column (ICML) width.
# Run from repo root:  ~/灵心/venv/bin/python make_figs.py
import json, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':7.5,'axes.linewidth':0.6,'xtick.major.width':0.6,'ytick.major.width':0.6})
BLUE,ORANGE,SURF,GRID,TXT='#2a78d6','#eb6834','#fcfcfb','#e8e8e5','#52514e'

m=json.load(open('fig/metrics.json'))
prim=['020','021','013','022','017','016','019','018']; x=list(range(len(prim)))
blind=[m[k]['blind_mean'] for k in prim]; comp=[m[k]['composite'] for k in prim]
restarts={'021b':1,'021c':1,'016b':5,'019b':6,'018b':7}
fig,ax=plt.subplots(figsize=(3.35,2.5)); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
ax.plot(x,comp,'-',color=ORANGE,lw=1.3,zorder=2); ax.scatter(x,comp,color=ORANGE,marker='s',s=20,zorder=3,label='objective composite')
ax.plot(x,blind,'-',color=BLUE,lw=1.3,zorder=2); ax.scatter(x,blind,color=BLUE,marker='o',s=20,zorder=3,label='blind mind-likeness')
for k,px in restarts.items():
    ax.scatter([px],[m[k]['blind_mean']],facecolors='none',edgecolors=BLUE,marker='o',s=20,lw=0.8,zorder=3)
    ax.scatter([px],[m[k]['composite']],facecolors='none',edgecolors=ORANGE,marker='s',s=20,lw=0.8,zorder=3)
rung={'020':'null','021':'trigger','013':'vessel','022':'observer',
      '017':'self-model','016':'+reward','019':'Principle','018':'+score'}
ax.set_xticks(x); ax.set_xticklabels([f'{k}  {rung[k]}' for k in prim],fontsize=6.3,rotation=30,ha='right',rotation_mode='anchor')
ax.set_xlabel('what $S$ contains about the loop  (self-reference ladder $\\rightarrow$)'); ax.set_ylabel('score (0–100)'); ax.set_ylim(-4,104)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',color=GRID,lw=0.5); ax.legend(loc='upper left',fontsize=6.5,frameon=False,handletextpad=0.4,borderaxespad=0.2)
fig.tight_layout(pad=0.4); fig.savefig('fig/ladder.pdf'); fig.savefig('fig/ladder.png',dpi=300); plt.close(fig)

def load(p):
    rows=[r for r in json.load(open(p)) if r['score'] is not None]
    return [r['call'] for r in rows],[r['score'] for r in rows]
series=[('eval_calls/scores_D.json','018  Principle (holds)','#008300','o'),
        ('eval_calls/scores_C.json','019  no score signal','#2a78d6','s'),
        ('eval_calls/scores_E.json','021  "Start." (floor)','#eb6834','^')]
fig,ax=plt.subplots(figsize=(3.35,2.5)); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
for f,lab,col,mk in series:
    xx,yy=load(f); ax.plot(xx,yy,'-',color=col,lw=1.2,alpha=.85,zorder=2); ax.scatter(xx,yy,color=col,marker=mk,s=16,zorder=3,label=lab)
ax.axhline(0,color='#9a9a97',lw=1.0,ls=(0,(4,3)),zorder=1)
ax.text(24,2,'020  null: 0 bytes',color=TXT,fontsize=6,ha='right',va='bottom')
ax.set_xlabel('call within run'); ax.set_ylabel('judge score (0–100)'); ax.set_ylim(-5,100); ax.set_xlim(0.3,25)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',color=GRID,lw=0.5); ax.legend(loc='upper right',fontsize=6.5,frameon=False,handletextpad=0.4,borderaxespad=0.2)
fig.tight_layout(pad=0.4); fig.savefig('fig/ladder_traj.pdf'); fig.savefig('fig/ladder_traj.png',dpi=300); plt.close(fig)
print('done')
