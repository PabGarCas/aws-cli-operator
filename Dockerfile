FROM alpine:3.20.3

RUN apk add --no-cache python3 py3-pip py3-kubernetes git curl bash
WORKDIR /tmp
RUN curl -LO https://dl.k8s.io/release/v1.31.1/bin/linux/amd64/kubectl && mv kubectl /bin
RUN git clone https://github.com/PabGarCas/aws-cli-operator.git
RUN mkdir -p /opt/aws-cli-operator/bin /opt/aws-cli-operator/templates
RUN cp aws-cli-operator/assets/operator.py /opt/aws-cli-operator/bin && chmod +x /opt/aws-cli-operator/bin/operator.py 
RUN cp aws-cli-operator/assets/templates/*.yaml /opt/aws-cli-operator/templates

CMD ["/bin/bash", "-c", "/opt/aws-cli-operator/bin/operator.py"]