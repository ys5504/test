from ldap3 import Server, Connection, ALL, SUBTREE

# 대상 AD 서버 정보
ldap_server = '192.168.0.10'  # 도메인 컨트롤러 IP 또는 호스트명
base_dn = ''  # RootDSE를 먼저 조회해서 알 수 있음

# 서버 객체 생성
server = Server(ldap_server, get_info=ALL)

# 익명 바인딩 시도
conn = Connection(server, authentication=None, raise_exceptions=False)

if not conn.bind():
    print("[!] 익명 바인딩 실패")
    print(conn.result)
else:
    print("[+] 익명 바인딩 성공")

    # RootDSE 정보 조회
    conn.search(search_base='', search_filter='(objectClass=*)',
                search_scope='BASE', attributes=['defaultNamingContext'])

    naming_context = conn.entries[0]['defaultNamingContext']
    print("[*] 도메인 DN (Naming Context):", naming_context)

    # 사용자 목록 일부 조회 (최대 10개)
    conn.search(search_base=str(naming_context),
                search_filter='(objectClass=user)',
                search_scope=SUBTREE,
                attributes=['sAMAccountName', 'cn'],
                size_limit=10)

    for entry in conn.entries:
        print("[+] 사용자:", entry['sAMAccountName'], "| 이름:", entry['cn'])

    conn.unbind()
