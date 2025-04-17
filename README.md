# TwittersCrawl
## 推特最新数据抓取（推文+回复）
 1. 本项目基于 twikit 作的二次开发 ，所有涉及破解推特的相关headers，cookies 生成方案 均来自于 twikit 软件包 
    相关项目地址参考：https://github.com/d60/twikit
 2. 本项目为了提升效率，采用的是twitter网站抓取到的 推文+回复二合一接口，因此只能用于监控最新推文，如需抓取全部推文，以及全部回复，请自行抓包分析
 3. 本项目采用 AGPL 进行分发，允许任何人使用、修改和分发，但仅限于非商业性用途。未经作者明确书面同意，不得将此软件用于商业用途，违者后果自负。

4. 所有涉及config.py文件内容请参考如下格式自行填充,项目文件中不提供

   ![image-20250417193231249](https://collection-data.bj.bcebos.com/jiaohaicheng/selfspace/6070b5ac_ddda_4428_b426_21a2e9560980/image-20250417193231249.png?authorization=bce-auth-v1%2F359794b9ccff4c03a01bdaaf0ede3be2%2F2025-04-17T11%3A32%3A35Z%2F-1%2F%2F6d391202e370372a751ce000533cb8c4c667198d0e2cc1bfc74ab12abc428273)

   5. 涉及到的twitter账号可以去 https://hdd.cm/ 自行购买，购买到的账号格式如下：（以下账号相关信息经过处理，无法直接使用，参考这个格式即可）

      ```
      Shehovtsov5813----08b3J8a24MdTPa24SWb----mykeymaker192@trinity.blockchainrese.com----f2a3b246825a3c23ee8535ade84d986a51471cf----60191ecff6ccc471397e42d362c7c33991ef543abe680fe8d501f01490ba31c52a84086e00b85a96d3c4beed90b09fb9fa221d0af5b80d9897ac06fbf3beb2e7f8405f345106138bcab354f58987de8----B5HGB6IPPQZHXWR----rtezf9xx9qy
      ```

      只要买来的号里有auth_token + ct0 就行 ，格式不一样可以自己写解析脚本 具体参见：scripts/add_accounts.py 里的 parse_accounts()函数

