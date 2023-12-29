# GhScription

World First Inscription For Developers

Tokens: https://github.com/ghscr/ghscription/blob/main/tokens.json

Inscriptions: https://github.com/ghscr/ghscription/tree/main/inscriptions

Join Telegram: https://t.me/+oaTuuPLnYaNjNDFh

### How it works?

Add an issue to this repository with the following content. A bot would automatically commit a JSON if the issue is valid.

**Token Deployment**
```
{
 "p": "GRC20",
 "op": "deploy",
 "tick": "GitHub",
 "max": "1000000000",
 "lim": "2000"
}
```
Example: https://github.com/ghscr/ghscription/issues/1

**Token Mint**
```
{  
  "p": "GRC20", 
  "op": "mint", 
  "tick": "GitHub", 
  "amt": "2000"
}
```
Example: https://github.com/ghscr/ghscription/issues/2

Example Inscription: https://github.com/ghscr/ghscription/blob/main/inscriptions/2.json 

Due to ratelimit, it may take a few minutes to index. Issues are the source of truth. 

**Token Transfer**  
Cumming soon
