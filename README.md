# 🔐 Enhanced Netcat (nETCAT)

A powerful, cross-platform, encrypted Netcat clone with AES-256-CBC encryption, multi-client support, file transfer capabilities, and interactive remote shell functionality.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Features

- 🔒 **AES-256-CBC Encryption** - Secure encrypted communication
- 🌐 **Multi-Client Support** - Handle multiple connections with threading
- 💻 **Cross-Platform** - Works on Linux, Windows, and macOS
- 🖥️ **Interactive Shell** - Remote command execution
- 📁 **File Transfer** - Upload and download files securely
- 🔄 **TCP/UDP Support** - Both protocols supported
- 🎨 **Beautiful CLI** - Dark Royal Blue 3D ASCII logo with usage commands
- ⚡ **Netcat Compatible** - Familiar command-line interface

## 📋 Requirements

- Python 3.6 or higher
- pycryptodome

## 🚀 Installation

### Option 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/brandy-build/enhanced-netcat.git
cd enhanced-netcat

# Install dependencies
pip install -r requirements.txt

# Run the tool
python enhanced_netcat.py --help
```

### Option 2: Manual Installation

```bash
# Install pycryptodome only
pip install pycryptodome

# Download the script
wget https://raw.githubusercontent.com/brandy-build/enhanced-netcat/main/enhanced_netcat.py

# Make it executable (Linux/macOS)
chmod +x enhanced_netcat.py

# Run it
python enhanced_netcat.py --help
```

### Option 3: Virtual Environment (Isolated)

```bash
# Create virtual environment
python -m venv netcat-env

# Activate it
# On Windows:
netcat-env\Scripts\activate
# On Linux/macOS:
source netcat-env/bin/activate

# Install dependencies
pip install pycryptodome

# Run the tool
python enhanced_netcat.py --help
```

## Usage

### Server (listen mode)
```sh
python enhanced_netcat.py -l -p 4444
```

### Client (connect to server)
```sh
python enhanced_netcat.py -t 192.168.1.10 -p 4444
```

### Encrypted Shell
```sh
# Server
python enhanced_netcat.py -l -p 4444

# Client
python enhanced_netcat.py -t 192.168.1.10 -p 4444 --shell
```

### File Upload
```sh
python enhanced_netcat.py -t 192.168.1.10 -p 4444 --upload myfile.txt
```

### File Download
```sh
python enhanced_netcat.py -t 192.168.1.10 -p 4444 --download secret.pdf
```

### UDP Mode
```sh
python enhanced_netcat.py -l -p 4444 -u
python enhanced_netcat.py -t 192.168.1.10 -p 4444 -u
```

## Requirements

- Python 3.6+
- pycryptodome

## Optional Improvements

- Stealth: randomize ports, change User-Agent, obfuscate traffic
- TTY spawn for full interactive shells (e.g., `python -c 'import pty; pty.spawn("/bin/bash")'`)
- Key exchange (Diffie-Hellman) instead of static key
- Logging, authentication, IPv6 support

## 📖 Examples

### Example 1: Start the server (listen mode)
```bash
$ python enhanced_netcat.py -l -p 4444
[+] Listening on 0.0.0.0:4444 (TCP)
```

### Example 2: Connect as a client and open a shell
```bash
$ python enhanced_netcat.py -t 127.0.0.1 -p 4444 --shell
Shell ready. Type commands.
Shell> whoami
user123
Shell> uname -a
Linux myhost 5.15.0-xx-generic #1 SMP ...
Shell> exit
```

### Example 3: Upload a file
```bash
$ python enhanced_netcat.py -t 127.0.0.1 -p 4444 --upload myfile.txt
Upload complete.
```

### Example 4: Download a file
```bash
$ python enhanced_netcat.py -t 127.0.0.1 -p 4444 --download secret.pdf
Download complete.
```

### Example 5: UDP Mode
```bash
# Server
$ python enhanced_netcat.py -l -p 5555 -u

# Client
$ python enhanced_netcat.py -t 127.0.0.1 -p 5555 -u
```

## 🔧 Configuration

### Change Encryption Key
Edit the `SECRET_KEY` variable in `enhanced_netcat.py`:
```python
SECRET_KEY = b"your_32_byte_secret_key_here!!!!"  # Must be exactly 32 bytes
```

## 🛡️ Security Notes

- **AES-256-CBC Encryption**: All TCP communications are encrypted by default
- **Static Key**: Currently uses a static key (change for production use)
- **Key Exchange**: For enhanced security, implement Diffie-Hellman key exchange
- **Authentication**: No built-in authentication (add as needed)

## ⚠️ Legal Disclaimer

This tool is provided for **educational and authorized security testing purposes only**.

- ✅ Use on systems you own or have explicit permission to test
- ✅ Use for learning networking and security concepts
- ❌ DO NOT use for unauthorized access to computer systems
- ❌ DO NOT use for illegal activities

**Users are responsible for complying with all applicable laws and regulations.**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the original Netcat tool
- Built for educational purposes and security research

## 📧 Contact

Project Link: [https://github.com/brandy-build/nETCAT-Project](https://github.com/brandy-build/nETCAT-Project)

---

**⭐ Star this repository if you find it useful!**
