from ldap3 import Server, Connection

# LDAP 서버 주소 (도메인 컨트롤러 IP나 호스트 이름)
ldap_server = '192.168.0.10'  # ← 여기에 네 서버 주소 입력

# 서버 객체 생성
server = Server(ldap_server, get_info=None)
conn = Connection(server, authentication=None)

# 익명 바인딩 시도
if not conn.bind():
    print("[!] 익명 바인딩 실패")
    exit()

# RootDSE에서 모든 속성 조회
conn.search(search_base='',
            search_filter='(objectClass=*)',
            search_scope='BASE',
            attributes=['*'])  # 모든 속성 요청

# 결과 출력
print("[+] RootDSE 전체 속성:")
for attr, value in conn.entries[0].entry_attributes_as_dict.items():
    print(f" - {attr}: {value}")

conn.unbind()
