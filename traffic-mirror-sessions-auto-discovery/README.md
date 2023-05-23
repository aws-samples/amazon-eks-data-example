## 方案说明
### 常见VPC Traffic Mirror架构
![image1](image/../%20image/1.jpeg)

常见的VPC Traffic Mirror会使用NLB为多个Mirror Target进行负载，NLB可以提供高可用性、负载均衡和弹性扩展的能力。但在大流量场景下，NLB费用占比会比较高。

### 本方案VPC Traffic Mirror架构
![image2](image/../%20image/2.png)

本方案中使用DynamoDB存储Mirror Target的元数据与绑定的session数量，通过EC2 State Event触发Lambda把新建EC2的ENI直接绑定到可用的Mirror Target上，从而节省NLB的费用。