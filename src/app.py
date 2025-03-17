# #!/usr/bin/env python3

# import os
# import sys
# import signal
# import multiprocessing
# from camoufox.server import launch_server
# from fastapi import FastAPI
# import uvicorn
# import uuid

# app = FastAPI()
# server_process = None  

# def run_server():
#     """Khởi động server giả lập."""
#     try:
#         ws_uuid = str(uuid.uuid4())
#         server = launch_server(
#             headless=False,  
#             geoip=True,
#             humanize=True,
#             os='windows',
#             webgl_config=("Google Inc. (NVIDIA)", "ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar"),
#             port=3002, 
#             ws_path=ws_uuid
#         )
#         print("Server đã khởi chạy:", server)
#         print(f"Server đã khởi chạy với ws_path: {ws_uuid}")
#     except Exception as e:
#         print("Lỗi khi khởi chạy server:", e)
#         sys.exit(1)

# @app.get("/ping")
# async def ping():
#     """API kiểm tra trạng thái."""
#     global server_process
#     if server_process is None or not server_process.is_alive():
#         server_process = multiprocessing.Process(target=run_server, daemon=True)
#         server_process.start()
#         return {"message": "Server đang khởi chạy"}
#     return {"message": "Server đã chạy"}

# def stop_server():
#     """Dừng server khi FastAPI thoát."""
#     global server_process
#     if server_process and server_process.is_alive():
#         print("\nDừng tiến trình server...")
#         server_process.terminate()  # Dừng tiến trình con
#         server_process.join()
#         print("Server đã dừng.")

# def signal_handler(sig, frame):
#     """Xử lý Ctrl+C để dừng cả FastAPI và server."""
#     stop_server()
#     sys.exit(0)

# def main():
#     """Chạy FastAPI server."""
#     signal.signal(signal.SIGINT, signal_handler)  # Bắt Ctrl+C
#     signal.signal(signal.SIGTERM, signal_handler)  # Bắt tín hiệu dừng
#     uvicorn.run(app, host="0.0.0.0", port=3000, reload=False)

# if __name__ == "__main__":
#     try:
#         main()
#     finally:
#         stop_server()  # Đảm bảo tiến trình được dừng khi thoát


print("has run")