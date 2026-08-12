# -*- coding: utf-8 -*-
"""批次审计汇总：跑全部审计并输出 UTF-8 汇总"""
import subprocess, sys, io

sys.stdout.reconfigure(encoding="utf-8")

SCRIPTS = ["_xref_audit.py", "_img_audit.py", "_render_check.py", "_fignum_audit.py", "_html_check.py"]
for s in SCRIPTS:
    r = subprocess.run([sys.executable, s], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")
    lines = [l for l in out.splitlines() if l.strip()]
    print("=" * 12, s)
    print("\n".join(lines[-8:]))
