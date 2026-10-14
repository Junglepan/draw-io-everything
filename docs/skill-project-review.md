# draw.io skill 项目鉴赏与取舍

本次查看了公开仓库 README 与可访问的 skill 指令；属于文档与工作流评审，没有安装、执行或全面审计第三方项目，也不以星数判断绘图质量。下面是针对本项目目标的取舍，不是通用排名。

| 项目 | 值得借鉴的做法 | 本项目的落点 |
| --- | --- | --- |
| [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | 将生成、导出、样式复用和多来源绘图纳入完整流程 | 保持可编辑源文件与渲染闭环；按需求选择工具，不为图标数量或输出格式扩张依赖 |
| [Sunwood-ai-labs/draw-io-skill](https://github.com/Sunwood-ai-labs/draw-io-skill) | 检查连线穿框、标签碰撞、文字对比度和溢出；强调 lint 不能替代视觉检查 | 将这些缺陷作为视觉审阅清单；当前只宣称本仓库实际具备的结构检查，不假称拥有其 SVG linter |
| [uulab-official/drawio-skills](https://github.com/uulab-official/drawio-skills) | 先建立结构化图模型，再生成可编辑图，并设置质量门槛 | 先确定节点、关系、边界及事实，再安排坐标和颜色；固定示例使用可复现脚本，不引入本次不需要的完整中间表示引擎 |

## 我们吸收的经验

1. 原生 `.drawio` 是编辑依据。预览必须从对应源文件导出，修源后重渲染，不单独修 PNG。
2. 可测的结构问题交给代码；语义和视觉仍需要实际审阅。成功解析 XML 不证明图好看。
3. 先定义图要回答的问题，再选布局。画廊按用途组织，不能只是同一模板换颜色。
4. 用来源、适用范围、迁移案例和版本积累经验；审美偏好与技术验证分别记录。
5. 把常见失败变成可执行的检查点：长标签、短箭头末端、边界标题碰撞、线穿节点、聚合含义不清。

## 本次未采用

不复制第三方代码、图例或整个 skill 指令；不增加自动更新、自运行服务、品牌图标集合或通用自动布局引擎。已有基础图形足以覆盖当前目标，重点仍是关系准确、比例、间距、配色和可读性。

## 公开材料

- [Sunwood 的 skill 指令](https://github.com/Sunwood-ai-labs/draw-io-skill/blob/main/SKILL.md)
- [uulab 的 README](https://github.com/uulab-official/drawio-skills/blob/main/README.md)
- [Agents365 仓库](https://github.com/Agents365-ai/drawio-skill)

以上功能描述以本次访问的材料为准，不把项目宣传视为本地验证结果。
