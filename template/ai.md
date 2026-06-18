# AI

## Ollama

```bash
ollama list

# 6.3 GB
ollama run krishairnd/Gemma-4-Uncensored

# 12 GB
ollama run igorls/gemma-4-12B-it-qat-q4_0-unquantized-heretic:Q8_0
```

## OpenCode

```shell
# C:\Users\{USER}\.config\opencode\opencode.jsonc
```

```json
{
  "$schema": "https://opencode.ai/config.json",
  "disabled_providers": [
    "ollama"
  ],
  "provider": {
    "ollama IP": {
      "name": "Ollama (local)",
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "http://IP:11434/v1"
      },
      "models": {
        "krishairnd/Gemma-4-Uncensored": {
          "name": "krishairnd/Gemma-4-Uncensored"
        }
      }
    }
  }
}
```

## OpenClaw

Ubuntu 24.04

```bash
sudo apt install curl

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub > linux_signing_key.pub
sudo install -D -o root -g root -m 644 linux_signing_key.pub /etc/apt/keyrings/linux_signing_key.pub
sudo sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/linux_signing_key.pub] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable

curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
source ~/.bashrc

openclaw models status

openclaw models scan
openclaw models set openrouter/nvidia/nemotron-3-ultra-550b-a55b:free

openclaw gateway run --force

# Prompts
# talk to agent
# Prompts
# open the web browser and open the yahoo.com.tw
# 用 browser 工具開啟 yahoo.com.tw 並擷取畫面截圖
# 用 browser 工具開啟 yahoo.com.tw
# 開啟股市相關新聞

openclaw chat

openclaw browser doctor

openclaw logs --follow

openclaw pairing approve telegram CODE

openclaw pairing list telegram

openclaw secrets configure

openclaw config set browser.headless false

openclaw browser start

openclaw gateway stop

openclaw gateway start
```


