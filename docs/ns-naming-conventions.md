# NS 命名规范文档（ns-naming-conventions.md）

**文档ID**：ns-naming-conventions
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协作支持

---

## 🎯 文档目的

本规范文档用于统一 NS 项目在 GCP 各类资源、代码目录、配置键名、日志字段等方面的命名规则，确保整体工程具备一致性、可读性与可维护性。

---

## 🌐 GCP 资源命名规范

| 资源类型                 | 命名规则                                   | 示例                        |
| -------------------- | -------------------------------------- | ------------------------- |
| 项目名称                 | `ns-[env]`                             | `ns-dev`, `ns-prod`       |
| Cloud Function       | `func-[job]`                           | `func-apod-daily`         |
| Cloud Run 服务         | `api-[name]`                           | `api-config-viewer`       |
| Pub/Sub Topic        | `topic-[name]`                         | `topic-job-dispatch`      |
| Pub/Sub Subscription | `sub-[topic]-[purpose]`                | `sub-job-dispatch-logger` |
| Firestore 集合名        | `job_config`, `job_status`, `failures` | 固定命名，避免误操作                |
| Cloud Storage Bucket | `ns-temp-[env]`                        | `ns-temp-dev`             |

> 所有资源命名遵循小写、短横线连接，不使用下划线、驼峰、空格。

---

## 🧩 代码与目录结构命名

### Monorepo 结构

| 类别           | 命名示例                               |
| ------------ | ---------------------------------- |
| 项目根目录        | `ns/`                              |
| GCP 函数目录     | `apps/[job]/` → `apps/apod/`       |
| Terraform 配置 | `infra/gcp/` / `infra/cloudflare/` |
| 公共工具函数       | `packages/utils/`                  |
| 部署脚本         | `scripts/deploy_[target].sh`       |
| 文档目录         | `docs/`                            |

---

## ⚙️ Terraform 命名约定

| 类型     | 规则                                       |
| ------ | ---------------------------------------- |
| 资源名称前缀 | 按功能模块 + 环境组合，例如 `apod_dev_scheduler`     |
| 变量名    | `snake_case` 风格，如 `project_id`, `region` |
| 输出变量   | 统一添加模块前缀，如 `apod_function_url`           |
| 模块目录   | `modules/[resource_type]/`               |

---

## 📄 文档与日志字段命名

### 文档文件名

* 命名格式：`ns-[文档内容说明].md`
* 示例：`ns-security-policy.md`, `ns-data-design.md`

### 日志字段命名

| 字段名            | 说明                      |
| -------------- | ----------------------- |
| `trace_id`     | 用于全链路追踪（来源于 Pub/Sub 消息） |
| `job_id`       | 当前任务类型，如 `apod-daily`   |
| `execution_id` | 某次函数执行的唯一标识             |
| `status`       | 成功/失败状态字段               |
| `duration_ms`  | 执行耗时（毫秒）                |

---

## 🧠 命名原则总结

1. **统一风格**：小写 + 短横线，用于所有 GCP 资源与可视标识
2. **环境隔离**：dev/test/prod 明确体现在命名中（尤其是资源名、bucket）
3. **可读可排序**：日志字段使用有序字段名，支持 BigQuery 或其他结构化查询
4. **无歧义**：避免 job / task / function 等命名重叠
5. **接口即文档**：命名中尽量体现用途，如 `topic-job-dispatch`

---

## ✅ 推荐阅读

* [`ns-resource-inventory.md`](./ns-resource-inventory.md)
* [`ns-observability-guidelines.md`](./ns-observability-guidelines.md)
* [`ns-architecture-summary.md`](./ns-architecture-summary.md)
