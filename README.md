# 01-ollama-chatbot-EC2
===========================================
1. First, understand what we are building
===========================================
Normally, Ollama runs an LLM on a local computer. In our project, we will install Ollama on an AWS EC2 Ubuntu instance.

What is the difference between OpenAI and Ollama?
OpenAI API	Ollama
Uses cloud-hosted models	Runs models on your EC2 server
API key required	No model-provider API key required
API usage can be charged	Ollama software is free
Internet required for API access	Model can run without internet after download
Model runs on provider infrastructure	Model uses your EC2 CPU/RAM/GPU

Important: Ollama is free software, but AWS EC2 is not free in general. You pay for EC2 compute, storage, and data transfer as applicable. Model quality also depends on the model you select.

========================================
2. Understand our project requirements
========================================
Before creating the EC2 instance, let's decide the server configuration.
EC2 instance configuration

Ubuntu Server 24.04 LTS

Configuration	Selection
Cloud provider	AWS
Service	EC2
OS	Ubuntu 24.04 LTS
Architecture	64-bit x86
Instance	t3.large (starting point)
vCPU	2
RAM	8 GB
Storage	40 GB gp3
Region	ap-south-1 (Mumbai)
Access	SSH


My recommendation: For learning, start with t3.large and a small quantized model such as llama3.2:1b. A larger llama3.2:3b model may need more memory and can be slow on a 2-vCPU CPU-only instance.

If you want a better experience with larger models, consider an instance with 16 GB or more RAM. GPU instances are another option, but they cost more.

Do not assume that an 8 GB instance can comfortably run every Ollama model.

================================
3. Step-by-step AWS EC2 setup
================================

Step 1 – Login to AWS Console
Open:
AWS Management Console1. Login to your AWS account.
2. Search for EC2.
3. Open the EC2 dashboard.
4. Select the Mumbai region (ap-south-1), if that is where you want to deploy.
5. Name Instance -ollama-Vm
6. AMI - Ubuntu Server 24.04 LTS
          64-bit (x86)
7. Instance Type - t3.large

D. Key pair
- Click Create new key pair.
- Key pair name: ollama-key
- Key pair type: RSA.
- Private key format: .pem
- Download the key pair.
Keep this file safe. It is required to connect to your EC2 server.

E. Network settings

Create or select a security group.

For our learning project, configure:
Type	Port	Source
SSH	22	My IP
Custom TCP	8501	My IP
Custom TCP	11434	Do not open publicly

Why?
- Port 22: SSH connection to Ubuntu.
- Port 8501: Access Streamlit chatbot.
- Port 11434: Ollama API. We will keep this private and access it locally from the same EC2 instance.
F. Configure storage

Set:
40 GB
General Purpose SSD (gp3)
Click Launch instance.

===============================
Step 3 – Connect to Ubuntu EC2
===============================
After the instance is launched:
1. Open EC2 → Instances.
2. Select ollama-genai-server.
3. Wait until the instance is running.
4. Select Connect.
5. Choose EC2 Instance Connect, if available

Using MobaXterm Connect EC2

Once connected, you should see something similar to:
EC2 connected
This means you are now working inside the Ubuntu server, not your laptop.  

=================================
4. Install Ollama on Ubuntu EC2
==================================

Now we will install Ollama software on our Ubuntu server. Run Command one by one

# What does this command do?
# Update Ubuntu packages
It updates the Ubuntu package information so that we can install the latest available packages.
Execute:
$ sudo apt update

# This upgrades installed packages.
Execute:
$ sudo apt upgrade -y

# Step 4.2 – Install required utilities
$ sudo apt install curl -y

What is curl?
Curl is a command-line utility used to communicate with URLs and APIs.
For example, we will use curl to download and test Ollama.

# Step 4.3 – Install Ollama
Run the official Ollama Linux installation command:
$ curl -fsSL https://ollama.com/install.sh | sh

# Step 4.4 – Verify Ollama installation
Execute:
$ ollama --version

# Step 4.5 – Check Ollama service
On Ubuntu, the installer normally configures Ollama as a systemd service.
Execute:
$ sudo systemctl status ollama

# If it is not running:
 $ sudo systemctl enable --now ollama


# Understand these commands:
- systemctl – Manages Linux services.
- enable – Starts the service automatically during boot.
- --now – Starts the service immediately.
# Important: If the Ollama service is already running, don't execute ollama serve again. Otherwise, you may get an address-already-in-use error.

