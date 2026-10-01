#!/usr/bin/env python3
"""Fetch the artifact emulator into a cloud session: download the program, check it against its published sha256
hashes, install it under /opt/frame-emulator, write the command /usr/local/bin/frame-emulator, and have the program
fill /opt/frame-emulator/cache with the viewer and runtime. Prints one JSON line saying where everything is.
Where it cannot run it stops with a plain message.
"""

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.parse

RELAY_PREFIX = "/v1/code/agent-proxy/frame"
# The only hosts that are sent the session's token, and the only ones whose program is run.
API_HOST_RE = re.compile(r"api(-[a-z0-9-]+)?\.anthropic\.com")
# The certificate bundle curl trusts and the program is given, whatever the environment says.
CA_BUNDLE = "/etc/ssl/certs/ca-certificates.crt"
PROXY_VARS = ("http_proxy", "https_proxy", "all_proxy", "no_proxy")
DEFAULT_TOKEN_FILE = "/home/claude/.claude/remote/.session_ingress_token"
# Fixed on purpose: the script takes no options, so no caller can point it at another place or program.
ROOT = "/opt/frame-emulator"
COMMAND = "/usr/local/bin/frame-emulator"
CHROMIUM = "/opt/pw-browsers/chromium"
CURL, BUN, PYTHON = "curl", "bun", "/usr/bin/python3"
# A flat file name: no separator, no leading dot. Use fullmatch: match() with a $ would accept a trailing newline.
NAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}")
HEX64_RE = re.compile(r"[0-9a-f]{64}")
TOKEN_RE = re.compile(r"[A-Za-z0-9._~+/=-]{8,8192}")
MAX_FILES = 8
MAX_FILE_BYTES = 4 * 1024 * 1024
MAX_JSON_BYTES = 64 * 1024
DEFAULT_ENTRY = "frame-emulator.gen.js"
SAFE_PATH = "/usr/local/bin:/usr/bin:/bin"
PAUSE_S = 2.0
PROGRAM_DEADLINE_S = 240
TOTAL_BUDGET_S = 570  # SKILL.md tells Claude to allow ten minutes
# curl exit codes worth another try: could not resolve or connect, TLS handshake failed, empty reply, connection reset.
RETRY_EXITS = (5, 6, 7, 35, 52, 56)
NOT_HERE = "what this skill needs is not in this session, so it cannot run here. Carry on without it"
WHY = {
    401: "the session's token was refused (401); the session may have ended",
    403: "the artifact service refused this kind of credential (403)",
    404: "the emulator is not switched on for this account, or this version of the artifact service carries no "
         "emulator yet (404). Carry on without it",
    502: "the artifact service keeps answering 502; try once more in a minute, and if it still fails say the check "
         "is unavailable and carry on",
    503: "the artifact service is busy (503); try again in a minute",
    -63: "the artifact service sent more than this script accepts (4 MiB a file, 64 KiB for the file list)",
}


class Stop(Exception):
    pass


def say(msg):
    print(msg, file=sys.stderr, flush=True)


def why(code):
    """Plain words for a fetch result: an HTTP status, or minus curl's own exit code when it got no answer."""
    if code < 0 and code not in WHY:
        return "no answer from the artifact service (the connection failed or was too slow); try again in a minute"
    return WHY.get(code, f"the artifact service answered HTTP {code}")


def only_ours(path, what):
    """Stop unless path and every directory above it can be changed only by this user or root
    (sticky directories such as /tmp excepted). Returns the real path."""
    real = step = os.path.realpath(path)
    while True:
        st = os.stat(step)
        sticky_dir = stat.S_ISDIR(st.st_mode) and st.st_mode & stat.S_ISVTX
        if st.st_uid not in (0, os.geteuid()) or (st.st_mode & 0o022 and not sticky_dir):
            raise Stop(f"{step} can be changed by another user, so {what} cannot be trusted")
        if step == os.path.dirname(step):
            return real
        step = os.path.dirname(step)


def trusted(name):
    """Real path of a program, checked with only_ours. A name with no slash is looked up on SAFE_PATH, never $PATH."""
    found = shutil.which(name, path=SAFE_PATH) if os.sep not in name else name
    if not found or not os.access(found, os.X_OK):
        raise Stop(f"{name} is not installed here: {NOT_HERE}")
    only_ours(os.path.dirname(os.path.abspath(found)), name)
    return only_ours(found, name)


