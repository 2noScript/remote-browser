Remote Browser Architecture
├── Client (ws://localhost:8080/{port})
│   └── Remote Connection (WebSocket)
│
├── Reverse Proxy (Nginx or Proxy)
│   └── Forward Request
│
├── Container (http://app:{port}/browser)
│   └── HTTP Request
│
└── Backend Service (Web App or API)
