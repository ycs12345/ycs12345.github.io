# 留白 · 第七页序

> 此人存在，具体用途不明。

欢迎使用个人博客「留白」。这是一个可以随时修改文字的极简文艺博客网站，包含四个板块：首页、文章归档、作者介绍、文章阅读页；三个栏目：生活随笔、读书笔记、小说创作。

**最重要的是：** 网站页面、示例文章和卡通插画都已经制作完成；可本地预览。新版本去掉了旧版的大相框、装饰性卡片和大段英文标签，强调书页式留白与清晰的文章列表。要真正获得公开网址，需要用你的 GitHub 账号完成一次部署。图文文章后台使用 [Pages CMS](https://app.pagescms.org)，发布网站使用免费的 [GitHub Pages](https://pages.github.com)。两个服务均需要你拥有 / 登录 GitHub 账号。

## 一、立即预览

如果你下载的是「留白_极简版_网页预览.zip」：

1. 解压 ZIP 文件。
2. 双击里面的 `index.html`，即可打开网站；点击“文章”“关于”等链接即可浏览其他页面。
3. 打开 `archive.html` 可以筛选或搜索文章；文章页支持目录、复制链接和阅读进度条。
4. 可以切换深色模式。页面支持手机和电脑。

**注意：** 本地预览只能看文章，无法连接云端写作后台；后台需要先按下面的步骤上线。

## 二、免费上线（推荐：GitHub Desktop 上传整套源码）

你需要：GitHub 账号 + 一次性把源码上传到 GitHub。不需要购买服务器或域名。

**第 1 步：确认 GitHub 账号**

你已连接的 GitHub 用户名为 `ycs12345`，对应博客仓库是 `ycs12345/ycs12345.github.io`。

**第 2 步：确认免费站点仓库**

1. 下载并解压「留白_极简版_可上线源码.zip」。
2. 打开你的仓库：https://github.com/ycs12345/ycs12345.github.io 。
3. 如果仓库尚为空，点击 **uploading an existing file**；如果已存在文件，选择 **Add file → Upload files**。
4. 将解压后根目录的**所有文件和文件夹**拖入上传区（不是 ZIP 文件本身）。务必包含隐藏的 `.github` 文件夹和 `.pages.yml` 文件。
5. 点击 **Commit changes** 保存。若网页上传无法保留以 `.` 开头的配置目录，建议使用 GitHub Desktop 执行同样的上传步骤。
6. 若之前已上传旧版，网页端通常无法通过一次上传覆盖所有同名文件和目录，建议通过 GitHub Desktop 用新源码替换旧版后提交，避免遗漏。

如果上传后发现仓库中的 `.github/workflows/deploy.yml` 或 `.pages.yml` 缺失，说明 GitHub 不能正常构建或管理文章，请补全这两处配置。

**第 3 步：打开 GitHub Pages**

1. 在 GitHub 网页打开新仓库 `ycs12345.github.io`。
2. 点击 **Settings → Pages**。
3. 在 Build and deployment 下，将 Source 设置为 **GitHub Actions**。
4. 若第一次运行未成功，在仓库的 **Actions** 页面找到「发布「留白」博客」工作流，点击 **Run workflow** 手动运行一次。
5. 工作流出现绿色成功标记后，打开 `https://ycs12345.github.io/`。

注意：你的博客网址中 `ycs12345` 是**你的 GitHub 用户名**，不是笔名“第七页序”。仓库需要公开，且上传的源码对所有访客可见；不要把任何私密资料上传到里面。

**第 4 步：确认博客的公开网址**

`siteUrl` 已预先填写为 `https://ycs12345.github.io`。如将来更换 GitHub 用户名或网址，可在 Pages CMS「博客资料」中修改。

## 三、像公众号一样写文章、插入图片和发布

1. 打开写作后台：**https://app.pagescms.org**。
2. 点击 **Sign in with GitHub**，用你自己的 GitHub 账号登录。
3. 根据提示安装 / 授权 Pages CMS GitHub App。**建议只授权你的博客仓库**，无需授予全部仓库权限。
4. 选择 `ycs12345.github.io` 仓库。项目根目录已提供 `.pages.yml`，不需要再新建一次。
5. 点击「**文章管理**」→ **New** 创建文章。
6. 填写标题、日期、分类、摘要；正文直接在可视化编辑器里写，支持标题、加粗、引用、列表、链接和图片。
7. 图片可以选择 / 拖入文章编辑器上传（文件将保存到 GitHub 仓库的 `media/images` 目录）。封面图可用独立的「文章封面图」字段上传。
8. 发布前建议先把「**保存为草稿**」开关保持开启；准备公开时关闭草稿并保存。首页与归档页默认按日期从新到旧排列。
9. 保存后，Pages CMS 会把内容写回 GitHub。GitHub Actions 自动生成并部署新网页，稍后刷新你的公开博客即可看到新文章。

**不需要重传 ZIP，也不需要会写网页代码。** 以后登录 Pages CMS 就能修改文章、上传图片、修改作者介绍。

## 四、如何自己修改网站上的文字

上线并授权 Pages CMS 后，进入 [Pages CMS](https://app.pagescms.org)：

- **博客资料**：修改「留白」、作者昵称、简介、首页介绍、文章区标题、归档页文字、关于页介绍及页脚短句；保存后网页会自动重新构建。
- **文章管理**：新建或修改标题、日期、分类、摘要和完整图文；正文支持标题、加粗、列表、引用、插入图片等。
- **固定导航项**（例如“首页”“文章”“关于”）、字号、颜色和页面布局是网站模板的一部分，不能在 Pages CMS 的文章编辑器中直接点击修改，需要编辑 `templates/` 或 `styles.css`。你也可以让我帮助修改这些内容。

尚未上线时，可在解压后的源码文件中直接编辑 `data/site.yml` 的值，编辑 `content/posts/*.md` 的文章内容，再按下方命令运行 `python build.py --output dist` 生成网页。下载的预览版是静态成品，直接修改预览网页不会同步到正式博客。

## 五、关于示例文章

初始附有四篇**演示文章**，分别用于测试三个分类。它们**不是你本人写的文章，也不代表你的真实生活或读书经历**。

第一次上线后，在 Pages CMS → 文章管理里，可以把四篇演示文章改成自己的正式作品，或者删除它们。建议完成替换后，再把网址分享给朋友。

## 六、网站源码目录

```text
留白博客/
├─ .pages.yml                    # 写作后台配置，极重要
├─ .github/workflows/deploy.yml  # 每次保存文章后自动发布网站
├─ build.py                      # 静态网站生成器
├─ requirements.txt              # 网站生成依赖
├─ data/site.yml                 # 博客名称、作者、简介
├─ content/posts/*.md            # 每篇文章一个 Markdown 文件
├─ media/images/                 # 未来上传的文章图片
├─ assets/avatar.webp            # 卡通头像插画
├─ templates/                    # 页面模板
├─ styles.css                    # 文艺排版 / 移动端 / 深色模式
├─ app.js                        # 搜索、分类、主题、菜单
├─ favicon.svg                   # 网站小图标
└─ README.md                     # 本说明
```

预览 ZIP 包含可离线打开的成品网页。源码 ZIP 只包含构建所需文件和图文后台配置；部署时会自动生成 `dist/`，不需要手动上传已生成的网页。

## 七、开发者 / 本地构建（非必须）

需要 Python 3.12+，命令如下：

```bash
pip install -r requirements.txt
python build.py --output dist
```

构建出的 `dist/index.html` 可本地双击打开。GitHub Actions 会自动执行这些命令，你不用手动操作。

## 八、功能边界

- ✅ 免费公开网址（GitHub Pages），独立文章链接，手机端适配。
- ✅ 第三方网页后台可视化编辑文章、管理草稿、上传正文图片和封面。
- ✅ 文章分类、搜索、深色模式、阅读进度、目录、基础 SEO。
- ⚠️ Pages CMS 管理后台是第三方服务，不是你博客域名下的内置管理后台；必须联网、使用 GitHub 登录。
- ⚠️ GitHub Pages 是静态托管，不提供评论数据库、私密文章访问控制或微信推送；这些需要未来额外集成。
- ⚠️ 演示文章需在分享博客前替换。创建仓库、授权 Pages CMS、开启 Pages 是你本人必须完成的账号操作。

**参考文档**：[Pages CMS 官方入门](https://pagescms.org/docs/quick-start/) · [GitHub Pages 官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

## 九、三幅画和分类栏

首页三个分类栏分别使用：梅花（生活随笔）、兰花（读书笔记）、竹子（小说创作）。
画作已优化为 WebP 以降低网页加载体积，保留原来的图像内容。
相关文件位于 `assets/category-mei.webp`、`assets/category-lan.webp`、`assets/category-zhu.webp`。
将来可替换同名文件以更新分类配图。
点击任意画作，会自动筛选首页相应分类的文章。
原「个人成长」演示文章已归入「生活随笔」；Pages CMS 文章分类也同步调整为三个选项。
