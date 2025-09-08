# NS 项目初始化与任务追踪清单（ns-project-checklist.md）

**文档ID**：ns-project-checklist
**最后更新时间**：2025-09-08
**维护者**：T o（总架构师） + AI 协同支持

---

## 🎯 文档目的

本清单文件用于：

1.  指导 NS 项目的初始化过程（GCP 配置、Terraform、服务账号）
2.  跟踪项目各阶段的关键任务完成情况
3.  为未来迭代提供断点续接与可追溯性基础

---

## ✅ 项目初始化任务

| 阶段 | 操作项 | 是否完成 | 备注 |
| :--- | :--- | :--- | :--- |
| GCP 项目设置 | 创建 GCP 项目 | ✅ | 项目ID: `sigma-outcome` |
| Billing 设置 | 绑定结算账号并启用预算提醒 | ✅ | (已确认) |
| API 启用 | 启用所有必需的GCP服务API | ✅ | (已通过gcloud确认) |
| 本地工具 | 安装 asdf + terraform + gcloud CLI | ✅ | (已通过asdf current确认) |
| Terraform 初始化 | 配置远程 backend，执行 `terraform init` | ⏳ | 待执行 |
| 服务账号 | 通过 Terraform 创建函数运行身份 | ⏳ | 待执行 |
| Firestore 初始化 | 运行 `scripts/init_config.py` 写入初始配置 | ⏳ | 待执行 |

---

## 🧠 抓取函数开发任务

| 抓取类型 | 状态 | 说明 |
| :--- | :--- | :--- |
| `apod` | ⏳ 待开发 | NASA 天文图像日更接口 |
| `asteroids-neows`| ⏳ 待开发 | 近地小行星数据服务 |
| `donki` | ⏳ 待开发 | 空间天气事件数据库 |
| `earth` | ⏳ 待开发 | 地球观测数据 |
| `eonet` | ⏳ 待开发 | 地球观测自然事件追踪 |
| `epic` | ⏳ 待开发 | 地球多色成像相机 |
| `exoplanet` | ⏳ 待开发 | 系外行星档案数据 |
| `genelab` | ⏳ 待开发 | 基因实验室数据系统 |
| `insight` | ⏳ 待开发 | 火星天气服务 |
| `mars-rover-photos`| ⏳ 待开发 | 火星车照片 |
| `nasa-ivl` | ⏳ 待开发 | NASA 图片视频库 |
| `techport` | ⏳ 待开发 | NASA 技术项目数据 |
| `techtransfer` | ⏳ 待开发 | 技术转移数据 |

---

## 🌐 前端任务

| 模块 | 状态 | 说明 |
| :--- | :--- | :--- |
| 前端页面 | ⏳ 待部署 | 静态文件骨架已创建 |
| 配置修改能力 | ❌ 暂不实现 | 当前仅为只读展示用途 |
| 页面托管 | ⏳ 待部署 | 将通过 Cloud Run 部署 |

---

## 🔒 安全与权限任务

| 模块 | 子任务 | 是否完成 | 备注 |
| :--- | :--- | :--- | :--- |
| 服务账号权限 | 通过 Terraform 绑定最小权限 | ⏳ | 待执行 |
| Secrets 管理 | 机密信息通过 `.tfvars` 管理 | ✅ | (决策完成) |
| Firestore 限权 | 通过 Terraform 定义 IAM 策略 | ⏳ | 待执行 |
| 日志权限 | 限制 Cloud Logging Viewer 范围 | ⏳ | 待执行 |

---

## 🧰 工程与维护自动化

| 模块 | 子任务 | 是否完成 | 备注 |
| :--- | :--- | :--- | :--- |
| GitHub 仓库 | 初始化 Git 并推送到远程仓库 | ✅ | (已完成) |
| 文档生成自动化 | Markdown 结构由 AI 协作生成 | ✅ | (当前流程) |
| Firestore 初始化脚本 | `scripts/init_config.py` 文件已创建 | ✅ | (文件已就位) |
| CI/CD | GitHub Actions 自动部署 | ❌ 暂不实现 |
| 开发流程决策 | 不编写自动化测试用例 | ✅ | (决策完成) |

---

## 🧭 下一步行动

* 执行 Terraform 初始化 (`terraform init`)。
* 编写并部署第一个抓取函数 (例如 `apps/apod`) 的代码和 Terraform 配置。