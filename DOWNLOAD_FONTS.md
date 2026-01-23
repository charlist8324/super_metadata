# 下载 Font Awesome 字体文件（手动）

## 问题
图标显示为方块或空白，是因为缺少 Font Awesome 的字体文件。

## 解决方案

### 方法一：手动下载（推荐）

#### 步骤 1：下载字体文件

访问以下链接下载 Font Awesome 6.0.0 Web 版本：

**下载地址：**
```
https://use.fontawesome.com/releases/v6.0.0/fontawesome-free-6.0.0-web.zip
```

或者从 GitHub 下载：
```
https://github.com/FortAwesome/Font-Awesome/releases/download/6.0.0/fontawesome-free-6.0.0-web.zip
```

#### 步骤 2：解压文件

下载完成后，解压 `fontawesome-free-6.0.0-web.zip` 文件。

#### 步骤 3：复制字体文件

在解压后的文件夹中，找到 `webfonts/` 目录，复制以下文件到项目目录：

**目标目录：**
```
D:\python\py_opencode\metadata_manager\static\libs\fontawesome\webfonts\
```

**需要复制的文件：**
```
fa-solid-900.woff2
fa-regular-400.woff2
fa-brands-400.woff2
fa-v4compatibility.ttf
```

**完整路径示例：**
```
从: fontawesome-free-6.0.0-web/webfonts/fa-solid-900.woff2
到: D:\python\py_opencode\metadata_manager\static\libs\fontawesome\webfonts\fa-solid-900.woff2
```

#### 步骤 4：验证

复制完成后，检查 `webfonts` 目录应该包含：
```
static/libs/fontawesome/webfonts/
├── fa-solid-900.woff2
├── fa-regular-400.woff2
├── fa-brands-400.woff2
└── fa-v4compatibility.ttf
```

#### 步骤 5：刷新浏览器

刷新浏览器页面，图标应该正常显示了。

---

### 方法二：使用下载脚本（需要网络访问 GitHub）

如果网络可以访问 GitHub，运行：
```bash
python download_fonts.py
```

该脚本会自动下载并提取字体文件。

---

### 方法三：禁用图标（临时方案）

如果暂时不需要图标，可以暂时忽略此问题，系统功能不受影响。

---

## 常见问题

### Q: 图标还是不显示？
A: 检查浏览器控制台（F12）→ Network 标签，查看字体文件是否加载成功（状态 200）。

### Q: 下载后图标还是方块？
A: 清除浏览器缓存并刷新：
- Windows: `Ctrl + Shift + Delete`
- Mac: `Cmd + Shift + Delete`

### Q: 只想用基础图标，能不下载吗？
A: 不能，Font Awesome 的所有图标都需要字体文件支持。

---

## 字体文件说明

| 文件 | 用途 | 图标类型 |
|------|------|----------|
| fa-solid-900.woff2 | 实心图标 | `fas fa-*` |
| fa-regular-400.woff2 | 线条图标 | `far fa-*` |
| fa-brands-400.woff2 | 品牌图标 | `fab fa-*` |
| fa-v4compatibility.ttf | v4 兼容 | 旧版图标 |

---

## 快速验证

下载完成后，访问：http://localhost:5000

应该能看到：
- ✅ 用户头像图标
- ✅ 导航菜单图标
- ✅ 按钮图标
- ✅ 操作按钮图标

如果图标都正常显示，说明字体文件已成功加载！
