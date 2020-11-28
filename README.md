# Slack mention/message count script

Can be used to find number of occurences of a message or handle mention within a slack channel

## Prerequisite
- A Slack app need to be created with below listed perimissions
- Slack app has to added to a channel with command
```shell script
/invite sample-app
``` 

**Permissions required by app**

BOT TOKEN SCOPES: 
 - channels:read :
  View basic information about public channels in a workspace

USER TOKEN SCOPES:
- channels:history :
  View messages and other content in a user’s public channels

## Sample script run command 
```shell script
SLACK_TOKEN='xoxb-abc-xyz-123' python3 scraper.py "@here" "Nov 28, 2020 @ 06:40:00 UTC" "Nov 28, 2020 @ 07:13:00 UTC"
```

### Token
You can get slack token from app details under Signing Secret of the app