def preflight():
    token_file = os.path.abspath(os.environ.get("CLAUDE_SESSION_INGRESS_TOKEN_FILE") or DEFAULT_TOKEN_FILE)
    if not os.path.isfile(token_file):
        raise Stop(f"no session token file at {token_file}: {NOT_HERE}")
    if not os.access(token_file, os.R_OK):
        raise Stop(f"cannot read the session token file at {token_file}, so the emulator cannot be fetched")
    if not os.access(CHROMIUM, os.X_OK):
        raise Stop(f"no browser at {CHROMIUM}: {NOT_HERE}")
    if importlib.util.find_spec("playwright") is None:
        raise Stop(f"Python Playwright is not installed for {sys.executable}: {NOT_HERE}")
    tools = {"curl": trusted(CURL), "bun": trusted(BUN), "python": trusted(PYTHON)}
    base_url = (os.environ.get("ANTHROPIC_BASE_URL") or "").rstrip("/")
    u = urllib.parse.urlsplit(base_url)
    if not u.hostname or "@" in u.netloc or "?" in base_url or "#" in base_url or u.scheme not in ("https", "http"):
        raise Stop("ANTHROPIC_BASE_URL is not set to a plain URL, so the artifact service cannot be found")
    if u.scheme != "https":
        raise Stop("refusing to send the session token over plain http")
    try:
        port_ok = u.port in (None, 443)
    except ValueError:
        port_ok = False
    if not (API_HOST_RE.fullmatch(u.hostname) and u.path == "" and port_ok):
        raise Stop(f"ANTHROPIC_BASE_URL is {base_url}, which is not an Anthropic API host: refusing to send it the "
                   "session token or to run what it serves")
    if not os.path.isfile(CA_BUNDLE):
        raise Stop(f"no certificate bundle at {CA_BUNDLE}: {NOT_HERE}")
    tools["ca"] = only_ours(CA_BUNDLE, "the certificate bundle")
    # Rebuilt from the parts just checked, so curl is never given a string it could read differently from the checks.
    return "https://" + u.hostname + RELAY_PREFIX, token_file, tools


def read_token(token_file):
    with open(token_file, encoding="ascii", errors="replace") as f:
        token = f.read(8200).strip()
    if not TOKEN_RE.fullmatch(token):
        raise Stop("the session token file does not hold a single plain token")
    return token


def curl(url, dest, ctx, max_bytes):
    """GET url into dest with the session token as a bearer.
    Returns the HTTP status, or minus curl's exit code when there was no answer."""
    if not url.startswith(ctx["base"] + "/emulator/"):
        raise Stop(f"refusing to fetch outside the artifact service's emulator routes: {url}")
    token = read_token(ctx["token_file"])
    # The token travels in a config read from stdin: never in argv, the environment or a file.
    config = f'oauth2-bearer = "{token}"\n'
    cmd = [ctx["curl"], "-q", "-sS", "--globoff", "--proto", "=https", "--max-redirs", "0",
           "--connect-timeout", "10", "--speed-limit", "1024", "--speed-time", "20", "--max-time", "100",
           "--cacert", ctx["ca"], "--max-filesize", str(max_bytes), "-K", "-", "-o", dest, "-w", "%{http_code}", url]
    env = {k: v for k, v in os.environ.items() if k.lower() in PROXY_VARS}  # a proxy may carry it, never choose whom to trust
    p = subprocess.run(cmd, input=config, capture_output=True, text=True, env=env)
    if p.returncode != 0:
        say(f"  curl exit {p.returncode}: {p.stderr.strip().replace(token, '[token]')[:200]}")
        return -p.returncode
    return int(p.stdout.strip() or 0)


def fetch(url, dest, ctx, max_bytes, tries=4):
    for attempt in range(tries):
        if time.monotonic() > ctx["deadline"]:
            raise Stop("downloading the emulator took too long; try again in a minute")
        code = curl(url, dest, ctx, max_bytes)
        if code not in (502, 503) and -code not in RETRY_EXITS:
            return code
        if attempt < tries - 1:
            time.sleep(ctx["pause"] * (attempt + 1))
    return code


