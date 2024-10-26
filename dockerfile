FROM amazonlinux:latest
USER root
RUN mkdir /opt/src
RUN chmod -R 777 /opt/src
WORKDIR /opt/src
COPY requirements.txt requirements.txt
RUN yum install -y pip && \
    pip install -r requirements.txt && \
    rm -rf /var/cache
COPY run.sh run.sh
COPY src src
#COPY .streamlit/ src/.streamlit/
USER root
RUN chmod a+x run.sh
CMD ["./run.sh"]