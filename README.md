# GhScription

World First Inscription For Developers

Tokens: https://github.com/ghscr/ghscription/blob/main/tokens.json

Inscriptions: https://github.com/ghscr/ghscription/tree/main/inscriptions

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


**Token Transfer**  
Cumming soon
