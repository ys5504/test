from ldap3 import Server, Connection, ALL, SUBTREE

# AD 서버 주소 (IP or 도메인 컨트롤러 호스트명)
ldap_server = '192.168.0.10'

server = Server(ldap_server, get_info=ALL)
conn = Connection(server, authentication=None, raise_exceptions=False)

if not conn.bind():
    print("[!] 익명 바인딩 실패:", conn.result)
    exit()

print("[+] 익명 바인딩 성공")

# 1. RootDSE 정보 확인
conn.search(search_base='', search_filter='(objectClass=*)',
            search_scope='BASE', attributes=['defaultNamingContext', 'supportedLDAPVersion'])

entry = conn.entries[0]
base_dn = str(entry['defaultNamingContext'])
print("[*] Base DN:", base_dn)
print("[*] 지원 LDAP 버전:", entry['supportedLDAPVersion'])

# 2. OU 정보 노출 여부 확인
print("\n[*] 조직 단위(OU) 노출 여부:")
conn.search(search_base=base_dn,
            search_filter='(objectClass=organizationalUnit)',
            search_scope=SUBTREE,
            attributes=['ou'], size_limit=10)

if conn.entries:
    for e in conn.entries:
        print("  [+]", e.entry_dn)
else:
    print("  [-] OU 정보 접근 차단")

# 3. 사용자 정보 노출 여부 확인
print("\n[*] 사용자(user) 객체 노출 여부:")
conn.search(search_base=base_dn,
            search_filter='(objectClass=user)',
            search_scope=SUBTREE,
            attributes=['cn', 'sAMAccountName'], size_limit=5)

if conn.entries:
    for e in conn.entries:
        print("  [!] 사용자 노출됨:", e['sAMAccountName'], "| 이름:", e['cn'])
else:
    print("  [+] 사용자 객체 접근 차단 (정상)")

# 4. 그룹 정보 노출 여부 확인
print("\n[*] 그룹(group) 객체 노출 여부:")
conn.search(search_base=base_dn,
            search_filter='(objectClass=group)',
            search_scope=SUBTREE,
            attributes=['cn'], size_limit=5)

if conn.entries:
    for e in conn.entries:
        print("  [!] 그룹 노출됨:", e['cn'])
else:
    print("  [+] 그룹 객체 접근 차단 (정상)")

# 5. 기타: Configuration/Schema 접근 여부 확인
print("\n[*] Configuration 접근 여부:")
conf_dn = "CN=Configuration," + base_dn
conn.search(search_base=conf_dn, search_filter='(objectClass=*)',
            search_scope='BASE', attributes=['cn'])
if conn.entries:
    print("  [!] Configuration 객체 접근 가능")
else:
    print("  [+] 접근 차단")

conn.unbind()
