# PIOPIY Python SDK

The PIOPIY python SDK is used to integrate communications into your python applications using the PIOPIY REST API. Using the PIOPIY python SDK, you will be able to make voice calls and can control your call flows.

## Install

Follow the below installation instructions

### Prerequisites

Prerequisites for javascript web server.

- <a href="https://www.python.org/" target="_blank">python</a> (>= 2.7.16 required)
- <a href="https://pypi.org/project/pip/" target="_blank">pip</a> (>= 18.1 required)

## Installation

Install the SDK using npm

```bash
$ pip install piopiy
```


### Authentication

In order to authenticate your app, and to make an API request, you should have an app id and secret for authentication. Find your App ID and secret in your <a href="https://doc.telecmi.com/piopiy/docs/build-app#app-id-and-secret" target="_blank">PIOPIY dashboard</a>

Specifiy the authentication credentials 

```python
import piopiy
client=piopiy.RestClient('your_app_id','your_app_secret')
```

### Make a call

To make a call, mention the to_number, piopiy_phone_number and <a href="https://doc.telecmi.com/piopiy/docs/configure-url" target="_blank">answer_url</a>.

```python
response=client.make(
     'your_to_number',
     'your_piopiy_phone_number',
     'your_answer_url'
)
```

### Hold a call

To hold a call, mention the cmiuuid of the call.

```python
response=client.hold('cmiuuid')
```

### Unhold a call
To unhold a call, mention the cmiuuid of the call.

```python
response=client.unhold('cmiuuid')
```
### Toggle a call
To toggle a call, mention the cmiuuid of the call.

```python
response=client.toggle('cmiuuid')
```

### Hangup a call
To Hangup a call, mention the cmiuuid of the call.

```python
response=client.hanup('cmiuuid')
```
### More Examples

Refer to the <a href="https://doc.telecmi.com/piopiy/docs/pcmo-overview" target="_blank">piopiy docs</a> for more examples. Now create the <a href="https://doc.telecmi.com/piopiy/docs/get-started#signup" target="_blank">PIOPIY account</a> and setup the flask server and test out your integration in few minutes.




### Reporting issues

For any feedbacks and problems, you can report us by <a href="https://github.com/telecmi/piopiy_python/issues" >opening an issue on github</a>.