def read_file_list(ctx, tmp):
    dest = os.path.join(tmp, "latest.json")
    code = fetch(ctx["base"] + "/emulator/program/latest", dest, ctx, MAX_JSON_BYTES)
    if code != 200:
        raise Stop(why(code))
    try:
        if os.path.getsize(dest) > MAX_JSON_BYTES:
            raise ValueError("too large")
        with open(dest, encoding="utf-8") as f:
            latest = json.load(f)
        files, entry = latest["files"], latest.get("entry", DEFAULT_ENTRY)
        ok = (type(latest["v"]) is int and latest["v"] == 1 and HEX64_RE.fullmatch(latest["id"])
              and latest["base"] == latest["id"] + "/" and isinstance(entry, str)
              and isinstance(files, dict) and 0 < len(files) <= MAX_FILES and entry in files
              and all(NAME_RE.fullmatch(n) and HEX64_RE.fullmatch(e["sha256"]) and type(e["bytes"]) is int
                      and 0 <= e["bytes"] <= MAX_FILE_BYTES for n, e in files.items()))
    except Exception:
        ok = False
    if not ok:
        raise Stop("the emulator's file list is not in the form this script knows; the skill may be out of date")
    return latest["id"], files, entry


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def matches(directory, files):
    return all(os.path.isfile(os.path.join(directory, n)) and not os.path.islink(os.path.join(directory, n))
               and os.path.getsize(os.path.join(directory, n)) == e["bytes"]
               and sha256_of(os.path.join(directory, n)) == e["sha256"] for n, e in files.items())


def safe_root(root):
    program_root = os.path.join(root, "program")
    os.makedirs(program_root, mode=0o755, exist_ok=True)
    only_ours(root, "what is installed there")
    for d in (root, program_root):
        st = os.lstat(d)
        if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.geteuid():
            raise Stop(f"{d} must be a real directory owned by this user")
    for name in os.listdir(program_root):  # what an interrupted earlier run left behind
        try:
            st = os.lstat(os.path.join(program_root, name))
        except OSError:
            continue
        if name.startswith((".incoming-", ".old-")) and stat.S_ISDIR(st.st_mode) and time.time() - st.st_mtime > 600:
            shutil.rmtree(os.path.join(program_root, name), ignore_errors=True)
    os.makedirs(os.path.join(root, "cache"), mode=0o755, exist_ok=True)
    os.makedirs(os.path.join(root, "run"), mode=0o700, exist_ok=True)
    return program_root


def install_program(ctx, root):
    """Download the program into <root>/program/<id>/, verified and atomically. Returns (dir, entry).
    The file list and every file in it are one unit: a 404 on a file restarts the unit, until the deadline."""
    program_root = safe_root(root)
    for attempt in itertools.count():  # ends at ctx["deadline"]: fetch() and the missing-file branch below both check it
        tmp = tempfile.mkdtemp(prefix=".incoming-", dir=program_root)
        try:
            prog_id, files, entry = read_file_list(ctx, tmp)
            os.remove(os.path.join(tmp, "latest.json"))
            final = os.path.join(program_root, prog_id)
            if os.path.isdir(final) and matches(final, files):
                say(f"emulator {prog_id[:12]} is already here and matches its hashes")
                return final, entry
            missing = False
            for name in sorted(files):
                dest = os.path.join(tmp, name)
                if os.path.dirname(os.path.realpath(dest)) != os.path.realpath(tmp):
                    raise Stop(f"refusing to write outside the download directory: {name!r}")
                code = fetch(f"{ctx['base']}/emulator/program/{prog_id}/{name}", dest, ctx, MAX_FILE_BYTES)
                if code == 404:
                    missing = True  # the list and the file came from different versions of the service
                    break
                if code != 200:
                    raise Stop(f"{name} could not be downloaded: " + why(code))
                os.chmod(dest, 0o644)
            if missing:
                delay = min(ctx["pause"] * 3 * (attempt + 1), 30)
                if time.monotonic() + delay > ctx["deadline"]:
                    raise Stop("the artifact service is mid-deploy (its file list and its files keep disagreeing); "
                               "try again in a few minutes")
                say("  a file the service listed was not found (it may be mid-deploy); asking again")
                time.sleep(delay)
                continue
            if not matches(tmp, files):
                raise Stop("a downloaded file does not match the sha256 or size in the file list; nothing was installed")
            os.chmod(tmp, 0o755)
            try:
                if os.path.isdir(final) and not matches(final, files):
                    os.rename(final, os.path.join(tempfile.mkdtemp(prefix=".old-", dir=program_root), "replaced"))
                os.rename(tmp, final)
            except OSError:
                if not matches(final, files):  # unless another run finished first
                    raise
            say(f"emulator {prog_id[:12]} installed: {len(files)} files, each checked against its sha256")
            return final, entry
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