=====================================
5. Download an AI model using Ollama
======================================
Now Ollama software is installed, but we haven't downloaded any AI model.

Remember:
# Ollama is the software that runs the model. Llama is the AI model that generates answers.

# Step 5.1 – Download Llama 3.2 1B
Execute:
$ ollama pull llama3.2:1b

# Step 5.2 – Check downloaded models
$ ollama list

# Step 5.3 – Check model information
$ ollama show llama3.2:1b

# Step 5.4 – Execute the model
$ ollama run llama3.2:1b

===========================
6. Expose Ollama as an API
===========================
Important GenAI concept
Now we have:
- Ubuntu EC2 server.
- Ollama software.
- Llama 3.2 model.
Next, we need to understand how Python communicates with Ollama.
What is Ollama API?
Ollama provides a REST API that allows other applications to communicate with its models.

The default local API endpoint is:
http://localhost:11434

# Step 6.1 – Verify Ollama API
Execute:
curl http://localhost:11434/api/tags


Expected response:
{
  "models": [
    {
      "name": "llama3.2:1b"
    }
  ]
}


Your actual output will contain additional model information.

This confirms that Ollama is responding to API requests.
# Step 6.2 – Test the model through API
Execute:
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Explain Python in simple English",
  "stream": false
}'


What happens?
1. Curl sends a request to Ollama.
2. Ollama receives the request.
3. Llama 3.2 processes the prompt.
4. The model generates an answer.
5. Ollama returns the response in JSON format.
# Remember this difference
# ollama run is used to interact with a model through the terminal.
# Ollama API is used by Python or another application to interact with the model programmatically.

# Security note: Do not expose port 11434 to the public internet. Our Python application and Ollama will run on the same EC2 server, so Python can access localhost:11434 directly.

=======================================
7. Create GenAI project on Ubuntu EC2
=======================================
Now we will develop our chatbot application using Python and Streamlit.
Earlier, we created our project on Windows. Now we will create the same project directly on Ubuntu.
Step 7.1 – Create project directory

Execute:
$ mkdir 02-ollama-gpt-chat-bot
Go inside the project directory:
 $ cd 02-ollama-gpt-chat-bot

# Step 7.2 – Install Python and virtual environment
Ubuntu may already have Python installed. Check:

$ python3 --version

Install the required packages:

$ sudo apt install python3-pip python3-venv -y 

# Why do we need these packages?
- python3-pip: Installs Python libraries.
- python3-venv: Creates an isolated Python environment.

# Step 7.3 – Create virtual environment
Execute:
$ python3 -m venv venv

This creates a folder named venv inside our project.
# Activate it:
$ source venv/bin/activate

# Step 7.4 – Create requirements.txt
Create the file:
$ vim requirements.txt
        ollama
        streamlit

# Install libraries:
$ pip install -r requirements.txt

Check installed libraries:
$ pip list

=======================
8. Create backend.py
=======================

# This is where we write the Python logic to communicate with our Llama model.
Create the file:
$ vim backend.py

=======================================
9. Create frontend.py using Streamlit
=======================================
Now we will develop our chatbot user interface.
Create:
$ vim frontend.py

=======================================
10. Run the application on AWS EC2
=======================================
Now we have completed the frontend and backend.
Our project structure should look like this:
02-ollama-gpt-chat-bot/
│
├── venv/
│
├── backend.py
│
├── frontend.py
│
└── requirements.txt
		

Step 10.1 – Verify Ollama is running
sudo systemctl status ollama


If the service is stopped:
sudo systemctl start ollama


Step 10.2 – Verify the model
ollama list


You should see:
llama3.2:1b


# Step 10.3 – Start Streamlit
Make sure you are inside your project directory and your virtual environment is activated.

Execute:
$ streamlit run frontend.py \
--server.address 0.0.0.0 \
--server.port 8501


# Why do we use 0.0.0.0?
By default, Streamlit listens on localhost.
But our application is running on an EC2 server, and we want to access it from our laptop's browser.
0.0.0.0 tells Streamlit to listen on all network interfaces.

# Step 10.4 – Open the application in your browser
Find the public IPv4 address of your EC2 instance.
For example:
13.201.100.X


Open this URL in your laptop browser:
http://13.201.100.X:8501







