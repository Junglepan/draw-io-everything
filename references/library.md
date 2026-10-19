# 持久资产约定

## 存储和索引

默认根目录为 `~/.drawio-everything/library`；用户指定库时将以下路径相对该根解析。源文件与业务内容可能敏感，保留本地，不自动同步、发布或提交版本控制。

技能改名为 `draw-io-everything` 不改变此兼容路径；不自动搬移、合并或覆盖既有个人库。

`index.json` 初始内容：

```json
{"schema_version":1,"assets":[],"defaults":{}}
```

assets 的每条索引使用 `{id, kind, version, path, status, tags}`，kind 为 example/style/template/pattern/feedback；path 是库内相对路径。索引只列每个 id 的当前版本，历史由记录的 previous 指向。status 取 candidate/validated/deprecated。example 和 feedback 通常保留 candidate，不表示用户未认可。

按需创建 `examples/`、`styles/`、`templates/`、`patterns/`、`feedback/`、`sources/`、`previews/`；没有内容不批量造占位资产。命名使用稳定的 ASCII id 和正整数 version，如 `templates/three-column-pipeline.v1.json`。原始文件保留扩展名，记录文件哈希以识别重复；不覆盖用户原件。

## 记录字段

所有记录包含：`schema_version:1`、`id`、`kind`、`version`、`status`、`title`、`created_at`、`updated_at`、`previous`（首次 null，后续旧版本相对路径）、`sources`、`tags`、`applicability`、`user_preference`、`validation`、`change_reason`。

- sources：数组，每项包含 `type`（image/drawio/puml/url/text_description）、`location`（真实路径、URL 或文字来源）、`sha256`（未知 null）、`observed`（是否直接读取该 type 的来源；读过 text_description 不表示见过图片）、`notes`。转换产物与原始来源分开标识。
- applicability：`diagram_types`、`audiences`、`use_when`、`avoid_when`，均为数组。
- user_preference：`status`（unknown/partial/endorsed/rejected）、`liked_aspects`、`disliked_aspects`、`evidence`。用户认可不等于技术通过。
- validation：`status`（not_run/simulated/passed/failed）、`cases`。每个 case 记录场景、原生文件、预览路径、结构检查、语义检查、视觉检查、结果和日期；没有证据的字段为 null。
- status=validated 仅用于 style/template/pattern，且 validation=passed，至少一个新内容迁移案例有真实源文件和渲染检查。用于提炼的原图本身不是迁移案例。

PlantUML 资产另记源格式 puml、所需本地 include 样式及其哈希；validation.cases 记录 PlantUML 版本、JAR 校验值、JDK、字体和语法/渲染结果，并保留独立的语义与视觉检查。已有个人候选不能因为公开示例通过就自动标为 validated。

按 kind 添加以下字段：

| kind | 必填内容 |
| --- | --- |
| example | observations 数组：aspect、value、basis（measured/visual_estimate/user_description/inference）、confidence（high/medium/low）、region；derived_assets 数组 |
| style | tokens 对象：palette、typography、shapes、edges、spacing、iconography；每项写 value、basis、confidence，不确定为 null；semantic_exceptions 数组 |
| template | skeleton（区域与槽位）、fixed_features、variable_slots、layout_rules、growth_rules、overflow_rules、style_refs、pattern_refs、artifact（无原生模板时 null） |
| pattern | problem、structure、adaptation_rules、semantic_constraints、artifact |
| feedback | scope（current_diagram/asset/global）、target、request、before、after、applied、promote_to_default（默认 false） |

### 观察、缺陷与前后对照

复用现有 examples/、feedback/、patterns/，以字段区分反馈，不新增正向库、负向库或评分系统。以下为 schema_version=1 的增量字段约定：旧记录缺少字段时按 unknown/null/空数组读取，不自动改写历史或推断通过；新增或更新反馈时补齐对应字段。

example.observations 和 feedback.observations 使用相同的观察结构。feedback 新增 observations 数组，每项保留 example 原有的 aspect、value、basis、confidence、region，并补充：

| 字段 | 内容 |
| --- | --- |
| feedback_type | positive/negative/mixed/unknown；评价针对本条观察，不代表整图结论 |
| source_refs | 本记录 sources 的 location 数组，指向实际来源；region 用页名、cell id 或可定位区域描述 |
| reading_impact | 具体改善或妨碍的阅读行为；未知 null |
| cause_hypothesis | `{explanation, status, evidence}`；status 为 untested/supported/refuted；没有假设时 null，修复前不写 supported |
| strategy | 保留、修正或规避方法；尚未提出时 null |
| acceptance_criteria | 可在最终渲染上核对的条件数组；负反馈不得仅写“更美观” |
| before / after | `{source_file, preview_file, region}`，文件为真实路径，未提供或未生成的字段 null；after 整体可为 null |
| validation | 与记录级 validation 相同的 `{status, cases}`；只评价本条观察，不能由整图导出成功自动设为 passed |

每条负反馈都记录来源、区域、缺陷（value）、阅读影响、原因假设、策略、验收条件、前后对照和验证状态。未查明的项留空并说明缺口，不补造截图或原因。混合反馈可拆为共享 source_refs 的正负观察；保留项与修正项分别定位。feedback 顶层 before/after 表示本次修改的整体产物，observations 中的 before/after 定位局部；保持两者一致。

user_preference 继续只记录用户明确表达的评价与范围，个人偏好不自动变成质量禁令。局部反馈仍使用 scope=current_diagram、promote_to_default=false；未经明确要求不写 defaults。发现可复用的规避方法时，可建立有版本的 pattern；example 和 feedback 可用 derived_assets 数组关联提炼产物，每项为 `{id, version}`，原始反馈保留原 kind 和来源。

validation.cases 中分别记录结构、语义、可读性与审美结果，以及整体适屏和实际阅读尺寸两种检查尺度；未执行项为 null。附最终源文件和预览的哈希、所改变的变量、未解决问题与检查日期，以识别旧预览和过期结论。修复当前案例与新内容迁移是不同 case；validated 的门槛仍要求真实迁移与渲染证据，不因记录字段齐全或用户认可而放宽。

style_refs 和 pattern_refs 使用 `{id, version}`，不使用模糊“最新”。骨架中的槽位描述角色与关系，不复制源图的业务事实。文字描述的骨架不是已生成的原生 draw.io 模板。

defaults 按用户明确的范围设置，如 `{"architecture":{"style":{"id":"...","version":1}}}`；没有明确授权保持 `{}`。不要将 unknown 自动解析成已确认默认。

## 写入和读取

1. 修改前读索引和目标记录；同一来源和内容优先复用而不重复入库。
2. 新记录或新版本先写文件，再更新索引，保留旧版本。使用 JSON 解析/序列化，不通过文本替换修改结构。
3. 检查 id 与路径冲突、必填字段、引用的 id/version 是否存在、库内路径无越界。发现并发改变先重新读取，不覆盖他人更新。
4. 索引更新用同目录临时文件加原子替换；保存后回读 JSON，确认索引与记录一致。
5. 文件写入失败则保留已有版本并报告未保存的内容，不声称记忆已更新。

检索先筛 diagram_types、use_when、audiences，再评估结构相似度与验证范围。索引 tags 可补充跨区、多分支、回流、长标签及缺陷类别等标签，按需读取少量相关记录：正向候选帮助选布局，负向观察帮助生成本次检查项，明确的个人偏好帮助选风格。负反馈即使 validation=not_run 也可用于提示风险，但其修复策略不能称已验证。显式指定候选可使用，但交付要标未验证；无合适模板时新建布局，不硬套。不要一次加载全部历史反馈。
