# AI

## Ollama

```bash
ollama list

# 6.3 GB
ollama run krishairnd/Gemma-4-Uncensored

# 12 GB
ollama run igorls/gemma-4-12B-it-qat-q4_0-unquantized-heretic:Q8_0

ollama show baytout3/Qwen3.6-27B-Uncensored-HauhauCS-Balanced:IQ4_XS --modelfile
ollama show krishairnd/Gemma-4-Uncensored --modelfile

# modelfile for ollama
ollama create Qwen3.6-27B-Uncensored-HauhauCS-Balanced-IQ4_XS -f D:\data\ai\models\llm\baytout3\Qwen3.6-27B-Uncensored-HauhauCS-Balanced\modelfile
```

## LM Studio

To ensure LM Studio can automatically load models correctly, the directory C:\Users\\[USER]\\\.lmstudio\hub must be placed in the custom models root directory.

The Runtime version can be deleted to save several gigabytes of space.

## ComfyUI

extra_model_paths.yaml for customize models path

ComfyUI-Manager

```bash
.\python_embeded\python.exe -m pip install -r ComfyUI\manager_requirements.txt

.\python_embeded\python.exe -m pip install matrix-nio

.\python_embeded\python.exe -m pip install triton-windows

.\python_embeded\python.exe -m pip install sageattn3 --no-build-isolation --extra-index-url https://comfy-org.github.io/wheels

.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --enable-manager

.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --enable-manager --user-directory "D:\data\ai\comfyui\user" --output-directory "D:\data\ai\comfyui\output" --input-directory "D:\data\ai\comfyui\input"
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

openclaw status --usage

openclaw gateway usage-cost

sqlite3 ~/.openclaw/agents/main/agent/openclaw-agent.sqlite \
  "UPDATE auth_profile_store
   SET store_json = json_set(store_json, '\$.profiles.\"openrouter:default\".key', 'API_KEY'),
       updated_at = $(date +%s%3N)
   WHERE store_key = 'primary';"

sqlite3 ~/.openclaw/agents/main/agent/openclaw-agent.sqlite "SELECT store_json FROM auth_profile_store;"
```

## Telegram

https://api.telegram.org/botTHE_GUID_FOR_BOT/getUpdates

