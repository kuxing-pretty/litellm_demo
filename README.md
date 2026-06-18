# LiteLLM Demo - Claude Code 使用自定义模型

通过 LiteLLM Proxy 将 Claude Code 的请求转发到 DashScope 的 qwen3.7-plus 模型。

## 架构

```
Claude Code (VS Code)
    |  Anthropic Messages API
    |  model: claude-sonnet-4-6 / claude-opus-4-8 / ...
    |  Base URL: http://localhost:4000
    v
LiteLLM Proxy (localhost:4000)
    |  Anthropic -> OpenAI 协议转换
    v
DashScope API (dashscope.aliyuncs.com)
    |
    v
qwen3.7-plus
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `.env` | DashScope API Key 和 Base URL |
| `config.yaml` | LiteLLM 代理配置，映射模型名到 qwen3.7-plus |
| `test_litellm_sdk.py` | SDK 直接调用测试脚本 |
| `.claude/settings.local.json` | Claude Code 项目级环境变量 |

## 使用步骤

### 1. 安装依赖

```bash
pip install litellm[proxy] python-dotenv
```

### 2. 配置 .env

确保 `.env` 文件中包含：

```
DASHSCOPE_API_KEY="your-api-key"
DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

### 3. 启动 LiteLLM 代理

```bash
cd e:\AI\project_codes\litellm_demo
litellm --config config.yaml --port 4000
```

启动成功后会显示：

```
LiteLLM: Proxy initialized with Config, Set models:
    qwen3.7-plus
    claude-sonnet-4-6
    claude-opus-4-8
    claude-haiku-4-5-20251001
    claude-fable-5
```

### 4. 验证代理

```bash
# 健康检查
curl http://localhost:4000/health

# 列出可用模型
curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-litellm-demo-key"

# 测试调用
curl -X POST http://localhost:4000/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk-litellm-demo-key" \
  -d "{\"model\": \"claude-sonnet-4-6\", \"max_tokens\": 100, \"messages\": [{\"role\": \"user\", \"content\": \"say hello\"}]}"
```

### 5. 配置 Claude Code

在 Claude Code 中设置环境变量，指向 LiteLLM 代理：

```bash
export ANTHROPIC_BASE_URL="http://localhost:4000"
export ANTHROPIC_API_KEY="sk-litellm-demo-key"
```

或者通过项目级 `.claude/settings.local.json` 自动加载：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:4000",
    "ANTHROPIC_API_KEY": "sk-litellm-demo-key"
  }
}
```

### 6. SDK 测试（可选）

```bash
python test_litellm_sdk.py
```

## 注意事项

- **Windows 编码**：`config.yaml` 中不要使用中文注释，否则 YAML 解析器在 Windows 上会因 GBK 编码报错
- **master_key**：`sk-litellm-demo-key` 是 LiteLLM 代理的访问密钥，Claude Code 的 `ANTHROPIC_API_KEY` 需与之匹配
- **模型映射**：Claude Code 无论选择哪个 Claude 模型名，都会被路由到 qwen3.7-plus
- **drop_params**：自动丢弃 DashScope 不支持的参数，避免请求报错

## Settings 加载优先级

Claude Code 的 settings 加载顺序（从低到高）：

1. `~/.claude/settings.json` — 用户全局配置
2. `<project>/.claude/settings.json` — 项目共享配置（可提交到 git）
3. `<project>/.claude/settings.local.json` — 项目本地配置（不提交到 git）

**不会冲突**：`settings.local.json` 中的 `env` 字段会合并到全局设置中，同名环境变量会被项目级覆盖。
