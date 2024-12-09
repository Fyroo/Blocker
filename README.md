````markdown
# 🛑 Blocker

## Getting Started

Before diving into the project, ensure you have your virtual environment activated. Then, run the following command to install all the necessary dependencies.

## 🚀 Features

- **Dependency Management**: Easily set up all required libraries with `requirements.txt`.
- **Fast Start**: Get started with minimal setup steps.

## 🛠 Prerequisites

- **Python**: Ensure Python 3.x is installed on your machine.
- **Virtual Environment**: It’s recommended to use a virtual environment to manage dependencies.

## 🔧 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Fyroo/Blocker.git
   ```
````

2. Navigate to the project directory:
   ```bash
   cd blocker
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📂 Project Structure

```
blocker/
├── requirements.txt  # Dependency file
├── blocker/          # Source code
├── README.md         # Project documentation
└── ...
```

---

## 🛑 Known Issues

### **Chrome Secure DNS Issue**

If packets are not being shown in the packet sniffer, it may be caused by Chrome's Secure DNS feature. Disabling Secure DNS in Chrome can resolve this issue.

To disable Secure DNS in Chrome:

1. Open Chrome settings (`chrome://settings/`).
2. Scroll to **Privacy and security**.
3. Under **Security**, toggle off **Use secure DNS**.

This will allow the packet sniffer to capture packets correctly.

---

Happy Coding! ✨

```

```
