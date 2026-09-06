import sqlite3,json,urllib.request,urllib.error,getpass,sys
from pathlib import Path
root=Path(__file__).resolve().parent; db=root/'database'/'ahtech.db'
if not db.exists(): print('Banco V23 não encontrado em database/ahtech.db');sys.exit(1)
url=input('URL do sistema online (ex. https://gestao.ahtech.com.br): ').strip().rstrip('/')
email=input('E-mail do administrador: ').strip(); password=getpass.getpass('Senha: ')
con=sqlite3.connect(db); row=con.execute('SELECT revision,state_gzip FROM app_state WHERE id=1').fetchone();con.close()
if not row: print('O banco V23 está vazio.');sys.exit(1)
import gzip
state=json.loads(gzip.decompress(row[1]).decode('utf-8'))
def req(path,method='GET',payload=None,cookie=None):
 data=json.dumps(payload).encode() if payload is not None else None; r=urllib.request.Request(url+path,data=data,method=method,headers={'Content-Type':'application/json'}); 
 if cookie:r.add_header('Cookie',cookie)
 return urllib.request.urlopen(r,timeout=30)
r=req('/api/auth/login','POST',{'email':email,'password':password}); cookie=r.headers.get('Set-Cookie').split(';',1)[0]; print('Login online OK.')
r=req('/api/state','GET',cookie=cookie); current=json.loads(r.read());
payload={'revision':int(current.get('revision',0)),'state':state,'clientId':'migration-v23','clientName':'Migração V23'}
try:r=req('/api/state','PUT',payload,cookie=cookie);print('Migração concluída:',r.read().decode())
except urllib.error.HTTPError as e: print('Falha:',e.read().decode());sys.exit(2)
