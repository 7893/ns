#!/usr/bin/env python3
"""
简单的部署测试脚本，检查所有必要文件是否存在
"""

import os
import sys
from pathlib import Path

def check_deployment_readiness():
    """检查部署就绪状态"""
    
    print("🔍 检查部署就绪状态...")
    
    # 检查基础目录结构
    required_dirs = [
        "apps",
        "infra/gcp", 
        "packages/ns_packages",
        ".github/workflows"
    ]
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ 缺少目录: {dir_path}")
            return False
        print(f"✅ 目录存在: {dir_path}")
    
    # 检查所有函数
    apps_dir = Path("apps")
    expected_functions = [
        "dispatcher", "apod", "asteroids-neows", "donki", "earth", 
        "eonet", "epic", "exoplanet", "genelab", "insight", 
        "mars-rover-photos", "nasa-ivl", "techport", "techtransfer"
    ]
    
    for func in expected_functions:
        func_dir = apps_dir / func
        main_py = func_dir / "main.py"
        requirements_txt = func_dir / "requirements.txt"
        
        if not func_dir.exists():
            print(f"❌ 函数目录不存在: {func}")
            return False
            
        if not main_py.exists():
            print(f"❌ main.py不存在: {func}")
            return False
            
        if not requirements_txt.exists():
            print(f"❌ requirements.txt不存在: {func}")
            return False
            
        print(f"✅ 函数完整: {func}")
    
    # 检查Terraform文件
    terraform_files = [
        "infra/gcp/main.tf",
        "infra/gcp/functions.tf", 
        "infra/gcp/variables.tf",
        "infra/gcp/locals.tf"
    ]
    
    for tf_file in terraform_files:
        if not Path(tf_file).exists():
            print(f"❌ Terraform文件不存在: {tf_file}")
            return False
        print(f"✅ Terraform文件存在: {tf_file}")
    
    print("\n🎉 所有检查通过！部署就绪。")
    print("\n📋 可能的GitHub Actions失败原因:")
    print("1. GitHub Secrets未配置: GCP_SA_KEY, NASA_API_KEY")
    print("2. GCP服务账号权限不足")
    print("3. GCP项目配置问题")
    
    return True

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    success = check_deployment_readiness()
    sys.exit(0 if success else 1)
