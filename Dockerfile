FROM registry.access.redhat.com/ubi8

WORKDIR /app

COPY Pipfile* /app/

## NOTE - rhel enforces user container permissions stronger ##
USER root
RUN yum -y install python3
RUN yum -y install python3-pip wget

RUN pip3 install --upgrade pip \
  && pip3 install --upgrade pipenv \
  && pipenv install --system --deploy

RUN mkdir -p /app/server/audio_extractions
RUN mkdir -p /app/server/video_uploads
RUN mkdir -p /app/server/output_transcriptions

RUN chown 1001 /app/server/audio_extractions
RUN chown 1001 /app/server/video_uploads
RUN chown 1001 /app/server/output_transcriptions

COPY . /app

ENV FLASK_APP=server/__init__.py
CMD ["python3", "manage.py", "start", "0.0.0.0:3000"]
