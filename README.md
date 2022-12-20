# acs-alert-viewer

A bare-bones Flask/Redis site that allows you to send and view alerts from Red Hat Advanced Cluster Security for Kubernetes (RHACS).  

### Deploy to OpenShift

```shell
$ git clone https://github.com/caseyrobb/acs-alert-viewer
$ oc apply -k acs-alert-viewer/openshift
$ ACSALERT=$(oc get route -n acs-alert-viewer acs-alert-viewer -o jsonpath='{.spec.host}{"\n"}')
```



### Configure via RHACS Web UI

Navigate to *Platform Configuration -> Integrations -> Generic Webhook* and enter `${ACSALERT}/api/v1/webhook` as the Endpoint URL. 



### Configure via API

```shell
$ CENTRAL=$(oc get route -n stackrox central -o jsonpath='{.spec.host}{"\n"}')


$ curl -XPOST \
				-H 'Content-Type: application/json' \
			 	-H "Authorization: Bearer ${ROX_API_TOKEN}" \
				-d @acs-alert-viewer.json \
				https://${CENTRAL}/v1/notifiers
```

acs-alert-viewer.json example:
```json
{
  "id": "",
  "name": "webhook",
  "generic": {
    "endpoint": "https://${ACSALERT}/api/v1/webhook",
    "skipTlsVerify": false,
    "auditLoggingEnabled": false,
    "caCert": "",
    "username": "",
    "password": "",
    "headers": [],
    "extraFields": []
  },
  "labelDefault": "",
  "labelKey": "",
  "uiEndpoint": "https://${CENTRAL}",
  "type": "generic"
}
```
