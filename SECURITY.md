# 安全指南

## 🔒 敏感信息保护

### 禁止提交的文件类型
- `.env` - 环境变量文件
- `*.tfstate*` - Terraform状态文件
- `*.json` - 服务账号密钥文件（除package.json）
- `*.key`, `*.pem` - 私钥文件

### 环境变量管理
- 使用 `.env.example` 作为模板
- 本地开发使用 `.env` 文件（已被gitignore）
- 生产环境使用GitHub Secrets

### API密钥使用规范
```python
# ✅ 正确：从环境变量读取
api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")

# ❌ 错误：硬编码密钥
api_key = "ILeecsesMNeEs1LBJRa8G2R5RYKdp0I50d4nbyOo"
```

### 安全检查
运行安全检查脚本：
```bash
./scripts/security-check.sh
```

### Git钩子
项目已配置pre-commit钩子，会在提交前自动检查敏感信息。

## 🚨 发现安全问题？
请立即联系项目维护者，不要在公开渠道讨论。
