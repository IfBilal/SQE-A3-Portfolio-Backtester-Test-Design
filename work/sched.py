import json, plan, plan_bva
KEY={'BT':'bt','MC':'mc','SW':'sw','OP':'op','EF':'ef','LD':'ld','TV':'tv','RB':'rb'}
order={f[0]:i for i,f in enumerate(plan.FORMS)}
FL=sorted(plan.FIELDS,key=lambda x:order[x[0]])
BCL=sorted(plan_bva.BC,key=lambda x:order[x[0]])
S=[]; ec=0
for form,field,rows in FL:
    for (desc,rep,typ,exp,sets,mode) in rows:
        ec+=1
        S.append(dict(id='TC-EP-%03d'%ec, ec='EC-%03d'%ec, kind='EP', form=form, field=field, desc=desc, rep=rep, typ=typ, exp=exp, sets=sets, mode=mode, key=KEY.get(form)))
for i,(desc,rep,exp,sets,mode) in enumerate(plan.STRONG,1):
    S.append(dict(id='TC-EP-S%d'%i, ec='multiple', kind='EPS', form='BT', field='multiple fields', desc=desc, rep=rep, typ='VEC/IEC mix', exp=exp, sets=sets, mode=mode, key='bt'))
n=0
for bi,(form,field,ecref,desc,bval,cases) in enumerate(BCL,1):
    for (val,pos,sets,exp,mode) in cases:
        n+=1
        S.append(dict(id='TC-BVA-%03d'%n, bc='BC-%03d'%bi, kind='BVA', form=form, field=field, desc=desc, rep=val, pos=pos, exp=exp, sets=sets, mode=mode, key=KEY.get(form), bval=bval, ecref=ecref))
json.dump(S, open('schedule.json','w'), indent=1, ensure_ascii=False)
print(len(S))
