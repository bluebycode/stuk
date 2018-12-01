# Mock constants

#Endpoints
AUTH_MOCK_ENDPOINT   = 'http://172.16.64.77:3000/verify/YWx2YXJvL3plbC5lZHUvNDg1OTQ1'

#Paths
AUTHORIZED_KEYS_PATH = "/home/cybercamp/.ssh/.authorizedkeys"
PLATFORM_KEYS_PATH   = ".keys/platform.key"

#Communication
DEFAULT_FILTER_SEQUENCE = 'ip proto \\tcp and ((tcp dst port 4000 or 4001 or 4002 or 22) and tcp[tcpflags] & tcp-syn != 0)'

