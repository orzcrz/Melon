# Melon

同步本地环境

## 使用须知

- **如果是已有环境，请先备份好$HOME下的已有配置文件，脚本涉及部分文件的删除替换。**

- **如果是 _intel_ 处理器需要手动预装 `Homebrew`。**
```
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```
  
- **如果没有安装过 `Xcode Command Line`，需要手动安装。**
```
xcode-select --install
```

## 安装命令
```
sh <(curl -fsSL https://raw.githubusercontent.com/orzcrz/Melon/master/setup)
```
如果无法访问，修改host 
```
185.199.108.133               raw.githubusercontent.com
185.199.109.133               raw.githubusercontent.com
185.199.110.133               raw.githubusercontent.com
185.199.111.133               raw.githubusercontent.com
```
> 如果还不行，通过这个地址去查下最新IP地址
> https://sites.ipaddress.com/raw.githubusercontent.com/

## 包含配置

- oh-my-zsh
  - zsh-syntax-highlighting
  - zsh-autosuggestions
- lldbinit
  - dk_lldb
  - zlldb
  - lldb_chisel

### 工具包

- homebrew
- pyenv
- rbenv
- nodenv
- wget
- cookiecutter
- tree
- ~~cocoapods~~
- ~~node~~

### 软链

- ~/.zshrc
- ~/.zprofile
- ~/.bash_profile
- ~/.lldbinit
- ~/.pip
- ~/.gitignore_global

## 附加项

### 关于git的提交附带表情

- 出处
在gitmoji里扒扒看 ，传送门：https://gitmoji.dev/

#### 常用emoji整理
<table>
  <thead>
    <tr>
      <th align="left">emoji</th>
      <th align="left">emoji 代码</th>
      <th align="left">commit 说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left">🎉</td>
      <td align="left"><code>:tada:</code></td>
      <td align="left">初始化项目</td>
    </tr>
    <tr>
      <td align="left">🎨</td>
      <td align="left"><code>:art:</code></td>
      <td align="left">改进代码结构/代码格式</td>
    </tr>
    <tr>
      <td align="left">⚡️</td>
      <td align="left"><code>:zap:</code></td>
      <td align="left">提升性能</td>
    </tr>
    <tr>
      <td align="left">🔥</td>
      <td align="left"><code>:fire:</code></td>
      <td align="left">移除代码或文件</td>
    </tr>
    <tr>
      <td align="left">🐛</td>
      <td align="left"><code>:bug:</code></td>
      <td align="left">修复 BUG</td>
    </tr>
    <tr>
      <td align="left">🚑️</td>
      <td align="left"><code>:ambulance:</code></td>
      <td align="left">重要补丁</td>
    </tr>
    <tr>
      <td align="left">✨</td>
      <td align="left"><code>:sparkles:</code></td>
      <td align="left">引入新功能</td>
    </tr>
    <tr>
      <td align="left">📝</td>
      <td align="left"><code>:memo:</code></td>
      <td align="left">撰写文档</td>
    </tr>
    <tr>
      <td align="left">💄</td>
      <td align="left"><code>:lipstick:</code></td>
      <td align="left">更新 UI 和样式文件</td>
    </tr>
    <tr>
      <td align="left">♻️</td>
      <td align="left"><code>:recycle:</code></td>
      <td align="left">重大重构</td>
    </tr>
    <tr>
      <td align="left">🙈</td>
      <td align="left"><code>:see_no_evil:</code></td>
      <td align="left">更新.gitignore文件</td>
    </tr>
    <tr>
      <td align="left">➕</td>
      <td align="left"><code>:heavy_plus_sign:</code></td>
      <td align="left">加了依赖</td>
    </tr>
    <tr>
      <td align="left">⬆️</td>
      <td align="left"><code>:arrow_up:</code></td>
      <td align="left">依赖升级</td>
    </tr>
    <tr>
      <td align="left">⬇️</td>
      <td align="left"><code>:arrow_down:</code></td>
      <td align="left">依赖降级</td>
    </tr>
    <tr>
      <td align="left">⚰️</td>
      <td align="left"><code>:coffin:</code></td>
      <td align="left">清理dead code</td>
    </tr>
    <tr>
      <td align="left">🔧</td>
      <td align="left"><code>:wrench:</code></td>
      <td align="left">更新配置文件</td>
    </tr>
    <tr>
      <td align="left">🔨</td>
      <td align="left"><code>:hammer:</code></td>
      <td align="left">更新开发工具</td>
    </tr>
    <tr>
      <td align="left">📄</td>
      <td align="left"><code>:page_facing_up:</code></td>
      <td align="left">更新License</td>
    </tr>
    <tr>
      <td align="left">💡</td>
      <td align="left"><code>:bulb:</code></td>
      <td align="left">增加注释</td>
    </tr>
    <tr>
      <td align="left">🍱</td>
      <td align="left"><code>:bento:</code></td>
      <td align="left">更新资源文件</td>
    </tr>
  </tbody>
</table>