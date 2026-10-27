#!/usr/bin/env python3
"""Source-preserving conversation tree / flattened export adapter; standard library only."""
import argparse, hashlib, json, pathlib, zipfile, re

def digest(b): return hashlib.sha256(b).hexdigest()

def text_parts(obj):
    """Extract text representations; non-text remains in unchanged source JSON."""
    if isinstance(obj,str): return [obj]
    if isinstance(obj,list):
        result=[]
        for item in obj: result.extend(text_parts(item))
        return result
    if isinstance(obj,dict):
        if isinstance(obj.get('text'),str): return [obj['text']]
        if isinstance(obj.get('content'),str): return [obj['content']]
        if 'parts' in obj: return text_parts(obj['parts'])
        if 'contents' in obj: return text_parts(obj['contents'])
    return []

def from_tree(source):
    mapping=source['mapping']; nid=source.get('current_node'); rev=[]; seen=set(); fault=None
    while nid is not None:
        if nid in seen: fault='parent_cycle'; break
        seen.add(nid)
        node=mapping.get(nid)
        if not node: fault='missing_parent:'+str(nid); break
        msg=node.get('message')
        if msg:
            content=msg.get('content') or {}; parts=text_parts(content)
            rev.append({'id':msg.get('id') or nid,'node_id':nid,'role':(msg.get('author') or {}).get('role'),
                'channel':msg.get('channel'),'created_at':msg.get('create_time'),
                'content_type':content.get('content_type') if isinstance(content,dict) else None,
                'text_parts':parts,'text':''.join(parts),'text_part_count':len(parts),
                'has_unrendered_content':not parts and bool(content),'source':'tree'})
        nid=node.get('parent')
    rev.reverse()
    return rev,{'active_branch_nodes':len(seen),'total_mapping_nodes':len(mapping),'branch_fault':fault,
                'nonactive_nodes':len(mapping)-len(seen)}

def from_flat(source):
    return [{'id':item.get('id'),'ids':item.get('ids'),'role':item.get('role'),'created_at':item.get('created_at'),
            'text_parts':text_parts(item.get('contents',[])),
            'text':''.join(text_parts(item.get('contents',[]))),
            'text_part_count':len(text_parts(item.get('contents',[]))),'source':'flat'} for item in source]

def render_md(rows,title):
    # JSON literals preserve escaped message contents for exact round-trip recovery.
    out=['# '+title,'','ACTIVE BRANCH transcript derived from supplied source.',
         'Each `text_json` field round-trips to source-extracted text.',
         'Non-text and alternative branches remain in unchanged source JSON.','']
    for i,r in enumerate(rows,1):
        out += [f'## Message {i} — {r.get("role") or "unknown"}',
                f'- ID: `{r.get("id")}`',f'- Channel: `{r.get("channel")}`',
                f'- Source content type: `{r.get("content_type")}`','',
                '```json',json.dumps({'text_json':r['text'],'text_parts':r['text_parts']},ensure_ascii=False,indent=2),
                '```','']
    return '\n'.join(out)+'\n'

def validate_md(md,rows):
    matches=re.findall(r'```json\n(.*?)\n```',md,re.S)
    if len(matches)!=len(rows): return False
    try: return all(json.loads(s)['text_json']==r['text'] and json.loads(s)['text_parts']==r['text_parts'] for s,r in zip(matches,rows))
    except Exception: return False

def archive_run(archive,out):
    with zipfile.ZipFile(archive) as z:
        records=[]
        for name in z.namelist():
            if name.startswith('__MACOSX') or not name.endswith('.json') or '/._' in name or pathlib.PurePosixPath(name).name.startswith('._'): continue
            raw=z.read(name)
            try: obj=json.loads(raw)
            except Exception: continue
            if isinstance(obj,dict) and isinstance(obj.get('mapping'),dict):
                kind='tree'; rows,meta=from_tree(obj); title=obj.get('title') or name
            elif isinstance(obj,list) and obj and isinstance(obj[0],dict) and 'contents' in obj[0]:
                kind='flat'; rows=from_flat(obj); meta={}; title=name
            else: continue
            base=pathlib.PurePosixPath(name).stem
            rec={'source_name':name,'kind':kind,'conversation_id':obj.get('conversation_id') if kind=='tree' else obj[0].get('chatGroupId'),
                 'title':title,'source_sha256':digest(raw),'records':len(rows),
                 'nontext_or_empty':sum(not r['text_parts'] for r in rows),**meta}
            md=render_md(rows,title)
            rec['markdown_round_trip_pass']=validate_md(md,rows)
            prefix=f'EXPORTS/{kind}/{base}'
            records.append((prefix,raw,rows,md,rec))
    manifest={'input_archive':str(archive),'input_archive_sha256':digest(pathlib.Path(archive).read_bytes()),
              'export_count':len(records),'exports':[r[4] for r in records],
              'qualification':'SOURCE_RELATIVE_ONLY_NOT_CHAT_UI_COMPLETE'}
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as zz:
        for prefix,raw,rows,md,rec in records:
            zz.writestr(prefix+'.source.json',raw)
            zz.writestr(prefix+'.active_branch.json',json.dumps(rows,ensure_ascii=False,indent=2))
            zz.writestr(prefix+'.md',md)
        zz.writestr('QA_MANIFEST.json',json.dumps(manifest,indent=2,ensure_ascii=False))
    with zipfile.ZipFile(out) as z: assert z.testzip() is None
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source_zip');p.add_argument('output_zip');a=p.parse_args()
    m=archive_run(a.source_zip,a.output_zip)
    print(json.dumps({'output':a.output_zip,'exports':m['export_count'],
      'round_trip_passes':sum(r['markdown_round_trip_pass'] for r in m['exports'])}))
