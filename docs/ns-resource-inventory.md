# NS 资源清单与 IaC 管理边界 (ns-resource-inventory.md)

**文档ID**: ns-resource-inventory
**最后更新时间**: 2025-09-09
**维护者**: T o（总架构师） + AI 协同支持

---

## 🎯 文档目的

本文件是 NS 项目云端资源的**唯一事实来源 (Single Source of Truth)**。它旨在：
1.  **全面盘点**: 完整列出由 Terraform 在 GCP `sigma-outcome` 项目中创建和管理的所有资源。
2.  **明确边界**: 清晰定义哪些资源由 IaC (Terraform) 管理，哪些由其他方式（手动、脚本、GCP自动生成）管理。
3.  **解释关联**: 说明核心资源之间的关系及其在整体架构中的作用。

---

## 📈 资源概览

当前，本项目在云端共部署了 **46 个**核心基础设施资源，分布如下：

| 资源类别 | 数量 | 备注 |
| :--- | :-- | :--- |
| Cloud Functions | 14 | 1个总调度员 + 13个工作函数 |
| Pub/Sub Topics | 14 | 1个调度主题 + 13个工作主题 |
| Cloud Schedulers | 3 | 按每日/每小时/每周划分 |
| GCS Buckets | 1 | `ns-2025` 统一存储桶 |
| GCS Objects | 14 | 14个函数的源码压缩包 |
| **总计** | **46** | |

---

## 🕹️ 管理边界说明

清晰的管理边界是保证基础设施稳定性的基石。

### 1. ✅ 由 Terraform 严格管理的资源
以下所有类型的资源，其**生命周期（创建、更新、销毁）完全由 Terraform 代码控制**。**严禁**在 GCP Console 中对这些资源进行任何手动修改，否则会导致状态漂移。

* `google_storage_bucket`
* `google_storage_bucket_object`
* `google_pubsub_topic`
* `google_cloudfunctions2_function`
* `google_cloud_scheduler_job`

### 2. 🟡 手动或脚本管理的资源
以下资源不由 Terraform 直接管理，其变更应遵循特定流程。

* **IAM 权限绑定**: 我们已通过 `gcloud` 命令为默认服务账号授予了所需角色。此操作为一次性初始化，当前未纳入Terraform管理。
* **Firestore 数据**: `job_config` 和 `job_status` 等集合中的**数据**，属于应用层数据，将通过 `scripts/init_config.py` 等脚本或应用逻辑进行管理。

### 3. 🚫 GCP 自动生成的资源
在部署过程中，GCP 会自动创建一些辅助性资源。我们**不应也无需**管理或修改它们。

* **`gcf-v2-sources-[...]-[region]` GCS Bucket**: Cloud Functions 服务用于存放中间构建产物的内部存储桶。
* **`[project-id]_cloudbuild` GCS Bucket**: Cloud Build 服务用于存放构建日志的默认存储桶。
* **Eventarc 触发器**: 每个Cloud Function的事件触发器，在后台由GCP管理。

---

## 🗂️ 详细资源清单

| 逻辑分组 | 资源类型 | Terraform 资源名 | GCP 实际名称 / 作用 |
| :--- | :--- | :--- | :--- |
| **存储系统** | `google_storage_bucket` | `function_source_code` | **`ns-2025`**: 统一存储桶，根目录下有`source/`文件夹。 |
| | `google_storage_bucket_object`| `source_objects["dispatcher"]` | **`source/dispatcher/...zip`**: 总调度函数的源码包。 |
| | `google_storage_bucket_object`| `source_objects["apod"]` | **`source/apod/...zip`**: APOD工作函数的源码包。 |
| | `...` | `...` | (...其余12个工作函数的源码包) |
| **消息系统** | `google_pubsub_topic` | `scheduler_triggers_topic`| **`ns-topic-scheduler-triggers`**: 供3个调度器发布通用信号的**总调度Topic**。 |
| | `google_pubsub_topic` | `worker_topics["apod"]` | **`ns-topic-apod`**: APOD工作函数的**专属Topic**。 |
| | `google_pubsub_topic` | `worker_topics["neows"]` | **`ns-topic-asteroids-neows`**: NeoWs工作函数的**专属Topic**。 |
| | `...` | `...` | (...其余11个工作函数的专属Topic) |
| **计算核心** | `google_cloudfunctions2_function` | `dispatcher_function` | **`ns-func-dispatcher`**: **总调度函数**，接收通用信号并向各专属Topic分发任务。 |
| | `google_cloudfunctions2_function` | `worker_functions["apod"]` | **`ns-func-apod`**: **APOD工作函数**，监听`ns-topic-apod`并执行抓取。 |
| | `google_cloudfunctions2_function` | `worker_functions["neows"]` | **`ns-func-asteroids-neows`**: **NeoWs工作函数**，监听`ns-topic-asteroids-neows`。|
| | `...` | `...` | (...其余11个工作函数) |
| **调度系统** | `google_cloud_scheduler_job` | `daily_scheduler` | **`ns-scheduler-main-daily`**: **每日调度器**，触发总调度函数处理每日任务。 |
| | `google_cloud_scheduler_job` | `hourly_scheduler` | **`ns-scheduler-fast-hourly`**: **每小时调度器**，处理高频任务。 |
| | `google_cloud_scheduler_job` | `weekly_scheduler` | **`ns-scheduler-slow-weekly`**: **每周调度器**，处理低频任务。 |