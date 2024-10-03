FROM selenium/standalone-firefox

RUN sudo apt update && sudo apt install supervisor python3 python3-pip -y

RUN python3 -m pip install --upgrade pip --break-system-packages

RUN sudo mkdir -p /app && sudo chmod 777 -R /app

WORKDIR /app

COPY application .

RUN pip install -r requirements.txt --break-system-packages

COPY config/supervisord.conf /etc/supervisord.conf

ENV PYTHONDONTWRITEBYTECODE=1

RUN python3 -c 'from db import init; init()'
RUN python3 -c 'from db import create_user; create_user("admin", "secpassword123!", "", "Hi!")'

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
