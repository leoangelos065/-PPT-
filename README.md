# 图片转ppt功能 · Image to editable PowerPoint

把截图、流程图、信息图重建为高保真、可编辑的 `.pptx`。适用于 Codex；包含 Windows 与 macOS 的执行说明。

这是一套经过实际迭代的 agent skill，不是一键转换程序，也不承诺任意图片都能像素级还原。效果取决于源图质量、字体、可用工具和实际渲染核验。

## 在 Mac 或 Windows 安装

在 Codex 新对话中粘贴：

```text
使用 $skill-installer 安装 https://github.com/leoangelos065/-PPT-/tree/main/skills/image-to-ppt-function
```

安装后，在下一轮对话使用；如果未显示，重启 Codex。

手动安装：下载本仓库 ZIP，把 `skills/image-to-ppt-function` 文件夹放到本机的用户 skills 目录。当前官方文档的用户目录是 `~/.agents/skills/`；部分安装器或旧环境使用 `~/.codex/skills/`，以本机实际发现的目录为准，不要在两个目录同时安装同名副本。

官方说明：[Build skills](https://learn.chatgpt.com/docs/build-skills)。

## 激活

附上原始图片，然后输入：

```text
使用 $image-to-ppt-function 把这张图重建为可编辑 PPT。保留普通可编辑文字、独立可拖动组件，并与上传原图逐区域核验。
```

也可输入“使用图片转ppt功能”。

## 核心标准

- 标题、正文、图中标签保留普通文本，匹配字体、字重、局部加粗、字号、字距、基线和颜色。
- 面板、边框、分隔线、徽章等拆为原生组件；可组合移动，子项仍可编辑。
- 勾号等图案不用外观不同的字体字符凑合；按原图使用独立路径或紧密裁切图片。
- 圆形内的文字需核对大小写、拼写、轮廓相对位置和视觉居中，不擅自纠正原图文字。
- 用原始上传文件验收，不把粘贴进 PPT 后的图片当唯一基准。
- 通过实际 PPT 渲染和局部对照迭代，不以整页平均误差或结构检查代替视觉核验。
- 在用户授权自我更新的任务中，把验证过的教训写回本机 skill；不后台运行，不自动上传更新到 GitHub。

## 环境与边界

Skill 本身是文本指令。附带的结构验收脚本只需要 Python 3.10+ 标准库：

```sh
python3 skills/image-to-ppt-function/scripts/audit_pptx.py --pptx your-file.pptx --report audit.json
```

生成与渲染 PPT 需要 agent 环境中相应的工具。常见 Python 路线会使用 `python-pptx`、Pillow、NumPy；字形描摹可选 Inkscape。脚本不会自动安装软件、下载模型或调用付费接口。

Windows 可使用 PowerPoint COM；macOS 不支持 Windows COM，应使用当地可用的 PowerPoint 导出方式或明确标注的替代渲染器。macOS 安装后的真实 PowerPoint 渲染结果尚未在本仓库制作环境中测试，不能仅因能安装就宣称跨设备外观完全一致。

字体不随仓库分发。缺少字体时从有权分发的来源获取并核对具体字重；不得用未经授权的商业字体包。照片、复杂艺术和照片内标注可能保留为独立图片，需要在交付时说明。

## 更新

重新安装前保留本机自我更新的 `SKILL.md`，先比较差异，避免覆盖你的改进。仓库更新与本机自我更新是两回事；向 GitHub 发布变更需另行明确授权。

仓库不包含用户原始图片、PPT、聊天记录、账号凭据、下载的字体或第三方模型。
