from ldap3 import Server, Connection, ALL, SUBTREE

ldap_server = '192.168.0.10'  # ← 여기에 도메인 컨트롤러 IP
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, authentication=None, raise_exceptions=False)

if not conn.bind():
    print("[!] 익명 바인딩 실패:", conn.result)
else:
    print("[+] 익명 바인딩 성공")

    # 1. 도메인 이름 (base_dn) 얻기
    conn.search(search_base='', search_filter='(objectClass=*)',
                search_scope='BASE', attributes=['defaultNamingContext'])

    base_dn = str(conn.entries[0]['defaultNamingContext'])
    print("[*] Base DN:", base_dn)

    # 2. 사용자 목록 조회
    conn.search(search_base=base_dn,
                search_filter='(objectClass=user)',
                search_scope=SUBTREE,
                attributes=['sAMAccountName', 'cn'],
                size_limit=10)

    if conn.entries:
        for entry in conn.entries:
            print("[+] 사용자:", entry['sAMAccountName'], "| 이름:", entry['cn'])
    else:
        print("[!] 사용자 정보 없음 (접근 권한 부족 or 사용자 없음)")

    conn.unbind()
