---
name: drawio-everything
description: Use when creating or editing draw.io diagrams, learning reusable styles, layouts and defect-avoidance strategies from examples or positive/negative feedback, or applying previously learned diagram preferences. Also applies to follow-up requests to extract, compare, review, refine, or reuse diagram examples. Not for generic image generation or unrelated charts.
---

# drawio-everything

从图例和具体反馈持续积累风格、模板、局部模式与缺陷经验，再用于可编辑 draw.io 绘图。正向经验帮助选方案，负向案例帮助发现问题，个人偏好指导风格，验证结果决定经验的可复用范围。先明确表达目的，再准确表达关系；用布局组织信息，用风格与色彩增强可读性和美观。优先简单图形，不追求装饰复杂度。

## 按任务读取

- 学习、比较图例或总结反馈：读 [learning.md](references/learning.md) 和 [library.md](references/library.md)。
- 新建或修改图：读 [drawing.md](references/drawing.md) 和 [visual-design.md](references/visual-design.md)，再读资产索引；需要选图种时读 [selection.md](references/selection.md)。
- 反馈修正或交付前复查：读 [quality-review.md](references/quality-review.md)；需要提炼或保存经验时，再读 [learning.md](references/learning.md) 和 [library.md](references/library.md)。
- 更新资产或长期偏好：读 [library.md](references/library.md)。只加载候选记录，不一次读取全部图例。

- 复杂业务图或专业评审：读 [professional-diagrams.md](references/professional-diagrams.md)，先明确关系、异常和省略范围；需要构图备选或局部表达时读 [composition-patterns.md](references/composition-patterns.md)。
- 需要公开示例或空库起步：读 [gallery.md](references/gallery.md)，按需打开 `examples/` 中对应源文件。

## 资产入口

默认库为 `~/.drawio-everything/library/index.json`，`~` 按当前用户主目录解析，不写死创建者路径。用户可以明确指定项目库；不要静默切换库或将项目内容带入个人默认。库不存在时按 library.md 初始化。库独立于 skill 目录，升级指令不覆盖用户资产。

目前是否有已学习模板，以实际索引为准。空库可以使用 drawing.md 的临时基线画图，但不能称其为用户风格。无需安装或依赖第三方 drawio skill；现有工具可按需复用，先核对接口和表示法。

## 核心约定

1. 区分四件事：参考图实际特征、用户明确表达的正负评价、模型推测、验证结果。只有文字描述时记录描述来源，不声称已观察图像。
2. 分别记录风格、结构模板和局部模式。学到的是带适用条件的表达方法，不是所有新图都照搬原图。
3. 同一图种保留多个独立风格与构图模板，按目的、读者、规模和介质选择兼容组合；新案例不自动成为唯一默认。保留风格个性。不要强制统一七色、把深色改浅色或将多个样式平均合并。中文标签不能仅靠英文关键词分类。
4. 图种语义优先于样式：箭头、虚实线和符号有标准含义时，不被视觉预设覆盖。遇到参考图错误，保留可取表达并记录修正。
5. 用户让学习图例即授权保存候选与来源，无需逐项确认。记录为 validated 必须有真实迁移与渲染证据；用户偏好确认与技术验证是两个字段。
6. “这次”修改只影响当前图。只有用户明确要求以后默认如此，才修改长期默认；重复反馈可形成待选建议，不能自动升级。
7. 不把源图中的业务内容、隐含关系或未授权素材复用到新项目。未给定事实保持未知；不能为适应模板虚构节点和连接。
8. 正负反馈标在具体观察与区域上，不给整张图贴好坏标签；同图可保留结构、修正连线。可见缺陷、原因假设、个人偏好与修复验证分别记录。
9. XML 合法和导出成功只证明对应操作完成。交付前按语义、可读性缺陷、审美质量依次检查最终渲染；修正后重渲染受影响页，不沿用旧预览的通过结论。

## 交付

学习任务：给出具体观察、风格/模板/模式候选、相关缺陷经验、适用边界、保存路径与未验证项。必要澄清只问影响结论的问题；其余记录未知并继续。

反馈任务：说明保留与修正的具体区域、阅读影响、修正策略、验收结果与前后对照；原因尚未验证时标假设。用户没有提供原图时，只记录描述来源，不声称已发现或修复图中缺陷。

绘图任务：交付 `.drawio` 源文件与实际可用预览，说明使用的资产及版本、针对内容的适配、验证情况。未完成渲染时仍交付源文件，明确未验证视觉效果，不宣称完整通过。
