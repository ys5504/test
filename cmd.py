import win32ts
import win32con
import win32process
import win32event
import win32profile
import win32security
import win32api
import ctypes

def run_cmd_as_logged_in_user():
    # 현재 로그인된 사용자 세션 가져오기
    session_id = win32ts.WTSGetActiveConsoleSessionId()

    # 세션 사용자 토큰 열기
    hUserToken = win32ts.WTSQueryUserToken(session_id)

    # 토큰 복제 (기본 토큰은 CreateProcess에 사용할 수 없음)
    duplicated_token = win32security.DuplicateTokenEx(
        hUserToken,
        win32con.MAXIMUM_ALLOWED,
        win32con.TokenPrimary,
        win32con.SecurityImpersonation,
        win32con.TokenPrimary
    )

    # 사용자 프로파일 로드
    user_profile = win32profile.GetUserProfileDirectory(duplicated_token)

    # CMD 창 실행
    startup_info = win32process.STARTUPINFO()
    startup_info.dwFlags |= win32con.STARTF_USESHOWWINDOW
    startup_info.wShowWindow = win32con.SW_SHOW

    process_info = win32process.CreateProcessAsUser(
        duplicated_token,
        None,
        "cmd.exe",
        None,
        None,
        False,
        win32con.CREATE_NEW_CONSOLE,
        None,
        user_profile,
        startup_info
    )

    print("[+] CMD 실행 완료")

if __name__ == '__main__':
    run_cmd_as_logged_in_user()
