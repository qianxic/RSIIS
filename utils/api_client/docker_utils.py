"""
Docker API服务管理工具
"""
import os
import logging
import subprocess
import time
import platform
import json
from typing import Tuple, Dict, Any, Optional, List

import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)


def check_docker_running() -> bool:
    """检查Docker服务是否运行中
    
    Returns:
        如果Docker服务运行中，返回True，否则返回False
    """
    try:
        if platform.system() == "Windows":
            # Windows平台
            command = ["docker", "info"]
            result = subprocess.run(command, capture_output=True, text=True)
            return result.returncode == 0
        else:
            # Linux/Mac平台
            command = ["systemctl", "is-active", "docker"]
            result = subprocess.run(command, capture_output=True, text=True)
            return "active" in result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def get_docker_containers() -> List[Dict[str, Any]]:
    """获取所有Docker容器信息
    
    Returns:
        容器信息列表
    """
    try:
        command = ["docker", "ps", "--format", "{{json .}}"]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"获取Docker容器失败: {result.stderr}")
            return []
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    container_info = json.loads(line)
                    containers.append(container_info)
                except json.JSONDecodeError:
                    logger.warning(f"解析容器信息失败: {line}")
        
        return containers
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.error(f"执行Docker命令失败: {str(e)}")
        return []


def find_api_container(name_pattern: str = "fastapi") -> Optional[Dict[str, Any]]:
    """查找匹配名称模式的API容器
    
    Args:
        name_pattern: 容器名称匹配模式
        
    Returns:
        如果找到匹配的容器，返回容器信息，否则返回None
    """
    containers = get_docker_containers()
    for container in containers:
        # 检查容器名称是否包含指定模式
        container_name = container.get("Names", "")
        if name_pattern.lower() in container_name.lower():
            return container
    return None


def get_container_status(container_id: str) -> str:
    """获取容器状态
    
    Args:
        container_id: 容器ID
        
    Returns:
        容器状态
    """
    try:
        command = ["docker", "inspect", "--format", "{{.State.Status}}", container_id]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"获取容器状态失败: {result.stderr}")
            return "unknown"
        
        return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.error(f"执行Docker命令失败: {str(e)}")
        return "unknown"


def start_container(container_id: str) -> bool:
    """启动容器
    
    Args:
        container_id: 容器ID
        
    Returns:
        如果启动成功，返回True，否则返回False
    """
    try:
        command = ["docker", "start", container_id]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"启动容器失败: {result.stderr}")
            return False
        
        # 等待容器启动
        for _ in range(10):  # 最多等待10秒
            status = get_container_status(container_id)
            if status == "running":
                return True
            time.sleep(1)
        
        return False
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.error(f"执行Docker命令失败: {str(e)}")
        return False


def stop_container(container_id: str) -> bool:
    """停止容器
    
    Args:
        container_id: 容器ID
        
    Returns:
        如果停止成功，返回True，否则返回False
    """
    try:
        command = ["docker", "stop", container_id]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"停止容器失败: {result.stderr}")
            return False
        
        return True
    except (subprocess.SubprocessError, FileNotFoundError) as e:
        logger.error(f"执行Docker命令失败: {str(e)}")
        return False


def check_api_service(host: str = "localhost", port: int = 8080, 
                     endpoint: str = "/api/v1/ping", timeout: int = 5) -> Tuple[bool, Optional[str]]:
    """检查API服务是否可用
    
    Args:
        host: 主机名
        port: 端口
        endpoint: 检查端点
        timeout: 超时时间（秒）
        
    Returns:
        (可用性, 错误信息)
    """
    url = f"http://{host}:{port}{endpoint}"
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True, None
        else:
            return False, f"HTTP错误: {response.status_code}"
    except RequestException as e:
        return False, f"连接错误: {str(e)}"


def ensure_api_service(container_name_pattern: str = "fastapi", 
                      host: str = "localhost", 
                      port: int = 8080) -> Tuple[bool, Optional[str]]:
    """确保API服务可用，如果未运行则尝试启动
    
    Args:
        container_name_pattern: API容器名称匹配模式
        host: 主机名
        port: 端口
        
    Returns:
        (可用性, 错误信息)
    """
    # 首先检查API服务是否已经可用
    is_available, error = check_api_service(host, port)
    if is_available:
        return True, None
    
    # 检查Docker是否运行
    if not check_docker_running():
        return False, "Docker服务未运行"
    
    # 查找API容器
    container = find_api_container(container_name_pattern)
    if not container:
        return False, f"未找到匹配的API容器: {container_name_pattern}"
    
    container_id = container.get("ID", "")
    container_status = get_container_status(container_id)
    
    # 如果容器未运行，尝试启动
    if container_status != "running":
        logger.info(f"尝试启动API容器: {container_id}")
        if not start_container(container_id):
            return False, f"无法启动API容器: {container_id}"
        
        # 等待API服务启动
        for i in range(20):  # 最多等待20秒
            time.sleep(1)
            is_available, _ = check_api_service(host, port)
            if is_available:
                logger.info(f"API服务已成功启动")
                return True, None
        
        return False, "API服务启动超时"
    
    # 容器已运行但API服务不可用
    return False, "API容器已运行但服务不可用" 