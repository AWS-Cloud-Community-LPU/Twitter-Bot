# Twitter-Bot
Official Twitter Bot for AWS Cloud Community LPU

[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/AWS-Cloud-Community-LPU/Twitter-Bot)


## :zap: Installation
**1. Clone this repo by running this command.**
```bash
git clone https://github.com/AWS-Cloud-Community-LPU/Twitter-Bot.git
```
**2. Now, run the following commands:**

```bash
cd Twitter-Bot
pip install -r requirements.txt
```
This will install all the project dependencies.

**3. Configure Bot Key:**

**File: secrets.ini**

A file ```secrets.ini``` is missing as it contains a tokens to access API of [Twitter Bot](https://twitter.com/AWScommLPU). The file is structured in this way: 
```
[KEYS]
API_KEY = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
API_SECRET_KEY = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ACCESS_TOKEN = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ACCESS_TOKEN_SECRET = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

**4. :tada: Run the bot:**
```bash
python3 main.py
```

## :page_facing_up: License
[MIT](./LICENSE) © [AWS-Cloud-Community-LPU](https://github.com/AWS-Cloud-Community-LPU)