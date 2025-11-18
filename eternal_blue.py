#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MS17-010 (EternalBlue) Vulnerability Scanner for Python 2.6.6
# Safe diagnostic-only version. No exploit.
#
# Requires: impacket <= 0.9.15 (Python 2.6 compatible)

from impacket import smb, smbconnection
import sys

def check_ms17010(ip):
    try:
        print("[*] Connecting to SMB: %s" % ip)
        conn = smbconnection.SMBConnection(ip, ip, sess_port=445, timeout=4)

        try:
            conn.login("", "")
        except:
            # guest / anonymous login 실패는 정상
            pass

        tid = conn.connectTree("IPC$")
        fid = conn.openFile(tid, "\\srvsvc", desiredAccess=1)

    except Exception as e:
        # 취약점 여부 확인을 위한 핵심 부분: 
        # MS17-010 시스템은 특유의 STATUS_INSUFF_SERVER_RESOURCES 오류를 반환함.
        error_msg = str(e)

        if "STATUS_INSUFF_SERVER_RESOURCES" in error_msg:
            print("[+] Vulnerable to MS17-010 (EternalBlue)!")
            return True

        if "STATUS_OBJECT_NAME_NOT_FOUND" in error_msg:
            print("[-] Not Vulnerable (Named pipe not available).")
            return False

        print("[-] Unknown SMB response, cannot confirm.")
        print("[-] Error: %s" % error_msg)
        return False

    print("[-] Not Vulnerable (Normal SMB response).")
    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ms17010_scan.py <target_ip>")
        sys.exit(1)

    target = sys.argv[1]
    check_ms17010(target)
