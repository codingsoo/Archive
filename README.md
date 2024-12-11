# Archive of Projects

This repository contains archived projects that are no longer actively maintained. Each project showcases past efforts, achievements, and implementations that might still serve as references or inspiration. While these projects are no longer supported or updated, they highlight valuable contributions to various fields.

---

## Archived Projects

### 1. Social Engineering Defense

**Summary:** The Social Engineering Defense project is designed to detect scam emails using advanced text analysis techniques. The system integrates multiple open-source tools for email crawling, sentence processing, form item detection, command analysis, and question analysis, making it a robust solution for identifying phishing attempts.

**Achievements:**
- **Presented at BlackHat USA 2018**: [Whitepaper](https://i.blackhat.com/us-18/Thu-August-9/us-18-Harris-Catch-Me-Yes-We-Can-wp.pdf)  
- **Published in SA 2019**: [IEEE Paper](https://ieeexplore.ieee.org/abstract/document/8938036)  

**Key Features:**
- **Email Crawling**: Retrieves and processes email data with tools like BeautifulSoup and Langid.
- **Sentence Processing**: Uses Punctuator2 and Punkt for sentence boundary detection and grammar restoration.
- **Form Item Detection**: Converts forms into question formats for analysis.
- **Sentence Type Identification**: Detects commands and questions using Stanford CoreNLP and a POS tagger.
- **Blacklist Verification**: Uses TF-IDF to identify malicious command patterns.
- **Question Scam Detection**: Employs a modified Paralex Question Answering System for scam detection.

**Directory:** All related files for this project can be found in the [`social-engineering-defense`](social-engineering-defense/) directory. Latest version is available on [GitLab](https://gitlab.com/security-defenders/social-engineering-defense).

### 2. [Smart Contract Vulnerability Checker](sc-vulnerability-checker/)

**Summary:** The Smart Contract Vulnerability Checker was developed to analyze vulnerabilities in Ethereum-based smart contracts without requiring access to their source code. By combining a custom smart contract (Kookmin Security Token) with a vulnerability analysis server, this tool offered an innovative way to detect and report potential security issues.

**Achievements:**  
- Received the 2018 Korea Computer Congress Best Undergraduate Paper Award.  
- Published paper (in Korean): [Link to DBpia](http://www.dbpia.co.kr/Journal/ArticleDetail/NODE07503549).

**Key Features:**  
- Utilized a custom ERC20-compatible smart contract (Kookmin Security Token) to interface with users.  
- Allowed users to submit smart contract addresses for analysis.  
- Communicated with an analysis server using `web3.js` to process the bytecode and report results.  

**Architecture:** The project implemented a real-time vulnerability detection workflow using Ethereum smart contracts and external analysis servers.  
![Architecture](https://github.com/codingsoo/Archive/blob/main/sc-vulnerability-checker/architecture.PNG)

**Results:** The tool successfully identified vulnerabilities in a dataset of 19 smart contracts, demonstrating its effectiveness.  
![Results](https://github.com/codingsoo/Archive/blob/main/sc-vulnerability-checker/result.PNG)

**Directory:** All related files for this project can be found in the [`sc-vulnerability-checker`](sc-vulnerability-checker/) directory.

### 3. [Virtual Girlfriend Chatbot](virtual-girlfriend/)

**Summary:** The Virtual Girlfriend Chatbot is a web application that simulates conversations with an imaginary girlfriend. Users can choose between two personality concepts—friendly and softy. Through machine learning, the chatbot can read documents and respond in a human-like manner.

**Achievement:** 3rd Prize in OpenHack Korea 2017 [Event Link](https://sigoss.github.io/hackathon2017/index.html).

**Key Features:**  
- Two chatbot concepts: friendly and softy.  
- Machine learning-powered document reading and conversational abilities.  
- Extendable with custom models for improved responses.

**Directory:** All related files for this project can be found in the [`virtual-girlfriend`](virtual-girlfriend/) directory.

---

## Notes on Archived Projects

Projects in this archive are preserved in their original form and are not actively maintained. If you find value in these works, feel free to fork or reference them, but keep in mind that updates or support will not be provided.
