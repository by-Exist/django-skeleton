from tempfile import mkdtemp
import multiprocessing
import environ


# ENVIRON
# ==============================================================================
env = environ.Env()

DEBUG = env.bool("DEBUG")

FORWARDED_ALLOW_IPS = env.str("GUNICORN_FORWARDED_ALLOW_IPS")
PROXY_ALLOW_IPS = env.str("GUNICORN_PROXY_ALLOW_IPS")


# Config
# ==============================================================================
config = "./gunicorn.conf.py"  # 설정파일 경로
wsgi_app = "config.wsgi:application"  # wsgi_app 경로, 파이썬모듈:변수


# Debugging
# ==============================================================================
# reload = False  # 코드 변경시 워커 reload
reload = True if DEBUG else False

reload_engine = "auto"  # 코드 변경 추적 엔진 설정
reload_extra_files = []  # reload 시 리로드되는 대상 확장
spew = False  # 서버 실행 모든 라인 출력 (주의)
check_config = False  # config가 정상적인지 확인하고 종료 (exit code, O=0, X=1)
print_config = False  # config 출력


# Logging
# ==============================================================================
# accesslog = None  # 액세스 로그 파일 경로, "-" = stdout
accesslog = "-" if DEBUG else "/var/log/gunicorn.access.log"
# errorlog = "-"  # 에러 로그 파일 경로, "-" = stdout
errorlog = "-" if DEBUG else "/var/log/gunicorn.error.log"
capture_output = False  # stdout + stderr를 errorlog 파일에 리디렉션
# loglevel = "info"  # err log 출력 레벨, debug < info < warning < error < critical
loglevel = "debug" if DEBUG else "info"
disable_redirect_access_to_syslog = False  # 리디렉션 액세스 로그 비활성화
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
    if DEBUG
    else '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)

logger_class = "gunicorn.glogging.Logger"  # 로깅에 사용될 로거
logconfig = None  # python logging 모듈 구성 파일 경로
logconfig_dict = {}  # python logging 모듈에 사용될 dict, logconfig보다 우선
syslog = False  # syslog에 로그를 전송
syslog_addr = "udp://localhost:514"  # syslog를 보낼 주소
syslog_prefix = None  # syslog에서 사용될 프로그램 이름 매개변수, gunicorn.<prefix>
syslog_facility = "user"  # syslog 기능 이름
enable_stdio_inheritance = False  # stdio 상속 활성화
statsd_host = None  # StatsD 서버의 host:port
dogstatsd_tags = ""  # StatsD에서 활용될 태그 목록, ,로 구분
statsd_prefix = ""  # StatsD에 전송될 때 사용될 접두사


# Process Naming
# ==============================================================================
proc_name = None  # gunicorn 프로세스 이름 설정, None일 경우 default_proc_name 사용
default_proc_name = "gunicorn"  # gunicorn 기본 프로세스 이름


# SSL
# ==============================================================================
keyfile = None  # SSL 키 파일 경로
certfile = None  # SSL 인증서 파일 경로
do_handshake_on_connect = False if DEBUG else True

ssl_version = "TLSv1_2"  # 사용될 ssl의 버전
cert_reqs = 0  # 클라이언트 인증서 필요 여부 (stdlib ssl 모듈 참조)
ca_certs = None  # CA 인증서 파일 경로
suppress_ragged_eofs = True  # 비정성 EOF 억제 (stdlib ssl 모듈 참조)
# do_handshake_on_connect = False  # 소켓 연결 시 SSL 핸드 셰이크 수행 여부
ciphers = None  # 암호화 방식, None일 경우 ssl 모듈의 기본 암호 list 활용


# Security
# ==============================================================================
limit_request_line = 1024  # HTTP request 최대 바이트 크기
limit_request_fields = 100  # HTTP request 헤더 최대 갯수 제한
limit_request_field_size = 1024  # HTTP request 헤더 필드 허용 크기 제한


# Server Mechanics
# ==============================================================================
# chdir = "/app"  # app 로드 전에 chdir, Dockerfile에서 설정됨.
daemon = False  # gunicorn 프로세스 백그라운드 실행 여부
preload_app = False  # 워커 프로세스 fork 전 app code를 preload
secure_scheme_headers = {
    "X-FORWARDED-PROTOCOL": "ssl",
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}  # 프론트엔드 프록시가 HTTPS 요청을 표시하는데에 사용될 헤더 및 값 dict
# forwarded_allow_ips = "127.0.0.1"  # 보안 헤더 처리 가능 프론트엔드 IP (쉼표 구분, * 사용 가능, None일 경우 FORWARDED_ALLOW_IPS ENV 활용)
# proxy_allow_ips = "127.0.0.1"  # 프록시 요청 수락 허용 프론트엔드 IP (쉼표 구분, * 사용 가능)
proxy_allow_ips = "*" if DEBUG else PROXY_ALLOW_IPS
forwarded_allow_ips = "*" if DEBUG else FORWARDED_ALLOW_IPS
proxy_protocol = False  # 프록시 프로토콜 감지 활성화

