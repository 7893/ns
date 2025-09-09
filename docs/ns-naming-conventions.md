# NS 命名规范文档（ns-naming-conventions.md）

**文档ID**: ns-naming-conventions
**最后更新时间**: 2025-09-09
**维护者**: T o（总架构师） + AI 协同支持

---

## 🎯 文档目的

本规范文档用于统一 NS 项目在**所有层面**的命名规则，包括但不限于：GCP 资源、Terraform 代码、代码目录、配置键名、日志字段等。

制定本规范的目标是：
* **提高可读性**: 任何成员都能通过名称快速理解组件的用途。
* **降低歧义**: 避免因命名混乱导致的配置错误。
* **支持自动化**: 规范的命名便于编写自动化脚本进行管理和监控。
* **确保一致性**: 保证整个项目的工程外观和感觉高度统一。

---

## 🧠 核心命名哲学

所有命名都应遵循以下三大哲学原则：

1.  **`ns-` 前缀原则**: 所有在GCP上创建的、由本项目管理的资源，都必须以 `ns-` 作为前缀。
    * **理由**: 这是项目的命名空间（Namespace），可以在GCP控制台数以百计的资源中，**一眼识别**出属于本项目的资源，便于筛选、权限管理和成本核算。

2.  **结构化命名原则**: 采用 `[前缀]-[类型]-[功能]-[环境]` 的分段式结构。
    * **理由**: 这种结构使名称本身携带了大量元信息，且便于排序和过滤。例如，`ns-func-apod-prod` 清晰地表明了它属于 `ns` 项目、是一个`函数`、功能是 `apod`、部署在 `prod` 环境。

3.  **小写与短横线原则**: 所有GCP资源名称必须使用`kebab-case`（小写字母和短横线）。
    * **理由**: 这是Google Cloud推荐的、也是业界最广泛的实践。它可以保证与DNS等系统的最大兼容性，避免因大小写或下划线(`_`)导致的一些潜在问题。

---

## 🌐 GCP 资源命名规范

| 资源类型 | 命名模式 | 示例 | 详细说明 |
| :--- | :--- | :--- | :--- |
| Cloud Function | `ns-func-[job]` | `ns-func-apod`, `ns-func-dispatcher` | `[job]`部分应清晰描述函数的核心业务。 |
| Pub/Sub Topic | `ns-topic-[name]` | `ns-topic-scheduler-triggers`, `ns-topic-apod` | `[name]`部分描述该主题承载的消息类型或目标。 |
| Cloud Storage Bucket| `ns-[year]` | `ns-2025` | **全局唯一**。命名必须在所有GCP用户中唯一，因此采用项目名+年份的组合。 |
| Cloud Scheduler | `ns-scheduler-[frequency]`| `ns-scheduler-main-daily`, `ns-scheduler-fast-hourly` | `[frequency]`部分描述该调度任务的频率或分组。|
| Firestore 集合名 | `[purpose]_[type]`| `job_config`, `job_status` | **例外**：应用层数据，不加`ns-`前缀，使用蛇形命名法(`snake_case`)。 |

---

## ⚙️ Terraform 资源与变量命名

| 元素类型 | 命名规则 | 示例 | 详细说明 |
| :--- | :--- | :--- | :--- |
| **Terraform 资源** | `[provider]_[type].[name]` | `google_pubsub_topic.worker_topics` | 遵循 `snake_case`。`[name]`应能体现其逻辑作用，例如`worker_topics`代表一组工作主题。|
| **Terraform 变量** | `snake_case` | `variable "project_id" {}` | 所有在 `variables.tf` 中定义的变量。|
| **Terraform 本地变量**| `snake_case` | `locals { worker_functions = ... }` | 所有在 `locals.tf` 中定义的本地变量。|
| **Terraform 输出** | `snake_case` | `output "dispatcher_function_uri" {}` | 所有在 `outputs.tf` 中定义的输出。|

---

## 📄 代码与目录结构命名

| 类别 | 命名示例 | 详细说明 |
| :--- | :--- | :--- |
| 项目根目录 | `ns/` | 简洁，作为所有子目录的命名空间。 |
| GCP 函数目录 | `apps/[job]/` → `apps/apod/` | 每个函数一个独立目录，目录名与函数功能名一致。 |
| Terraform 配置 | `infra/gcp/` | 按云厂商和环境划分，结构清晰。 |
| 公共代码包 | `packages/ns_packages/` | 可供多个函数共享的Python包。 |
| 脚本目录 | `scripts/` | 存放辅助性、一次性的脚本，如 `init_config.py`。 |
| 文档目录 | `docs/` | 存放所有Markdown设计文档。 |

---

## 🔍 日志与元数据字段命名

为了实现有效的可观测性，所有结构化日志和 Firestore 状态记录中的字段都应遵循以下规范（`snake_case`）。

| 字段名 | 类型 | 示例值 | 详细说明 |
| :--- | :--- | :--- | :--- |
| `trace_id` | String | `"abc-123-xyz-456"` | **(规划中)** 用于贯穿整个调用链路的唯一ID。 |
| `job_id` | String | `"apod"` | 任务的唯一标识符，与函数名和Topic名中的功能部分对应。|
| `status` | String | `"SUCCESS"`, `"ERROR"` | 表示任务执行的最终状态。 |
| `duration_ms` | Integer| `1784` | 任务执行的总耗时，单位为毫秒。 |
| `event_type` | String | `"job_dispatched"`, `"api_fetch_failed"` | 描述日志所记录的业务事件类型。 |
| `trigger_type` | String | `"scheduler"`, `"manual"` | 触发本次任务的来源。 |
| `error_message`| String | `"API returned status 500"` | 当 `status` 为 `ERROR` 时，记录详细的错误信息。|

---

## ✅ 命名实践清单 (Dos and Don'ts)

-   **务必 (Do)**:
    -   所有GCP资源都以 `ns-` 开头。
    -   使用 `kebab-case` (短横线连接) 为GCP资源命名。
    -   使用 `snake_case` (下划线连接) 为Terraform资源和变量命名。
    -   让名称具有描述性，见名知意。

-   **禁止 (Don't)**:
    -   在GCP资源名称中使用大写字母或下划线。
    -   使用模糊不清的名称，如 `test-bucket`, `my-function`。
    -   在不同类型的资源上混用命名风格。