from ldap3 import Server, Connection, SUBTREE

server = Server('192.168.0.10')
conn = Connection(server, authentication=None)

if not conn.bind():
    print("[!] 익명 바인딩 실패")
    exit()

# RootDSE에서 Base DN 추출
conn.search('', '(objectClass=*)', search_scope='BASE', attributes=['defaultNamingContext'])
base_dn = str(conn.entries[0]['defaultNamingContext'])

# 테스트 대상 속성 리스트
attributes_to_test = ['sAMAccountName', 'userPassword', 'memberOf', 'description', 'lastLogon', 'cn']

print(f"[*] Base DN: {base_dn}")
print("[*] 속성별 접근 가능 여부:")

# 속성별 테스트 실행
for attr in attributes_to_test:
    conn.search(search_base=base_dn,
                search_filter='(objectClass=*)',
                search_scope=SUBTREE,
                attributes=[attr],
                size_limit=1)
    if conn.entries:
        print(f"[!] '{attr}' 속성 노출됨 → {conn.entries[0].entry_attributes_as_dict}")
    else:
        print(f"[+] '{attr}' 접근 차단됨")

conn.unbind()
