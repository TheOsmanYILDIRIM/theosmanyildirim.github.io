"""Rebuild the corpus aggregate from the upstream Turkish FrequencyWords file.

Upstream is a word-rank list built from subtitles; it is NOT a balanced Turkish
prose corpus. No automatic network traffic unless --download is selected.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import urllib.request
from pathlib import Path

SOURCE_URL = 'https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2016/tr/tr_50k.txt'
SHA1_BLOB = 'f7c73d59b5654be9b10c38a17ce65fbc82ad3a35'
ALPHABET = 'abcçdefgğhıijklmnoöprsştuüvyz'
ALLOWED = re.compile(r'^[abcçdefgğhıijklmnoöprsştuüvyz]{2,25}$')
INDEX = {letter:i for i,letter in enumerate(ALPHABET)}

def js_fnv(word: str) -> int:
    h=2166136261
    for ch in word:
        h=((h^ord(ch))*16777619) & 0xffffffff
    return h

def aggregate(text: str, *, limit: int=15000) -> dict:
    def empty():return {'words':0,'uni':[0]*29,'bi':[0]*(29*29)}
    train,test=empty(),empty()
    prompts=[]
    for line in text.splitlines()[:limit]:
        fields=line.split()
        if len(fields)!=2 or not fields[1].isdigit():continue
        word=fields[0].replace('İ','i').replace('I','ı').lower()
        if not ALLOWED.fullmatch(word):continue
        portion=test if js_fnv(word)%5==0 else train
        portion['words']+=1
        weight=max(1,round(math.sqrt(int(fields[1]))))
        prev=-1
        for ch in word:
            j=INDEX[ch]
            portion['uni'][j]+=weight
            if prev>=0: portion['bi'][prev*29+j]+=weight
            prev=j
        if len(prompts)<120 and 3<=len(word)<=14 and word not in prompts:prompts.append(word)
    # base36 compact encoding, exactly matching web in-browser decoder.
    def b36(n:int)->str:
        if not n:return '0'
        digits='0123456789abcdefghijklmnopqrstuvwxyz';out=''
        while n:n,d=divmod(n,36);out=digits[d]+out
        return out
    for part in (train,test):
        for key in ('uni','bi'):part[key]='.'.join(b36(v) for v in part[key])
    return {'alphabet':ALPHABET,
      'source':'HermitDave FrequencyWords/OpenSubtitles2016 Turkish 2016; first 15000 ranked entries filtered to 29 Turkish letters',
      'source_blob_sha':SHA1_BLOB,
      'weighting':'round(sqrt(count)); FNV1a(word UTF-16) modulo 5 = 0 held out',
      'source_url':'https://github.com/hermitdave/FrequencyWords/blob/master/content/2016/tr/tr_50k.txt',
      'train':train,'test':test,'prompts':prompts}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,help='Existing complete tr_50k.txt file')
    p.add_argument('--download',action='store_true',help='Download from GitHub and verify exact blob')
    p.add_argument('--out',type=Path,default=Path('data/corpus_stats.json'))
    args=p.parse_args()
    if bool(args.input)==bool(args.download):
        p.error('Specify exactly one of --input or --download')
    blob=args.input.read_bytes() if args.input else urllib.request.urlopen(SOURCE_URL,timeout=40).read()
    sha=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\\x00'+blob).hexdigest()
    if sha!=SHA1_BLOB:raise SystemExit(f'Corpus version conflict: {sha} != {SHA1_BLOB}')
    data=aggregate(blob.decode('utf-8-sig'))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\\n',encoding='utf-8')
    print('OK:',data['train']['words']+data['test']['words'],'eligible entries; split:',
          data['train']['words'],data['test']['words'])

if __name__=='__main__':main()
