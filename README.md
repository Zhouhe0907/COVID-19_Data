## COVID-19疫情数据



#### 数据选择

> 数据来源：<font color = blue>Johns Hopkins University</font> 
>
> 网页地址：https://github.com/CSSEGISandData/

#### 从Github提取数据的原因：

> * 其他疫情数据网站里，可能出于控制网页数据量的目的，只会保存当天的实时数据，网页信息里面找不到历史数据，也找不到子网站存有历史数据
> * 其他疫情数据网站里大多只有到国家的信息，下面的省市州的数据基本没有
> * 符合命名格式为英文、有历史数据、有子城市等需求的数据暂时只找到了这一个


<br/>

### 数据库表格式

| Admin                                    | Province_State                         | Country_Region                           | Confirmed | Deaths   | Recovered | Active       | LastUpdate                                  |
| ---------------------------------------- | -------------------------------------- | ---------------------------------------- | --------- | -------- | --------- | ------------ | ------------------------------------------- |
| <font color = "B22222" >行政区/市</font> | <font color = "B22222" >省份/州</font> | <font color = "B22222" >国家/地区</font> | 确诊人数  | 死亡人数 | 治愈人数  | 当前患病人数 | <font color = "B22222" >数据更新日期</font> |

##### 主键：<font color = "B22222" >Admin、Province、Country、LastUpdate</font> 

> 限定 <font color = "6495ED" >**LastUpdate**</font> 条件选用具体某一天的全部数据
>
> 限定 <font color = "6495ED" >**Country_Region**</font> 条件选用某些国家的全部数据


<br/>


* <font  size =3 >世界级数据格式形如</font>

| Admin                                | Province_State                       | Country_Region                       | Confirmed  | Deaths     | Recovered  | Active       | LastUpdate                                  |
| ------------------------------------ | ------------------------------------ | ------------------------------------ | ---------- | ---------- | ---------- | ------------ | ------------------------------------------- |
| <font color = "B22222" >World</font> | <font color = "B22222" >World</font> | <font color = "B22222" >World</font> | 总确诊人数 | 总死亡人数 | 总治愈人数 | 当前患病人数 | <font color = "B22222" >数据更新日期</font> |
| <font color = "B22222" >World</font> | <font color = "B22222" >World</font> | <font color = "B22222" >World</font> | 0          | 0          | 0          | 0            | <font color = "B22222" >2020-05-31</font>   |

> 调用数据时限定<font color = "6495ED" > **Admin = 'World'** </font>条件获得世界数据
>
> 附加 <font color = "6495ED" >**LastUpdate =  '2020-xx-xx'**</font>  条件获得具体日期的世界级数据

<br/>

* <font  size =3 >国家级数据格式形如</font>

| Admin                                 | Province_State                        | Country_Region                        | Confirmed  | Deaths     | Recovered  | Active       | LastUpdate                                  |
| ------------------------------------- | ------------------------------------- | ------------------------------------- | ---------- | ---------- | ---------- | ------------ | ------------------------------------------- |
| <font color = "B22222" >国家名</font> | <font color = "B22222" >国家名</font> | <font color = "B22222" >国家名</font> | 总确诊人数 | 总死亡人数 | 总治愈人数 | 当前患病人数 | <font color = "B22222" >数据更新日期</font> |
| <font color = "B22222" >China</font>  | <font color = "B22222" >China</font>  | <font color = "B22222" >China</font>  | 0          | 0          | 0          | 0            | <font color = "B22222" >2020-05-31</font>   |

> 调用数据时限定 <font color = "6495ED" >**Country_Region = Admin = Province_State**</font>  <font color = "B22222" >&&</font>  <font color = "6495ED" >**Admin !=  'World'**</font> 条件获得国家数据
>
> *  <font color = "6495ED" size = 2.7 >**Admin !=  'World'**</font>  用来排除世界数据
>
> 附加 <font color = "6495ED" >**LastUpdate =  '2020-xx-xx'**</font>  条件获得具体日期的国家级数据
>
> 附加 <font color = "6495ED" > **Admin = ‘xxx’** </font>  条件获得具体国家的国家级数据

<br/>

* <font  size =3 >省级数据格式形如</font>

