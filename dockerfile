FROM python:3.10



WORKDIR /var/www
ADD . /var/www

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    python3-pip \
    && pip install opencv-python \
    && pip install pillow \
    && pip install pytesseract \
    && pip install flask \
    && python3 -m pip install -r requirements.txt \
    && pip3 install virtualenv

#COPY . .
COPY ./ .var/www
EXPOSE 5000

CMD gunicorn wsgi:app -c gunicorn_config.py