# user = 1005  # worker의 프로세스를 해당 작업자로 실행
user = None
# group = 205  # worker의 프로세스를 해당 group으로 실행
group = None
umask = 0  # gunicorn 작성 파일의 파일 모드 비트마스크
initgroups = False  # True일 경우 해당 그룹만 워커 프로세스 엑세스
# worker_tmp_dir = None  # worker가 임시 파일을 다룰 때 사용할 디렉토리
worker_tmp_dir = mkdtemp(prefix="gunicorn_")
sendfile = None  # sendfile() 활성화 여부, None일 경우 SENDFILE 환경변수 활용
reuse_port = False  # 동일 포트에 여러 listen 소켓 bind 허용 여부
raw_env = []  # 환경변수 추가 설정, ["foo=bar"]
pidfile = None  # PID 파일 이름
tmp_upload_dir = None  # 임시 요청 데이터 저장 디렉토리
pythonpath = None  # 파이썬 경로
paste = None  # PasteDeploy 구성 파일 로드
raw_paste_global_conf = []  # PasteDeploy 환경변수 설정, ['foo=bar']
strip_header_spaces = False  # 헤더 빈 공간 strip, 비사용 권장


# Server Socket
# ==============================================================================
# bind = None  # None일 경우 ["127.0.0.8000"], PORT 환경변수 ["0.0.0.0:$PORT"]
bind = ["0.0.0.0:8000"]
backlog = 1024  # 보류 최대 연결 수


# Worker Processes
# ==============================================================================
# workers = 1  # request 처리 worker 프로세스 수, 일반적으로 2-4 x $(NUM_CORES)
workers = multiprocessing.cpu_count() * 2 + 1
if DEBUG:
    workers = 1
# worker_class = 'sync'  # 사용 worker 종류
worker_class = "sync" if DEBUG else "gevent"

# threads = 1  # gthread 전용, 워커의 스레드 개수, 일반적으로 2-4 x $(NUM_CORES), gthread를 사용하지 않음.
worker_connections = 1000  # eventlet, gevent 전용, 동시 클라이언트 최대 수
max_requests = 10000  # 워커 처리 최대 요청 수, 넘길 경우 reload, 0일 경우 worker reload 비활성
max_requests_jitter = 1000  # worker의 max_request = randint(0, max_requests_jitter)
timeout = 30  # 해당 초 동안 응답 없는 작업자는 리로드 트리거
graceful_timeout = 30  # 해당 초 동안 살아있는 작업자도 리로드 트리거
keepalive = 3  # sync 제외, 해당 초동안 request를 받기 위해 connection 유지


# Server Hooks
# ==============================================================================
def on_starting(server):
    """
    마스터 프로세스의 __init__ 직전 호출
    """


def on_reload(server):
    """
    SIGHUP를 통해 worker가 reload될 때 호출
    """


def when_ready(server):
    """
    서버가 시작된 직후 호출
    """


def pre_fork(server, worker):
    """
    워커가 fork되기 직전 호출
    """


def post_fork(server, worker):
    """
    워커가 fork된 직후 호출
    """


def post_worker_init(worker):
    """
    워커가 __init__ 작업을 끝낸 직후 호출
    """


def worker_int(worker):
    """
    워커가 SIGINT 또는 SIGQUIT에서 종료된 직후 호출
    """


def worker_abort(worker):
    """
    워커가 SIGABRT 신호를 받았을 때 호출, 일반적으로 시간 초과시 발생
    """


def pre_exec(server):
    """
    새로운 마스터 프로세스가 fork되기 직전 호출
    """


def pre_request(worker, req):
    """
    워커가 request를 처리하기 직전에 호출
    """
    worker.log.debug("%s %s", req.method, req.path)


def post_request(worker, req, environ, resp):
    """
    워커가 request를 처리한 직후 호출
    """


def child_exit(server, worker):
    """
    마스터 프로세스에서 워커가 종료된 직후 호출
    """


def worker_exit(server, worker):
    """
    워커 프로세스에서 워커가 종료된 직후 호출
    """


def nworkers_changed(server, new_value, old_value):
    """
    num_workers가 변경된 직후 호출
    """


def on_exit(server):
    """
    gunicorn 종료 직전 호출
    """
