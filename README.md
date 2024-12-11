# Archive of Projects

This repository contains archived projects that are no longer actively maintained. Each project showcases past efforts, achievements, and implementations that might still serve as references or inspiration. While these projects are no longer supported or updated, they highlight valuable contributions to various fields.

---

## Archived Projects

### 1. [Smart Contract Vulnerability Checker](sc-vulnerability-checker/)

**Summary:**  
The Smart Contract Vulnerability Checker was developed to analyze vulnerabilities in Ethereum-based smart contracts without requiring access to their source code. By combining a custom smart contract (Kookmin Security Token) with a vulnerability analysis server, this tool offered an innovative way to detect and report potential security issues.

**Achievements:**  
- Received the **2018 Korea Computer Congress Best Undergraduate Paper Award**.  
- Published paper (in Korean): [Link to DBpia](http://www.dbpia.co.kr/Journal/ArticleDetail/NODE07503549).

**Key Features:**  
- Utilized a custom ERC20-compatible smart contract (Kookmin Security Token) to interface with users.  
- Allowed users to submit smart contract addresses for analysis.  
- Communicated with an analysis server using `web3.js` to process the bytecode and report results.  

**Architecture:**  
The project implemented a real-time vulnerability detection workflow using Ethereum smart contracts and external analysis servers.  
![Architecture](https://github.com/codingsoo/Archive/blob/main/sc-vulnerability-checker/architecture.PNG)

**Results:**  
The tool successfully identified vulnerabilities in a dataset of 19 smart contracts, demonstrating its effectiveness.  
![Results](https://github.com/codingsoo/Archive/blob/main/sc-vulnerability-checker/result.PNG)

**Directory:** All related files for this project can be found in the [`sc-vulnerability-checker`](sc-vulnerability-checker/) directory.

### 2. [Virtual Girlfriend Chatbot](virtual-girlfriend/)

**Summary:**  
The Virtual Girlfriend Chatbot is a web application that simulates conversations with an imaginary girlfriend. Users can choose between two personality concepts—friendly and softy. Through machine learning, the chatbot can read documents and respond in a human-like manner.

**Achievement:** Secured **3rd Prize** in **OpenHack Korea 2017** [Event Link](https://sigoss.github.io/hackathon2017/index.html).

**Key Features:**  
- Two chatbot concepts: friendly and softy.  
- Machine learning-powered document reading and conversational abilities.  
- Extendable with custom models for improved responses.

**Directory:** All related files for this project can be found in the [`virtual-girlfriend`](virtual-girlfriend/) directory.

---

## Notes on Archived Projects

Projects in this archive are preserved in their original form and are not actively maintained. If you find value in these works, feel free to fork or reference them, but keep in mind that updates or support will not be provided.
