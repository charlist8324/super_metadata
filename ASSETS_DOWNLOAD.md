# 前端资源下载说明

## 问题描述
系统默认使用 CDN 加载前端资源（Bootstrap、Font Awesome、Chart.js），这会导致：
- 网络不稳定时无法加载样式
- 内网环境无法访问外部资源
- CDN 服务暂时不可用时页面样式丢失

## 解决方案

### 方案一：手动下载（推荐）

1. **下载 Bootstrap 5.3.0**
   - CSS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
   - JS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js
   - 保存到：`static/libs/bootstrap/` 目录
   - CSS 保存为：`bootstrap.min.css`
   - JS 保存为：`bootstrap.bundle.min.js`

2. **下载 Font Awesome 6.0.0**
   - CSS: https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css
   - WebFonts: 下载所有字体文件到 `static/libs/fontawesome/webfonts/` 目录
   - 下载链接：https://use.fontawesome.com/releases/v6.0.0/fontawesome-free-6.0.0-web.zip
   - 解压后复制 `webfonts/` 目录和 `css/all.min.css` 到 `static/libs/fontawesome/`

3. **下载 Chart.js 4.4.0**
   - JS: https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js
   - 保存到：`static/libs/chartjs/` 目录
   - 文件名：`chart.umd.min.js`

### 方案二：使用下载脚本

1. 确保网络可以访问 GitHub 和 jsdelivr.net
2. 运行脚本：
   ```bash
   python download_libs.py
   ```

3. 如果下载失败，请手动下载（方案一）

### 方案三：使用国内镜像 CDN（备选）

如果网络访问国外 CDN 慢，可以修改模板使用国内镜像：

1. **BootCDN（推荐国内用户）**
   - Bootstrap: `https://cdn.bootcdn.net/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css`
   - Font Awesome: `https://cdn.bootcdn.net/ajax/libs/font-awesome/6.4.0/css/all.min.css`
   - Chart.js: `https://cdn.bootcdn.net/ajax/libs/Chart.js/4.4.0/chart.umd.min.js`

2. **修改模板文件**
   将所有 `cdn.jsdelivr.net` 替换为 `cdn.bootcdn.net/ajax/libs`

## 目录结构

下载完成后，目录结构应该是：
```
static/
├── css/
│   └── style.css
├── js/
│   ├── main.js
│   └── table_details.js
└── libs/
    ├── bootstrap/
    │   ├── css/
    │   │   └── bootstrap.min.css
    │   └── js/
    │       └── bootstrap.bundle.min.js
    ├── fontawesome/
    │   ├── css/
    │   │   └── all.min.css
    │   └── webfonts/
    │       ├── fa-solid-900.woff2
    │       ├── fa-regular-400.woff2
    │       └── ... (其他字体文件)
    └── chartjs/
        └── chart.umd.min.js
```

## 更新模板引用

下载完成后，运行以下脚本更新所有模板文件：

```bash
python update_templates.py
```

脚本会将所有模板中的 CDN 链接替换为本地路径。

## 手动更新模板（如果脚本失败）

如果脚本运行失败，可以手动修改模板文件。

### 替换规则

**Bootstrap CSS：**
```html
<!-- 替换前 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- 替换后 -->
<link href="{{ url_for('static', filename='libs/bootstrap/css/bootstrap.min.css') }}" rel="stylesheet">
```

**Bootstrap JS：**
```html
<!-- 替换前 -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- 替换后 -->
<script src="{{ url_for('static', filename='libs/bootstrap/js/bootstrap.bundle.min.js') }}"></script>
```

**Font Awesome CSS：**
```html
<!-- 替换前 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<!-- 替换后 -->
<link rel="stylesheet" href="{{ url_for('static', filename='libs/fontawesome/css/all.min.css') }}">
```

**Chart.js：**
```html
<!-- 替换前 -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

<!-- 替换后 -->
<script src="{{ url_for('static', filename='libs/chartjs/chart.umd.min.js') }}"></script>
```

## 验证

1. 重启 Flask 应用：
   ```bash
   python app.py
   ```

2. 打开浏览器访问：http://localhost:5000

3. 按 F12 打开开发者工具，查看 Network 标签

4. 刷新页面，检查所有资源是否加载成功（状态 200）

5. 如果显示 `404` 或红色，说明文件路径不正确

## 常见问题

### Q: 下载失败怎么办？
A: 使用手动下载方式（方案一），或者使用国内镜像 CDN。

### Q: 页面还是样式丢失？
A: 检查浏览器控制台（F12）的 Console 和 Network 标签，查看具体哪个资源加载失败。

### Q: Font Awesome 图标不显示？
A: 确保下载了所有 webfonts 文件到正确的目录。

### Q: 想回退到 CDN 怎么办？
A: 重新下载原始模板文件，或者手动将本地路径改回 CDN 链接。

## 推荐配置

对于生产环境，建议：
1. 使用本地资源（方案一或二）
2. 配置 Nginx/Apache 设置静态资源缓存
3. 考虑使用 CDN 加速静态资源

对于开发环境，可以使用 CDN 快速开发。

---

**注意**：如果使用 Docker 部署，确保将 `static/libs/` 目录包含在镜像中。
