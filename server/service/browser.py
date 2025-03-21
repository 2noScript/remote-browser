from pm2 import AioPM2

aiopm2 = AioPM2()

class Browser:
    def __init__(self):
        self.history = []
    async def get_browser_list(self):
        processes = await aiopm2.list()
        results = []

        for process in processes:
            data=process.json()
            results.append({
                "id":process.pm_id,
                "name":process.name,
                "status":process.status,
                "uptime": process.uptime,
                "monit":process.monit,
                "created_at":process.created_at,
                "restart":process.restart,
            })

        return results

    async def stop_browser(self,id):
        result=await aiopm2.stop(id)
        return result
    
    async def start_browser(self,id):
        result=await aiopm2.start(id)
        return result

    async def delete_browser(self,id):
        result=await aiopm2.delete(id)
        return result
    

    
    







