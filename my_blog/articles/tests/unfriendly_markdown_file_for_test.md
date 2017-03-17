# 乾颐堂 CCNAv3.0 路由与交换

## 知识集 13

#### 1.2、SVI 交换虚接口（switch virtual interface）

多层交换机，更好的 VLAN 间路由的方案

SVI 情况下 PC 的网关设置在多层交换机上

开始割接：

// 配置 3 个 VLAN

...

###### 配置路由

```shell
SW1(config)# ip route 0.0.0.0 0.0.0.0 vlan 30 10.1.30.254
Branch(config)# ip route 10.1.10.0 255.255.255.0 e0/0 10.1.30.253
Branch(config)# ip route 10.1.20.0 255.255.255.0 e0/0 10.1.30.253
```

静态路由过于繁琐，不能自动修改	——> 动态路由协议（RIP、OSPF、EIGRP）

#### 2、DHCP 协议

CCNAv3.0 考点（排错题）

2.1、常规的 DHCP

场景：使用思科设备（R & S）配置 DHCP 服务，对终端设备（iPhone、PC）下发 IP、DNS、域名等内容

DHCP UDP，bootps 和 bootpc（端口号 67、68）

路由器作为 DHCP 客户端实施：

```shell
PC1(config-if)# ip address dhcp
```

需求：

* 配置 Branch 作为 DHCP 服务器
* 下发 10.1.10.0/24 和 20.0/24
* 排除 IP 地址 10.1.10.250 - 254、10.1.20.250-254


* 下发 DNS 服务器为 114.114.114.114
* 下发域名为 qytang.com

```shell
Branch(config)#ip  dhcp pool VLAN10
Branch(config)# ip dhcp excluded-address 10.1.10.250 10.1.10.254
Branch(dhcp-config)# network 10.1.10.0 /24
Branch(dhcp-config)# default-router 10.1.10.254
Branch(dhcp-config)# dns-server 114.114.114.114 8.8.8.8
Branch(dhcp-config)# domain-name qytang.com
```

###### 调试及验证

```shell
Branch# debug ip dhcp server events
Branch# show ip dhcp pool
Branch# show ip dhcp conflict
Branch# clear ip dhcp conflict *	// 清除冲突 IP 地址
PC# show dhcp server	// 验证 DHCP 服务
```

注意以上这些的前提：主机和网关通信

以上为 DHCP 服务器和 PC 在同一网段

#### 2.3、DHCP 的中继技术

DHCP 服务器和客户端不是直连的，中间跨越了 N 个设备

#### 【作业】

##### 1、Branch 和 PC1、PC2 实现单臂路由，使得 PC1 和 PC2 可以通信

###### 配置 vlan.10

```shell
Branch(config)#default int e0/0
Branch(config)#int e0/0.10
Branch(config-subif)#encapsulation dot1Q 10
Branch(config-subif)#ip address 10.1.10.254 255.255.255.0
Branch(config-subif)#description VLAN10_gateway
```

###### 配置 vlan.20

```shell
Branch(config)#int e0/0.20
Branch(config-subif)#encapsulation dot1Q 20
Branch(config-subif)#ip address 10.1.20.254 255.255.255.0
Branch(config-subif)#description VLAN20_gateway
```

###### 开启

```shell
Branch(config)#int e0/0
Branch(config-subif)#no shutdown
```

###### 配置 trunk

```shell
SW1(config)#int e0/0
SW1(config-if)#switchport trunk encapsulation dot1q
SW1(config-if)#switchport mode trunk
SW1(config-if)#switchport trunk allowed vlan 10,20
```

###### 配置默认路由

```shell
PC2#show ip route
PC2(config)#ip default-gateway 10.1.20.254
PC1(config)#ip default-gateway 10.1.10.254
```

###### 确保 SW1 的 VLAN 都有 IP

```shell
SW1(config)#int vlan 20
SW1(config-if)#ip address 10.1.20.99 255.255.255.0
SW1#show ip int b
Vlan10                 10.1.10.99      YES manual up                    up
Vlan20                 10.1.20.99      YES manual up                    up
```
##### 2、Branch 作为 DHCP 服务器，为 VLAN10 和 VLAN20 下的客户端分配 IP 地址（通过 show dhcp server 以及 sh ip int b 验证）

###### 取消 PC 的 IP 地址

```shell
PC1(config)#int e0/1
PC1(config-if)#no ip address
```

######  配置 Branch 作为 DHCP 服务器

```shell
Branch(config)#ip dhcp pool VLAN10
Branch(config)#ip dhcp excluded-address 10.1.10.250 10.1.10.254
Branch(config)#ip dhcp excluded-address 10.1.20.250 10.1.20.254
Branch(dhcp-config)#network 10.1.10.0 /24
Branch(dhcp-config)#default-router 10.1.10.254
Branch(dhcp-config)#dns-server 114.114.114.114 8.8.8.8
Branch(dhcp-config)#domain-name qytang.com
Branch(config)#ip dhcp pool VLAN20
Branch(dhcp-config)#network 10.1.20.0 /24
Branch(dhcp-config)#default-router 10.1.20.254
Branch(dhcp-config)#dns-server 114.114.114.114 8.8.8.8
Branch(dhcp-config)#domain-name qytang.com
```

###### 开启 PC 的 DHCP 服务

```shell
PC2(config)#int e0/1
PC2(config-if)#ip address dhcp
PC2(config-if)#do show ip int e0/1
PC1(config)#int e0/1
PC1(config-if)#ip address dhcp
```

###### 验证

```shell
Branch#show ip dhcp pool
```