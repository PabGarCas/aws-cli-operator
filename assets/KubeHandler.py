import os, json
from kubernetes import client, config
'''
    Wrapper for using kubernetes client for python.
    
    It's intented to be executed within a pod, the serviceaccount
    executing this pod must have the following permissions:

    Role:
        pods: get, list, watch, create, delete, update, patch
        AwsCredential: get, list, watch, create, delete, update, patch
    
    ClusterRole:
        nodes: get, list, watch
        namespace: get, list, watch
'''
class KubeHandler:
    # Client
    configuration = None
    configurationApi = None
    client = None
    clientApi = None

    def __init__(self):
        # Direct client
        self.configuration = config.load_incluster_config()
        self.client = client.CoreV1Api(client.ApiClient(self.configuration))
        
        # Api client (for crds)
        self.configurationApi = client.Configuration()

        self.configurationApi.host = 'https://'+os.getenv('KUBERNETES_SERVICE_HOST')
        self.configurationApi.api_key_prefix = {"authorization": "bearer"}
        self.configurationApi.ssl_ca_crt = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        self.configurationApi.verify_ssl = False

        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token:
            self.configurationApi.api_key['authorization'] = token.read()

        
    def example(self):
        print("Listing all pods:")
        for namespace in self.get_namespaces():
            print("Pods in '"+namespace.metadata.name+"':")
            
            pods = self.get_pods(namespace='default')
            for pod in pods:
                print("\tPod:"+pod.metadata.name)

    def list_namespaces(self):
        return self.client.list_namespace().items

    def list_pods(self, namespace):
        return self.client.list_namespaced_pod(namespace=namespace).items
    
    def list_aws_credentials(self, namespace):
        api_client = client.ApiClient(self.configurationApi)
        api_instance = client.CustomObjectsApi(api_client)
        group = 'kai.aws-operator'
        version = 'v1'
        plural = 'awscredentials'
        return api_instance.list_namespaced_custom_object(group, 
                                                          version, 
                                                          namespace, 
                                                          plural).items
            
    def get_aws_credential(self, namespace, name):
        return self.client.get_namespaced_custom_object(group="kai.aws-operator",
                                                        version="v1",
                                                        plural="awscredentials",
                                                        namespace=namespace,
                                                        name=name)
    
kh = KubeHandler()
print(kh.list_aws_credentials('default'))
for awscredential in kh.list_aws_credentials('default'):
    print(awscredential)
#print(kh.get_aws_credential("default",'aws-credential'))
