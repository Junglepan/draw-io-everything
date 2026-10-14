# 持久资产约定

## 存储和索引

默认根目录为 `~/.drawio-everything/library`；用户指定库时将以下路径相对该根解析。源文件与业务内容可能敏感，保留本地，不自动同步、发布或提交版本控制。

`index.json` 初始内容：

```json
{"schema_version":1,"assets":[],"defaults":{}}
```

assets 的每条索引使用 `{id, kind, version, path, status, tags}`，kind 为 example/style/template/pattern/feedback；path 是库内相对路径。索引只列每个 id 的当前版本，历史由记录的 previous 指向。status 取 candidate/validated/deprecated。example 和 feedback 通常保留 candidate，不表示用户未认可。

按需创建 `examples/`、`styles/`、`templates/`、`patterns/`、`feedback/`、`sources/`、`previews/`；没有内容不批量造占位资产。命名使用稳定的 ASCII id 和正整数 version，如 `templates/three-column-pipeline.v1.json`。原始文件保留扩展名，记录文件哈希以识别重复；不覆盖用户原件。

## 记录字段

所有记录包含：`schema_version:1`、`id`、`kind`、`version`、`status`、`title`、`created_at`、`updated_at`、`previous`（首次 null，后续旧版本相对路径）、`sources`、`tags`、`applicability`、`user_preference`、`validation`、`change_reason`。

- sources：数组，每项包含 `type`（image/drawio/url/text_description）、`location`（真实路径、URL 或文字来源）、`sha256`（未知 null）、`observed`（是否直接读取该 type 的来源；读过 text_description 不表示见过图片）、`notes`。转换产物与原始来源分开标识。
- applicability：`diagram_types`、`audiences`、`use_when`、`avoid_when`，均为数组。
- user_preference：`status`（unknown/partial/endorsed/rejected）、`liked_aspects`、`disliked_aspects`、`evidence`。用户认可不等于技术通过。
- validation：`status`（not_run/simulated/passed/failed）、`cases`。每个 case 记录场景、原生文件、预览路径、结构检查、语义检查、视觉检查、结果和日期；没有证据的字段为 null。
- status=validated 仅用于 style/template/pattern，且 validation=passed，至少一个新内容迁移案例有真实源文件和渲染检查。用于提炼的原图本身不是迁移案例。

按 kind 添加以下字段：

| kind | 必填内容 |
| --- | --- |
| example | observations 数组：aspect、value、basis（measured/visual_estimate/user_description/inference）、confidence（high/medium/low）、region；derived_assets 数组 |
| style | tokens 对象：palette、typography、shapes、edges、spacing、iconography；每项写 value、basis、confidence，不确定为 null；semantic_exceptions 数组 |
| template | skeleton（区域与槽位）、fixed_features、variable_slots、layout_rules、growth_rules、overflow_rules、style_refs、pattern_refs、artifact（无原生模板时 null） |
| pattern | problem、structure、adaptation_rules、semantic_constraints、artifact |
| feedback | scope（current_diagram/asset/global）、target、request、before、after、applied、promote_to_default（默认 false） |

style_refs 和 pattern_refs 使用 `{id, version}`，不使用模糊“最新”。骨架中的槽位描述角色与关系，不复制源图的业务事实。文字描述的骨架不是已生成的原生 draw.io 模板。

defaults 按用户明确的范围设置，如 `{"architecture":{"style":{"id":"...","version":1}}}`；没有明确授权保持 `{}`。不要将 unknown 自动解析成已确认默认。

## 写入和读取

1. 修改前读索引和目标记录；同一来源和内容优先复用而不重复入库。
2. 新记录或新版本先写文件，再更新索引，保留旧版本。使用 JSON 解析/序列化，不通过文本替换修改结构。
3. 检查 id 与路径冲突、必填字段、引用的 id/version 是否存在、库内路径无越界。发现并发改变先重新读取，不覆盖他人更新。
4. 索引更新用同目录临时文件加原子替换；保存后回读 JSON，确认索引与记录一致。
5. 文件写入失败则保留已有版本并报告未保存的内容，不声称记忆已更新。

检索先筛 diagram_types、use_when、audiences 与 validation，再评估结构相似度。显式指定候选可使用，但交付要标未验证；无合适模板时新建布局，不硬套。
