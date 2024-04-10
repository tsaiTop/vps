from fastapi import HTTPException,status
import requests
import os

class ServersApi:
    def __init__(self):
        self.serverUrl = os.getenv("API_SERVER_URL")
        self.email = os.getenv("API_USER_EMAIL")
        self.password = os.getenv("API_USER_PASSWORD")
        self.session = None
        isLogin = self.login()
        if not isLogin:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="服务暂时不可用，请稍后再试")

    def request(self, url, method, data=None, secured=False):
        if data is None:
            data = {}
        
        headers = {}
        if secured and self.session:
            headers['session'] = self.session
            headers["Content-Type"] = "application/json"

        try:
            if method == 'POST':
                res = requests.post(f'{self.serverUrl}/{url}', json=data, headers=headers)
                
            elif method == 'GET':
                res = requests.get(f'{self.serverUrl}/{url}', headers=headers)
            else:
                raise ValueError("Unsupported method")

            # res.raise_for_status()

            if 'session' in res.headers:
                self.session = res.headers['session']
            if res.status_code == 200:
                return {'data': res.json(), 'headers': res.headers, 'success': True}
            else:
                return {'data': res.text.strip(), 'success': False}
        except requests.RequestException as e:
            return {'data': e.response.json() if e.response else "No response", 'headers': e.response.headers if e.response else {}, 'success': False}

    def login(self):
        res = self.request('auth/login', 'POST', {'email': self.email, 'password': self.password})
        if res['success']:
            return True
        return res
    
    def buy(self, product_id):
        result = self.request('servers/order', 'POST',product_id,True)
        buyStatus = result["data"]
        
        if "NoIpsAvailable" in buyStatus:
            # 没有ip不扣款
            res = {"status": "error", "msg": "请留言: 添加IP!"}
        return res
    
    # 获取可用的os
    def getServerOsById(self, server_id):
        res = self.request(f'servers/get-reinstall-oses', 'POST', server_id, True)
        if res['success']:
            return res['data']
        return res

    # 重装
    def serverReinstall(self, server_id, os):
        reInstallRes = self.request(f'servers/reinstall', 'POST', {'server_id': server_id, 'os': os}, True)
        reInstallStatus = reInstallRes["data"]
        res = {"status": "success", "msg": "操作成功"}
        if "NoData" in reInstallStatus:
            res = {"status": "error", "msg": "没有发送数据"}
        elif "ServerUnavailable" in reInstallStatus:
            res = {"status": "error", "msg": "服务器不可用或未找到"}
        return res
    
    
    # 设置服务器状态
    def serverSetStatus(self, server_id, status):
        setStatusRes = self.request(f"servers/{status}", 'POST', server_id, True)
        setStatus = setStatusRes["data"]
        res = {"status": "success", "msg": "操作成功"}
        if "NoData" in setStatus:
            res = {"status": "error", "msg": "没有发送数据"}
        elif "ServerUnavailable" in setStatus:
            res = {"status": "error", "msg": "服务器不可用或未找到"}
        return res
    
    # 续费
    def serverRenew(self, server_id: str, month: int):
        renewRes = self.request(f"servers/renew", 'POST', {"server_id": server_id, "period": month}, True)
        renewStatus = renewRes["data"]
        res = {"status": "success", "msg": "操作成功"}
        if "NotEnoughFunds" in renewStatus:
            res = {"status": "error", "msg": "余额不足"}
        return res