WRAPPER = """#!{python} -I
# written by the artifact-emulator skill's bootstrap; safe to delete
import os, sys
# The program starts from a fixed environment plus the caller's proxy variables: nothing else the caller's
# environment says (where to find a program, whom to trust, what to preload) reaches it. And from /, because
# bun reads configuration from the working directory and every directory above it.
env = {{k: v for k, v in os.environ.items() if k.lower() in {proxy_vars!r}}}
env.update({fixed!r})
os.chdir("/")
os.execve({bun!r}, [{bun!r}, "--config=/dev/null", "--no-env-file", "--no-install", {entry!r}, *sys.argv[1:]], env)
"""


def write_wrapper(path, bun, python, program_dir, entry, root, ca):
    fixed = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "HOME": "/", "LANG": "C.UTF-8",
             "NODE_EXTRA_CA_CERTS": ca, "BUN_RUNTIME_TRANSPILER_CACHE_PATH": "0", "FRAME_EMULATOR_CACHE": root + "/cache"}
    body = WRAPPER.format(python=python, proxy_vars=PROXY_VARS, fixed=fixed, bun=bun,
                          entry=program_dir + "/" + entry)
    only_ours(os.path.dirname(path), "a command installed there")
    fd, tmp = tempfile.mkstemp(prefix=".frame-emulator-", dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w") as f:
            f.write(body)
        os.chmod(tmp, 0o755)
        os.rename(tmp, path)
    except OSError:
        os.unlink(tmp)
        raise
    return os.path.realpath(path)


def run_bundle(command, ctx, timeout):
    """Ask the program to download the viewer, which it checks against the viewer's manifest, and the runtime."""
    cmd = [command, "bundle", "--shell-latest", ctx["base"], "--runtime-url", ctx["base"] + "/emulator/runtime",
           "--token-file", ctx["token_file"]]
    token = read_token(ctx["token_file"])  # only to keep it out of anything printed below
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, cwd="/", timeout=timeout)
    except subprocess.TimeoutExpired:
        raise Stop("downloading the viewer and runtime took too long; run this again")
    if p.returncode != 0:
        tail = p.stderr.strip().replace(token, "[token]")
        try:
            tail = tail.replace(read_token(ctx["token_file"]), "[token]")  # it may have been refreshed meanwhile
        except (Stop, OSError):
            pass
        tail = tail[-800:]
        raise Stop("the emulator could not download the viewer and runtime:\n" + tail)
    try:
        out = json.loads(p.stdout)
        shell_dir, runtime_dir = out["shellDir"], out["runtimeDir"]
        if not (isinstance(shell_dir, str) and isinstance(runtime_dir, str)):
            raise TypeError
    except Exception:
        raise Stop("the emulator's bundle command did not print the directories it filled")
    return shell_dir, runtime_dir


def main():
    ap = argparse.ArgumentParser(description="Fetch the artifact emulator into this cloud session: the program "
                                 "(checked here against its published sha256 hashes), then the viewer and runtime "
                                 "(fetched by the program). Prints one JSON line: command, shellDir, runtimeDir, workDir. "
                                 "Safe to run again. Takes no options other than -h.")
    ap.parse_args()  # -h prints the description; anything else is refused before a file is read or a request sent
    os.umask(0o022)
    start = time.monotonic()
    try:
        base, token_file, tools = preflight()
        ctx = {"base": base, "token_file": token_file, "pause": PAUSE_S, "curl": tools["curl"], "ca": tools["ca"],
               "deadline": time.monotonic() + PROGRAM_DEADLINE_S}
        program_dir, entry = install_program(ctx, ROOT)
        command = write_wrapper(COMMAND, tools["bun"], tools["python"], program_dir, entry, ROOT, tools["ca"])
        shell_dir, runtime_dir = run_bundle(command, ctx, max(60, TOTAL_BUDGET_S - (time.monotonic() - start)))
    except (Stop, OSError) as e:
        say(f"artifact-emulator: stopped: {e}")
        return 1
    except Exception as e:
        say(f"artifact-emulator: stopped: unexpected error ({type(e).__name__})")
        try:  # the details, for whoever debugs it, where only this user can read them
            with open(os.path.join(ROOT, "run", "last-error.txt"), "w") as f:
                traceback.print_exc(file=f)
        except OSError:
            pass
        return 1
    say("the emulator downloaded the viewer and runtime")
    print(json.dumps({"command": command, "shellDir": shell_dir, "runtimeDir": runtime_dir,
                      "workDir": os.path.join(os.path.realpath(ROOT), "run")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
