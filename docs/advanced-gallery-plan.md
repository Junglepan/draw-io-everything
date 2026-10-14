# 进阶画廊：专业信息密度

## 目标

以四种真实工作问题组织虚构场景，在可读性之外体现关系含义、边界、异常处理和数据口径。保留入门示例；新示例置于 README 首屏。

## 文件与分工

- `scripts/build_advanced_architecture.py` → `examples/advanced/retail-landscape.*`、`revenue-lineage.*`。
- `scripts/build_advanced_process.py` → `examples/advanced/returns-collaboration.*`、`reconciliation-flow.*`。
- `references/professional-diagrams.md`：专业图的选型与质量准则。
- `references/gallery.md`、`README.md`：场景入口与预览。
- `scripts/check_gallery.py`：同时校验基础与进阶示例。

## 验收

原生可编辑；虚构事实与省略范围明确；图种语义一致；长标签可读；线不穿越无关节点；条件分支与循环出口明确；每个 PNG 从相应源文件实际导出并目视检查。仅通过固定场景检查，不宣称全面 BPMN/C4 合规或任意规模自动布局。

## 来源边界

用户指定的四幅图是设计参考。本次提炼阅读顺序、分组、文字层级与语义表达，不复制其业务事实、原图或产品 UI。个人偏好保存在本地资产库，不作为所有使用者的默认风格。