| Admin                                | Province_State                       | Country_Region                       | Confirmed  | Deaths     | Recovered  | Active       | LastUpdate                                  |
| ------------------------------------ | ------------------------------------ | ------------------------------------ | ---------- | ---------- | ---------- | ------------ | ------------------------------------------- |
| <font color = "B22222" >#NULL</font> | <font color = "4169E1" >省/州</font> | <font color = "4169E1" >国家</font>  | 总确诊人数 | 总死亡人数 | 总治愈人数 | 当前患病人数 | <font color = "4169E1" >数据更新日期</font> |
| <font color = "B22222" >#NULL</font> | <font color = "4169E1" >China</font> | <font color = "4169E1" >China</font> | 0          | 0          | 0          | 0            | <font color = "4169E1" >2020-05-31</font>   |

> 调用数据时限定<font color = "6495ED" >**Admin = '#NULL‘**</font>  <font color = "B22222" >&&</font>  <font color = "6495ED" >**Province_State  !=  ‘#NULL’**</font>  条件获得省级数据
>
> 附加 <font color = "6495ED" >**LastUpdate =  '2020-xx-xx'**</font>  条件获得具体日期的省级数据
>
> 附加 <font color = "6495ED" > **Country_Region = ‘xxx’** </font>  条件获得具体某个国家的省级数据
>
> 附加 <font color = "6495ED" > **Province_State =  ‘xxx’** </font>  条件获得具体某个省级数据

<br/>

* <font  size =3 >市级数据格式形如</font>

| Admin                                 | Province_State                        | Country_Region                       | Confirmed  | Deaths     | Recovered  | Active       | LastUpdate                                |
| ------------------------------------- | ------------------------------------- | ------------------------------------ | ---------- | ---------- | ---------- | ------------ | ----------------------------------------- |
| <font color = "B22222" >行政区</font> | <font color = "4169E1" >省/州</font>  | <font color = "4169E1" >国家</font>  | 总确诊人数 | 总死亡人数 | 总治愈人数 | 当前患病人数 | <font color = "4169E1" >更新日期</font>   |
| <font color = "B22222" >Jimei</font>  | <font color = "4169E1" >Xiamen</font> | <font color = "4169E1" >China</font> | 0          | 0          | 0          | 0            | <font color = "4169E1" >2020-05-31</font> |

> 调用数据时限定
>
> <font color = "6495ED" >**Admin != '#NULL'**</font> <font color = "B22222" >&&</font> <font color = "6495ED" >**Admin != '#RDForCalculate'**</font> <font color = "B22222" >&&</font> <font color = "6495ED" >**Admin !=  'World'**</font> <font color = "B22222" >&&</font> <font color = "6495ED" >**Admin != Country_Region**</font> 条件获得市级数据
>
> * <font color = "6495ED" size =2.5 >**Admin != '#NULL'**</font>  排除省级数据
> * <font color = "6495ED" size = 2.7>**Admin != '#RDForCalculate' **</font>排除用于计算的特殊格式的数据
> * <font color = "6495ED" size = 2.7>**Admin != Country_Region' **</font>排除国家级数据

<br/>

* <font  size =4>特殊数据格式形如</font>

| Admin                                          | Province_State                        | Country_Region                      | Confirmed  | Deaths     | Recovered  | Active       | LastUpdate                                |
| ---------------------------------------------- | ------------------------------------- | ----------------------------------- | ---------- | ---------- | ---------- | ------------ | ----------------------------------------- |
| <font color = "B22222" >#RDForCalculate</font> | <font color = "4169E1" >省/州</font>  | <font color = "4169E1" >国家</font> | 总确诊人数 | 总死亡人数 | 总治愈人数 | 当前患病人数 | <font color = "4169E1" >更新日期</font>   |
| <font color = "B22222" >#RDForCalculate</font> | <font color = "4169E1" >Alaska</font> | <font color = "4169E1" >US</font>   | 0          | 0          | 0          | 0            | <font color = "4169E1" >2020-05-31</font> |

> 此数据格式设置的原因：网页数据中存在一些负数数据来计算Active人数
>
> 限定 <font color = "6495ED" >**Admin !=  ‘#RDForCalculate’**</font> 条件排除此特殊格式数据

<br/>

### 数据中存在的一些问题： 

* <font color = "B22222" >4月28日、4月23日</font> 两天出现数据丢失或不全的问题

* 国外数据在一、二月份统计不完整，但影响不大

  