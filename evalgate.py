import json
import os
import sys
from pathlib import Path
from statistics import mean, median

def evaluate(candidate):
    docs=[json.loads(p.read_text()) for p in sorted(Path('documents').glob('*.json'))]
    if not docs or len({d['id'] for d in docs})!=len(docs):
        raise ValueError('Expected unique labeled documents')
    runs=[]
    for name in ('baseline',candidate):
        records=json.loads(Path(name+'.json').read_text())
        by_id={r['id']:r for r in records}
        if len(by_id)!=len(records):
            raise ValueError('Duplicate output record')
        runs.append(by_id)
    for run in runs:
        if set(run)!={d['id'] for d in docs}:
            raise ValueError('Mismatched evaluation corpus')
    slices=[]
    for layout in ('all','clean','scan','ambiguous'):
        group=[d for d in docs if layout=='all' or d['layout']==layout]
        for field in docs[0]['fields']:
            correct=[[run[d['id']]['fields'].get(field)==d['fields'][field] for d in group] for run in runs]
            delta=mean(int(b)-int(a) for a,b in zip(*correct))
            status='insufficient' if len(group)<5 else 'pass'
            if status=='pass' and layout=='scan' and field=='total' and delta<0:
                status='block'
            slices.append(dict(layout=layout,field=field,n=len(group),baseline=mean(correct[0]),
                candidate=mean(correct[1]),paired_delta=delta,status=status,
                regressions=[d['id'] for d,a,b in zip(group,*correct) if a and not b]))
    metrics=[]
    for run in runs:
        complete=sum(run[d['id']]['fields']==d['fields'] for d in docs)
        metrics.append(dict(accuracy=mean(run[d['id']]['fields'].get(f)==v for d in docs for f,v in d['fields'].items()),
            median_ms=median(r['ms'] for r in run.values()),
            microdollars_per_correct_document=sum(r['microdollars'] for r in run.values())/complete if complete else None))
    return dict(baseline=metrics[0],candidate=metrics[1],slices=slices)

if __name__=='__main__':
    report=evaluate(sys.argv[1] if len(sys.argv)>1 else Path('release.txt').read_text().strip())
    print(json.dumps(report,indent=2))
    if 'GITHUB_STEP_SUMMARY' in os.environ:
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as log:
            prefix=os.path.relpath(os.getcwd(),os.environ['GITHUB_WORKSPACE']).replace(os.sep,'/').strip('.')
            prefix=(prefix+'/') if prefix else ''
            for row in report['slices']:
                if row['status']!='pass':
                    print(row['layout'],row['field'],row['status'],file=log)
                    for doc in row['regressions']:
                        print(f"- [{doc}](https://github.com/{os.environ['GITHUB_REPOSITORY']}/blob/{os.environ['GITHUB_SHA']}/{prefix}documents/{doc}.json)",file=log)
    sys.exit(any(r['status']=='block' for r in report['slices']))

