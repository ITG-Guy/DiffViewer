gunicorn -w 4 -b 0.0.0.0:5000 --certfile=tools/pem/cert.pem --keyfile=tools/pem/key.pem app:app


# 	•	--certfile=tools/pem/cert.pem: 인증서 파일 경로
# 	•	--keyfile=tools/pem/key.pem: 개인 키 파일 경로
# 	•	-w 4: 워커(worker) 프로세스 수 (필요에 따라 조정 가능)
# 	•	-b 0.0.0.0:5000: 모든 IP 주소에서 5000번 포트로 바인딩

# 이 방법을 사용하면 Gunicorn이 자체적으로 HTTPS 연결을 처리합니다.
