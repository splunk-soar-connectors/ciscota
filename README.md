[comment]: # "Auto-generated SOAR connector documentation"
# Cisco Tetration Analytics

Publisher: Phantom  
Connector Version: 1\.0\.6  
Product Vendor: Cisco  
Product Name: Cisco Tetration Analytics  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 3\.5\.180  

This app supports variety of investigative actions on Cisco Tetration Analytics

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Cisco Tetration Analytics asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**server\_url** |  required  | string | Server URL \(e\.g\. https\://10\.10\.10\.10\)
**verify\_server\_cert** |  optional  | boolean | Verify server certificate
**api\_key** |  required  | string | API key
**api\_secret** |  required  | password | API secret

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate credentials provided for connectivity  
[list endpoints](#action-list-endpoints) - List all endpoints  
[list scopes](#action-list-scopes) - List all scopes  
[get flows](#action-get-flows) - Get flow information  
[lookup ip](#action-lookup-ip) - Get endpoint details and flows of a specific IP  
[list user groups](#action-list-user-groups) - List configured user groups  
[list annotations](#action-list-annotations) - List all uploaded annotations of specific scope  
[create annotations](#action-create-annotations) - Upload annotations to specific scope  
[delete annotations](#action-delete-annotations) - Clear all annotations of specific scope  
[list dimensions](#action-list-dimensions) - List all dimensions  
[list metrics](#action-list-metrics) - List all metrics  

## action: 'test connectivity'
Validate credentials provided for connectivity

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list endpoints'
List all endpoints

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.agent\_type | string | 
action\_result\.data\.\*\.cpu\_quota\_mode | numeric | 
action\_result\.data\.\*\.cpu\_quota\_usec | numeric | 
action\_result\.data\.\*\.current\_sw\_version | string | 
action\_result\.data\.\*\.data\_plane\_disabled | boolean | 
action\_result\.data\.\*\.deleted\_at | numeric | 
action\_result\.data\.\*\.desired\_sw\_version | string | 
action\_result\.data\.\*\.enable\_pid\_lookup | boolean | 
action\_result\.data\.\*\.host\_name | string |  `host name` 
action\_result\.data\.\*\.interfaces\.\*\.family\_type | string | 
action\_result\.data\.\*\.interfaces\.\*\.ip | string |  `ip` 
action\_result\.data\.\*\.interfaces\.\*\.mac | string |  `mac address` 
action\_result\.data\.\*\.interfaces\.\*\.name | string | 
action\_result\.data\.\*\.interfaces\.\*\.netmask | string | 
action\_result\.data\.\*\.interfaces\.\*\.vrf | string | 
action\_result\.data\.\*\.last\_config\_fetch\_at | numeric | 
action\_result\.data\.\*\.last\_software\_update\_at | numeric | 
action\_result\.data\.\*\.platform | string | 
action\_result\.data\.\*\.uuid | string | 
action\_result\.summary\.total\_endpoints | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list scopes'
List all scopes

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.child\_app\_scope\_ids | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.dirty | boolean | 
action\_result\.data\.\*\.dirty\_short\_query | string | 
action\_result\.data\.\*\.filter\_type | string | 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.name | string |  `cisco ta scope` 
action\_result\.data\.\*\.parent\_app\_scope\_id | string | 
action\_result\.data\.\*\.policy\_priority | string | 
action\_result\.data\.\*\.priority | string | 
action\_result\.data\.\*\.query\.field | string | 
action\_result\.data\.\*\.query\.filters\.\*\.field | string | 
action\_result\.data\.\*\.query\.filters\.\*\.filters\.\*\.field | string | 
action\_result\.data\.\*\.query\.filters\.\*\.filters\.\*\.type | string | 
action\_result\.data\.\*\.query\.filters\.\*\.filters\.\*\.value | string | 
action\_result\.data\.\*\.query\.filters\.\*\.type | string | 
action\_result\.data\.\*\.query\.filters\.\*\.value | string | 
action\_result\.data\.\*\.query\.type | string | 
action\_result\.data\.\*\.query\.value | string | 
action\_result\.data\.\*\.short\_name | string | 
action\_result\.data\.\*\.short\_priority | string | 
action\_result\.data\.\*\.short\_query\.field | string | 
action\_result\.data\.\*\.short\_query\.filters\.\*\.field | string | 
action\_result\.data\.\*\.short\_query\.filters\.\*\.type | string | 
action\_result\.data\.\*\.short\_query\.filters\.\*\.value | string | 
action\_result\.data\.\*\.short\_query\.type | string | 
action\_result\.data\.\*\.short\_query\.value | string | 
action\_result\.data\.\*\.vrf\_id | string | 
action\_result\.summary\.total\_scopes | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get flows'
Get flow information

Type: **investigate**  
Read only: **True**

If the <b>filter</b> is empty \(i\.e\. \{\}\), then the query matches all flows\. If parameter <b>dimensions</b> is not specified, flowsearch returns all the available dimensions\. This option is useful to specify a subset of the available dimensions when the caller does not care about the rest of the dimensions\. If parameter <b>metrics</b> is not specified, flowsearch results returns all the available metrics\. This option is useful to specify a subset of the available metrics when the caller does not care about the rest of the metrics\. <br>The app supports multiple methods for specifying <b>filter</b> dictionary\. Please refer to the OpenAPI documentation for more information\. Below is an example for a <b>filter</b> dictionary\:<br>\{"type"\: "and", "filters"\: \[\{"type"\: "contains", "field"\: "src\_hostname", "value"\: "prod"\}, \{"type"\: "in", "field"\: "dst\_port", "values"\: \["80",  "443"\]\}\]\}

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start\_time** |  required  | Flow search start time \(epoch or ISO 8601\) | string | 
**end\_time** |  required  | Flow search end time \(epoch or ISO 8601\) | string | 
**filter** |  optional  | Query filter \(JSON format\) | string | 
**scope\_name** |  optional  | Full name of the scope to which query is restricted to | string |  `cisco ta scope` 
**dimensions** |  optional  | Dimensions | string |  `cisco ta dimension` 
**metrics** |  optional  | Metrics | string |  `cisco ta metrics` 
**limit** |  optional  | Number of response flows limit \(default\: 100\) | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.dimensions | string |  `cisco ta dimension` 
action\_result\.parameter\.end\_time | string | 
action\_result\.parameter\.filter | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.metrics | string |  `cisco ta metrics` 
action\_result\.parameter\.scope\_name | string |  `cisco ta scope` 
action\_result\.parameter\.start\_time | string | 
action\_result\.data\.\*\.bandwidth\_bytes\_per\_second | string | 
action\_result\.data\.\*\.dst\_address | string |  `ip` 
action\_result\.data\.\*\.dst\_enforcement\_epg\_name | string | 
action\_result\.data\.\*\.dst\_hostname | string |  `host name` 
action\_result\.data\.\*\.dst\_is\_internal | string | 
action\_result\.data\.\*\.dst\_port | string |  `port` 
action\_result\.data\.\*\.dst\_scope\_name | string |  `cisco ta scope` 
action\_result\.data\.\*\.fwd\_ack\_count | numeric | 
action\_result\.data\.\*\.fwd\_allzero\_count | numeric | 
action\_result\.data\.\*\.fwd\_bytes | numeric | 
action\_result\.data\.\*\.fwd\_cwr\_count | numeric | 
action\_result\.data\.\*\.fwd\_ece\_count | numeric | 
action\_result\.data\.\*\.fwd\_fin\_count | numeric | 
action\_result\.data\.\*\.fwd\_finnoack\_count | numeric | 
action\_result\.data\.\*\.fwd\_nc\_count | numeric | 
action\_result\.data\.\*\.fwd\_network\_latency\_usec | string | 
action\_result\.data\.\*\.fwd\_null\_count | numeric | 
action\_result\.data\.\*\.fwd\_pingdeath\_count | numeric | 
action\_result\.data\.\*\.fwd\_pkts | numeric | 
action\_result\.data\.\*\.fwd\_psh\_count | numeric | 
action\_result\.data\.\*\.fwd\_rst\_count | numeric | 
action\_result\.data\.\*\.fwd\_syn\_count | numeric | 
action\_result\.data\.\*\.fwd\_synfin\_count | numeric | 
action\_result\.data\.\*\.fwd\_synrst\_count | numeric | 
action\_result\.data\.\*\.fwd\_tiny\_count | numeric | 
action\_result\.data\.\*\.fwd\_urg\_count | numeric | 
action\_result\.data\.\*\.fwd\_xmas\_count | numeric | 
action\_result\.data\.\*\.proto | string | 
action\_result\.data\.\*\.rev\_ack\_count | numeric | 
action\_result\.data\.\*\.rev\_allzero\_count | numeric | 
action\_result\.data\.\*\.rev\_bytes | numeric | 
action\_result\.data\.\*\.rev\_cwr\_count | numeric | 
action\_result\.data\.\*\.rev\_ece\_count | numeric | 
action\_result\.data\.\*\.rev\_fin\_count | numeric | 
action\_result\.data\.\*\.rev\_finnoack\_count | numeric | 
action\_result\.data\.\*\.rev\_nc\_count | numeric | 
action\_result\.data\.\*\.rev\_network\_latency\_usec | string | 
action\_result\.data\.\*\.rev\_null\_count | numeric | 
action\_result\.data\.\*\.rev\_pingdeath\_count | numeric | 
action\_result\.data\.\*\.rev\_pkts | numeric | 
action\_result\.data\.\*\.rev\_psh\_count | numeric | 
action\_result\.data\.\*\.rev\_rst\_count | numeric | 
action\_result\.data\.\*\.rev\_syn\_count | numeric | 
action\_result\.data\.\*\.rev\_synfin\_count | numeric | 
action\_result\.data\.\*\.rev\_synrst\_count | numeric | 
action\_result\.data\.\*\.rev\_tiny\_count | numeric | 
action\_result\.data\.\*\.rev\_urg\_count | numeric | 
action\_result\.data\.\*\.rev\_xmas\_count | numeric | 
action\_result\.data\.\*\.server\_app\_latency\_usec | numeric | 
action\_result\.data\.\*\.server\_stack\_latency\_usec | string | 
action\_result\.data\.\*\.src\_address | string |  `ip` 
action\_result\.data\.\*\.src\_enforcement\_epg\_name | string | 
action\_result\.data\.\*\.src\_hostname | string |  `host name` 
action\_result\.data\.\*\.src\_is\_internal | string | 
action\_result\.data\.\*\.src\_port | string |  `port` 
action\_result\.data\.\*\.src\_scope\_name | string |  `cisco ta scope` 
action\_result\.data\.\*\.srtt\_available | string | 
action\_result\.data\.\*\.srtt\_usec | numeric | 
action\_result\.data\.\*\.start\_timestamp | string | 
action\_result\.data\.\*\.timestamp | string | 
action\_result\.data\.\*\.total\_network\_latency\_usec | numeric | 
action\_result\.data\.\*\.total\_perceived\_latency\_usec | numeric | 
action\_result\.data\.\*\.vrf\_name | string | 
action\_result\.summary\.total\_flows | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'lookup ip'
Get endpoint details and flows of a specific IP

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**ip** |  required  | IP to query | string |  `ip` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.ip | string |  `ip` 
action\_result\.data\.\*\.endpoints\.\*\.agent\_type | string | 
action\_result\.data\.\*\.endpoints\.\*\.cpu\_quota\_mode | numeric | 
action\_result\.data\.\*\.endpoints\.\*\.cpu\_quota\_usec | numeric | 
action\_result\.data\.\*\.endpoints\.\*\.current\_sw\_version | string | 
action\_result\.data\.\*\.endpoints\.\*\.data\_plane\_disabled | boolean | 
action\_result\.data\.\*\.endpoints\.\*\.deleted\_at | numeric | 
action\_result\.data\.\*\.endpoints\.\*\.desired\_sw\_version | string | 
action\_result\.data\.\*\.endpoints\.\*\.enable\_pid\_lookup | boolean | 
action\_result\.data\.\*\.endpoints\.\*\.host\_name | string |  `host name` 
action\_result\.data\.\*\.endpoints\.\*\.interfaces\.\*\.family\_type | string | 
action\_result\.data\.\*\.endpoints\.\*\.interfaces\.\*\.ip | string |  `ip` 
action\_result\.data\.\*\.endpoints\.\*\.interfaces\.\*\.mac | string |  `mac address` 
action\_result\.data\.\*\.endpoints\.\*\.interfaces\.\*\.name | string | 
action\_result\.data\.\*\.endpoints\.\*\.interfaces\.\*\.netmask | string | 
action\_result\.data\.\*\.endpoints\.\*\.interfaces\.\*\.vrf | string | 
action\_result\.data\.\*\.endpoints\.\*\.last\_config\_fetch\_at | numeric | 
action\_result\.data\.\*\.endpoints\.\*\.last\_software\_update\_at | numeric | 
action\_result\.data\.\*\.endpoints\.\*\.platform | string | 
action\_result\.data\.\*\.endpoints\.\*\.uuid | string | 
action\_result\.data\.\*\.flow\.\*\.bandwidth\_bytes\_per\_second | string | 
action\_result\.data\.\*\.flow\.\*\.dst\_address | string |  `ip` 
action\_result\.data\.\*\.flow\.\*\.dst\_enforcement\_epg\_name | string | 
action\_result\.data\.\*\.flow\.\*\.dst\_hostname | string |  `host name` 
action\_result\.data\.\*\.flow\.\*\.dst\_is\_internal | string | 
action\_result\.data\.\*\.flow\.\*\.dst\_port | string |  `port` 
action\_result\.data\.\*\.flow\.\*\.dst\_scope\_name | string |  `cisco ta scope` 
action\_result\.data\.\*\.flow\.\*\.fwd\_ack\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_allzero\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_bytes | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_cwr\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_ece\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_fin\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_finnoack\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_nc\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_network\_latency\_usec | string | 
action\_result\.data\.\*\.flow\.\*\.fwd\_null\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_pingdeath\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_pkts | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_psh\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_rst\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_syn\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_synfin\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_synrst\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_tiny\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_urg\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.fwd\_xmas\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.proto | string | 
action\_result\.data\.\*\.flow\.\*\.rev\_ack\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_allzero\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_bytes | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_cwr\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_ece\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_fin\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_finnoack\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_nc\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_network\_latency\_usec | string | 
action\_result\.data\.\*\.flow\.\*\.rev\_null\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_pingdeath\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_pkts | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_psh\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_rst\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_syn\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_synfin\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_synrst\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_tiny\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_urg\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.rev\_xmas\_count | numeric | 
action\_result\.data\.\*\.flow\.\*\.server\_app\_latency\_usec | numeric | 
action\_result\.data\.\*\.flow\.\*\.server\_stack\_latency\_usec | string | 
action\_result\.data\.\*\.flow\.\*\.src\_address | string |  `ip` 
action\_result\.data\.\*\.flow\.\*\.src\_enforcement\_epg\_name | string | 
action\_result\.data\.\*\.flow\.\*\.src\_hostname | string |  `host name` 
action\_result\.data\.\*\.flow\.\*\.src\_is\_internal | string | 
action\_result\.data\.\*\.flow\.\*\.src\_port | string |  `port` 
action\_result\.data\.\*\.flow\.\*\.src\_scope\_name | string |  `cisco ta scope` 
action\_result\.data\.\*\.flow\.\*\.srtt\_available | string | 
action\_result\.data\.\*\.flow\.\*\.srtt\_usec | numeric | 
action\_result\.data\.\*\.flow\.\*\.start\_timestamp | string | 
action\_result\.data\.\*\.flow\.\*\.timestamp | string | 
action\_result\.data\.\*\.flow\.\*\.total\_network\_latency\_usec | numeric | 
action\_result\.data\.\*\.flow\.\*\.total\_perceived\_latency\_usec | numeric | 
action\_result\.data\.\*\.flow\.\*\.vrf\_name | string | 
action\_result\.summary\.total\_endpoints | numeric | 
action\_result\.summary\.total\_flows | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list user groups'
List configured user groups

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.users\.\*\.disabled\_at | string | 
action\_result\.data\.\*\.users\.\*\.email | string |  `email` 
action\_result\.data\.\*\.users\.\*\.first\_name | string | 
action\_result\.data\.\*\.users\.\*\.id | string | 
action\_result\.data\.\*\.users\.\*\.last\_name | string | 
action\_result\.data\.\*\.users\.\*\.preferences\.app\_scope\_id | string | 
action\_result\.data\.\*\.users\.\*\.preferences\.tenant\_id | string | 
action\_result\.data\.\*\.users\.\*\.preferences\.vrf\_id | string | 
action\_result\.data\.\*\.users\.\*\.role\_ids | string | 
action\_result\.summary\.total\_roles | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list annotations'
List all uploaded annotations of specific scope

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**scope\_name** |  required  | Scope name | string |  `cisco ta scope` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.scope\_name | string |  `cisco ta scope` 
action\_result\.data\.\*\.annotation\_name | string | 
action\_result\.summary\.total\_annotations | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create annotations'
Upload annotations to specific scope

Type: **generic**  
Read only: **False**

Upload a CSV file in vault to add or delete user annotations\. Vault ID or file name of uploaded CSV will be used to upload annotations\. The uploaded CSV must contains IP as a column header\.<br>Sample CSV is shown below<br>IP,VRF,Department,Datacenter,\.\.\.,Column HeaderK<br>7\.7\.7\.7,Disco,HR,SJC,\.\.\.,columnK\_Value<br>\.\.\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**operation** |  required  | Operation | string | 
**scope\_name** |  required  | Scope name | string |  `cisco ta scope` 
**vault\_id** |  optional  | Vault ID | string |  `vault id` 
**filename** |  optional  | File name | string |  `file name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.filename | string |  `file name` 
action\_result\.parameter\.operation | string | 
action\_result\.parameter\.scope\_name | string |  `cisco ta scope` 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.data\.\*\.warnings | string | 
action\_result\.summary\.warnings | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'delete annotations'
Clear all annotations of specific scope

Type: **generic**  
Read only: **False**

Please ensure these annotations are not used by any filters or scopes as they will no longer work as expected\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**scope\_name** |  required  | Scope name | string |  `cisco ta scope` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.scope\_name | string |  `cisco ta scope` 
action\_result\.data | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list dimensions'
List all dimensions

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.dimension\_name | string |  `cisco ta dimension` 
action\_result\.summary\.total\_dimensions | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list metrics'
List all metrics

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.metric\_name | string |  `cisco ta metrics` 
action\_result\.summary\.total\_metrics | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 