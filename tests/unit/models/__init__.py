import os
from google.appengine.api import apiproxy_stub_map, datastore_file_stub

appId = 'sharedhat-lab'

os.environ['APPLICATION_ID'] = appId
datastoreFile = os.path.join(os.path.dirname(__file__), '../../dev/null')
#datastoreFile = os.path.join('../../datastore')

apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
stub = datastore_file_stub.DatastoreFileStub(appId, datastoreFile, '/')
apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)