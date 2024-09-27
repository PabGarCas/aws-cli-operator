import os

from kubernetes import client

class KubeHandler:
    # Client info
    tokenPath = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    CAPath = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
    token = None
    caCert = None
    kubernetesServiceHost = None
    kubernetesServicePort = None
    configuration = None
    client = None

    def __init__(self):
        with open(self.tokenPath, 'r') as token:
            self.token = token.read()

        with open(self.CAPath, 'r') as ca:
            self.caCert = ca.read()

        self.kubernetesServiceHost = os.getenv('KUBERNETES_SERVICE_HOST')
        self.kubernetesServicePort = os.getenv('KUBERNETES_SERVICE_PORT')

        self.configuration = client.Configuration()
        self.configuration.api_key["authorization"] = self.token
        self.configuration.api_key_prefix['authorization'] = 'Bearer'
        self.configuration.host = 'https://'+self.kubernetesServiceHost
        self.configuration.ssl_ca_cert = self.caCert

        self.client = client.CoreV1Api(client.ApiClient(self.configuration))

        print("Listing pods with their IPs:")
        ret = self.client.list_pod_for_all_namespaces(watch=False)
        print("STart")

        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

        print("ENd")

kh = KubeHandler()