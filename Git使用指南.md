# Git仓库设置完整流程总结

## 准备工作

1. **选择项目目录**：
   - 确定一个固定的工作目录（例如：`D:\VS_WORKBASE\PySide6\遥感影像智能解译系统V1.0`）
   - 确保所有项目文件已准备就绪

2. **GitHub准备**：
   - 创建GitHub账号（如果还没有）
   - 在GitHub上创建新的空仓库，不初始化README或其他文件

## 本地Git仓库初始化 - 基础步骤

1. **进入项目目录**：
   ```bash
   cd D:\VS_WORKBASE\PySide6\遥感影像智能解译系统V1.0
   ```

2. **初始化Git仓库**：
   ```bash
   git init
   ```

3. **创建.gitignore文件**：
   ```bash
   echo __pycache__/ > .gitignore
   echo *.pyc >> .gitignore
   echo .vscode/ >> .gitignore
   ```

4. **添加文件到暂存区**：
   ```bash
   git add .
   ```

5. **设置用户信息**（如果是首次使用Git）：
   ```bash
   git config --global user.name "你的GitHub用户名"
   git config --global user.email "你的邮箱"
   ```

6. **首次提交代码**：
   ```bash
   git commit -m "初始提交：遥感影像智能解译系统"
   ```

## 连接GitHub仓库

1. **添加远程仓库**：
   ```bash
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   ```

2. **确认远程仓库设置**：
   ```bash
   git remote -v
   ```

3. **创建并切换到main分支**（如果需要）：
   ```bash
   git checkout -b main
   ```
   或简单地：
   ```bash
   git branch -M main
   ```

4. **推送到GitHub**：
   ```bash
   git push -u origin main
   ```

## 验证与确认

1. **检查本地状态**：
   ```bash
   git status
   ```

2. **在GitHub网站上确认**：
   - 访问`https://github.com/你的用户名/你的仓库名`
   - 确认文件已成功上传

## 日常使用流程

1. **获取最新更改**（如果多人协作）：
   ```bash
   git pull
   ```

2. **修改代码**

3. **查看更改状态**：
   ```bash
   git status
   ```

4. **添加更改到暂存区**：
   ```bash
   git add .
   ```
   或添加特定文件：
   ```bash
   git add 文件名
   ```

5. **提交更改**：
   ```bash
   git commit -m "描述性提交信息"
   ```

6. **推送到GitHub**：
   ```bash
   git push
   ```

## 常见问题解决方法

1. **远程仓库配置错误**：
   ```bash
   git remote remove origin
   git remote add origin 正确的URL
   ```

2. **分支名称问题**：
   ```bash
   git branch -M main
   ```

3. **拒绝合并不相关历史**：
   ```bash
   git pull origin main --allow-unrelated-histories
   ```

4. **本地分支落后于远程**：
   ```bash
   git pull origin main
   ```

## 最佳实践

1. **只在一个目录下维护Git仓库**，避免多个副本
2. **定期提交小的更改**，提交信息要有描述性
3. **经常推送到远程**，避免大量累积的更改
4. **使用分支**处理新功能和实验性更改
5. **保持.gitignore更新**，避免提交不必要的文件

遵循这些步骤和最佳实践，你可以建立一个干净、有组织的Git工作流程，有效管理你的项目代码。

# Git安装与配置

## 下载与安装Git

在开始使用Git之前，你需要先下载并安装Git：

1. **下载Git**：
   - 访问官方网站：https://git-scm.com/downloads
   - 根据你的操作系统(Windows/Mac/Linux)选择相应版本

2. **安装Git**：
   - Windows用户：运行下载的安装程序，按照安装向导操作
     - 安装时推荐选择"Git Bash Here"和"Git GUI Here"选项
     - 建议选择"Use Git from Git Bash only"选项，除非你需要从命令提示符使用Git
     - 对于行尾设置，选择"Checkout as-is, commit as-is"
   - Mac用户：可以使用DMG安装包或通过Homebrew安装：`brew install git`
   - Linux用户：使用包管理器安装，例如Ubuntu：`sudo apt-get install git`

3. **验证安装**：
   - 打开命令行或Git Bash
   - 输入命令：`git --version`
   - 如果显示Git版本号，表示安装成功

## 初始设置

安装Git后，需要进行一些基本设置：

1. **设置用户信息**：
   ```bash
   git config --global user.name "你的GitHub用户名"
   git config --global user.email "你的邮箱地址"
   ```
   这些信息会出现在你的每次提交中

2. **设置默认编辑器**（可选）：
   ```bash
   git config --global core.editor "notepad"  # Windows记事本
   # 或
   git config --global core.editor "code --wait"  # VS Code
   ```

3. **设置默认分支名**（推荐）：
   ```bash
   git config --global init.defaultBranch main
   ```
   这将使新创建的仓库默认分支名为"main"而非"master"

4. **查看当前配置**：
   ```bash
   git config --list
   ```

5. **设置凭证助手**（可选，但推荐）：
   - Windows: 
     ```bash
     git config --global credential.helper wincred
     ```
   - Mac: 
     ```bash
     git config --global credential.helper osxkeychain
     ```
   这样你只需要输入一次GitHub密码，Git会记住它

## GitHub身份验证设置

为了与GitHub交互，你需要设置身份验证：

1. **使用HTTPS方式**（推荐新手使用）：
   - 首次推送时，Git会请求你输入GitHub用户名和密码
   - 如果启用了双因素认证，需要使用个人访问令牌(PAT)而不是密码：
     - 在GitHub上：Settings → Developer settings → Personal access tokens
     - 生成新令牌，选择适当的权限（至少需要`repo`权限）
     - 使用此令牌代替密码

2. **使用SSH方式**（更安全，但设置复杂）：
   - 生成SSH密钥对：
     ```bash
     ssh-keygen -t ed25519 -C "你的邮箱地址"
     ```
   - 将公钥添加到GitHub账户：
     - 复制`~/.ssh/id_ed25519.pub`文件内容
     - 在GitHub上：Settings → SSH and GPG keys → New SSH key
   - 测试连接：
     ```bash
     ssh -T git@github.com
     ``` 